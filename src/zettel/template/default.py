# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import zettel


def printTemplate(bucket: list[zettel.Item],
                  p: zettel.AbstractPrinter
                  ):
    with p.center():
        p.heading('ToDo')

    for i in bucket:
        p.listItem(i.name, checkbox=True)
