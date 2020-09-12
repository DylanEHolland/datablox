import datablox.subroutines as subs
import pandas
import os
from datetime import datetime
import json
import requests
import sys
from datablox import allowed_types
from .row import datablox_row

class datablox(object):
    created_at = None
    db_directory = None
    end_iter = False
    head = None
    name = None
    row_type = None
    signature = None
    tail = None
    committed = False
    current_block = None
    index = None
    hash_list = None
    
    def __del__(self):
        self.socket = None

    def __init__(self, *args, **kwargs):
        name = None
        agent = None
        loaded = False

        if len(kwargs):
            name = kwargs.get('name')
            row_type = kwargs.get('row_type')
            db_directory = kwargs.get('db_directory')
            foreign_details = kwargs.get('from_dict')
            
            if 'agent' in kwargs:
                agent = kwargs.get('agent')

            if db_directory:
                self.db_directory = db_directory

            if name:
                self.name = name

            if foreign_details and type(foreign_details) == dict:
                self.from_dict(foreign_details)
                loaded = True

            if row_type:
                if row_type in allowed_types:
                    self.row_type = row_type
                else:
                    raise Exception(self.row_type, "is not an allowed type")

        if not agent:
            raise Exception("Uh... must provide an agent")
        else:
            self.agent = agent

        if not self.db_directory:
            self.db_directory = "/tmp/datablox"

        if len(args):
            self.name = args[0]
    
        if not self.name:
            raise Exception("Uh... Datablox have to have a name.")
        else:
            if os.path.isfile("%s/details.json" % self.directory()):
                self.load()

        if not self.row_type:
            raise Exception("Uh... No type defined.")

        if not self.hash_list:
            self.hash_list = []

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.hash_list):
            raise StopIteration
        
        block = datablox_row(self.hash_list[self.index], parent = self)
        self.index += 1
        return block

    def __str__(self):
        output = "<wip datablox>"

        if self.committed:
            output = "<[Datablox in %s]: %s @ %s>" % (
                self.db_directory,
                self.name,
                self.tail
            )

        return output

    def dataframe(self):
        column_buffer = [
            datablox_row(row, parent = self).value
            for row in self.hash_list
        ]

        return pandas.DataFrame(
            column_buffer,
            columns = [self.name]
        )

    def digest(self):
        hashable = "%s-%s-%s" % (
            str(self.created_at),
            str(self.row_type),
            str(self.name)
        )

        return subs.hash_digest(hashable.encode())

    def directory(self):
        return "%s/%s" % (self.db_directory, self.name)

    def dump(self):
        return self.hash_list

    def from_dict(self, foreign_details):
        self.created_at = subs.datetime_from_string(foreign_details.get('created_at'))
        self.head = foreign_details.get('head')
        self.tail = foreign_details.get('tail')
        self.signature = foreign_details.get('signature')
        self.row_type = foreign_details.get('row_type')

    def add(self, value):
        output = datablox_row(
            value = value,
            parent = self
        )

        return output

    def commit(self, force = False):
        info_file = "%s/details.json" % self.directory()
        hashlist_file = "%s/list.json" % self.directory()
        blockdir = "%s/blocks" % self.directory()

        if not self.committed:
            if not os.path.exists(blockdir):
                subs.mkdir_recursively(blockdir)

            if not self.created_at:
                self.created_at = datetime.now()
            
            if not self.signature:
                self.signature = self.digest()

            self.committed = True

        subs.write_file(info_file, json.dumps(self.to_dict()))
        write_hashlist = False
        if os.path.isfile(hashlist_file):
            old_hashlist = json.loads(subs.read_file(hashlist_file))
            if len(self.hash_list) != len(old_hashlist):
                write_hashlist = True
        else:
            write_hashlist = True

        if write_hashlist:
            subs.write_file(hashlist_file, json.dumps(self.hash_list))

    def load(self):
        if not os.path.exists(self.directory()):
            raise Exception("Uhh... No datablox by that name.")

        details_filename = "%s/%s" % (self.directory(), "details.json")
        details = subs.read_file(details_filename)
        details = json.loads(details)
        
        hashlist_filename = "%s/%s" % (self.directory(), "list.json")
        hashlist = subs.read_file(hashlist_filename)
        hashlist = json.loads(hashlist)

        self.created_at = subs.datetime_from_string(details['created_at'])
        self.head = details['head']
        self.tail = details['tail']
        self.row_type = details['row_type']
        self.signature = details['signature']
        self.hash_list = hashlist

        if self.signature != self.digest():
            raise Exception("Uhh... Problem in ", self.name, "'s digest/signature match.")
        
        self.committed = True


    def to_dict(self):
        return {
            'created_at': str(self.created_at),
            'head': self.head,
            'row_type': self.row_type,
            'tail': self.tail,
            'signature': self.signature
        }