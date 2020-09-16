from datablox import datablox, datablox_agent

def f(x):
    return (3*x) + (7)

def test_agent():
    db_agent = datablox_agent("dylan", db_directory = "/tmp/datablox")
    print(db_agent)
    print(db_agent.commit())
    print(db_agent)

def test_create_datablox():
    db_agent = datablox_agent("dylan", db_directory = "/tmp/datablox")
    dbx = datablox(
        name = "test_ledger",
        row_type = "integer",
        agent = db_agent
    )
    dbx.commit()
    
    for n in range(10):
        new_row = dbx.add(f(n))
        new_row.commit()
        print(new_row)
    dbx.commit()
    print(dbx)
    print(dbx.hash_list)

def test_load_datablox():
    db_agent = datablox_agent("dylan", db_directory = "/tmp/datablox")
    dbx = datablox("test_ledger", db_directory = "/tmp/datablox", agent = db_agent)
    for row in dbx:
        print(row.value)

    print(dbx.dataframe())

if __name__ == "__main__":
    test_agent()
    test_create_datablox()
    test_load_datablox()