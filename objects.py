from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, type):
        self.type = type
        self.lexical_parent = None

    @abstractmethod
    def to_string(self):
        "Returns a string representation for printing"
        pass
    


class FunctionObject(Object):
    def __init__(self, name, args, statements, lexical_parent):
        self.name = name
        self.args = args
        self.statements = statements
        self.lexical_parent = lexical_parent
        

    def to_string(self):
        return f"<function {self.name} at {hex(id(self))}>"

class Int(Object):
    def __init__(self, value: int):
        self.value = value

    def to_string(self):
        return str(self.value)

class Float(Object):
    def __init__(self, value: float):
        self.value = value

    def to_string(self):
        return str(self.value)

class Str(Object):
    def __init__(self, value: str):
        self.value = value

    def to_string(self):
        return self.value