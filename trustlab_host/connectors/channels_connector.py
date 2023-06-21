import asyncio
import json
import websockets
from config import WEBSOCKET_MAX, create_chunked_transfer_id
from connectors.basic_connector import BasicConnector
from pympler import asizeof
from time import sleep
import random
import string


class ChannelsConnector(BasicConnector):
    async def register_at_director(self):
        """
        Registering at the Director as Supervisor, by connecting the web socket and sending the registration message
        with the amount of max agents for this supervisor.
        """
        print("Registering at Director...")
        await self.connect_web_socket()
        await self.set_max_agents()
        print(f"Fully Registered a capacity of max. {self.max_agents} agents at Director.")

    async def register_as_evaluator(self):
        """
        Registering at the Director as Evaluator, by connecting the web socket
        and sending the evaluation registration message.
        """
        print('Registering as evaluator...')
        await self.connect_web_socket()
        await self.send_json({'type': 'register_eval_run'})
        await self.receive_json()
        print('Fully Registered at Director and locked WebUI.')

    async def connect_to_director(self):
        """
        Registering at the Director as Evaluator, by connecting the web socket
        but without sending an evaluation registration message.
        """
        print("Connecting to Director...")
        await self.connect_web_socket()
        print("Connected to Director.")

    async def connect_web_socket(self):
        """
        Connecting to the Director via web socket. Function retries until the connection is established.
        """
        connection_attempts = 0
        while self.websocket is None:
            try:
                self.websocket = await websockets.connect(self.director_uri)
            except ConnectionRefusedError:
                sleep(5 + connection_attempts * 2)
                connection_attempts = connection_attempts + 1

    async def set_max_agents(self):
        """
        Sending the max agents message to the Director and expecting the acknowledgement.
        """
        register_max_agents = {"type": "max_agents", "max_agents": self.max_agents}
        register_max_agents.update(self.supervisor_info)
        await self.send_json(register_max_agents)
        await self.receive_json()

    async def get_scales_per_agent(self, agent_id):
        register_max_agents = {"type": "get_scales_per_agent", "agent": agent_id}
        register_max_agents.update(self.supervisor_info)
        await self.send_json(register_max_agents)
        return await self.receive_json()

    async def send_json(self, message):
        """
        Sending a JSON message to the Director.

        :param message: The message to be sent.
        :type message: dict or list
        """
        await self.websocket.send(json.dumps(message))

    async def receive_json(self):
        """
        Receiving a JSON message from the Director. It is currently expected that it is a valid JSON object.
        """
        return await self.websocket.recv()

    async def consuming_message(self, message):
        """
        Consuming the full message received from the websocket.

        :param message: The complete received message as JSON object.
        :type message: dict or list
        """
        if 'evaluator' in self.pipe_dict.keys():
            await self.pipe_dict["evaluator"].coro_send(message)
        elif message["type"] == "scenario_registration":
            await self.pipe_dict["supervisor"].coro_send(message)
        elif message["scenario_run_id"] in self.pipe_dict.keys() \
                and not message["type"] == "scenario_registration":
            await self.pipe_dict[message["scenario_run_id"]].coro_send(message)
        else:
            # TODO implement what happens if message does not fit in another case
            pass

    async def consuming_chunked_transfer(self, message):
        """
        Consuming the messages which are part of the chunked transfer via the websocket.

        :param message: The received message as JSON object, where type has to be 'chunked_transfer'.
        :return: dict or list
        """
        chunked_transfer_id = message['chunked_transfer_id']
        if chunked_transfer_id not in self.chunked_parts.keys() and message['part_number'][0] == 1:
            self.chunked_parts[chunked_transfer_id] = message['part']
        elif chunked_transfer_id in self.chunked_parts.keys() and message['part_number'][0] <= message['part_number'][1]:
            self.chunked_parts[chunked_transfer_id] += message['part']
        else:
            print('ChannelsConnector received chunked transfer with unexpected status.')
            print(f'Chunked <{chunked_transfer_id}> parts {"exist" if self.chunked_parts else "do NOT exist"} '
                  f'while message indicates part {message["part_number"]}.')
        await self.send_json({'type': 'chunked_transfer_ack', 'chunked_transfer_id': message['chunked_transfer_id'],
                              'part_number': message['part_number']})
        if message['part_number'][0] == message['part_number'][1]:
            print(f'Received chunked message with {message["part_number"][1]} parts.')
            actual_message = json.loads(self.chunked_parts[chunked_transfer_id])
            del self.chunked_parts[chunked_transfer_id]
            await self.consuming_message(actual_message)

    async def send_message(self, message):
        """
        Sending a message to the Director via the websocket, but also checking if the message is too large
        to be sent at once. If so, the chunked transfer is used.

        :param message: The message to be sent.
        :type message: dict or list
        """
        message_size = asizeof.asizeof(message)
        if message_size < WEBSOCKET_MAX:
            await self.send_json(message)
        else:
            message_str = json.dumps(message)
            chunked_transfer_id = create_chunked_transfer_id()
            self.parts_to_send[chunked_transfer_id] = [message_str[i:i + WEBSOCKET_MAX] for i in
                                                       range(0, len(message_str), WEBSOCKET_MAX)]
            await self.send_chunked_part(chunked_transfer_id, 0)

    async def send_chunked_part(self, chunked_transfer_id, part_number):
        """
        Sending a part of a chunked transfer to the Director via the websocket.

        :param chunked_transfer_id: The ID of the chunked transfer.
        :type chunked_transfer_id: str
        :param part_number: The number of the part to be sent.
        :type part_number: int
        """
        parts_for_id_exist = chunked_transfer_id in self.parts_to_send.keys()
        existing_parts = len(self.parts_to_send[chunked_transfer_id]) if parts_for_id_exist else 0
        if parts_for_id_exist and part_number < existing_parts:
            # print(f'Transferring part {part_number + 1}/{existing_parts} ...')
            await self.send_json({
                'type': 'chunked_transfer',
                'chunked_transfer_id': chunked_transfer_id,
                'part_number': (part_number + 1, existing_parts),
                'part': self.parts_to_send[chunked_transfer_id][part_number]
            })
            if part_number == existing_parts - 1:
                del self.parts_to_send[chunked_transfer_id]

    async def consumer_handler(self):
        async for message in self.websocket:
            message_json = json.loads(message)
            if message_json['type'] == 'chunked_transfer':
                await self.consuming_chunked_transfer(message_json)
            elif message_json["type"] == "chunked_transfer_ack":
                await self.send_chunked_part(message_json["chunked_transfer_id"], message_json["part_number"][0])
            elif message_json['type'] == 'end_socket':
                return
            else:
                await self.consuming_message(message_json)

    async def producer_handler(self):
        while True:
            message = await self.send_queue.coro_get()
            await self.send_message(message)
            if message['type'] == 'end_socket':
                return

    async def handler(self):
        consumer_task = asyncio.ensure_future(self.consumer_handler())
        producer_task = asyncio.ensure_future(self.producer_handler())
        done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.ALL_COMPLETED)
        for task in pending:
            task.cancel()

    def run(self):
        if self.no_registration:
            asyncio.get_event_loop().run_until_complete(self.connect_to_director())
        else:
            if self.max_agents > 0:
                asyncio.get_event_loop().run_until_complete(self.register_at_director())
            else:
                asyncio.get_event_loop().run_until_complete(self.register_as_evaluator())
        asyncio.get_event_loop().run_until_complete(self.handler())

    def __init__(self, director_hostname, max_agents, send_queue, pipe_dict, sec_conn, supervisor_info=None,
                 no_registration=False):
        super().__init__(director_hostname, max_agents, send_queue, pipe_dict, sec_conn, supervisor_info)
        self.director_uri = f"{'wss://' if sec_conn else 'ws://'}{self.director_hostname}" \
                            f"{'/lab/' if max_agents==0 else'/supervisors/'}"
        self.websocket = None
        self.chunked_parts = {}
        self.parts_to_send = {}
        self.no_registration = no_registration
