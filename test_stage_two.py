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

def test_clone():
    db_agent = datablox_agent("cli", db_directory = "/tmp/datablox_clone")
    db_agent.commit()
    db_agent.connect()

    data = {
        "clone": ["test_ledger"]
    }

if __name__ == "__main__":
    #test_client()
    test_agent_handshake()