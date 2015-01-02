Clocks
------

LSDJ's clocks serve as a way to track the amount of time the current song has
been worked on. Clocks also have a checksum, which provides a check against
file corruption.

:py:class:`pylsdj.clock.Clock` is a wrapper around a song's clock
data. Modifying any of the clock's fields (``days``, ``hours``, or ``minutes``)
will also update the checksum accordingly.

Usage Examples
==============

Get a clock's days

>>> clock.days
5

Set a clock's hours:

>>> clock.hours = 6


API Documentation
=================

.. autoclass:: pylsdj.clock.Clock
   :members:
