from intbase import InterpreterBase, ErrorType
from environment import ENV_STATUS
from brewparse import parse_program
from element import Element
from environment import *
from objects import *

class RETURN:
    def __init__(self, value):
        self.value = value


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.env = Environment()

        # Handle Builtin Functions
        self.builtin_dict = {
            'print': self.output,
            'inputi': self.get_input
        }



    def run(self, program):
        program_node = parse_program(program)

        self.eval_program(program_node)

    
    def eval_program(self, node: Element):
        function_defs = node.dict.get('functions', [])
        function_names = [f.get('name') for f in function_defs]

        if 'main' not in function_names:
            super().error(ErrorType.NAME_ERROR, "No main() function was found")
        

        for def_node in function_defs:
            self.eval_function_def(def_node)
    
    def eval_function_def(self, node: Element):
        Environment.create_object(name = node.get('name'), node=node, env=self.env, value=None, obj_type=OBJECT_TYPES.FUNCTION)
        func_obj: FunctionObject = self.env.retrieve(node.get('name'))

        if func_obj.get('name') == 'main':
            self.fcall(func_obj)

    def eval_statement(self, node: Element):
        match node.elem_type:
            case self.VAR_DEF_NODE:
                self.eval_vardef(node)
            case self.ASSIGNMENT_NODE:
                self.eval_assign(node)
            case self.FCALL_NODE:
                self.fcall(node)

    def eval_vardef(self, node: Element) -> None:
        identifier = node.get('name')
        if self.env.define_identifier(identifier=identifier, value=None) == ENV_STATUS.REDEFINE:
            super().error(ErrorType.NAME_ERROR, f'Redefinition of {identifier}')
    
    def eval_assign(self, node: Element) -> None:
        identifier = node.get('var')
        expression_node = node.get('expression')
        expression_val = self.eval_expr(expression_node)

        STATUS = self.env.assign_identifier(identifier=identifier, value=expression_val)

    def eval_expr(self, node: Element):
        element_type = node.elem_type

        # Binary Operation Expression
        if element_type in ['+', '-']:
            operand_1_node = node.get('op1')
            operand_2_node = node.get('op2')

            val1 = self.eval_expr(operand_1_node)
            val2 = self.eval_expr(operand_2_node)

            if isinstance(val1, str) or isinstance(val2, str):
                super().error(ErrorType.TYPE_ERROR, f'{val1} or {val2} must be an integer')

            if element_type == '+':
                return val1 + val2
            else: return val1 - val2
        elif element_type == self.FCALL_NODE:
            return self.fcall(node)
        elif element_type == self.QUALIFIED_NAME_NODE:
            identifier = node.get('name')

            if identifier == None:
                super().error(ErrorType.NAME_ERROR, f"Variable {identifier} has not been defined")

            value = self.env.retrieve(identifier=identifier)
            if value == ENV_STATUS.IDENTIFIER_NOT_FOUND:
                super().error(ErrorType.NAME_ERROR, f'Variable {identifier} was defined but not initialized')

            return value
        
        elif element_type == self.INT_NODE:
            return node.get('val')
        elif element_type == self.STRING_NODE:
            return node.get('val')

    def fcall(self, node: FunctionObject):
        identifier = node.get('name')

        if identifier not in self.builtin_dict.keys() and not isinstance(node, FunctionObject):
            self.error(ErrorType.TYPE_ERROR, f'{identifier} is not callable')
        return_val = None
        args = [(arg.get('name'), self.eval_expr(arg)) for arg in node.get('args')]

        self.env.push_frame(static_link=self.env.current_frame)

        for arg_name, arg_value in args:
            if self.env.define_identifier(arg_name, arg_value) == ENV_STATUS.REDEFINE:
                super().error(ErrorType.NAME_ERROR, f'Redefinition of {arg_name}')


        if identifier not in self.builtin_dict:
            for statement in node.statements:
                result = self.eval_statement(statement)

                if isinstance(result, RETURN):
                    return_val = result.value
                    break

            self.env.pop_frame()
            return return_val
        else:
            if identifier == 'print':
                return_string = ""

                for name, value in args:
                    return_string += str(value)

                self.builtin_dict['print'](return_string) 

            if identifier == 'inputi':
                return_string = ""
                for name, value in args:
                    return_string += str(value)

                self.builtin_dict['print'](return_string)
                return self.builtin_dict['inputi']()


                
            






        


        


        

        