from datablox.networking import packet

def test_packet_create():
    pkt = packet(
        id = 1,
        user = "test",
        pword = "anoth3rt3$t"
    )

    pkt_two = packet(
        data = pkt.data
    )

    assert pkt.signature() == pkt_two.signature()

if __name__ == "__main__":
    test_packet_create()