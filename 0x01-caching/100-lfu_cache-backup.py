#!/usr/bin/env python3
"""
LFU Cache Module
"""

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """LFU Cache Class"""

    def __init__(self):
        """Initializer"""
        super().__init__()
        self.num_items = 0
        self.cache_recency = {}
        self.cache_frequency = {}
        self.counter = 0

    def put(self, key, item):
        """
        Assigns to the dictionary self.cache_data
        the item `value` for the key `key`.
        If the number of items in self.cache_data
        is higher than BaseCaching.MAX_ITEMS:
            * it discards the least frequently used item (LFU algorithm)
            * if it finds more than 1 item to discard, it uses the LRU
              algorithm to discard only the least recently used
            * it prints DISCARD: with the key discarded followed by a new line
        """
        if key is None or item is None:
            return

        if key not in self.cache_data.keys():
            self.num_items += 1

        if self.num_items > BaseCaching.MAX_ITEMS:
            sorted_cache_frequency = sorted(self.cache_frequency.items(),
                                            key=lambda x: x[1])
            i = 0
            lfu_key, lfu_value = sorted_cache_frequency[i]
            next_value = -1
            i += 1
            if i < len(sorted_cache_frequency):
                next_key, next_value = sorted_cache_frequency[i]
            while next_value == lfu_value:
                if self.cache_recency[next_key] < self.cache_recency[lfu_key]:
                    lfu_key, lfu_value = next_key, next_value
                i += 1
                if i < len(sorted_cache_frequency):
                    next_key, next_value = sorted_cache_frequency[i]
                else:
                    break
            del self.cache_recency[lfu_key]
            del self.cache_frequency[lfu_key]
            del self.cache_data[lfu_key]
            print("DISCARD: {}".format(lfu_key))
            self.num_items -= 1

        self.cache_data[key] = item
        self.cache_recency[key] = self.counter
        self.counter += 1
        if key in self.cache_frequency.keys():
            self.cache_frequency[key] += 1
        else:
            self.cache_frequency[key] = 1

    def get(self, key):
        """
        Returns the value in self.cache_data linked to `key`.
        """
        if key in self.cache_recency.keys():
            self.cache_recency[key] = self.counter
            self.counter += 1

        if key in self.cache_frequency.keys():
            self.cache_frequency[key] += 1

        return self.cache_data.get(key)
