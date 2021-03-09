# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import escpos.printer
import zettel


class Printer(zettel.AbstractPrinter):
    """
    ESC/POS printer.

    This printing class implements printing the task list with an ESC/POS
    thermal printer.
    """

    def __init__(self, type: str, **kwargs):
        """
        Constructor.

        This method initiates the communication with the configured ESC/POS
        printer. Different connection types of the underlaying ``python-escpos``
        driver are available by selecting the ``type`` argument. Additional
        arguments will be passed to the constructor of the driver class.


        :param type: The type of ESC/POS connection driver class. For a list of
            available class names and their arguments see the documentation of
            ``python-escpos``.
        """
        # Initiate the backend driver to comunicate with the printer. As the
        # communications library doesn't provide a single point of entry, the
        # right class to be used can be selected by the 'type' argument. Any
        # remaining arguments to its constructor.
        self._printer = getattr(escpos.printer, type)(**kwargs)

    def __exit__(self,  exc_type, exc_value, exc_traceback) -> None:
        """
        Exit the printing context.

        After printing all data, this method ensures to cut the paper. Raised
        exceptions don't have effects on this.
        """
        self._printer.cut()

    def text(self, s) -> None:
        # Inherit the documentation from AbstractPrinter
        self._printer.text(s)
