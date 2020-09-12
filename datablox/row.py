import datablox.subroutines as subs
import os
from datablox import allowed_types
from datetime import datetime
import json

class datablox_row(object):
    committed = None
    created_at = None
    directory = None
    parent = None
    previous = None
    value = None
    parent_signature = None
    signature = None

    def __init__(self, *args, **kwargs):
        potential_hash = None
        loaded = False

        if len(args):
            potential_hash = args[0]
        
        directory = ""    
        if len(kwargs):
            parent = kwargs.get('parent'),
            value = kwargs.get('value')
            foreign_data = kwargs.get('from_dict')
            if parent and len(parent) and parent[0]:
                self.parent = parent[0]
                self.directory = self.parent.directory() + "/blocks"
                self.value = value

            if foreign_data and type(foreign_data) == dict:
                self.from_dict(foreign_data)
                loaded = True

        if potential_hash:
            # Load existing
            self.signature = potential_hash
            self.load()

    def __str__(self):
        return "<%s: %s>" % (
            self.parent.name,
            self.signature
        )

    def __setattr__(self, key, value):
        if key == "value" and type(value) != allowed_types[self.parent.row_type] and value != None:
            raise TypeError(self.parent.name, "is of", self.parent.row_type, "type")

        object.__setattr__(self, key, value)


    def commit(self):  
        if self.committed:
            return None

        if not self.previous:
            self.previous = self.parent.tail

        if not self.created_at:
            self.created_at = datetime.now()

        digest = self.digest()
        filename = self.directory + "/" + digest
        if not os.path.isfile(filename):
            subs.write_file(filename, json.dumps(self.to_dict()))

        if not self.parent.head:
            self.parent.head = digest     

        self.signature = digest
        self.parent.tail = digest
        self.parent.hash_list.append(digest)
        self.comitted = True
        
    
    def digest(self):
        hashable = "%s-%s" % (
            self.parent.signature,
            str(self.to_dict())
        )

        return subs.hash_digest(hashable.encode())
    
    def from_dict(self, foreign_data):
        self.created_at = subs.datetime_from_string(foreign_data.get('created_at'))
        self.previous = foreign_data.get('previous')
        self.value = allowed_types[self.parent.row_type](foreign_data.get('value'))
        self.parent_signature = foreign_data.get('parent_signature')

    def load(self):
        filename = "%s/%s" % (self.directory, self.signature)
        data = subs.read_file(filename)
        if data:
            data = json.loads(data)
            self.value = allowed_types[self.parent.row_type](data['value'])
            self.previous = data['previous']
            self.created_at = subs.datetime_from_string(data['created_at'])
            self.parent_signature = data['parent_signature']
            if self.digest() != self.signature:
                raise Exception("Uhh... Block Signature/Digest mismatch")
            else:
                self.committed = True

    def to_dict(self):
        return {
            'value': self.value,
            'type': self.parent.row_type,
            'previous': self.previous,
            'created_at': str(self.created_at),
            'parent_signature': self.parent.signature
        }