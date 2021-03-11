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


def printTemplate(bucket: list[zettel.Item],
                  p: zettel.AbstractPrinter
                  ):
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
        p.heading('ToDo')

    for i in bucket:
        p.listItem(i.name, checkbox=True)
