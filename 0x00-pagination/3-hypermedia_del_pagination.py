#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> dict:
        """ Get hypermedia pagination """

        dataset = self.indexed_dataset()
        index = index if index else 0
        dic_keys = sorted(dataset.keys())
        assert index >= 0 and index <= dic_keys[-1]
        index_list = []
        for i in dic_keys:
            if i >= index and len(index_list) <= page_size:
                index_list.append(i)
        data = []
        for j in index_list[:-1]:
            data.append(dataset[j])
        if len(index_list) - page_size == 1:
            next_index = index_list[-1]
        else:
            next_index = None
        return {
            'index': index,
            'data': data,
            'page_size': len(data),
            'next_index': next_index
            }
