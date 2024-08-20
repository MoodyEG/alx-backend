#!/usr/bin/python3
""" LIFO Caching """


BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO Caching Class """

    def __init__(self):
        """ Initiliaze of the Class """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return
        if len(self.cache_data) >= self.MAX_ITEMS \
                and key not in self.cache_data:
            discard = list(self.cache_data.keys())[-1]
            self.cache_data.pop(discard)
            print("DISCARD: {}".format(discard))
        if key in self.cache_data:
            self.cache_data.pop(key)
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
