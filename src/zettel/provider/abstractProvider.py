# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import abc
import collections.abc
from typing import cast, Union

from ..item import Item, Priority


class AbstractProvider(abc.ABC):
    """
    Abstract :py:class:`.Item` provider.

    This abstract class defines the interface, a provider needs to define. As a
    provider basically is just a single method to be called, these classes won't
    be complicated in design, but require a standard API to gather all items.
    """

    @staticmethod
    def _convertPriority(src: Union[str, int]) -> Priority:
        """
        Convert a priority from string or integer to :py:class:`.Priority`.

        This method takes a given string or integer and maps it to its related
        Zettel :py:class:`.Item` :py:class:`.Priority`. It can be used to parse
        the provider specific configurations into uniform Zettel abstractions in
        the provider's constructor.


        :param src: The source integer or string to be converted.

        :returns: The converted :py:class:`.Priority` object.
        """
        return (Priority[cast(str, src)] if type(src) is str else Priority(src))

    @abc.abstractmethod
    def fetch(self) -> collections.abc.Iterable[Item]:
        """
        Fetch all items from the provider's backend.

        This method will be called to gather all items from the provider's
        backend, which should be returned as list for further processing the
        data in Zettel.

        .. warning:: Providers should not alter the origin data in their related
            backends to give reproducible results on subsequent calls.


        :returns: A list of items this backend currently provides.
        """
        pass
