# app/model/enums.py

from enum import Enum


class SortOptions(str, Enum):
    date = "date"
    popularity = "popularity"
    creation = "creation"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"