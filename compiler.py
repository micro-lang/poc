# import re

class Capture:
    name = ""

    def __init__(self, _name):
        self.name = _name

    def __str__(self):
        return "Capture{".join(self.name).join("}")


class Rule:
    def __init__(self, name, match, result):
        self.name = name
        self.match = match
        self.result = result

    def check(self, compiler, tokens):
        print("checking rule `" + self.name + "` \
                for tokens `" + list_to_str(tokens) + "`")
        captures = []
        for j in range(len(self.match)):
            pattern = self.match[j]
            token = tokens[j]
            print("checking token [" + str(j) + "]\
                    | pattern: `" + str(pattern) + "` \
                    | token: `" + token + "`"
                  )
            if isinstance(pattern, Capture):
                print("pattern is capture, token captured")
                captures.append(token)
            elif pattern in compiler.keywords:
                print("pattern `" + pattern + "` is a keyword")
                if token != compiler.keywords[pattern]:
                    print("token `" + token + "` doesn't match the keyword")
                    return False
            elif token != pattern:
                print("pattern is literal, token doesn't match pattern")
                return False
        print("rule match, returning captures: " + list_to_str(captures))
        return captures


class MicroCompiler:

    def __init__(self):
        self.memory = {}
        self.keywords = {
            "var_kw": "new",
            "rule_kw": "rule",
            "keyword_kw": "keyword",
        }
        self.rules = {
            Rule(
                "variable_declaration",
                [
                    "var_kw",
                    Capture("var_name"),
                    "=",
                    Capture("var_value"),
                ],
                lambda compiler, captures:
                    compiler.allocate(
                        captures[0],
                        captures[1]
                    )
            )
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
        print("Micro compile:\n`" + source_code + "`")
        tokens = source_code.split()
        print("tokens: " + list_to_str(tokens))
        commands = []
        while len(tokens) > 0:
            print("current token: `" + tokens[0] + "`")
            found_rule_for_token = False
            for rule in self.rules:
                rule_result = rule.check(
                    self,
                    tokens[:len(rule.match)]
                )
                if rule_result is False:
                    print("rule returned false, skipping...")
                    continue
                print("rule returned commands, appending...")
                commands.append(
                    lambda compiler: rule.result(compiler, rule_result)
                )
                prev_tokens = tokens
                tokens = tokens[len(rule.match):]
                print("tokens removed: " + list_to_str(tokens[:len(rule.match)]) +
                      "\nprev_tokens: " + list_to_str(prev_tokens) +
                      "\nnew_tokens: " + list_to_str(tokens)
                      )
            if not found_rule_for_token:
                print("Invalid syntax at token " + tokens[0])
                return False
        print("code compiled successfully!")
        return commands


def list_to_str(items):
    def append(item):
        return "`".join(item).join("`")

    return "".join(append(i).join(", ") for i in items[:-1]).join(append(items[-1]))


# Create an instantce of the compiler
compiler = MicroCompiler()

# Load Micro code
# with open("./sample.mi") as file:
#     micro_code = file.read()

micro_code = """
new x = 2
new y = 3
"""

commands = compiler.compile(micro_code)

print(commands)
