# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import abc
import contextlib


class AbstractPrinter(contextlib.AbstractContextManager):
    """
    Abstract printing class.

    This abstract class defines the interface, a printing class needs to define.
    It allows templates to address the output format in an abstract way,
    allowing the items to be either printed or exported in any other format, as
    long as its implemented with an abstract printing class conforming to this
    interface.

    A printing class basically is just a python context manager, which allows to
    execute some steps before and after the template. Additional methods add an
    interface to format the printed text.
    """

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """
        Method run when leaving the context manager.

        This method is empty. By default no tasks will be performed, when the
        context is leaved. Printer implementations may override this method to
        perform any tasks before closing the output stream.
        """
        pass

    @abc.abstractmethod
    def text(self, s: str) -> None:
        """
        Print a line of text.

        This method takes a given string ``s`` and prints it to the output
        stream of the printer.


        :param s: The text to be printed.
        """
        pass

    @abc.abstractmethod
    def heading(self, s: str, large: bool = True) -> None:
        """
        Print a section heading.


        :param s: The text to be printed.
        :param large: Whether to use a large or small heading.
        """
        pass

    @abc.abstractmethod
    def center(self):
        """
        Context manager for centered text.

        Printing driver classes should implement this method with the
        ``@contextmanager`` decorator applied to execute commands to format the
        text before and after the context manager's body.
        """
        pass

    @abc.abstractmethod
    def bold(self):
        """
        Context manager for bold text.

        Printing driver classes should implement this method with the
        ``@contextmanager`` decorator applied to execute commands to format the
        text before and after the context manager's body.
        """
        pass

    @abc.abstractmethod
    def underline(self):
        """
        Context manager for underlined text.

        Printing driver classes should implement this method with the
        ``@contextmanager`` decorator applied to execute commands to format the
        text before and after the context manager's body.
        """
        pass

    @abc.abstractmethod
    def highlight(self):
        """
        Context manager for highlighted text.

        Printing driver classes should implement this method with the
        ``@contextmanager`` decorator applied to execute commands to format the
        text before and after the context manager's body.
        """
        pass

    @abc.abstractmethod
    def listItem(self, s: str, checkbox: bool = False) -> None:
        """
        Print a list item.

        This method prints a list item and allows setting vaious styles by
        changing its parameters.

        .. note:: This method doesn't provide a context manager and therefore is
            not compatible with printing drivers requireing some surrounding
            context around the individual list items. If that will be the case,
            this method needs to be refactored.


        :param s: The text to be printed.
        :param checkbox: Whether this list item is a checkbox or a regular one.
        """
        pass
