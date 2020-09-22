from argparse import ArgumentParser
from datablox import networking
import random

def test_create_connection():
    con = networking.connection("0.0.0.0", 11201)
    con.connect()
    data = {}
    for k in range(random.randint(10, 1000)):
        data[str(k)] = "test"

    con.send(data)

def test_server():
    con = networking.connection("0.0.0.0", 11201)
    con.bind()

    while True:
        try:
            incoming = con.receive()
            print(len(incoming.keys()))
        except KeyboardInterrupt as err:
            con = None

if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument("-serve", action="store_true")
    args = ap.parse_args()

    if args.serve:
        test_server()
    else:
        test_create_connection()