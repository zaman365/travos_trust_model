import math
import threading
import time
import trustlab.serializers.parser_definitions as parser_definitions
from collections import deque
from trustlab.lab.config import LOG_SCENARIO_READER
from asgiref.sync import sync_to_async


class ScenarioReader:
    def __init__(self, scenario_name, scenariopath, connector):
        self.filepath = scenariopath
        self.connector = connector
        self.scenario_name = scenario_name
        self.q = deque()
        self.doneItems = []
        self.definitions = deque()
        if LOG_SCENARIO_READER:
            print("Evaluating File lines")
            self.num_lines = sum(1 for line in open(self.filepath))
            print("File lines: " + str(self.num_lines))
        self.running = False
        self.threads = []
        self.lock = threading.Lock()

    def upload_data(self):
        while self.running or len(self.doneItems) > 0:
            items = []
            max = 0
            while True:
                with self.lock:
                    if len(self.doneItems) == 0 or max >= 100:
                        break
                    item = self.doneItems.pop()
                if item is not None:
                    item[2]["Type"] = item[1]
                    items.append(item[2])
                max += 1
            if len(items) > 0:
                self.connector.add_many_data(self.scenario_name, items)

    @sync_to_async
    def read(self):
        self.running = True
        for n in range(0, 4):
            x = threading.Thread(target=self.upload_data)
            x.start()
            self.threads.append(x)
        percentage = -1.00
        current_line_index = 0
        with open(self.filepath) as file:
            for line in file:
                if LOG_SCENARIO_READER:
                    current_line_index += 1
                    if self.num_lines > 100000:
                        new_percentage = round((current_line_index / self.num_lines), 2)
                    else:
                        new_percentage = math.floor((current_line_index / self.num_lines) * 100)
                    if new_percentage > percentage:
                        percentage = new_percentage
                        t = time.localtime()
                        current_time = time.strftime("%H:%M:%S", t)
                        print("Reading current status: " + str(percentage) + "[" + current_time + "]")
                while line is not None and len(line) > 0:
                    line = self.analyze_line(line)
        while len(self.doneItems) > 0:
            pass
        self.running = False
        # a non-blocking threads join alternative:
        while len(self.threads) > 0:
            for t in self.threads:
                if not t.is_alive():
                    self.threads.remove(t)
        if LOG_SCENARIO_READER:
            print("reading done!")

    def analyze_line(self, line):
        line = line.strip()
        if len(line) == 0:
            return ""
        if len(self.definitions) == 0:
            if '=' in line:
                classification_parts = line.split('=', 1)
                user_defined_classes = [i for i in dir(parser_definitions) if type(getattr(parser_definitions, i)) is type.__class__]
                if classification_parts[0].strip() in user_defined_classes:
                    new_definition = eval("parser_definitions." + classification_parts[0].strip())
                    new_definition.__init__(new_definition)
                    self.definitions.append(new_definition)
                    if LOG_SCENARIO_READER:
                        t = time.localtime()
                        current_time = time.strftime("%H:%M:%S", t)
                        print(classification_parts[0] + "[" + current_time + "]")
                    return classification_parts[1]
            return ""
        else:
            current_object = self.definitions.pop()
            line = current_object.add_line(current_object, line)
            done_objects = current_object.get_done_objects(current_object)
            if len(done_objects) > 0:
                for obj in done_objects:
                    with self.lock:
                        self.doneItems.append([self.scenario_name, current_object.__name__.lower(), obj])
                current_object.clear_objects(current_object)
                while len(self.doneItems) > 400:
                    pass
            if not current_object.is_done(current_object):
                self.definitions.append(current_object)
            if not current_object.get_next_object(current_object) is None:
                self.definitions.append(current_object.get_next_object(current_object))
        return line
