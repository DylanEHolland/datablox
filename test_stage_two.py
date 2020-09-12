from datablox import datablox, datablox_agent

def test_client():
    db_agent = datablox_agent("cli", db_directory = "/tmp/datablox_clone")
    db_agent.commit()
    db_agent.connect()
    data = {
        "test": {"one": [1,2,3,4], "two": "hello"},
    }
    
    con = db_agent.send(data)
    cb = db_agent.receive(con)
    print(cb)
    assert cb == "Test callback"

def test_agent_handshake():
    db_agent = datablox_agent("cli", db_directory = "/tmp/datablox_clone")
    db_agent.initiate()

def test_fetch():
    db_agent = datablox_agent("cli", db_directory = "/tmp/datablox_clone")
    blocks = db_agent.request({"fetch_blocks": "test_ledger"})
    block = db_agent.request({"datablox": "test_ledger", "block": blocks[0]})
    #block = db_agent.request({'datablox': 'test_ledger', 'block': '87caaccaa799d3f97019abac02039e32'})
    print(block)
    

if __name__ == "__main__":
    #test_client()
    #test_agent_handshake()
    test_fetch()