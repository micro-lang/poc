class Capture:
    def __init__(self, name, types):
        self.name = name
        self.types = types

    def match(self, token, compiler):
        def match_aux(t):
            compiled_type = compiler.type_get(t)
            if isinstance(compiled_type, bool):
                return compiled_type
            import re
            return re.match(compiled_type, token)

        if len(self) == 1:
            return match_aux(self.types)
        for t in self.types:
            if match_aux(t):
                return True
        return False

    def __len__(self):
        return 1 if type(self.types) is not list else len(self.types)

    def __str__(self):
        return "Capture{" + self.name + "}"
