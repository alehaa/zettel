# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import escpos.printer
import textwrap
import zettel


class Printer(zettel.AbstractPrinter):
    """
    ESC/POS printer.

    This printing class implements printing the task list with an ESC/POS
    thermal printer.
    """

    def __init__(self, type: str, width=42, **kwargs):
        """
        Constructor.

        This method initiates the communication with the configured ESC/POS
        printer. Different connection types of the underlaying ``python-escpos``
        driver are available by selecting the ``type`` argument. Additional
        arguments will be passed to the constructor of the driver class.


        :param type: The type of ESC/POS connection driver class. For a list of
            available class names and their arguments see the documentation of
            ``python-escpos``.
        :param width: Number of characters the printer puts on a single line.
            The default value of 42 fits 80mm paper on EPSON printers.
        """
        self._width = width

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

    def text(self, s: str, prefix: str = '') -> None:
        """
        Print a line of text.

        This method takes a given string ``s`` and prints via the connected
        ESC/POS printer. As it just can handle a fixed amount of characters, the
        words in ``s`` will be wrapped automatically for the desired length. An
        optional ``prefix`` can be used for printing some text once and
        indenting following lines automatically.


        :param s: The text to be printed.
        :param prefix: A prefix to be printed in the first line. Consecutive
            lines will be indented by the length of the prefix.
        """
        # Calculate the desired line length (without prefix) and split the input
        # string into multiple lines with the calculated maximum line length.
        lines = textwrap.wrap(s, (self._width - len(prefix)))

        # Print the first line including the prefix. Then, if the text exceeds a
        # single line, following lines will be printed with an indentation
        # matching the prefix length.
        self._printer.text(prefix)
        self._printer.text(f'{lines[0]}\n')
        for l in lines[1:]:
            self._printer.text(''.ljust(len(prefix)))
            self._printer.text(f'{l}\n')
