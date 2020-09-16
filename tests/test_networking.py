from datablox import networking
from argparse import ArgumentParser

def test_create_connection():
    con = networking.connection("0.0.0.0", 11201)
    print(con)

def test_server():
    pass

if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument("-serve", action="store_true")
    args = ap.parse_args()

    if args.serve:
        test_server()
    else:
        test_create_connection()