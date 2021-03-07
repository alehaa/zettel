# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

import abc

from ..item import Item


class AbstractProvider(abc.ABC):
    """
    Abstract :py:class:`.Item` provider.

    This abstract class defines the interface, a provider needs to define. As a
    provider basically is just a single method to be called, these classes won't
    be complicated in design, but require a standard API to gather all items.
    """

    @abc.abstractmethod
    def fetch(self) -> list[Item]:
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
