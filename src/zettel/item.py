# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

from enum import IntEnum
from typing import List, Optional


class Priority(IntEnum):
    """
    Priority enum used in :py:class:`.Item`.

    Provider backends may use different representations for priorities. This
    enum will be used for abstract categorization, which providers can map their
    custom priorities to.
    """
    VERYLOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERYHIGH = 5


class Item:
    """
    A basic item, as abstraction for the provider's backend.

    This class represents a basic item, Zettel can manage. Providers will use it
    to represent the data of their backends in a uniform way, to give the
    representation layer some form of abstraction.
    """

    def __init__(self,
                 name: str,
                 priority: Optional[Priority] = None,
                 tags: Optional[List[str]] = None
                 ):
        """
        Constructor.


        :param name: Name of this item.
        :param priority: Priority of this item.
        :param tags: A list of tags, by which this and other items could be
            grouped or filtered.
        """
        self.name = name
        self.priority = priority
        self.tags = tags
