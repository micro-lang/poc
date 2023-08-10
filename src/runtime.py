class MicroRuntime: def __init__(self, block):
        self.block = block

    def allocate(self, address, value):
        self.memory[address] = value

    def free(self, address):
        del self.memory[address]

    def run(self):
        def run_block(block):
            for command in block.content:
                if callable(command):
                    command.run(self)
                else: run_block(command)
