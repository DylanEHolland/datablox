import datablox.subroutines as subs
import os
import requests
from datetime import datetime
import json
from .hoarder import hoarder

class datablox_agent(object):
    created_at = None
    db_directory = None
    filename = None
    committed = None
    local_address = None
    public_address = None
    hostname = None
    name = None
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
        self.socket.listen(1)

        while True:
            try:
                connection, addr = self.socket.accept()
                incoming = self.receive(connection)
                
                if "test" in incoming:
                    print("Replying to test")
                    self.send("Test callback", connection=connection)
                else:
                    print(incoming)                
                    self.send("Something else", connection=connection)
            except KeyboardInterrupt as err:
                print("Cleanly shutting down")
                self.socket = None
                break
    def connect(self):
        self.socket.connect((self.local_address, 11001))

    def initiate(self):
        # Initiate session with server
        if not self.socket:
            self.connect()

        self.send(self.signature)

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
        data['agent'] = self.signature
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