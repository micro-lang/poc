# from src.data import (
#     Rule,
#     BlockStack,
#     ControlFlow,
#     Capture,
# )

from src.data.rule import Rule
from src.data.block_stack import BlockStack
from src.data.control_flow import ControlFlow
from src.data.capture import Capture


class MicroCompiler:
    def __init__(self):
        self.memory = {}
        self.keywords = {
            "kw_var": "new",
            "kw_rule": "rule",
            "kw_keyword": "kw",
            "kw_block_open": "{",
            "kw_block_close": "}",
            "kw_exit": "exit",
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
                    "kw_var",
                    Capture("var_name"),
                    "=",
                    Capture("var_value"),
                ],
                lambda compiler, captures:
                    compiler.allocate(
                        captures[0],
                        captures[1]
                    )
            ),
        }

    def rule_add(self, name, match, result):
        self.rules[name] = Rule(match, result)

    def rule_del(self, name):
        del self.rules[name]

    def allocate(self, address, value):
        self.memory[address] = value

    def free(self, address):
        del self.memory[address]

    def compile(self, source_code):
        # print("Micro compile: | `" + source_code + "`")
        tokens = source_code.split()
        # print("tokens: " + list_to_str(tokens))

        block_stack = BlockStack()

        while len(tokens) > 0 and len(block_stack) > 0:
            # print("current token: `" + tokens[0] + "`")

            found_rule_for_token = False
            for rule in self.rules:

                # print("checking rule `" + rule.name + "`")
                rule_result = rule.check(
                    self,
                    tokens[:len(rule.match)]
                )
                print("Rule Result: ", str(rule_result))

                if rule_result is False:
                    # print("rule returned false, skipping...")
                    continue

                print(
                    str(rule_result.run)
                    + " is "
                    + str(ControlFlow.BLOCK_OPEN)
                    + " ? "
                    + str(rule_result == str(ControlFlow.BLOCK_OPEN))
                )
                print(
                    str(rule_result.run)
                    + " is "
                    + str(ControlFlow.BLOCK_CLOSE)
                    + " ? "
                    + str(rule_result == str(ControlFlow.BLOCK_CLOSE))
                )
                print(
                    str(rule_result.run)
                    + " is "
                    + str(ControlFlow.BLOCK_STACK_CLOSE)
                    + " ? "
                    + str(rule_result == str(ControlFlow.BLOCK_STACK_CLOSE))
                )

                if rule_result.run == ControlFlow.BLOCK_OPEN:
                    block_stack.open()
                elif rule_result.run == ControlFlow.BLOCK_CLOSE:
                    block_stack.close()
                elif rule_result.run == ControlFlow.BLOCK_STACK_CLOSE:
                    return block_stack.finish()

                # TODO: change Rule.check result type to be:
                # 1. the `Command` itself to be added to `block_stack`.
                #       Give `compiler` as argument of Rule.check
                # 2. a ControlFlow.
                #       This way the above checks of Block_OPEN (etc) work
                else:
                    # print("rule returned commands, appending...")
                    block_stack.append(rule_result)

                tokens = tokens[len(rule.match):]
                found_rule_for_token = True

            if not found_rule_for_token:
                # print("Invalid syntax at token " + tokens[0])
                return False

        # print("code compiled successfully!")
        return block_stack.finish()
