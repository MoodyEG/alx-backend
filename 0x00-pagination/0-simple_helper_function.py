#!/usr/bin/env python3
""" Where are we """


def index_range(page: int, page_size: int) -> tuple:
    """ Where are we """
    return (page - 1) * page_size, page * page_size
