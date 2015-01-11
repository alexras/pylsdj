Instruments
-----------

:py:class:`pylsdj.Instrument` is a wrapper class allowing manipulation of a
project's instrument. It is typically accessed by looking up the instrument in
its parent song's ``instruments`` field.

Importing and Exporting Instruments
===================================

Instruments export in what I'm calling ``lsdinst`` format, which is really just
a JSON encoding of the instrument's data.

Importing an instrument is handled by its parent song, so that it can do the necessary bookkeeping if the instrument's type changes.

.. autoclass:: pylsdj.Instruments
   :noindex:
   :members: import_from_file

.. autoclass:: pylsdj.Instrument
   :members: export_to_file

Usage Examples
^^^^^^^^^^^^^^

.. code-block:: python

   # Editing a song's instrument $06
   instrument = song.instruments[0x06]

   # Change the instrument's name
   instrument.name = "ABCDE"

   # Export the instrument to a file
   instrument.export_to_file("my_instrument.lsdinst")

   # Import the instrument, overwriting instrument $09
   song.instruments.import_from_file(0x09, "my_instrument.lsdinst")


Instrument Fields
=================

All instrument types have the following fields:

* ``name``: the instrument's name
* ``type``: the instrument's type (pulse, wave, noise, or kit)

Different instruments have different additional fields, corresponding to the
fields that an instrument has in LSDJ. These fields are described below.

Vibrato
^^^^^^^

The pulse, wave, and kit instrument types all have a vibrato control, accessed
through their ``vibrato`` fields, which has the following structure:

.. autoclass:: pylsdj.Vibrato
   :members:

Pulse Instruments
^^^^^^^^^^^^^^^^^

.. autoclass:: pylsdj.PulseInstrument
   :members:
   :exclude-members: export_to_file
   :inherited-members:


Wave Instruments
^^^^^^^^^^^^^^^^

.. autoclass:: pylsdj.WaveInstrument
   :members:
   :exclude-members: export_to_file
   :inherited-members:


Noise Instrument Fields
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pylsdj.NoiseInstrument
   :members:
   :exclude-members: export_to_file
   :inherited-members:


Kit Instrument Fields
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pylsdj.KitInstrument
   :members:
   :exclude-members: export_to_file
   :inherited-members:
