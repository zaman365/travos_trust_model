import gridfs
import json
import pymongo
import pymongo.errors
import time
from trustlab.lab.config import LOG_SCENARIO_READER_DETAILS
from asgiref.sync import sync_to_async


class MongoDbConnector:
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)
        try:
            self.client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            raise TimeoutError("Invalid API")
        self.database = self.client["trustlab"]
        self.fs = gridfs.GridFS(self.database)

    def add_metrics_grid_data(self, scenario_name, type, data):
        if LOG_SCENARIO_READER_DETAILS:
            print(f'Adding {type} to Scenario {scenario_name}[{time.strftime("%H:%M:%S", time.localtime())}]')
        data["Type"] = type.lower()
        self.fs.put(json.dumps(data).encode(), type=type, scenario_name=scenario_name, parent=data["parent"])

    def add_data(self, scenario_name, type, data):
        if type == "metrics_per_agent":
            return self.add_metrics_grid_data(scenario_name, type, data)
        if LOG_SCENARIO_READER_DETAILS:
            print(f'Adding {type} to Scenario {scenario_name}[{time.strftime("%H:%M:%S", time.localtime())}]')
        data["Type"] = type.lower()
        self.database[scenario_name].insert_one(data)

    def add_many_data(self, scenario_name, data):
        new_data = []
        for d in data:
            if "Type" in d and d["Type"] == "metrics_per_agent":
                self.add_metrics_grid_data(scenario_name, "metrics_per_agent", d)
            else:
                new_data.append(d)
        if len(new_data) == 0:
            return
        if LOG_SCENARIO_READER_DETAILS:
            print(f'Adding data (len: {len(new_data)}) to Scenario {scenario_name}'
                  f'[{time.strftime("%H:%M:%S", time.localtime())}]')
        self.database[scenario_name].insert_many(new_data)

    @sync_to_async
    def reset_scenario(self, scenario_name):
        self.database.drop_collection(scenario_name)
        for grid_out in self.fs.find({"type": "metrics_per_agent", "scenario_name": scenario_name}):
            self.fs.delete(grid_out._id)

    @sync_to_async
    def get_observations(self, scenario_name, scenario_id, agents):
        collection = self.database[scenario_name]
        observations_not_done = collection.find_one({"Type": "observations_to_do", "scenario_id": scenario_id})
        aggregates = collection.aggregate(
            [
                {
                    "$match": {
                        "Type": "observations",
                        "$or": [
                            {
                                "before": {
                                    "$nin": observations_not_done['observations_todo'],
                                }
                            },
                            {
                                "before": []
                            }
                        ],
                        "sender": {
                            "$in": agents
                        },
                        "observation_id": {"$nin": observations_not_done['observations_already_send']}
                    }
                }, {
                    "$sort": {
                        "_id": 1
                    }
                }, {
                    "$group": {
                        "_id": "$sender",
                        "first": {
                          "$first": "$$ROOT"
                        }
                    }
                }
            ]
        )
        observations = []
        for o in aggregates:
            if o["_id"] is None:
                continue
            details = list(self.database[scenario_name].find({"Type": "details", "observation_id": o['first']['_id']},
                                                             {"_id": 0, "observation_id": 0, "Type": 0}))
            o['first']["details"] = {k: v for d in details for k, v in d.items()}
            observations.append(o['first'])
            observations_not_done['observations_already_send'].append(o['first']["observation_id"])
        if len(observations) > 0:
            collection.update_one({
                "Type": "observations_to_do",
                "scenario_id": scenario_id
            }, {
                "$set": {'observations_already_send': observations_not_done['observations_already_send']}
            })
        return observations

    def get_details(self, scenario_name, observation_id):
        return list(self.database[scenario_name].find({"Type": "details", "observation_id": observation_id}))

    @sync_to_async
    def set_observation_done(self, scenario_name, scenario_id, observation_id):
        collection = self.database[scenario_name]
        find = collection.find_one({"Type": "observations_to_do", "scenario_id": scenario_id})
        if observation_id in find['observations_todo']:
            find['observations_todo'].remove(observation_id)
            collection.update_one({"Type": "observations_to_do", "scenario_id": scenario_id},
                                  {"$set": {'observations_todo': find['observations_todo']}})

    @sync_to_async
    def set_all_observations_to_do(self, scenario_name, scenario_id):
        collection = self.database[scenario_name]
        ids = [f['observation_id'] for f in collection.find({"Type": "observations"}, {"_id": 0, "observation_id": 1})]
        collection.delete_one({"Type": "observations_to_do", "scenario_id": scenario_id})
        collection.insert_one({"Type": "observations_to_do", "scenario_id": scenario_id, "observations_todo": ids,
                               "observations_already_send": []})

    @sync_to_async
    def set_all_agents_available(self, scenario_name, scenario_id):
        collection = self.database[scenario_name]
        ids = [f['name'] for f in collection.find({"Type": "agents"}, {"_id": 0, "name": 1})]
        collection.delete_one({"Type": "agents_nothing_to_do", "scenario_id": scenario_id})
        collection.insert_one({"Type": "agents_nothing_to_do", "scenario_id": scenario_id, "agents": ids})

    @sync_to_async
    def get_metrics(self, scenario_name, agent):
        finds = json.loads(self.fs.find_one({"type": "metrics_per_agent", "parent": agent, "scenario_name": scenario_name}).read())
        if finds:
            return finds
        return None

    @sync_to_async
    def get_agents_available(self, scenario_name, scenario_id):
        find = self.database[scenario_name].find_one({"Type": "agents_nothing_to_do", "scenario_id": scenario_id},
                                                     {"_id": 0, "agents": 1})
        return list(find['agents'])

    @sync_to_async
    def set_agent_busy(self, scenario_name, scenario_id, agent):
        collection = self.database[scenario_name]
        find = collection.find_one({"Type": "agents_nothing_to_do", "scenario_id": scenario_id})
        if agent in find['agents']:
            find['agents'].remove(agent)
            collection.update_one({"Type": "agents_nothing_to_do", "scenario_id": scenario_id},
                                  {"$set": {'agents': find['agents']}})

    @sync_to_async
    def set_agent_available(self, scenario_name, scenario_id, agent):
        collection = self.database[scenario_name]
        find = collection.find_one({"Type": "agents_nothing_to_do", "scenario_id": scenario_id})
        if agent not in find['agents']:
            find['agents'].append(agent)
            collection.update_one({
                "Type": "agents_nothing_to_do",
                "scenario_id": scenario_id
            }, {
                "$set": {'agents': find['agents']}
            })

    @sync_to_async
    def get_scales(self, scenario_name, agent):
        finds = self.database[scenario_name].find_one({"Type": "scales_per_agent", "parent": agent},
                                                      {"_id": 0, "parent": 0, "Type": 0})
        return finds if finds else None

    @sync_to_async
    def get_history(self, scenario_name, agent):
        finds = self.database[scenario_name].find({"Type": "history", "parent": agent},
                                                  {"_id": 0, "parent": 0, "Type": 0})
        return list(finds) if finds else None

    @sync_to_async
    def get_agents_list(self, scenario_name):
        finds = self.database[scenario_name].find({"Type": "agents"}, {"_id": 0, "name": 1})
        return [f['name'] for f in finds] if finds else None

    @sync_to_async
    def scenario_exists(self, scenario_name):
        try:
            self.database.validate_collection(scenario_name)  # Try to validate a collection/scenario
        except pymongo.errors.OperationFailure:  # If the scenario doesn't exist
            return False
        return True

    @sync_to_async
    def get_observations_count(self, scenario_name):
        return self.database[scenario_name].count_documents({"Type": "observations"})

    @sync_to_async
    def cleanup(self, scenario_name, scenario_id):
        collection = self.database[scenario_name]
        collection.delete_one({"Type": "agents_nothing_to_do", "scenario_id": scenario_id})
        collection.delete_one({"Type": "observations_to_do", "scenario_id": scenario_id})
