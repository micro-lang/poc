from src.data.rule import Rule
from src.data.block_stack import BlockStack
from src.data.control_flow import ControlFlow
from src.data.capture import Capture
from src.util import list_to_str


class MicroCompiler:
    def __init__(self):
        self.keywords = {
            "kw_var_new": "new",
            "kw_var_get": "get",
            "kw_rule": "rule",
            "kw_keyword": "kw",
            "kw_block_open": "{",
            "kw_block_close": "}",
            "kw_exit": "exit",
        }
        self.memory = []
        self.types = {
            "any": True,
            "number": r"^\d+$",
            "name": r"^[a-zA-Z_]$|[a-zA-Z_][a-zA-Z0-9_]*$",
            "address": lambda compiler, token: compiler.mem_contains(token),
        }
        self.rules = {
            Rule(
                "open",
                ["kw_block_open"],
                ControlFlow.BLOCK_OPEN
            ),
            Rule(
                "close",
                ["kw_block_close"],
                ControlFlow.BLOCK_CLOSE
            ),
            Rule(
                "exit",
                ["kw_exit"],
                ControlFlow.BLOCK_STACK_CLOSE
            ),
            Rule(
                "variable_declaration",
                [
                    "kw_var_new",
                    Capture("var_name", "name"),
                    "=",
                    Capture("var_value", "any"),
                ],
                lambda runtime, captures: (
                    print("allocating ", captures[1], " to ", captures[0]),
                    runtime.allocate(
                        captures[0],
                        captures[1]
                    )
                ),
                lambda compiler, captures: (
                    print("registering address", captures[0], "on compiler"),
                    compiler.mem_add(captures[0])
                )
            ),
            Rule(
                "variable_access",
                [
                    "kw_var_get",
                    Capture("var_name", "address"),
                ],
                lambda runtime, captures:
                    runtime.get(captures[0])
            )
        }

    def type_add(self, name, pattern):
        self.types.append({name: pattern})

    def type_contains(self, name):
        return name in self.types.keys()

    def type_get(self, name):
        print(self.types[name])
        return self.types[name]

    def type_del(self, name):
        del self.types[name]

    def rule_add(self, name, match, result):
        self.rules[name] = Rule(match, result)

    def rule_del(self, name):
        del self.rules[name]

    def mem_add(self, address):
        self.memory.append(address)

    def mem_contains(self, address):
        return address in self.memory

    def mem_del(self, address):
        del self.memory[address]

    def compile(self, source_code):
        # print("Micro compile: | `" + source_code + "`")
        tokens = source_code.split()
        # print("tokens: " + list_to_str(tokens))

        block_stack = BlockStack()

        while len(tokens) > 0:
            print("CURRENT TOKENS: [" + list_to_str(tokens) + "]")

            found_rule_for_token = False
            for rule in self.rules:

                # print("checking rule `" + rule.name + "`")
                rule_result = rule.check(
                    self,
                    tokens[:len(rule)]
                )
                print("Rule Result: ", str(rule_result))

                if rule_result is False:
                    # print("rule returned false, skipping...")
                    continue

                if rule_result.run == ControlFlow.BLOCK_OPEN:
                    block_stack.open()
                elif rule_result.run == ControlFlow.BLOCK_CLOSE:
                    block_stack.close()
                elif rule_result.run == ControlFlow.BLOCK_STACK_CLOSE:
                    block_stack.finish()
                    return block_stack.first()

                else:
                    # print("rule returned commands, appending...")
                    block_stack.append(rule_result)

                tokens = tokens[len(rule):]
                found_rule_for_token = True

            if not found_rule_for_token:
                print("Invalid syntax at token " + tokens[0])
                return False

        if block_stack.isOpen():
            return False

        # print("code compiled successfully!")
        return block_stack.first()
