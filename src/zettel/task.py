# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

from datetime import date
from typing import Optional

from .item import Item, Priority


class Task(Item):
    """
    Task item.

    This class extends the :py:class:`~.Item` class with additional attributes
    to represent task items. This could be tickets from a CRM, issues or any
    other kind of task.
    """

    def __init__(self,
                 name: str,
                 priority: Optional[Priority] = None,
                 tags: Optional[list[str]] = None,
                 due: Optional[date] = None
                 ) -> None:
        """
        Constructor.

        This method initializes the task. It's identical to the one of
        :py:class:`~.Item`, except adding additional attributes.


        :param name: Name of this task.
        :param priority: Priority of this task.
        :param tags: A list of tags, by which this task and other items could be
            grouped or filtered.
        :param due: A specific date, until this task needs to be done.
        """
        self.due = due

        # As a task is basically just an item with additional attributes, the
        # remaining ones will be saved by initializing the parent class.
        super().__init__(name, priority, tags)
