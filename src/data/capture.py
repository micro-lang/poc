class Capture:
    name = ""

    def __init__(self, _name):
        self.name = _name

    def __str__(self):
        return "Capture{".join(self.name).join("}")
