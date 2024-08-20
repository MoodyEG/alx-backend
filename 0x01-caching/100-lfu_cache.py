#!/usr/bin/python3
""" LFU Caching """


BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ LFU Caching Class """

    def __init__(self):
        """ Initiliaze of the Class """
        super().__init__()
        self.used_keys = {}

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return
        if len(self.cache_data) >= self.MAX_ITEMS \
                and key not in self.cache_data:
            sorted_uk = sorted(self.used_keys, key=self.used_keys.get)
            discard = sorted_uk[0]

            check_list = []
            for keys in sorted_uk:
                if self.used_keys[keys] == self.used_keys[discard]:
                    check_list.append(keys)

            if len(check_list) != 1:
                counter = {}
                for keys in check_list:
                    counter[keys] = 0
                    for items in list(self.cache_data.keys()):
                        counter[keys] += 1
                        if items == keys:
                            break
                # print(counter)
                discard = min(counter, key=counter.get)

            self.cache_data.pop(discard)
            self.used_keys.pop(discard)
            print("DISCARD: {}".format(discard))
        if key in self.cache_data:
            self.cache_data.pop(key)
        self.cache_data[key] = item
        if key in self.used_keys:
            self.used_keys[key] += 1
        else:
            self.used_keys[key] = 1

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        self.cache_data[key] = self.cache_data.pop(key)
        self.used_keys[key] += 1
        return self.cache_data.get(key)
