from .block import Block


class BlockStack:

    def __init__(self):
        self.blocks = [Block()]

    def __len__(self):
        return len(self.blocks)

    def open(self):
        print(" -------------- new block -------------")
        self.blocks.append(Block())

    def close(self):
        print(" ------------- block closed -----------")
        self.blocks[-2].append(self.blocks.pop(-1))

    def append(self, item):
        self.blocks[-1].append(item)

    def finish(self):
        while len(self.blocks) > 1:
            self.close()
        return self.blocks[0]
