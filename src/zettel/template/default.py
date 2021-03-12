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

# Internationalization dictionary, containing all messages of this template in
# various languages.
#
# NOTE: If a message key is introduced, it needs to be available at least in the
#       english subkey, as its the fallback for all other languages.
messages = {
    # English, the default
    'en': {
        'tasks': 'Tasks',
    },

    # German
    'de': {
        'tasks': 'Aufgaben',
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


def printTemplate(bucket: list[zettel.Item],
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

    with p.center():
        p.heading(m('tasks'))

    for i in bucket:
        p.listItem(i.name, checkbox=True)
