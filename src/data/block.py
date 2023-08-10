class Block:
    def __init__(self):
        self.content = []

    def append(self, item):
        self.content.append(item)

    def print(self, identation):
        tabs = ''
        for _ in range(identation):
            tabs += "| "

        print(tabs)
        print(tabs + "Block | " + str(identation))
        for item in self.content:
            item.print(identation + 1)
        print(tabs)
