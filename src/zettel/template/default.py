# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import babel.dates
import datetime
import zettel
from typing import Callable


# Internationalization dictionary, containing all messages of this template in
# various languages.
#
# NOTE: If a message key is introduced, it needs to be available at least in the
#       english subkey, as its the fallback for all other languages.
messages = {
    # English, the default
    'en': {
        'tasks': 'Tasks',
        'tasks_overdue': 'overdue',
        'tasks_today': 'today',
    },

    # German
    'de': {
        'tasks': 'Aufgaben',
        'tasks_overdue': 'überfällig',
        'tasks_today': 'heute',
    },
}


def trans(lang: str, key: str) -> str:
    """
    Get translated message for a specific key.

    This function looks up the translation for a specific key. If no translation
    is available in the selected language, the default word in english will be
    used instead.


    :param lang: The desired language.
    :param key: The message key.

    :returns: The translated message key.
    """
    return messages[lang].get(key, messages['en'][key])


def printTemplate(bucket: zettel.Bucket,
                  p: zettel.AbstractPrinter,
                  lang: str = 'en'
                  ):
    # Define a shortcut function to avoid passing the 'lang' argument on every
    # message lookup call.
    def m(key: str) -> str:
        return trans(lang, key)

    # ======
    # Header
    # ======

    with p.center():
        p.text(babel.dates.format_datetime(datetime.datetime.now(),
                                           format='short'))
        p.blank()

    # =====
    # Tasks
    # =====

    # Use a helper function to print sections of selected tasks, matching a
    # specific criteria. These tasks will be removed from the
    def print_tasks(filter: Callable[[zettel.Task], bool], title: str) -> None:
        matches = tasks.fetch(filter)
        if matches:
            with p.underline():
                p.heading(m(title), large=False)
            for t in matches:
                p.listItem(t.name, checkbox=False)
            p.blank()

    # Get all tasks from the item bucket. If at least one task is in the bucket,
    # the following section will be processed and printed.
    tasks: zettel.Bucket[zettel.Task] = bucket.fetch(
        lambda i: isinstance(i, zettel.Task))
    if tasks:
        # To get a list of tasks sorted by priority and within each priority by
        # date, sort the list by these criteria in reverse order.
        tasks.sort(key=(lambda t: t.due if t.due else datetime.date.max))
        tasks.sort(key=(lambda t: t.priority
                        if t.priority else zettel.Priority.MEDIUM),
                   reverse=True)

        with p.center():
            p.heading(m('tasks'))
        print_tasks(lambda t: bool(t.due and t.due < datetime.date.today()),
                    'tasks_overdue')
        print_tasks(lambda t: (t.due == datetime.date.today()),
                    'tasks_today')
        for t in tasks:
            p.listItem(t.name, checkbox=False)
