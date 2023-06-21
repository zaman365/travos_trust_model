import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from pympler import asizeof
from trustlab_host.config import WEBSOCKET_MAX, create_chunked_transfer_id


class ChunkAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    """
    A websocket consumer for async handling with only json messages and the capability of chunked transfer.
    """

    async def send_websocket_message(self, message):
        """
        Handles all outgoing websocket messages to not overflow the size of one message manageable for the websocket
        connection. Thus, this function introduces chunked transfer of the given message if required. The maximum size
        of one message is set in config with parameter WEBSOCKET_MAX.py

        :param message: The message to be sent as JSON object via the websocket connection.
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
            await self.send_part(chunked_transfer_id, 0)

    async def send_part(self, chunked_transfer_id, part_number):
        """
        Sends the next part of a chunked transfer based on its chunked transfer id.

        :param chunked_transfer_id: The id of the chunked transfer.
        :type chunked_transfer_id: str
        :param part_number: The number of the part to be sent.
        :type part_number: int
        """
        parts_for_id_exist = chunked_transfer_id in self.parts_to_send.keys()
        existing_parts = len(self.parts_to_send[chunked_transfer_id]) if parts_for_id_exist else 0
        if parts_for_id_exist and part_number < existing_parts:
            await self.send_json({
                'type': 'chunked_transfer',
                'chunked_transfer_id': chunked_transfer_id,
                'part_number': (part_number + 1, existing_parts),
                'part': self.parts_to_send[chunked_transfer_id][part_number]
            })
            if part_number == existing_parts - 1:
                del self.parts_to_send[chunked_transfer_id]

    async def receive_chunk_traffic(self, content):
        """
        Method to work with all messages existing due to chunked transfer. It manages therewith incoming
        chunked transfer acknowledgements, but also incoming chunked transfer.

        :param content: The JSON content of the message.
        :type content: dict
        :return: A tuple of whether the message was handled already by this function due to chunked transfer
        and the full message if chunked transfer completed.
        """
        if content["type"] and content["type"] == "chunked_transfer_ack":
            await self.send_part(content["chunked_transfer_id"], content["part_number"][0])
            return True, None
        elif content["type"] and content["type"] == "chunked_transfer":
            chunked_transfer_id = content['chunked_transfer_id']
            if chunked_transfer_id not in self.chunked_parts.keys() and content['part_number'][0] == 1:
                self.chunked_parts[chunked_transfer_id] = content['part']
            elif chunked_transfer_id in self.chunked_parts.keys() and\
                    content['part_number'][0] <= content['part_number'][1]:
                self.chunked_parts[chunked_transfer_id] += content['part']
            else:
                print('ChannelsConsumer received chunked transfer with unexpected status.')
                print(f'Chunked <{chunked_transfer_id}> parts {"exist" if self.chunked_parts else "do NOT exist"} '
                      f'while message indicates part {content["part_number"]}.')
            await self.send_json({'type': 'chunked_transfer_ack', 'chunked_transfer_id': chunked_transfer_id,
                                  'part_number': content['part_number']})
            if content['part_number'][0] == content['part_number'][1]:
                print(f'Received chunked message with {content["part_number"][1]} parts.')
                actual_message = json.loads(self.chunked_parts[chunked_transfer_id])
                del self.chunked_parts[chunked_transfer_id]
                return False, actual_message
            return True, None
        else:
            return False, None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parts_to_send = {}
        self.chunked_parts = {}
