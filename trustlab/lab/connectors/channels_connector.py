from asgiref.sync import sync_to_async
from trustlab.lab.connectors.basic_connector import BasicConnector
from django.db import transaction
from django.db.models import F, Sum
from trustlab.models import Supervisor
from channels.layers import get_channel_layer


class ChannelsConnector(BasicConnector):
    """
    Manages the supervisor connections with expecting all supervisors to connect via websockets and thus using
    Django Channels as well as the database to store active channel connections.
    """
    @sync_to_async
    def sums_agent_numbers(self):
        sums = Supervisor.objects.aggregate(sum_max_agents=Sum('max_agents'), sum_agents_in_use=Sum('agents_in_use'))
        return sums['sum_max_agents'], sums['sum_agents_in_use']

    @sync_to_async
    def list_supervisors_with_free_agents(self):
        return list(set(Supervisor.objects.filter(agents_in_use__lt=F('max_agents'))))

    @sync_to_async
    def get_supervisors_without_given(self, given_channel_name):
        return list(set(Supervisor.objects.exclude(channel_name=given_channel_name)))

    @sync_to_async
    def get_supervisor_hostname(self, given_channel_name):
        return Supervisor.objects.get(channel_name=given_channel_name).hostname

    @staticmethod
    async def send_message_to_supervisor(channel_name, message):
        channel_layer = get_channel_layer()
        await channel_layer.send(channel_name, message)

    @staticmethod
    async def receive_with_scenario_run_id(scenario_run_id):
        channel_layer = get_channel_layer()
        response = await channel_layer.receive(scenario_run_id)
        return response

    @sync_to_async
    @transaction.atomic
    def reserve_agents_in_db(self, distribution):
        for channel_name in distribution.keys():
            supervisor = Supervisor.objects.get(channel_name=channel_name)
            supervisor.agents_in_use += len(distribution[channel_name])
            supervisor.save()

    async def start_scenario(self, involved_supervisors, scenario_run_id, scenario_name):
        start_message = {
            "type": "scenario.start",
            "scenario_run_id": scenario_run_id,
            "scenario_name": scenario_name,
            "scenario_status": "started"
        }
        for channel_name in involved_supervisors:
            await self.send_message_to_supervisor(channel_name, start_message)

    async def broadcast_done_observation(self, scenario_run_id, done_observations_with_id, supervisors_to_inform):
        done_message = {
            "type": "observation.done",
            "scenario_run_id": scenario_run_id,
            "observations_done": done_observations_with_id
        }
        for supervisor in supervisors_to_inform:
            await self.send_message_to_supervisor(supervisor.channel_name, done_message)

    @sync_to_async
    @transaction.atomic
    def free_agents_in_db(self, distribution):
        for channel_name in distribution.keys():
            supervisor = Supervisor.objects.get(channel_name=channel_name)
            supervisor.agents_in_use -= len(distribution[channel_name])
            supervisor.save()

    async def end_scenario(self, distribution, scenario_run_id):
        end_message = {
            "type": "scenario.end",
            "scenario_run_id": scenario_run_id,
            "scenario_status": "finished"
        }
        ram_usage = {}
        for channel_name in distribution.keys():
            await self.send_message_to_supervisor(channel_name, end_message)
            response = await self.receive_with_scenario_run_id(scenario_run_id)
            if response["type"] == "ram_usage":
                hostname = await self.get_supervisor_hostname(channel_name)
                if hostname:
                    ram_usage[hostname] = response["ram_usage"]
                else:
                    ram_usage[channel_name] = response["ram_usage"]
                response = await self.receive_with_scenario_run_id(scenario_run_id)
            # print(f"Scenario ended at supervisor '{channel_name}' with message: {response}")
        await self.free_agents_in_db(distribution)
        return ram_usage if len(ram_usage.keys()) > 0 else None



