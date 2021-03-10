# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import collections.abc
import datetime
import jira
import zettel
from typing import Optional


class Provider(zettel.AbstractProvider):
    """
    JIRA issue provider.

    This provider uses JIRA as its backend to return a list of issues managed in
    JIRA as :py:class:`.Task`.
    """

    def __init__(self,
                 filter: str,
                 format: str = '{i.key} {i.fields.summary}',
                 priorities: dict[str, zettel.Priority] = {},
                 **kwargs
                 ):
        """
        Constructor.

        .. note:: Initializing this provider will open a connection to the
            configured JIRA server.


        :param filter: The JQL search string.
        :param format: Format string, which will be used to construct the name
            of the new :py:class:`.Task`. ``i`` can be used to access the JIRA
            issue object.
        :param priorities: An optional mapping of JIRA instance specific
            priority names to abstract Zettel :py:class:`.Priority` levels.
        """
        self._filter = filter
        self._format = format
        self._priorities = priorities

        # Initialize the connection to the given JIRA server with the remaining
        # arguments passed to this constructor. Usually it would be sufficient
        # to open it just before querying the API in the 'fetch()' method.
        # However, opening it in the constructor allows directly raising
        # exceptions on invalid configuration and calling the 'fetch()' method
        # multiple times.
        self._jira = jira.JIRA(**kwargs)

    def _parsePriority(self, name: str) -> Optional[zettel.Priority]:
        """
        Match the issue's priority to a basic Zettel :py:class:`.Priority`.


        :param name: The priority name used in the JIRA issue.

        :returns: If the priority ``name`` could be matched, the related
            :py:class:`.Priority` is returned, otherwise :py:class:`None`.
        """
        return self._priorities.get(name)

    @staticmethod
    def _parseDate(datestr: str) -> Optional[datetime.date]:
        """
        Convert a ``datestr`` into a :py:class:`datetime.date`.


        :param datestr: The ISO 8601 formatted date string to be converted.

        :returns: If ``datestr`` is not :py:class:`None`, the converted date
            will be returned. Otherwise the date keeps being :py:class:`None`.
        """
        return (datetime.datetime.strptime(datestr, "%Y-%m-%d").date()
                if datestr else None)

    @staticmethod
    def _getTags(issue: jira.resources.Issue) -> list[str]:
        """
        Get tags assigned to a specific ``issue``.


        :param issue: The issue to evaluate.

        :returns: A default set of tags will be assigned to every issue, which
            includes the generic word `JIRA` and the key of the issue's project.
            If the issue type supports labels and has at least one assigned, the
            list of labels will be merged to the tag list.
        """
        return [
            'JIRA',
            issue.fields.project.key,

            # Merge the list of labels to the tag list. However, if the type of
            # issue doesn't support labels, just an empty list will be merged to
            # avoid compiler errors.
            *(getattr(issue.fields, 'labels', []))
        ]

    def fetch(self) -> collections.abc.Iterable[zettel.Task]:
        """
        Fetch all JIRA issues and return them as :py:class:`.Task`.

        This method will get all issues from the configured JIRA server and
        converts them to Zettel :py:class:`.Task` objects. Required filters and
        transformations will be applied as configured in the constructor.


        :returns: An iterable list of :py:class:`.Task` objects, representing
            related JIRA issues.
        """
        # Fetch all issues from the JIRA server, that match the filter provided
        # in the constructor. These issues will be converted into Zettel Task
        # objects, by parsing the necessary issue attributes.
        #
        # NOTE: This call tries to get ALL issues matching the filter. Therefore
        #       it should be set appropriate to match open issues with relevance
        #       only.
        for issue in self._jira.search_issues(self._filter, maxResults=False):
            yield zettel.Task(
                self._format.format(i=issue),
                self._parsePriority(issue.fields.priority.name),
                self._getTags(issue),
                self._parseDate(issue.fields.duedate)
            )
