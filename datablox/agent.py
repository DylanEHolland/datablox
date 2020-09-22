# import datablox.subroutines as subs
# import requests
# from datetime import datetime
# import json
# from .block import datablox
# from .row import datablox_row

import datablox.subroutines as sub
from datablox.config import config
from datablox.networking import connection

from datetime import datetime
import json
import os
import random

class agent:
    address = None
    created_at = None
    hostname = None
    parent = None
    previous = None

    def __init__(self, *args, **kwargs):
        incoming = sub.extract_args(*args, **kwargs)
        potential_signature = incoming.get('hash')
        arguments = incoming.get('arguments')
        
        if not potential_signature and not len(arguments):
            print("New agent?")

    def to_dict(self):
        return {
            'address': self.address,
            'hostname': self.hostname,
            'created_at': self.created_at
        }

    def from_dict(self):
        pass

class agent_chain:
    created_at = None
    parent = None
    seed = None

    new = None

    def __build_dir__(self):
        if not os.path.exists(config.agents_blocks_directory):
            sub.mkdir_recursively(config.agents_blocks_directory)
            return True
        return False

    def __del__(self):
        self.__sync__()

    def __init__(self, *args, **kwargs):
        incoming = sub.extract_args(*args, **kwargs)
        potential_signature = incoming.get('hash')
        arguments = incoming.get('arguments')

        if self.__build_dir__():
            self.new = True

        if self.new:
            self.seed, self.created_at = self.generate
            (
                arguments.get('seed')
            )
        else:
            if not potential_signature and not len(arguments):
                pass

    def __sync__(self):
        sub.write_file(
            "%s/signature.json" % config.agents_directory,
            json.dumps(self.signature())
        )

        sub.write_file(
            "%s/info.json" % config.agents_directory,
            json.dumps(self.to_dict())
        )

    def from_dict(self):
        pass

    def generate(self, seed = None):        
        created_at = datetime.now()
        if not seed:
            seed = random.randint(1, 100000)

        return seed, created_at
        

    def signature(self):
        return sub.hash_digest(
            json.dumps(
                self.to_dict()
            ).encode('utf-8')
        )

    def to_dict(self):
        return {
            'created_at': str(self.created_at),
            'parent': self.parent,
            'seed': self.seed
        }