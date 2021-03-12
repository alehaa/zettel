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
from contextlib import contextmanager


class Printer(zettel.AbstractPrinter):
    """
    ESC/POS printer.

    This printing class implements printing the task list with an ESC/POS
    thermal printer.
    """

    def __init__(self, type: str, width=42, **kwargs) -> None:
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

        # The backend driver just provides a single method for setting format
        # related parameters. Therefore, the following dictionary keeps track on
        # the used parameters to allow these to be set individually by the
        # related format methods of this class.
        self._param: dict = {}

    def __exit__(self,  exc_type, exc_value, exc_traceback) -> None:
        """
        Exit the printing context.

        After printing all data, this method ensures to cut the paper. Raised
        exceptions don't have effects on this.
        """
        self._printer.cut()

    @contextmanager
    def _set(self, **kwargs):
        """
        Set text format parameters for the printer's backend driver.

        This method is a wrapper for the ``set()`` function of ``python-escpos``
        to keep track of its arguments, allowing to set just a single one once
        at a time without altering the other ones. It's intended use is as
        context manager, setting the format inside a ``with`` block and
        restoring the original behaviour at its end.


        :param: All arguments passed to this function will be passed through to
            the backend driver. See the documentation of ``set()`` from
            ``python-escpos`` for allowed arguments.
        """
        # Save a copy of the current parameter set to restore it after executing
        # the context. Unfortunately, simply removing the parameters set after
        # the context is not an option, as this would compromise setting the
        # same parameter in nested contexts and lead to side effects.
        tmp = self._param.copy()

        # Update the internal parameter state with the arguments passed to this
        # method. The combined list of parameters will be used to update the
        # printer's state before entering the context by yielding.
        try:
            self._param.update(kwargs)
            self._printer.set(**self._param)
            yield

        # After executing the context, restore the internal parameter state with
        # its original contents before updating the printer's state yet again.
        finally:
            self._param = tmp
            self._printer.set(**self._param)

    def blank(self) -> None:
        """
        Print an empty line.
        """
        self._printer.text('\n')

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
        # string into multiple lines with the calculated maximum line length. If
        # the 'double_width' format parameter is set, the half width will be
        # used instead automatically.
        width = (self._width if not self._param.get('double_width')
                 else (self._width / 2))
        lines = textwrap.wrap(s, (width - len(prefix)))

        # Print the first line including the prefix. Then, if the text exceeds a
        # single line, following lines will be printed with an indentation
        # matching the prefix length.
        self._printer.text(prefix)
        self._printer.text(f'{lines[0]}\n')
        for l in lines[1:]:
            self._printer.text(''.ljust(len(prefix)))
            self._printer.text(f'{l}\n')

    def heading(self, s: str, large: bool = True) -> None:
        """
        Print a section heading.


        :param s: The text to be printed.
        :param large: Whether to print the text double sized or regular.
        """
        with self._set(bold=True, double_height=large, double_width=large):
            self.text(f'{s}\n')

        # To highlight the heading from the surrounding text, an empty line will
        # follow large headings. It needs to be added after the context above,
        # as it won't have effects in a 'double_height' environment.
        if large:
            self.blank()

    @contextmanager
    def center(self):
        with self._set(align='center'):
            yield

    @contextmanager
    def bold(self):
        with self._set(bold=True):
            yield

    @contextmanager
    def underline(self):
        with self._set(underline=True):
            yield

    @contextmanager
    def highlight(self):
        with self._set(invert=True):
            yield

    def listItem(self, s: str, checkbox: bool = False) -> None:
        self.text(s, prefix=('- ' if not checkbox else '[ ] '))
