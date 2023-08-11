class Command:
    def __init__(self, name, run):
        self.name = name
        self.run = run

    def print(self, identation):
        tabs = ''
        for _ in range(identation):
            tabs += "| "
        print(tabs + str(self))

    def __call__(self, runtime):
        return self.run(runtime)

    def __str__(self):
        return self.name + " " + str(self.run)
