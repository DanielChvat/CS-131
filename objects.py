from abc import ABC, abstractmethod

class ObjectInterface(ABC):
    def __init__(self, type):
        self.type = type
        self.lexical_parent = None

    @abstractmethod
    def to_string(self):
        "Returns a string representation for printing"
        pass
    
class FunctionObject(ObjectInterface):
    def __init__(self, name, args, statements, lexical_parent):
        self.dict = {}
        self.statements = statements
        self.lexical_parent = lexical_parent
        self.dict['name'] = name
        self.dict['args'] = args

    def get(self, key):
        if key not in self.dict:
            return None
        return self.dict[key]

    def to_string(self):
        return f"<function {self.name} at {hex(id(self))}>"

class Int(ObjectInterface):
    def __init__(self, name: str, value: int):
        self.value = value
        self.dict = {}
        self.dict['name'] = name

    def to_string(self):
        return str(self.value)

class Float(ObjectInterface):
    def __init__(self, name: str, value: float):
        self.value = value
        self.dict = {}
        self.dict['name'] = name

    def to_string(self):
        return str(self.value)

class Str(ObjectInterface):
    def __init__(self, name: str, value: str):
        self.value = value
        self.dict = {}
        self.dict['name'] = name

    def to_string(self):
        return self.value
