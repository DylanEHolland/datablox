from datablox import networking
from argparse import ArgumentParser

def test_create_connection():
    con = networking.connection("0.0.0.0", 11201)
    con.connect()
    con.send({"test": "message"})


def test_server():
    con = networking.connection("0.0.0.0", 11201)
    con.bind()

    while True:
        try:
            incoming = con.receive()
            print(incoming["test"])
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