from datablox.subroutines import create_socket

class connection:
    # A connection to a host
    def __del__(self):
        self.socket.close()

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = create_socket()
