# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import collections.abc
import datetime
import exchangelib
import zettel
from typing import Optional


class Provider(zettel.AbstractProvider):
    """
    Exchange provider.

    This provider uses Microsoft Exchange as its backend to return the managed
    data as Zettel items.
    """

    def __init__(self,
                 server: str,
                 account: str,
                 credentials: dict[str, str]
                 ) -> None:
        """
        Constructor.

        .. note:: Initializing this provider will open a connection to the
            configured Microsoft Exchange server.


        :param server: The server to connect to.
        :param account: The mail account (email address) to connect to.
        :param credentials: The credentials to be used for login. Values of this
            :py:class:`dict` will be passed through to the
            :py:class:`exchangelib.Credentials` class.
        """
        # Initialize the connection to the given Microsoft Exchange server with
        # the arguments passed in the constructor. As an attribute of this class
        # the connection can be reused by various methods in subsequenct calls.
        self._account = exchangelib.Account(
            primary_smtp_address=account,
            config=exchangelib.Configuration(
                server=server,
                credentials=exchangelib.Credentials(**credentials)
            ),
            autodiscover=True,
            access_type=exchangelib.DELEGATE
        )

    @staticmethod
    def _parsePriority(name: str) -> Optional[zettel.Priority]:
        """
        Match a priority of Microsoft Exchange to a basic Zettel
        :py:class:`.Priority`.


        :param name: The priority name used in Micrsoft Exchange.

        :returns: If the priority ``name`` could be matched, the related
            :py:class:`.Priority` is returned, otherwise :py:class:`None`.
        """
        return {
            'Low': zettel.Priority.LOW,
            'Normal': zettel.Priority.MEDIUM,
            'High': zettel.Priority.HIGH
        }.get(name)

    def _fetchTasks(self) -> collections.abc.Iterable[zettel.Task]:
        """
        Fetch all tasks managed in the Micrsoft Exchange account.

        This method will get all tasks managed in the configured Micrsoft
        Exchange account and converts them to Zettel :py:class:`.Task` objects.


        :returns: An iterable list of :py:class:`.Task` objects, representing
            related tasks in the Micrsoft Exchange account.
        """
        # Fetch all tasks not finished yet from the Microsoft exchange server,
        # as configured in the constructor. These tasks will be converted into
        # Zettel Task objects, by selecting and converting the necessary tasks
        # attributes.
        for task in self._account.tasks.filter(is_complete__not=True):
            yield zettel.Task(
                task.subject,
                self._parsePriority(task.importance),
                None,
                task.due_date
            )

    def fetch(self) -> collections.abc.Iterable[zettel.Item]:
        """
        Fetch all items from the Micrsoft Exchange server.


        :returns: An iterable list of :py:class:`.Item` objects, representing
            related objects in the Micrsoft Exchange account.
        """
        yield from self._fetchTasks()
