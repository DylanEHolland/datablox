from datablox.agent import foreign_agent

def test_create_foreign_agent():
    data = {"name": "dylan", "created_at": "2020-09-15 20:03:10.157952", "local_address": "127.0.1.1", "public_address": "50.44.230.100", "hostname": "grendel", "signature": "67fad5dd14456ac885f9b471d66d9cb5"}
    digest = data['signature']
    del(data['signature'])
    del(data['local_address'])

    foreign_agent(digest, from_dict = data)

if __name__ == "__main__":
    test_create_foreign_agent()