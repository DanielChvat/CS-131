from intbase import InterpreterBase
from brewparse import parse_program
from element import Element
from environment import Environment

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.env = Environment()

    def run(self, program):
        program_node = parse_program(program)

        self.eval_program(program_node)

    
    def eval_program(self, node: Element):
        function_defs = node.dict.get('functions', [])

        for def_node in function_defs:
            self.eval_function_def(def_node)
    
    def eval_function_def(self, node: Element):
        Environment.create_function_obj(node, self.env)
        obj = self.env.retrieve(node.get('name'))

        if obj.name == 'main':
            for statement_node in obj.statements:
                self.eval_statement(statement_node)

    def eval_statement(self, node: Element):
        match node.elem_type:
            case 'vardef':
                self.eval_vardef(node)
            case '=':
                pass
            case 'fcall':
                pass

    def eval_vardef(self, node):
        print('a')
        pass
        


        


        

        