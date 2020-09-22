#
#   Base datablox
#   A distributed list
#
import os
import json
from datablox.subroutines import mkdir_recursively, read_file, \
    write_file

class Block(object):
    created_at = None
    data = None
    previous = None

    def __del__(self):
        print("[Block] in __del__")

    def __getitem__(self, key):
        return self.data.get(key)

    def __init__(self, *args, **kwargs):
        print("[Block] in __init__")
        directory = None

        if not len(args) and not len(kwargs):
            print("Nothing to do")

        if len(kwargs.keys()):
            potential_dir = kwargs.get('directory')
            if not directory and potential_dir:
                directory = potential_dir

        if not directory:
            directory = ".blocks"
        
        self.directory = directory
        self.load()
        #self.data = Block_data()
            
    def __str__(self):
        return "<block>"

    def commit(self):
        print("[Block] commit")

    def digest(self):
        print("[Block] digest")

    def load(self):
        print(self.directory)
        
class Block_data:
    store = None

    def __init__(self, **data):
        if not len(data):
            raise Exception("Block_data with no data?")
        store_buffer = {}
        for key in data:
            store_buffer[key] = data.get('key')

        setattr(self, "store", store_buffer)

    def digest(self):
        pass

    def get(self, key):
        return getattr(self, "store").get(key)

class Block_dir:
    directory = None
    head = None