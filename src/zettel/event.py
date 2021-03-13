# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import datetime
from typing import Optional, Union

from .item import Item, Priority


class Event(Item):
    """
    Event item.

    This class extends the :py:class:`~.Item` class with additional attributes
    to represent event items, e.g. created from a calendar provider.
    """

    def __init__(self,
                 name: str,
                 start: Union[datetime.date, datetime.datetime],
                 end: Union[datetime.date, datetime.datetime],
                 all_day: bool = False,
                 priority: Optional[Priority] = None,
                 tags: Optional[list[str]] = None
                 ) -> None:
        """
        Constructor.

        This method initializes the event. It's identical to the one of
        :py:class:`~.Item`, except adding additional attributes.


        :param name: Name of this event.
        :param start: Start timestamp of this event.
        :param end: End timestamp of this event.
        :param all_day: If the event is all day.
        :param priority: Priority of this event.
        :param tags: A list of tags, by which this event and other items could
            be grouped or filtered.
        """
        self.start = start
        self.end = end
        self.all_day = all_day

        # As an event is basically just an item with additional attributes, the
        # remaining ones will be saved by initializing the parent class.
        super().__init__(name, priority, tags)
