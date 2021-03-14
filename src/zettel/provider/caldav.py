# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import caldav
import collections.abc
import datetime
import zettel

from .icalendar import Provider as iCalProvider


class Provider(zettel.AbstractProvider):
    """
    CalDAV provider.

    This provider uses a CalDAV account as its backend to return the managed
    data as Zettel items.
    """

    def __init__(self,
                 calendars: list[str] = [],
                 todoLists: list[str] = [],
                 **kwargs
                 ) -> None:
        """
        Constructor.


        :param calendars: A list of calendar names to fetch.
        :param todoLists: A list of todo list names to fetch.
        :param kwargs: All remaining parameters will be passed through to the
            :py:class:`caldav.DAVClient` constructor. Typically the ``username``,
            ``password`` and ``url`` parameters are required.
        """
        # Generate the principal to be used. It is created by any additonal
        # parameters passed to this constructor and shouldn't open a connection
        # to the server yet, but can be used to construct objects for accessing
        # the CalDAV account.
        principal = caldav.DAVClient(**kwargs).principal()

        # Depending on the parameters passed, create lists with objects to
        # access the CalDAV ressources.
        self._calendars = [principal.calendar(name=c) for c in calendars]
        self._todoLists = [principal.calendar(name=t) for t in todoLists]

    def _fetchCalendar(self) -> collections.abc.Iterable[zettel.Event]:
        """
        Fetch calender events scheduled for today.

        This method will get all calendar events from the configured CalDAV
        account, that are visible in the schedule of today's date.


        :returns: An iterable list of :py:class:`.Event` objects, representing
            related calendar events of the CalDAV account.
        """
        # For all calendars, get today's events. As each CalDAV calendar event
        # essentially is just a short iCalendar file, this file will be parsed
        # and its events returned as Zettel events.
        for calendar in self._calendars:
            for vevent in calendar.date_search(
                    start=datetime.date.today(),
                    end=datetime.date.today() + datetime.timedelta(1),
                    expand=True):
                events = vevent.icalendar_instance.subcomponents
                yield from iCalProvider.toZettelEvents(events)

    def _fetchTasks(self) -> collections.abc.Iterable[zettel.Task]:
        """
        Fetch all tasks managed in the CalDAV account.

        This method will get all calendar events from the configured CalDAV
        account and converts them to Zettel :py:class:`.Task` objects.


        :returns: An iterable list of :py:class:`.Task` objects, representing
            related tasks of the CalDAV account.
        """
        # For all todo lists, get the tasks (todos) it contains. As each CalDAV
        # todo event essentially is a short iCalendar file, this file will be
        # parsed and its todos returned as Zettel tasks.
        for todoList in self._todoLists:
            yield from map(
                lambda task: zettel.Task(
                    str(task['SUMMARY']),
                    {
                        1: zettel.Priority.HIGH,
                        2: zettel.Priority.MEDIUM,
                        3: zettel.Priority.LOW
                    }.get(task.get('PRIORITY')),
                    None,
                    task.decoded('DUE') if 'DUE' in task else None
                ),
                map(lambda t: t.icalendar_instance.subcomponents[0],
                    todoList.todos()))

    def fetch(self) -> collections.abc.Iterable[zettel.Item]:
        """
        Fetch all items from the CalDAV account.


        :returns: An iterable list of :py:class:`.Item` objects, representing
            related objects in the Micrsoft Exchange account.
        """
        yield from self._fetchCalendar()
        yield from self._fetchTasks()