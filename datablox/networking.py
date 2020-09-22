from datablox.subroutines import create_socket, hash_digest
import json

class data_packet:
    data = None

    def __init__(self, **kwargs):
        if 'data' not in kwargs:
            self.data = json.dumps(kwargs)
        else:
            self.data = kwargs.get('data')

    def header(self):
        size = len(self.data)
        output = list(str(size))
        output.append('E')

        return output

    def signature(self):
        return hash_digest(
            self.data.encode()
        )

    def to_dict(self):
        return json.loads(self.data)

class connection:
    def __del__(self):
        self.socket.close()
        self.socket = None

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = create_socket()

    def bind(self):
        self.socket.bind( (self.address, self.port) )
        self.socket.listen(1)

    def connect(self):
        self.socket.connect( 
            (self.address, self.port)
        )

    def send(self, data):
        pkt = data_packet(**data)
        tfr = transfer(self, pkt)
        tfr.push()

    def receive(self):
        tfr = transfer(self)
        return tfr.pull()

class transfer:
    def __init__(self, connection, packet = None):
        self.connection = connection

        if packet:
            self.packet = packet

    def push(self):
        # TODO: This should be it's own class
        for char in self.packet.header():
            self.connection.socket.send(bytes(char.encode('utf-8')))

        self.connection.socket.send(bytes(self.packet.data.encode('utf-8')))
        self.connection.socket.send(
            bytes(self.packet.signature().encode('utf'))
        )

    def pull(self):
        # TODO: This should be it's own class

        incoming_connection, incoming_address = self.connection.socket.accept()

        char = None
        incoming_packet_size = []
        while char != 'E':
            if char:
                incoming_packet_size.append(char)
            char = incoming_connection.recv(1).decode('utf-8')
        
        incoming_packet_size = int("".join(incoming_packet_size))
        data = incoming_connection.recv(incoming_packet_size).decode('utf-8')
        incoming_packet = data_packet(data = data)
        incoming_signature = incoming_connection.recv(32).decode('utf-8')
        
        if incoming_signature == incoming_packet.signature():
            return incoming_packet.to_dict()
        else:
            raise Exception("Packet mismatch")
