from .command import Command
from .capture import Capture
from ..util import list_to_str


class Rule:
    def __init__(self, name, match, result, compiler_result = None):
        self.name = name
        self.match = match
        self.result = result
        self.compiler_result = compiler_result

    def check(self, compiler, tokens):
        if len(self.match) != len(tokens):
            print(list_to_str(tokens))
            return False

        print(
            "---> RULE -- checking tokens ["
            + list_to_str(tokens)
            + "] on rule "
            + self.name
        )

        captures = []

        for j in range(len(self.match)):
            pattern = self.match[j]
            token = tokens[j]
            print(
                "     | RULE -- checking token [" + str(j)
                + "] | pattern: `" + str(pattern)
                + "` | token: `" + token + "`"
            )
            if isinstance(pattern, Capture):
                print("     | | RULE -- pattern is capture")
                if not pattern.match(token, compiler):
                    print("     | | | RULE == token not captured")
                    return False
                print("     | | | RULE == token captured!")
                captures.append(token)
            elif pattern in compiler.keywords:
                print("     | | RULE -- pattern `" + pattern + "` is a keyword")
                if token != compiler.keywords[pattern]:
                    print("     | | | RULE == token `" + token + "` doesn't match the keyword")
                    return False
                else:
                    print("     | | | RULE == token matches pattern keyword")

            elif isinstance(pattern, list):
                print(
                    "     | | RULE -- pattern is any of ["
                    + list_to_str(pattern) + "]"
                )
                if token not in pattern:
                    print("     | | | RULE == token `" + token + "` not in pattern")
                    return False
                else:
                    print("     | | | RULE == token matches one of pattern options")
            else:
                print("     | | RULE -- pattern is literal")
                if token != pattern:
                    print("     | | | RULE == token doesn't match pattern literal")
                    return False

        print("     | RULE -- MATCH, returning captures: " + list_to_str(captures))

        if self.compiler_result is not None:
            self.compiler_result(compiler, captures)

        return Command(
            list_to_str(tokens),
            (lambda runtime: self.result(runtime, captures))
            if callable(self.result)
            else self.result
        )

    def __len__(self):
        return len(self.match)
