Tables
------

Tables define the behavior of an instrument over time.

Each table consists of a list of volume envelopes, transposes and effect
commands. How (or whether) these commands are applied to an instrument depends
on that instrument's settings.

Usage Examples
==============

.. code-block:: python

   # Get table $4 from the song's table of tables
   table = song.tables[0x4]

   # Alternatively, get it from instrument $b
   table = song.instruments[0xb].table

   # Set the envelope in row $5 to $A6
   table.envelopes[0x5] = 0xa6

   # Set the value of the first effect's parameter to 5 in row $6
   table.fx1[0x6].value = 5

API Reference
=============

.. autoclass:: pylsdj.Table
   :members:

.. autoclass:: pylsdj.TableFX
   :members:
