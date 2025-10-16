from collections import deque
from enum import Enum, auto
from typing import Deque, Optional
from element import Element
from objects import *
import uuid

class ScopeRule(Enum):
    STATIC = auto()
    DYNAMIC = auto()

class ENV_STATUS(Enum):
    SUCCESS = auto()
    IDENTIFIER_NOT_FOUND = auto()
    REDEFINE = auto()
    FAILURE = auto()



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
    
    def define_identifier(self, identifier: str, value: any = None, node: Element = None):
        obj_type = None
        if isinstance(value, int):
            obj_type = OBJECT_TYPES.INT
        elif isinstance(value, float):
            obj_type = OBJECT_TYPES.FLOAT
        elif isinstance(value, str):
            obj_type = OBJECT_TYPES.STRING
        elif node.elem_type == 'func':
            obj_type = OBJECT_TYPES.FUNCTION
        elif value == None:
            obj_type = OBJECT_TYPES.UNINITIALIZED

        
        obj = Environment.create_object(name=identifier, node=node, env=self, value=value, obj_type=obj_type)
        STATUS = self.current_frame.define_identifier(identifier=identifier, value=obj)
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
                if value != ENV_STATUS.IDENTIFIER_NOT_FOUND: return value

        elif self.scope_rule == ScopeRule.STATIC:
            frame = self.current_frame
            while frame:
                value = frame.retrieve(identifier=identifier)
                if value != None: return value
                frame = frame.lexical_parent

        return ENV_STATUS.IDENTIFIER_NOT_FOUND
    
    @classmethod
    def create_object(cls, name: str, node: Element, env: "Environment", value: any = None, obj_type: Enum = OBJECT_TYPES.OBJECT):
        if not name:
            name = f"_lit_{uuid.uuid4().hex}"

        obj = None
        if obj_type == OBJECT_TYPES.INT:
            obj = Int(name, value)
        elif obj_type == OBJECT_TYPES.FLOAT:
            obj = Float(name, value)
        elif obj_type == OBJECT_TYPES.FUNCTION:
            args = node.get('args')
            statements = node.get('statements')
            obj = FunctionObject(
                name=name,
                args=args,
                statements=statements,
                lexical_parent=env.current_frame
            )
        elif obj_type == OBJECT_TYPES.STRING:
            obj = String(name, value)
        elif obj_type == OBJECT_TYPES.UNINITIALIZED:
            obj = OBJECT_TYPES.UNINITIALIZED

        return obj



    
    

        
