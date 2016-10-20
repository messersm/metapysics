# -*- coding: utf-8 -*-

"""Module to provide an 'intelligent' list class

ILists are useful, if you have a number of simular objects,
on which you would like to access the same properties and store
these properties in a new list:

l.<name> == [obj.<name> for obj in l]

Example:
>>> l = IList([complex(3, 4), complex(6)])
>>> l.real
[3.0, 6.0]

You can also use callable attributes of your objects:
>>> l = IList([complex(3, 4), complex(6)])
>>> l
[(3+4j), (6+0j)]
>>> l.conjugate()
[(3-4j), (6-0j)]

You can add callbacks, for appending and removing objects. These
callbacks must accept two positional arguments - the list and the object.
The callbacks are called _after_ executing append or remove:
>>> def on_append(l, x):
...     print("Adding %s to %s." % (x, l))
>>> def on_remove(l, x):
...     print("Removing %s from %s." % (x, l))
>>> l = IList(on_append=on_append, on_remove=on_remove)
>>> l.append(3)
Adding 3 to [3].
>>> l.remove(3)
Removing 3 from [].
>>> def invalid_callback(l):
...     print(l)
>>> l = IList(on_append=invalid_callback)
Traceback (most recent call last):
...
TypeError: on_append and on_remove must accept 2 positional arguments

ILists implement the __abs__ special method:
>>> l = IList([complex(3, 4), complex(6)])
>>> abs(l)
[5.0, 6.0]

Be aware, that only attribute names, that are not used by the list class
are overwritten, so if list implemented a attribute name, you can't use
it with ILists (unless you subclass them and overwrite the attribute
name). The following code doesn't work, because list implements
'__add__' (so the result is NOT [4, 5] as one could expect):
>>> l = IList([1, 2])
>>> l + 3
Traceback (most recent call last):
...
TypeError: can only concatenate list (not "int") to list
"""

import doctest
import inspect

class IList(list):
    """'intelligent' list object
    """
    def __init__(self, iterable=None, on_append=None, on_remove=None):
        """IList() -> new empty IList
        IList(iterable) -> new IList initialized from iterable's items

        on_append: callback for append()
        on_remove: callback for remove()

        Both callbacks must accept two positional arguments
        """

        # check on_append and on_remove and save them
        if on_append is None:
            on_append = lambda l, x: None
        if on_remove is None:
            on_remove = lambda l, x: None

        for func in on_append, on_remove:
            spec = inspect.getargspec(func)
            arglen = len(spec.args)

            if spec.defaults:
                arglen -= len(spec.defaults)

            if arglen < 2:
                raise TypeError(
                    "on_append and on_remove must accept 2 " + \
                    "positional arguments")

        self.__on_append = on_append
        self.__on_remove = on_remove

        # init list
        if iterable is not None:
            list.__init__(self, iterable)
        else:
            list.__init__(self)

        # run on_append on all given objects
        for value in self:
            self.__on_append(self, value)

    def append(self, obj):
        """Add obj to IList

        >>> l = IList()
        >>> l
        []
        >>> l.append(3)
        >>> l
        [3]
        """
        list.append(self, obj)
        self.__on_append(self, obj)

    def remove(self, obj):
        """Remove obj from IList

        >>> l = IList([8])
        >>> l
        [8]
        >>> l.remove(8)
        >>> l
        []
        >>> l.remove(6)
        Traceback (most recent call last):
        ...
        ValueError: list.remove(x): x not in list
        """
        list.remove(self, obj)
        self.__on_remove(self, obj)

    def __getattr__(self, name):
        return IList([getattr(obj, name) for obj in self])

    def __call__(self, *args, **kwargs):
        return IList([obj(*args, **kwargs) for obj in self])

    def __abs__(self):
        return IList([abs(obj) for obj in self])

if __name__ == '__main__':
    doctest.testmod()
