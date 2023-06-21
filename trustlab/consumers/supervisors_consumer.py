from trustlab.lab.connectors.channels_connector import ChannelsConnector
from trustlab.consumers.chunk_consumer import ChunkAsyncJsonWebsocketConsumer
from trustlab.lab.connectors.mongo_db_connector import MongoDbConnector
from trustlab.lab.config import MONGODB_URI
from trustlab.models import Supervisor


class SupervisorsConsumer(ChunkAsyncJsonWebsocketConsumer):
    async def connect(self):
        Supervisor.objects.create(channel_name=self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        Supervisor.objects.filter(channel_name__exact=self.channel_name).delete()

    async def scenario_registration(self, event):
        await self.send_websocket_message({
            "type": "scenario_registration",
            "scenario_run_id": event["scenario_run_id"],
            "scenario_name": event["scenario_name"],
            "agents_at_supervisor": event["agents_at_supervisor"]
        })

    async def scenario_discovery(self, event):
        await self.send_websocket_message({
            "type": "scenario_discovery",
            "scenario_run_id": event["scenario_run_id"],
            "discovery": event["discovery"]
        })

    async def scenario_end(self, event):
        await self.send_websocket_message({
            "type": "scenario_end",
            "scenario_run_id": event["scenario_run_id"],
            "scenario_status": event["scenario_status"]
        })

    async def send_data(self, event):
        message = {
            "type": event['new_type'],
            "scenario_run_id": event['scenario_run_id'],
            "data": event['data']
        }
        if 'agent' in event.keys() and event['agent'] is not None:
            message['agent'] = event['agent']
        await self.send_websocket_message(message)

    async def receive_json(self, content, **kwargs):
        handled, new_content = await super().receive_chunk_traffic(content)
        content = new_content if new_content else content
        if not handled:
            if content["type"] and content["type"] == "max_agents":
                supervisor = Supervisor.objects.get(channel_name=self.channel_name)
                supervisor.max_agents = content["max_agents"]
                supervisor.ip_address = content["ip_address"]
                if 'hostname' in content:
                    supervisor.hostname = content["hostname"]
                supervisor.save()
                answer = {"type": "max_agents", "status": 200}
                await self.send_json(answer)
            elif content["type"] and content["type"] in \
                    ["agent_discovery", "scenario_end", "observation_done", "agent_free", "ram_usage",
                     "get_scales_per_agent", "get_history_per_agent", "get_all_agents", "get_metrics_per_agent"]:
                content["response_channel"] = self.channel_name
                await self.channel_layer.send(content["scenario_run_id"], content)
            else:
                print("Could not resolve message and pinged back.")
                await self.send_websocket_message(content)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)