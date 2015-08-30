Kits
----

Kits are groupings of samples that can be played by the Game Boy's wave
channel; this is mostly used for drums.

Kits are defined in the ROM rather than the .sav data.

Usage Examples
==============

.. code-block:: python

   # Load kits from a ROM
   kits = Kits('lsdj.gb')

   # Get kit 13's name
   kit_13_name = kits[13].name

   # Get sample 4 from kit 10
   sample = kits[10].samples[4]

   # Save the sample to a .wav file
   sample.write_wav('my_sample.wav')

   # Load a new sample into kit 9, sample 3
   kits[9].samples[3].read_wav('load_sample.wav')


API Reference
=============

YATTA!

.. autoclass:: pylsdj.Kits
   :members:

.. autoclass:: pylsdj.Kit
   :members:

.. autoclass:: pylsdj.KitSample
   :members:
