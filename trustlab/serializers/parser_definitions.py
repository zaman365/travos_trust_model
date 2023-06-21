import json
import re
import uuid
from collections import deque


class AGENTS:
    def __init__(self):
        self.object = None
        self.done_objects = []
        self.storedString = ""
        self.done = False

    def add_line(self, line):
        line = self.storedString + line
        self.storedString = ""
        if len(line) == 0:
            return ""
        if line[:1] == ']':
            self.done = True
            return line[1:].strip()
        if line[:1] == '[':
            return line[1:].strip()
        parts = re.split("^'([^']+)'(?:,|)(.*)", line)
        if len(parts) <= 2:
            self.storedString = line
            return ""
        self.object = {"name": parts[1], "_id": uuid.uuid4().hex}
        self.done_objects.append(self.object)
        self.object = None
        return parts[2]

    def is_complex(self, key):
        for obj in (self,) + type(self).__mro__:
            if key in obj.__dict__:
                return True
        else:
            return False

    def get_next_object(self):
        return None

    def get_done_objects(self):
        return self.done_objects

    def clear_objects(self):
        self.done_objects = []

    def is_done(self):
        return self.done


class HISTORY:
    def __init__(self):
        self.object = None
        self.done_objects = []
        self.storedString = ""
        self.done = False
        self.storedKey = None
        self.q = deque()
        self.tq = deque()

    def add_line(self, line):
        line = line.strip()
        if len(line) == 0:
            return
        if (line[:1] == ']' or line[:1] == '}') and len(self.q) == 2:
            self.q.pop()
            self.done_objects.append(self.object)
            self.object = {}
            return line[1:].strip()
        if (line[:1] == '[' or line[:1] == '{') and len(self.q) == 1:
            self.q.append('[')
            self.object = {}
            return line[1:].strip()
        if line[:1] == '}' and len(self.q) == 1:
            self.done = True
            self.q.pop()
            return line[1:].strip()
        if line[:1] == '{' and len(self.q) == 0:
            self.q.append('{')
            return line[1:].strip()
        if line[:1] == ',' and len(self.q) == 2:
            self.done_objects.append(self.object)
            self.object = {}
            return line[1:].strip()
        if line[:1] == ',' and len(self.q) == 1:
            self.storedKey = None
            return line[1:].strip()
        if self.storedKey is None:
            parts = re.split("^'([^']+)':(?:,|)(.*)", line)
            if len(parts) <= 2:
                self.storedString = line
                return ""
            self.storedKey = parts[1]
            return parts[2]
        else:
            resstring = ""
            index = 0
            until_end = False
            if line[0] not in ['{', '[', '(', '\'']:
                until_end = True
            while index < len(line):
                if line[index] in ['{', '[', '(']:
                    self.tq.append(line[index])
                if line[index] == '}':
                    if self.tq.pop() != '{':
                        raise Exception("Configuration not valid!")
                if line[index] == ')':
                    if self.tq.pop() != '(':
                        raise Exception("Configuration not valid!")
                if line[index] == ']':
                    if self.tq.pop() != '[':
                        raise Exception("Configuration not valid!")
                if line[index] == "'":
                    if len(self.tq) == 0:
                        self.tq.append("'")
                    else:
                        last = self.tq.pop()
                        if not last == "'":
                            self.tq.append(last)
                            self.tq.append("'")
                resstring += line[index]
                index += 1
                if len(self.tq) == 0 and (not until_end or (len(line) > index and line[index] in ['}', ']', ')', ','])):
                    until_end = False
                    break
            if len(self.tq) > 0 or until_end:
                self.storedString = self.storedString + line
                return ""
            parts = re.split("^.'([^']*)',(?: |)'([^']*)',(?: |)((?:-|)\\d*[.]*\\d*).", self.storedString + resstring)
            self.object["parent"] = self.storedKey
            self.object["child"] = parts[1]
            self.object["url"] = parts[2]
            self.object["value"] = float(parts[3])
            self.storedString = ""
            return line[index:]

    def is_complex(self, key):
        for obj in (self,) + type(self).__mro__:
            if key in obj.__dict__:
                return True
        else:
            return False

    def get_next_object(self):
        return None

    def get_done_objects(self):
        return self.done_objects

    def clear_objects(self):
        self.done_objects = []

    def is_done(self):
        return self.done


class DETAILS:
    def __init__(self, parent_id):
        self.parentId = parent_id
        self.object = None
        self.done_objects = []
        self.storedString = ""
        self.storedKey = None
        self.done = False
        self.q = deque()

    def add_line(self, line):
        line = (self.storedString + line).strip()
        self.storedString = ""
        if len(line) == 0:
            return
        if self.object is None and line[:1] == '{':
            self.q.append('{')
            return line[1:].strip()
        if line[:1] == '}' and len(self.q) == 1:
            self.q.pop()
            self.done_objects.append(self.object)
            self.object = None
            self.storedKey = None
            self.done = True
            return line[1:].strip()
        if line[:1] == ',' and len(self.q) == 1:
            self.done_objects.append(self.object)
            self.object = None
            self.storedKey = None
            return line[1:].strip()
        if self.storedKey is None:
            parts = re.split("^'([^']+)':(?:,|)(.*)", line)
            if len(parts) <= 2:
                self.storedString = line
                return ""
            self.object = {"_id": uuid.uuid4().hex, "observation_id": self.parentId}
            self.storedKey = parts[1]
            return parts[2]
        else:
            resstring = ""
            index = 0
            tq = deque()
            until_end = False
            if line[0] not in ['{', '[', '(', '\'']:
                until_end = True
            while index < len(line):
                if line[index] in ['{', '[', '(']:
                    tq.append(line[index])
                if line[index] == '}':
                    if tq.pop() != '{':
                        raise Exception("Configuration not valid!")
                if line[index] == ')':
                    if tq.pop() != '(':
                        raise Exception("Configuration not valid!")
                if line[index] == ']':
                    if tq.pop() != '[':
                        raise Exception("Configuration not valid!")
                if line[index] == "'":
                    if len(tq) == 0:
                        tq.append("'")
                    else:
                        last = tq.pop()
                        if not last == "'":
                            tq.append(last)
                            tq.append("'")
                resstring += line[index]
                index += 1
                if len(tq) == 0 and (not until_end or (len(line) > index and line[index] in ['}', ']', ')', ','])):
                    until_end = False
                    break
            if len(tq) > 0 or until_end:
                self.storedString = line
                return ""
            self.object[self.storedKey] = json.loads(resstring.replace("'", '"'))
            return line[index:]

    def is_complex(self, key):
        for obj in (self,) + type(self).__mro__:
            if key in obj.__dict__:
                return True
        else:
            return False

    def get_next_object(self):
        return None

    def get_done_objects(self):
        return self.done_objects

    def clear_objects(self):
        self.done_objects = []

    def is_done(self):
        return self.done


class OBSERVATIONS:
    def __init__(self):
        self.object = None
        self.done_objects = []
        self.storedString = ""
        self.storedKey = None
        self.done = False
        self.next_object = None
        self.details = "DETAILS"
        self.q = deque()

    def add_line(self, line):
        line = (self.storedString + line).strip()
        self.storedString = ""
        if len(line) == 0:
            return
        if line[:1] == ']' and len(self.q) == 0:
            self.done = True
            return line[1:].strip()
        if self.object is None and line[:1] == '[':
            return line[1:].strip()
        if self.object is None and line[:1] == '{':
            self.object = {}
            self.object["_id"] = uuid.uuid4().hex
            return line[1:].strip()
        if line[:1] == '}' and len(self.q) == 0:
            self.done_objects.append(self.object)
            self.object = None
            return line[1:].strip()
        if line[:1] == ',' and len(self.q) == 0:
            self.storedKey = None
            self.next_object = None
            return line[1:].strip()
        if self.storedKey is None:
            parts = re.split("^'([^']+)':(?:,|)(.*)", line)
            if len(parts) <= 2:
                self.storedString = line
                return ""
            if self.is_complex(self, parts[1]):
                self.next_object = eval(getattr(self, parts[1]))
                self.next_object.__init__(self.next_object, self.object["_id"])
            self.storedKey = parts[1]
            return parts[2]
        else:
            resstring = ""
            index = 0
            tq = deque()
            until_end = False
            if line[0] not in ['{', '[', '(', '\'']:
                until_end = True
            while index < len(line):
                if line[index] in ['{', '[', '(']:
                    tq.append(line[index])
                if line[index] == '}':
                    if tq.pop() != '{':
                        raise Exception("Configuration not valid!")
                if line[index] == ']':
                    if tq.pop() != '[':
                        raise Exception("Configuration not valid!")
                if line[index] == ')':
                    if tq.pop() != '(':
                        raise Exception("Configuration not valid!")
                if line[index] == "'":
                    if len(tq) == 0:
                        tq.append("'")
                    else:
                        last = tq.pop()
                        if not last == "'":
                            tq.append(last)
                            tq.append("'")

                resstring += line[index]
                index += 1

                if len(tq) == 0 and (not until_end or (len(line) > index and line[index] in ['}', ']', ')', ','])):
                    until_end = False
                    break

            if len(tq) > 0 or until_end:
                self.storedString = line
                return ""

            self.object[self.storedKey] = json.loads(resstring.replace("'", '"'))

            return line[index:]

    def is_complex(self, key):
        for obj in (self,) + type(self).__mro__:
            if key in obj.__dict__:
                return True
        else:
            return False

    def get_next_object(self):
        return self.next_object

    def get_done_objects(self):
        return self.done_objects

    def clear_objects(self):
        self.done_objects = []

    def is_done(self):
        return self.done


class SCALES_PER_AGENT:
    def __init__(self):
        self.object = None
        self.done_objects = []
        self.storedString = ""
        self.storedKey = None
        self.parent = None
        self.done = False
        self.next_object = None
        self.q = deque()

    def add_line(self, line):
        line = (self.storedString + line).strip()
        self.storedString = ""
        if len(line) == 0:
            return
        if line[:1] == '}' and len(self.q) == 1:
            self.done = True
            self.q.pop()
            return line[1:].strip()
        if line[:1] == '{' and len(self.q) == 0:
            self.q.append('{')
            return line[1:].strip()
        if line[:1] == '{' and len(self.q) == 1:
            self.object = {}
            self.q.append('{')
            self.object["_id"] = uuid.uuid4().hex
            self.object["parent"] = self.parent
            return line[1:].strip()
        if line[:1] == '}' and len(self.q) == 2:
            self.done_objects.append(self.object)
            self.q.pop()
            self.object = None
            return line[1:].strip()
        if line[:1] == ',' and len(self.q) == 1:
            self.parent = None
            self.storedKey = None
            return line[1:].strip()
        if line[:1] == ',' and len(self.q) == 2:
            self.storedKey = None
            return line[1:].strip()
        if self.parent is None:
            parts = re.split("^'([^']{1,})':(?:,|)(.*)", line)
            if len(parts) <= 2:
                self.storedString = line
                return ""
            self.parent = parts[1]
            return parts[2]
        else:
            if self.storedKey is None:
                parts = re.split("^'([^']{1,})':(?:,|)(.*)", line)
                if len(parts) <= 2:
                    self.storedString = line
                    return ""
                self.storedKey = parts[1]
                return parts[2]
            else:
                resstring = ""
                index = 0
                tq = deque()
                until_end = False
                if line[0] not in ['{', '[', '(', '\'']:
                    until_end = True
                while index < len(line):
                    if line[index] in ['{', '[', '(']:
                        tq.append(line[index])
                    if line[index] == '}':
                        if tq.pop() != '{':
                            raise Exception("Configuration not valid!")
                    if line[index] == ')':
                        if tq.pop() != '(':
                            raise Exception("Configuration not valid!")
                    if line[index] == ']':
                        if tq.pop() != '[':
                            raise Exception("Configuration not valid!")
                    if line[index] == "'":
                        if len(tq) == 0:
                            tq.append("'")
                        else:
                            last = tq.pop()
                            if not last == "'":
                                tq.append(last)
                                tq.append("'")
                    resstring += line[index]
                    index += 1
                    if len(tq) == 0 and (not until_end or (len(line) > index and line[index] in ['}', ']', ')', ','])):
                        until_end = False
                        break
                if len(tq) > 0 or until_end:
                    self.storedString = line
                    return ""
                self.object[self.storedKey] = json.loads(resstring.replace("'", '"'))
                return line[index:]

    def is_complex(self, key):
        for obj in (self,) + type(self).__mro__:
            if key in obj.__dict__:
                return True
        else:
            return False

    def get_next_object(self):
        return None

    def get_done_objects(self):
        return self.done_objects

    def clear_objects(self):
        self.done_objects = []

    def is_done(self):
        return self.done


class METRICS_PER_AGENT:
    def __init__(self):
        self.object = None
        self.done_objects = []
        self.storedStrings = []
        self.storedKey = None
        self.parent = None
        self.done = False
        self.next_object = None
        self.q = deque()
        self.tq = deque()
        self.tq_count = 0

    def add_line(self, line):
        line = line.strip()
        if len(line) == 0:
            return
        if self.tq_count == 0:
            if line[:1] == '}' and len(self.q) == 1:
                self.done = True
                self.q.pop()
                return line[1:].strip()
            if line[:1] == '{' and len(self.q) == 0:
                self.q.append('{')
                return line[1:].strip()
            if line[:1] == '{' and len(self.q) == 1:
                self.object = {}
                self.q.append('{')
                self.object["_id"] = uuid.uuid4().hex
                self.object["parent"] = self.parent
                return line[1:].strip()
            if line[:1] == '}' and len(self.q) == 2:
                self.done_objects.append(self.object)
                self.q.pop()
                self.object = None
                return line[1:].strip()
            if line[:1] == ',' and len(self.q) == 1:
                self.parent = None
                self.storedKey = None
                return line[1:].strip()
            if line[:1] == ',' and len(self.q) == 2:
                self.storedKey = None
                return line[1:].strip()
        if self.parent is None:
            parts = re.split("^'([^']+)':(?:,|)(.*)", line)
            self.parent = parts[1]
            return parts[2]
        else:
            if self.storedKey is None:
                parts = re.split("^'([^']+)':(?:,|)(.*)", line)
                self.storedKey = parts[1]
                return parts[2]
            else:
                resstring = ""
                index = 0
                until_end = False
                if line[0] not in ['{', '[', '(', '\'']:
                    until_end = True
                while index < len(line):
                    if line[index] in ['{', '[', '(']:
                        self.tq.append(line[index])
                        self.tq_count += 1
                    if line[index] == '}':
                        if self.tq.pop() != '{':
                            raise Exception("Configuration not valid!")
                        self.tq_count -= 1
                    if line[index] == ')':
                        if self.tq.pop() != '(':
                            raise Exception("Configuration not valid!")
                        self.tq_count -= 1
                    if line[index] == ']':
                        if self.tq.pop() != '[':
                            raise Exception("Configuration not valid!")
                        self.tq_count -= 1
                    if line[index] == "'":
                        if self.tq_count == 0:
                            self.tq.append("'")
                            self.tq_count += 1
                        else:
                            last = self.tq.pop()
                            self.tq_count -= 1
                            if not last == "'":
                                self.tq.append(last)
                                self.tq.append("'")
                                self.tq_count += 2
                    resstring += line[index]
                    index += 1
                    if self.tq_count == 0 and (
                            not until_end or (len(line) > index and line[index] in ['}', ']', ')', ','])):
                        until_end = False
                        break
                if self.tq_count > 0 or until_end:
                    self.storedStrings.append(line)
                    return ""
                self.storedStrings.append(resstring)
                self.object[self.storedKey] = json.loads(("".join(self.storedStrings)).replace("'", '"'))
                self.storedStrings = []
                return line[index:]

    def is_complex(self, key):
        for obj in (self,) + type(self).__mro__:
            if key in obj.__dict__:
                return True
        else:
            return False

    def get_next_object(self):
        return None

    def get_done_objects(self):
        return self.done_objects

    def clear_objects(self):
        self.done_objects = []

    def is_done(self):
        return self.done
