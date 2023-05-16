#!/usr/bin/env python3
"""
Basic Cache Module
"""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """Basic Cache Class"""

    def put(self, key, item):
        """
        Assigns to the dictionary self.cache_data
        the item `value` for the key `key`.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """
        Returns the value in self.cache_data linked to `key`.
        """
        return self.cache_data.get(key)
