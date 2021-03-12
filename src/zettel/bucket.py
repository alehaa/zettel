# This file is part of Zettel.
#
# Copyright (c) Alexander Haase <ahaase@alexhaase.de>
#
# This project is licensed under the MIT License. For the full copyright and
# license information, please view the LICENSE file that was distributed with
# this source code.

from typing import Callable, TypeVar

from .item import Item


T = TypeVar('T')


class Bucket(list[T]):
    """
    :py:class:`.Item` bucket list class.

    This class is a wrapper around python's :py:class:`list` class, enhancing it
    with functions to query the list by specific criteria.
    """

    def fetch(self,
              filter: Callable[[T], bool]
              ) -> 'Bucket':
        """
        Query the list for items matching criteria and pop them from the list.

        This method is a combination of :py:meth:`pop` and a filter. It gets all
        items matching the criteria defined by the ``filter`` function parameter
        and pops them from the list to access them only once while printing.


        :param filter: A function, which takes an :py:class:`.Item` as first
            argument and returns a boolean. For :py:class:`True`, this
            :py:class:`.Item` is returned and poped from the list.

        :returns: A bucket list of items matching the ``filter``.
        """
        # Iterate over the list of items to match them against the filter. If
        # the filter matches, the item will be added to the return bucket and
        # removed from the original list.
        #
        # NOTE: A copy of the list is used, as iterating the list won't work
        #       reliable, if items are removed from it while iterating.
        temp: Bucket = self.__class__()
        for item in self.copy():
            if filter(item):
                temp.append(item)
                self.remove(item)

        return temp
