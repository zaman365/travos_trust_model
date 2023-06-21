import socket
import trustlab.lab.config as config
from asgiref.sync import sync_to_async
from trustlab.lab.connectors.channels_connector import ChannelsConnector
from trustlab.lab.distributors.greedy_distributor import GreedyDistributor
from trustlab.lab.distributors.round_robin_distributor import RoundRobinDistributor
from trustlab.models import ResultFactory, ScenarioResult
from trustlab.lab.connectors.mongo_db_connector import MongoDbConnector


class Director:
    """
    Organizes the testbed's environment for one specific scenario run.
    Therewith decides which supervisors should be involved,
    prepares the scenarios with them,
    overwatches the run by informing all involved supervisors about done observations,
    and terminates the evaluation run by signalling the end to all involved supervisors.
    All scenario run results are saved with the usage of ScenarioResult and ResultFactory.
    """
    async def prepare_scenario(self):
        """
        Prepares the scenario run by deciding which supervisors to involve,
        signalling them to prepare everything for the run,
        and distributing the global agent discovery to all involved supervisors.

        :return: The amount of supervisors used for this scenario run.
        :rtype: int
        """
        agents = await self.mongodb_connector.get_agents_list(self.scenario_name)
        # check if enough agents are free to work
        sum_max_agents, sum_agents_in_use = await self.channels_connector.sums_agent_numbers()
        free_agents = sum_max_agents - sum_agents_in_use
        if free_agents < len(agents):
            print(free_agents)
            print(len(agents))
            raise Exception('Currently there are not enough agents free for the chosen scenario.')
        # distribute agents on supervisors
        supervisors_with_free_agents = await self.channels_connector.list_supervisors_with_free_agents()
        self.distribution = await self.distributor.distribute(agents, supervisors_with_free_agents)
        # reserve agents at supervisors
        await sync_to_async(config.write_scenario_status)(self.scenario_run_id, f"Reserving Agents..")
        await self.mongodb_connector.set_all_observations_to_do(self.scenario_name, self.scenario_run_id)
        await self.mongodb_connector.set_all_agents_available(self.scenario_name, self.scenario_run_id)
        await self.reserve_agents()
        await sync_to_async(config.write_scenario_status)(self.scenario_run_id,
                                                          f"Scenario Distribution:\n{self.discovery}")
        return len(self.distribution.keys())

    async def reserve_agents(self):
        self.discovery = {}
        for channel_name in self.distribution.keys():
            # init agents at supervisors
            registration_message = {
                "type": "scenario.registration",
                "scenario_run_id": self.scenario_run_id,
                "scenario_name": self.scenario_name,
                "agents_at_supervisor": self.distribution[channel_name]
            }
            await self.channels_connector.send_message_to_supervisor(channel_name, registration_message)
            received_discovery = False
            while not received_discovery:
                message = await self.channels_connector.receive_with_scenario_run_id(self.scenario_run_id)
                if message['type'] == 'agent_discovery':
                    received_discovery = True
                    self.discovery = {**self.discovery, **message["discovery"]}
                else:
                    await self.handle_agent_request(message)
        await self.channels_connector.reserve_agents_in_db(self.distribution)
        # after registration and discovery knowledge share discovery with all involved supervisors
        discovery_message = {
            "type": "scenario.discovery",
            "scenario_run_id": self.scenario_run_id,
            "discovery": self.discovery,
            "distribution": self.distribution
        }
        for channel_name in self.distribution.keys():
            await self.channels_connector.send_message_to_supervisor(channel_name, discovery_message)

    async def run_scenario(self):
        """
        Runs the scenario and manages the correct observation sequence by broadcasting end of observation signal
        from one supervisor to all other supervisors involved.
        Further, it manages the scenario run results and initiates the save.
        """
        # await self.channels_connector.start_scenario(self.distribution.keys(), self.scenario_run_id, self.scenario_name)
        await self.send_next_observation()
        trust_log, trust_log_dict = [], []
        agents = await self.mongodb_connector.get_agents_list(self.scenario_name)
        agent_trust_logs = dict((agent, []) for agent in agents)
        agent_trust_logs_dict = dict((agent, []) for agent in agents)
        scenario_runs = True
        observations_to_do_amount = await self.mongodb_connector.get_observations_count(self.scenario_name)
        done_observations_with_id = []
        while scenario_runs:
            message = await self.channels_connector.receive_with_scenario_run_id(self.scenario_run_id)
            if message['type'] in ['observation_done', 'agent_free']:
                if message['type'] == 'agent_free':
                    await self.mongodb_connector.set_agent_available(self.scenario_name, self.scenario_run_id,
                                                                     message['agent'])
                else:
                    await self.mongodb_connector.set_observation_done(self.scenario_name, self.scenario_run_id,
                                                                      message["observation_id"])
                await self.send_next_observation()
            elif message['type'] in ['get_scales_per_agent', 'get_history_per_agent', 'get_all_agents',
                                     'get_metrics_per_agent']:
                await self.handle_agent_request(message)
            if message['type'] == 'observation_done':
                await sync_to_async(config.write_scenario_status)(self.scenario_run_id,
                                                                  f"Did observation {message['observation_id']}")
                done_observations_with_id.append(message['observation_id'])
                # merge send logs to saved results
                obs_receiver = message['receiver']
                recv_trust_log = message['trust_log'].split('<br>')
                new_trust_log = [line for line in recv_trust_log if line not in trust_log]
                recv_trust_dict = message['trust_log_dict']
                new_trust_log_dict = [d for d in recv_trust_dict if d not in trust_log_dict]
                recv_receiver_log = message['receiver_trust_log'].split('<br>')
                new_receiver_log = [line for line in recv_receiver_log if line not in agent_trust_logs[obs_receiver]]
                recv_receiver_log_dict = message['receiver_trust_log_dict']
                new_receiver_log_dict = [d for d in recv_receiver_log_dict if d not in agent_trust_logs_dict[obs_receiver]]
                trust_log.extend(new_trust_log)
                trust_log_dict.extend(new_trust_log_dict)
                agent_trust_logs[obs_receiver].extend(new_receiver_log)
                agent_trust_logs_dict[obs_receiver].extend(new_receiver_log_dict)
                if len(done_observations_with_id) == observations_to_do_amount:
                    scenario_runs = False
                    await sync_to_async(config.write_scenario_status)(self.scenario_run_id, f"Scenario finished.")
        for agent, log in agent_trust_logs.items():
            if len(log) == 0:
                agent_trust_logs[agent].append("The scenario reported no agent trust log for this agent.")
        await self.save_scenario_run_results(trust_log, trust_log_dict, agent_trust_logs, agent_trust_logs_dict)
        return trust_log, trust_log_dict, agent_trust_logs, agent_trust_logs_dict

    @sync_to_async
    def save_scenario_run_results(self, trust_log, trust_log_dict, agent_trust_logs, agent_trust_logs_dict, rams=None):
        """
        Saves the scenario run results with the usage of ScenarioResult and ResultFactory.

        :param trust_log: Scenario run trust log.
        :type trust_log: list
        :param trust_log_dict: Scenario run trust log in dictionaries.
        :type trust_log_dict: list
        :param agent_trust_logs: Trust logs per agent.
        :type agent_trust_logs: dict
        :param agent_trust_logs_dict: Trust logs per agent in dictionaries.
        :type agent_trust_logs_dict: dict
        :param rams: RAM usages of all supervisors.
        :type rams: list
        """
        result_factory = ResultFactory()
        result = ScenarioResult(self.scenario_run_id, self.scenario_name, len(self.distribution.keys()), trust_log,
                                trust_log_dict, agent_trust_logs, agent_trust_logs_dict, ram_usages=rams)
        result_factory.save_result(result)

    @sync_to_async
    def save_ram_usages(self, rams):
        """
        Saves the RAM usages of all supervisors.

        :param rams: RAM usages of all supervisors.
        :type rams: list
        """
        result_factory = ResultFactory()
        scenario_result = result_factory.get_result(self.scenario_run_id)
        scenario_result.ram_usages = rams
        result_factory.save_dict_log_result(scenario_result)

    async def end_scenario(self):
        """
        Signals the end of the scenario run to all involved supervisors.
        """
        rams = await self.channels_connector.end_scenario(self.distribution, self.scenario_run_id)
        if rams is not None:
            await self.save_ram_usages(rams)

    async def get_channel_for_agent(self, agent):
        """
        Looks up the supervisor's channel name hosting the given agent.

        :param agent: The agent for which the supervisor's channel name shall be returned.
        :type agent: str
        :return: The channel name or None if not found in distribution.
        :rtype: str
        """
        for channel_name, agents in self.distribution.items():
            if agent in agents:
                return channel_name
        return None  # TODO: handle exception that suddenly agent is not in distribution

    async def send_next_observation(self):
        """
        In the context of the given scenario's id and name, the next observation to be
        executed is sent to the correct supervisor.

        :param scenario_id: The scenario ID.
        :type scenario_id: str
        :param scenario_name: The scenario name.
        :type scenario_name: str
        """
        agents = await self.mongodb_connector.get_agents_available(self.scenario_name, self.scenario_run_id)
        if agents is not None and len(agents) > 0:
            observations = await self.mongodb_connector.get_observations(self.scenario_name, self.scenario_run_id,
                                                                         agents)
            if observations is not None:
                for observation in observations:
                    del(observation["_id"])
                    del(observation["Type"])
                    next_observation_msg = {
                        'type': 'send.data',
                        'new_type': 'new_observation',
                        'scenario_run_id': self.scenario_run_id,
                        'data': observation}
                    channel_to_send_obs = await self.get_channel_for_agent(observation['sender'])
                    await self.channels_connector.send_message_to_supervisor(channel_to_send_obs, next_observation_msg)
                    await self.mongodb_connector.set_agent_busy(self.scenario_name, self.scenario_run_id,
                                                                observation["sender"])

    async def handle_agent_request(self, message):
        """
        Handles a supervisor's request for agent data.

        :param message: The message.
        :type message: dict
        """
        agent = message["agent"] if message['type'] != 'get_all_agents' else None
        answer = {
            'type': 'send.data',
            'new_type': None,
            'scenario_run_id': self.scenario_run_id,
        }
        if agent is not None:
            answer['agent'] = agent
        data = None
        if message['type'] == 'get_scales_per_agent':
            data = await self.mongodb_connector.get_scales(self.scenario_name, agent)
            answer['new_type'] = 'get_scales_per_agent'
        elif message['type'] == 'get_history_per_agent':
            data = await self.mongodb_connector.get_history(self.scenario_name, agent)
            answer['new_type'] = 'get_history_per_agent'
        elif message['type'] == 'get_metrics_per_agent':
            data = await self.mongodb_connector.get_metrics(self.scenario_name, agent)
            answer['new_type'] = 'get_metrics_per_agent'
        elif message['type'] == 'get_all_agents':
            data = await self.mongodb_connector.get_agents_list(self.scenario_name)
            answer['new_type'] = 'get_all_agents'
        answer['data'] = data
        if answer['new_type'] is not None:
            await self.channels_connector.send_message_to_supervisor(message['response_channel'], answer)

    def __init__(self, scenario_name):
        self.HOST = socket.gethostname()
        self.scenario_run_id = config.create_scenario_run_id()
        self.scenario_name = scenario_name
        self.channels_connector = ChannelsConnector()
        if config.DISTRIBUTOR == "round_robin":
            self.distributor = RoundRobinDistributor()
        else:
            self.distributor = GreedyDistributor()
        self.distribution = None
        self.discovery = None
        self.mongodb_connector = MongoDbConnector(config.MONGODB_URI)
