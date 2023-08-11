class MicroRuntime:
    def __init__(self, block):
        self.block = block
        self.memory = {}

    def allocate(self, address, value):
        self.memory[address] = value

    def get(self, address):
        print(self.memory[address])
        return self.memory[address]

    def free(self, address):
        del self.memory[address]

    def run(self):
        print("starting")

        def run_block(block):
            for item in block.content:
                if callable(item):
                    print("running item")
                    print(item)
                    item(self)
                else:
                    print("running block")
                    item.print(0)
                    run_block(item)
        run_block(self.block)
        print("finished")
