README
======
**mtoolbox** - A collection of (meta-)programming tools for Python.

<https://github.com/messersm/mtoolbox>

Installation
------------
mtoolbox is available in the Python Package Index (PyPi).
Simply install it with: ``pip install mtoolbox``


Documentation
-------------
Documentation is available at:
<http://mtoolbox.readthedocs.io/en/latest/>.


Examples
--------
The IList class translates attribute access to the items it holds::

    >>> from mtoolbox.ilist import IList
    >>> l = IList([complex(3, 4), complex(6)])
    >>> l.real
    [3.0, 6.0]

