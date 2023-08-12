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
                    Capture("var_name"),
                    "=",
                    Capture("var_value"),
                ],
                lambda runtime, captures: (
                    print("allocating ", captures[1], " to ", captures[0]),
                    runtime.allocate(
                        captures[0],
                        captures[1]
                    )
                )
            ),
            Rule(
                "variable_access",
                [
                    "kw_var_get",
                    Capture("var_name"),
                ],
                lambda runtime, captures:
                    runtime.get(captures[0])
            )
        }

    def rule_add(self, name, match, result):
        self.rules[name] = Rule(match, result)

    def rule_del(self, name):
        del self.rules[name]

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
                    tokens[:len(rule.match)]
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
