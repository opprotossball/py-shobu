from collections import OrderedDict

class HashTable(OrderedDict):

    def __init__(self, *args, **kwds):
        self.size_limit = kwds.pop("size_limit", 2**20 + 7)
        OrderedDict.__init__(self, *args, **kwds)

    def __setitem__(self, key, value):
        if len(self) >= self.size_limit:
            self.popitem(last=False)
        OrderedDict.__setitem__(self, key, value)
