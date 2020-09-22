import os

def genvar(name, default):
    name = "dblx_%s" % name
    var_buffer = os.environ.get(name)
    return var_buffer if var_buffer else default

class config:
    def __init__(self):
        self.directory = genvar("directory", "/tmp/datablox")
        self.agents_directory = genvar("agents_directory", "%s/agents" % self.directory)
        self.agents_blocks_directory = genvar("agents_blocks_directory", "%s/blocks" % self.agents_directory)

config = config()