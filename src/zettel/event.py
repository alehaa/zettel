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
    def toDateTime(d: Union[datetime.date, datetime.datetime],
                   end: bool = False,
                   tzinfo: Optional[datetime.tzinfo] = None
                   ) -> datetime.datetime:
        """
        Convert ``d`` into a standardized :py:class:`datetime.datetime`.

        This method takes a :py:class:`datetime.date` or
        :py:class:`datetime.datetime` object and converts it into a
        timezone-aware :py:class:`datetime.datetime` object.

        .. note:: Providers should use this method to generate a standardized
            format of timestamps, which can be compared to each other and have
            a timezone applied.


        :param d: The :py:class:`datetime.datetime` or :py:class:`datetime.date`
            compatible object to convert.
        :param end: Whether this timestamp should represent the end of an event.
            If ``d`` is just a :py:class:`datetime.date` object, this parameter
            defines to use the maximum time of a day instead of the minimum.
        :param tzinfo: Optional timezone information to use. If :py:class:`None`
            is provided, the system's default timezone will be used.

        :returns: The converted :py:class:`datetime.datetime` object.
        """
        return (
            # If 'd' already is a datetime object, it can be used for further
            # processing without converting.
            d if isinstance(d, datetime.datetime)

            # Otherwise it is assumed, 'd' is just a date object without time
            # information. Therefore, this date will be merged with either the
            # minimum time of a day, or the maximum, if an end timestamp should
            # be generated.
            else datetime.datetime.combine(
                d,
                (datetime.datetime.min.time() if not end
                 else datetime.datetime.max.time()))

            # Finally, apply the desired timezone to the original or generated
            # datetime object. If no timezone has been defined, the system's
            # default timezone will be used.
        ).astimezone(tz=tzinfo)

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

    @classmethod
    def timeToday(cls,
                  end: bool = False,
                  tzinfo: Optional[datetime.tzinfo] = None
                  ) -> datetime.datetime:
        """
        Get a timestamp for today's date.

        For today's date, this method gets either the minimum date and time
        (midnight) or the maximum (just before midnight).


        :param end: Whether the timestamp should represent the end of the day.
        :param tzinfo: Optional timezone information to use. If :py:class:`None`
            is provided, the system's default timezone will be used.

        :returns: The :py:class:`datetime.datetime` object matching the criteria
            defined via parameters.
        """
        return cls.toDateTime(datetime.date.today(), end, tzinfo)

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
        self._start = start
        self._end = end

        # Flag the event as 'all day' not even just if the related parameter is
        # set, but for meetings spanning multiple days, as these are all day
        # from today's perspective, too.
        self.all_day = all_day or (not self._isToday(start)
                                   and not self._isToday(end))

        # As an event is basically just an item with additional attributes, the
        # remaining ones will be saved by initializing the parent class.
        super().__init__(name, priority, tags)

    @property
    def start(self) -> datetime.datetime:
        """
        Get the event's start time.

        This method returns the start timestamp of this event. For events
        spanning multiple days, it will be at least midnight of today.
        """
        return self._start if self._isToday(self._start) else self.timeToday()

    @property
    def end(self) -> datetime.datetime:
        """
        Get the event's end time.

        This method returns the end timestamp of this event. For events spanning
        multiple days, it will be at most midnight of today.
        """
        return self._end if self._isToday(self._end) else self.timeToday(True)
