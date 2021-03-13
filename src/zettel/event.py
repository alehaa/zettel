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

    @staticmethod
    def _isToday(d: Union[datetime.date, datetime.datetime]) -> bool:
        """
        Check if a specific date matches today's date.

        This method checks, whether a specific :py:class:`datetime.datetime` or
        :py:class:`datetime.date` matches today's date by just evaluating the
        date without time information.


        :param d: The :py:class:`datetime.date` object to be checked.
        """
        return ((d.date() if isinstance(d, datetime.datetime) else d)
                == datetime.date.today())

    @staticmethod
    def timeToday(min: bool = True,
                  tzinfo: Optional[datetime.tzinfo] = None
                  ) -> datetime.datetime:
        """
        Get a timestamp for today's date.

        For today's date, this method gets either the minimum date and time
        (midnight) or the maximum (just before mifnight).


        :param min: Whether to get the minimum or maximum date and time.
        :param tzinfo: Optional timezone information to use. If :py:class:`None`
            is provided, the system's default timezone will be used.

        :returns: The :py:class:`datetime.datetime` object matching the criteria
            defined via parameters.
        """
        return datetime.datetime.combine(datetime.datetime.today(),
                                         (datetime.datetime.min.time() if min
                                          else datetime.datetime.max.time())
                                         ).astimezone(tz=tzinfo)

    def __init__(self,
                 name: str,
                 start: datetime.datetime,
                 end: datetime.datetime,
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
        # The start and end timestamp will be used as attributes for this event
        # object. However, if the meeting doesn't start or end today, the
        # timestamps will be capped to the minimum and maximum time of today for
        # the right representation from today's perspective.
        self.start = (start if self._isToday(start) else self.timeToday())
        self.end = (end if self._isToday(end) else self.timeToday(False))

        # Flag the event as 'all day' not even just if the related parameter is
        # set, but for meetings spanning multiple days, as these are all day
        # from today's perspective, too.
        self.all_day = all_day or (not self._isToday(start)
                                   and not self._isToday(end))

        # As an event is basically just an item with additional attributes, the
        # remaining ones will be saved by initializing the parent class.
        super().__init__(name, priority, tags)
