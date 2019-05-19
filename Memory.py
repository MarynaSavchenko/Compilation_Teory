class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.elements = {}

    def has_key(self, name):  # variable name
        return name in self.elements

    def get(self, name):  # gets from memory current value of variable <name>
        return self.elements[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.elements[name] = value


class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = list()

        if memory is None:
            self.stack.insert(0, Memory("global"))
        else:
            self.stack.insert(0, memory)

    def get(self, name):  # gets from memory stack current value of variable <name>
        for memory in self.stack:
            if memory.has_key(name):
                return memory.get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[0].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        for memory in self.stack:
            if memory.has_key(name):
                memory.put(name, value)
                break

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.insert(0, memory)

    def pop(self):  # pops the top memory from the stack
        return self.stack.pop(0)
