#!/usr/bin/env python3
"""
FIFO Cache Module
"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """FIFO Cache Class"""

    def __init__(self):
        """Initializer"""
        super().__init__()
        self.num_items = 0

    def put(self, key, item):
        """
        Assigns to the dictionary self.cache_data
        the item `value` for the key `key`.
        If the number of items in self.cache_data
        is higher than BaseCaching.MAX_ITEMS:
            * it discards the first item put in cache (FIFO algorithm)
            * it prints DISCARD: with the key discarded followed by a new line
        """
        if key is None or item is None:
            return

        if key not in self.cache_data.keys():
            self.num_items += 1

        if self.num_items > BaseCaching.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            del self.cache_data[first_key]
            print("DISCARD: {}".format(first_key))
            self.num_items -= 1

        self.cache_data[key] = item

    def get(self, key):
        """
        Returns the value in self.cache_data linked to `key`.
        """
        return self.cache_data.get(key)
