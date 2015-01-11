Clocks
------

LSDJ's clocks serve as a way to track the amount of time the current song has
been worked on. The global clock also has a checksum, which provides a check
against file corruption.

:py:class:`pylsdj.clock.TotalClock` is a wrapper around a song's global clock
data. Modifying any of the clock's fields (``days``, ``hours``, or ``minutes``)
will also update the checksum accordingly.

:py:class:`pylsdj.clock.Clock` is a wrapper around a song's local clock
    data. It only tracks hours and minutes.

Usage Examples
==============

Get a clock's days

>>> clock.days
5

Set a clock's hours:

>>> clock.hours = 6


API Documentation
=================

.. autoclass:: pylsdj.clock.TotalClock
   :members:

.. autoclass:: pylsdj.clock.Clock
   :members:
