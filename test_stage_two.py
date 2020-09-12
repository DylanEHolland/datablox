from datablox import datablox, datablox_agent, datablox_row

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
    details = db_agent.request({"datablox": "test_ledger", "fetch_details": True})
    #print(details)
    dbx = datablox("test_ledger",
        agent = db_agent,
        db_directory = "/tmp/datablox_clone", 
        from_dict = details
    )

    dbx.commit()
    print(dbx)

def test_fetch_blocks():
    db_agent = datablox_agent("cli", db_directory = "/tmp/datablox_clone")
    #print(db_agent.request({"fetch_details": "test_ledger"}))
    blocks = db_agent.request({"fetch_blocks": "test_ledger"})
    block = blocks[-1]
    dbx = datablox("test_ledger", db_directory = "/tmp/datablox_clone", agent = db_agent)
    #print(dbx)
    while block != None:
        block = db_agent.request({"datablox": "test_ledger", "block": block})
        row = datablox_row(from_dict = block, parent = dbx)
        print(row.parent_signature)
        #print("From peer:", block)
        break
        test_block = dict(block)
        block = block['previous']

if __name__ == "__main__":
    test_client()
    test_agent_handshake()
    test_fetch()
    test_fetch_blocks()