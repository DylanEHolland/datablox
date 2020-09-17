import datablox.subroutines as subs
import os
import requests
from datetime import datetime
import json
from .block import datablox
from .row import datablox_row

class datablox_agent(object):
    agent_list = None
    committed = None
    created_at = None
    db_directory = None
    filename = None
    hostname = None
    local_address = None
    name = None
    public_address = None
    signature = None
    socket = None

    def __init__(self, *args, **kwargs):
        if len(args):
            self.name = args[0]

        if len(kwargs):
            if 'db_directory' in kwargs:
                self.db_directory = kwargs.get('db_directory')

        self.hostname = subs.socket.gethostname()
        self.local_address = subs.socket.gethostbyname(self.hostname)
        self.public_address = requests.get('https://checkip.amazonaws.com').text.strip()

        if not self.db_directory:
            self.db.directory = "./"
        self.directory = "%s/agents" % self.db_directory
        self.filename = "%s/%s" % (self.directory, self.name)
        self.agent_list = []
        if os.path.isfile(self.filename):
            self.load()
        self.socket = subs.create_socket()

    def __str__(self):
        if not self.signature:
            return "<%s [tmp agent]>" % (
                self.hostname
            )
        else:
            return "<%s:%s>" % (
                self.hostname,
                self.public_address
            )

    def commit(self):
        if not self.committed:
            self.created_at = datetime.now()
            self.signature = self.digest()
            
            if not os.path.exists(self.directory):
                subs.mkdir_recursively(self.directory)
            
            subs.write_file(self.filename, json.dumps(self.to_dict()))
            self.agent_list.append(self.signature)
        
        subs.write_file(self.db_directory + "/agents.json", json.dumps(self.agent_list))
        self.committed = True

    def digest(self):
        buffer = "%s-%s-%s-%s-%s" % (
            self.name,
            self.created_at,
            self.public_address,
            self.local_address,
            self.hostname
        )
        
        return subs.hash_digest(buffer.encode())

    def load(self):
        buffer = subs.read_file(self.filename)
        buffer = json.loads(buffer)
        if os.path.isfile("%s/agents.json" % self.db_directory):
            agents_buffer = subs.read_file("%s/agents.json" % self.db_directory)
            agents_buffer = json.loads(agents_buffer)
            self.agent_list = agents_buffer

        self.name = buffer['name']
        self.created_at = subs.datetime_from_string(buffer['created_at'])
        self.public_address = buffer['public_address']
        self.local_address = buffer['local_address']
        self.hostname = buffer['hostname']
        self.signature = buffer['signature']
        if not self.signature or (self.digest() != self.signature):
            raise Exception("Uhh... agent digest/signature mismatch")
        
        self.committed = True

    def serve(self):
        self.socket.bind((self.local_address, 11001))
        self.socket.listen(5)

        while True:
            try:
                connection, addr = self.socket.accept()
                print(addr)
                incoming = self.receive(connection)
                print(incoming, type(incoming))

                if not incoming:
                    self.send("[Error] You sent nothing", connection=connection)
                else:
                    if type(incoming) == dict and "test" in incoming:
                        print("Replying to test")
                        self.send("Test callback", connection=connection)
                    else:
                        agent = None                        
                        fetch_blocks = False
                        block = False
                        datablox_name = None
                        details = None

                        if type(incoming) == str:
                            agent = incoming                    
                            if agent not in self.agent_list:
                                print("Discovered new agent")
                                self.send(self.agent_list, connection = connection)
                                self.agent_list.append(agent)
                                self.commit()
                            
                                self.send("Success", connection = connection)
                        elif type(incoming) == dict:
                            print("Is dict")
                            if "agent" in incoming:
                                agent = incoming.get("agent")
                            
                            if "datablox" in incoming:
                                print("got datablox name")
                                datablox_name = incoming.get("datablox")

                            if "fetch_blocks" in incoming:
                                fetch_blocks = incoming.get("fetch_blocks")

                            if "fetch_details" in incoming:
                                details = True

                            if "block" in incoming:
                                print("looking for block")
                                block = incoming.get('block')

                        if not agent:
                            self.send("[Error] Agent required without test attr", connection=connection)

                        if agent not in self.agent_list:
                            self.send("[Error] Agent unknown. Initiate before making requests.", connection=connection)
                        
                        if fetch_blocks:
                            blocks = datablox(str(fetch_blocks), db_directory = self.db_directory, agent = self).dump()
                            self.send(blocks, connection=connection)
                        
                        if block and datablox_name:
                            print(block, datablox_name)
                            dbx = datablox(str(datablox_name), db_directory = self.db_directory, agent = self)
                            self.send(datablox_row(block, parent = dbx).to_dict(), connection=connection)

                        if details and datablox_name:
                            dbx = datablox(str(datablox_name), db_directory = self.db_directory, agent = self)
                            self.send(dbx.to_dict(), connection=connection)

                        self.send("[Warning] nothing to do", connection=connection)

            except KeyboardInterrupt as err:
                print("Cleanly shutting down")
                self.socket = None
                break
            
        self.socket = None

    def connect(self):
        if not self.socket:
            self.socket = subs.create_socket()

        self.socket.connect((self.local_address, 11001))

    def initiate(self):
        # Initiate session with server
        if not self.committed:
            print("[Error] Must commit agent before making calls to other nodes")
            return False

        self.connect()
        server_connection = self.send(self.signature)
        buffer = self.receive(server_connection)
        if type(buffer) == list:
            self.agent_list += buffer
            self.commit()
        else:
            if "Error" in buffer:
                print("Something went wrong:", buffer)
        self.socket = None
                
    def request(self, data):
        self.connect()
        data['agent'] = self.signature

        con = self.send(data)
        buffer = self.receive(con)
        self.socket = None
        return buffer

    def receive(self, connection):
        char = None
        packet_size = None
        packet_size_buffer = []
        while True:
            char = connection.recv(1).decode()
            if char == "E":
                break

            packet_size_buffer.append(char)
        
        packet_size = int("".join(packet_size_buffer))
        buffer = connection.recv(packet_size).decode('utf-8')
        buffer = json.loads(buffer)
        
        return buffer

    def send(self, data, connection = None):
        data = json.dumps(data).encode('utf-8')
        
        if not connection:
            socket = self.socket
        else:
            socket = connection

        # Send size first
        data_size = str(len(data))
        data_size = list(data_size)
        data_size.append('E')
        for n in data_size:
            socket.send(bytes(n.encode()))

        socket.send(bytes(data))
        return socket

    def to_dict(self):
        return {
            'name': self.name,
            'created_at': str(self.created_at),
            'local_address': self.local_address,
            'public_address': self.public_address,
            'hostname': self.hostname,
            'signature': self.digest()
        }

class foreign_agent:
    keys = ['name', 'created_at', 'public_address', 'hostname']
    
    created_at = None
    hostname = None
    name = None
    public_address = None
    signature = None

    def __init__(self, *args, **kwargs):
        arguments = subs.extract_args(*args, **kwargs)
        if arguments.get('hash'):
            self.signature = arguments.get('hash')

        if 'from_dict' in arguments['arguments']:
            self.load(arguments['arguments'].get('from_dict'))

    def load(self, data):
        for attr in data:
            print(attr in self.keys)