from .control_flow import ControlFlow
from .command import Command
from .capture import Capture
from ..util import list_to_str


class Rule:
    def __init__(self, name, match, result):
        self.name = name
        self.match = match
        self.result = result

    def check(self, compiler, tokens):
        if len(self.match) != len(tokens):
            print(list_to_str(tokens))
            return False

        print(
            "checking rule `"
            + self.name
            + "` for tokens "
            + list_to_str(tokens)
        )

        captures = []

        for j in range(len(self.match)):
            pattern = self.match[j]
            token = tokens[j]
            print(
                "checking token [" + str(j)
                + "] | pattern: `" + str(pattern)
                + "` | token: `" + token + "`"
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

        return Command(
            list_to_str(tokens),
            (lambda runtime: self.result(runtime, captures)) if callable(self.result)
            else self.result
        )
