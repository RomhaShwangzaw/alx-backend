#!/usr/bin/env python3
"""Index Range Module"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple of size two containing a start index and an
    end index corresponding to the range of indexes to return
    in a list for those particular pagination parameters.
    """
    start = page * page_size - page_size
    end = start + page_size
    return (start, end)
