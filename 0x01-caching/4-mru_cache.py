#!/usr/bin/env python3
"""
MRU Cache Module
"""

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """MRU Cache Class"""

    def __init__(self):
        """Initializer"""
        super().__init__()
        self.num_items = 0
        self.cache_recency = {}
        self.counter = 0

    def put(self, key, item):
        """
        Assigns to the dictionary self.cache_data
        the item `value` for the key `key`.
        If the number of items in self.cache_data
        is higher than BaseCaching.MAX_ITEMS:
            * it discards the most recently used item (MRU algorithm)
            * it prints DISCARD: with the key discarded followed by a new line
        """
        if key is None or item is None:
            return

        if key not in self.cache_data.keys():
            self.num_items += 1

        if self.num_items > BaseCaching.MAX_ITEMS:
            sorted_cache_recency = sorted(self.cache_recency.items(),
                                          key=lambda x: x[1], reverse=True)
            lru_key, lru_value = next(iter(sorted_cache_recency))
            del self.cache_recency[lru_key]
            del self.cache_data[lru_key]
            print("DISCARD: {}".format(lru_key))
            self.num_items -= 1

        self.cache_data[key] = item
        self.cache_recency[key] = self.counter
        self.counter += 1

    def get(self, key):
        """
        Returns the value in self.cache_data linked to `key`.
        """
        if key in self.cache_recency.keys():
            self.cache_recency[key] = self.counter
            self.counter += 1
        return self.cache_data.get(key)
