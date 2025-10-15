from collections import deque
from enum import Enum, auto
from typing import Deque, Optional
from objects import *

class ScopeRule(Enum):
    STATIC = auto()
    DYNAMIC = auto()

class ENV_STATUS(Enum):
    SUCCESS = 1
    IDENTIFIER_NOT_FOUND = None
    REDEFINE = 2
    FAILURE = -1



class Frame:
    def __init__(self, parent=None, lexical_parent=None):
        self.var: dict[str, object] = {}
        self.lexical_parent: Optional['Frame'] = lexical_parent
    
    def define_identifier(self, identifier, value) -> ENV_STATUS:
        if identifier in self.var.keys():
            return ENV_STATUS.REDEFINE
        self.var[identifier] = value
        return ENV_STATUS.SUCCESS

    def assign_identifier(self, identifier, value) -> ENV_STATUS:
        if identifier in self.var.keys():
            self.var[identifier] = value
            return ENV_STATUS.SUCCESS
        
        return ENV_STATUS.IDENTIFIER_NOT_FOUND
    
    def retrieve(self, identifier):
        return self.var.get(identifier, ENV_STATUS.IDENTIFIER_NOT_FOUND)

class Environment:
    def __init__(self, scope_rule = ScopeRule.DYNAMIC):
        self.scope_rule: ScopeRule = scope_rule
        self.frames: Deque[Frame] = deque()
        self.global_frame: Frame = Frame()
        self.frames.append(self.global_frame)

    @property
    def current_frame(self) -> Frame:
        return self.frames[-1]

    def push_frame(self, static_link=None):
        new_frame = Frame()
        new_frame.static_link = static_link
        self.frames.append(new_frame)
        return ENV_STATUS.SUCCESS
    
    def pop_frame(self):
        if len(self.frames) >= 1:
            self.frames.pop()
            return ENV_STATUS.SUCCESS
        
        return ENV_STATUS.FAILURE
    
    def define_identifier(self, identifier, value):
        STATUS = self.current_frame.define_identifier(identifier=identifier, value=value)
        return STATUS
 
    def assign_identifier(self, identifier, value):
        if self.scope_rule == ScopeRule.DYNAMIC:
            for frame in reversed(self.frames):
                    if frame.assign_identifier(identifier=identifier, value=value) == ENV_STATUS.SUCCESS: 
                        return ENV_STATUS.SUCCESS
        elif self.scope_rule == ScopeRule.STATIC:
            frame = self.current_frame
            while frame:
                if frame.assign_identifier(identifier=identifier, value=value) == ENV_STATUS.SUCCESS: 
                    return ENV_STATUS.SUCCESS
                frame = frame.lexical_parent
                
        return ENV_STATUS.IDENTIFIER_NOT_FOUND
    
    def retrieve(self, identifier):
        if self.scope_rule == ScopeRule.DYNAMIC:
            for frame in reversed(self.frames):
                value = frame.retrieve(identifier=identifier)
                if value != None: return value

        elif self.scope_rule == ScopeRule.STATIC:
            frame = self.current_frame
            while frame:
                value = frame.retrieve(identifier=identifier)
                if value != None: return value
                frame = frame.lexical_parent

        return ENV_STATUS.IDENTIFIER_NOT_FOUND
    
    @classmethod 
    def create_function_obj(cls, node, env: "Environment"):
        name = node.get('name')
        args = node.get('args')
        statements = node.get('statements')
        obj = FunctionObject(
            name=name,
            args=args,
            statements=statements,
            lexical_parent=env.current_frame
        )

        STATUS = env.define_identifier(name, obj)

        return STATUS


    
    

        
