class hoarder:
    def __new__(cls, **kwargs):
        print(kwargs)
        return "Hello"