# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import collections.abc
import datetime
import icalendar
import requests
import zettel


class Provider(zettel.AbstractProvider):
    """
    iCal provider.

    This provider retrieves iCalendar feeds from remote servers and returns the
    events it contains.
    """

    def __init__(self, url: str) -> None:
        """
        Constructor.


        :param url: The iCalendar feed URL.
        """
        self._url = url

    @staticmethod
    def toZettelEvents(calendar: collections.abc.Iterable[icalendar.cal.Event]
                       ) -> zettel.Event:
        """
        Convert a list of iCalendar events to Zettel events.

        This method takes a list of iCalendar events and converts them into
        Zettel events. To acomplish this, the iCalendar event attributes will be
        parsed and converted to the required formats, which can be used to
        create the Zettel events.


        :param calendar: A list of iCalendar events.

        :returns: An iterable list of :py:class:`.Event` objects, representing
            the related ``calendar`` events.
        """
        for event in calendar:
            # Decode the start and end timestamps of the event. These will be
            # used several times and therefore cached in these variables.
            a = event.decoded('DTSTART')
            b = event.decoded('DTEND')

            # Create a new Zettel Event and yield it back to the calle to make
            # the results of this function call iterable. Its arguments need to
            # be converted to standardized ones, useable by other components of
            # Zettel.
            yield zettel.Event(
                str(event['SUMMARY']),

                # Convert the event's timestamps into real datetime objects. For
                # 'all day' events, these will be date objects, where the end
                # date exceeds the real date by one day. Therefore, it will be
                # substracted before converting it.
                zettel.Event.toDateTime(a),
                zettel.Event.toDateTime((b if isinstance(b, datetime.datetime)
                                         else b - datetime.timedelta(1)),
                                        True),

                # If both start and end date are just dates without time, this
                # event is an 'all day' event.
                not (isinstance(a, datetime.datetime)
                     and isinstance(b, datetime.datetime))
            )

    def fetch(self) -> collections.abc.Iterable[zettel.Task]:
        """
        Fetch calender events from the iCalendar feed.

        This method retrieves the iCalendar feed from a remote server, parses it
        and returns the events it contains.


        :returns: An iterable list of :py:class:`.Event` objects, representing
            the related events of the iCalendar feed.
        """
        # Retrieve the iCalendar feed from a remote server and parse its
        # contents as complete calendar.
        feed = requests.get(self._url).text
        ical = icalendar.cal.Calendar.from_ical(feed)

        yield from filter(
            # The iCalendar feed may contain any number of events. However,
            # Zettel is interested in today's events only, so these should be
            # filtered to return today's selection of events only.
            lambda e: (e._start.date() <= datetime.date.today()
                       and e._end.date() >= datetime.date.today()),

            # To feed the filter above, convert just the iCalendar events into
            # Zettel events by passing a filtered subset of iCalendar items to
            # the conversion method.
            self.toZettelEvents(filter(
                lambda e: isinstance(e, icalendar.cal.Event),
                ical.walk()
            )))
