Instruments
-----------

:py:class:`pylsdj.Instrument` is a wrapper class allowing manipulation of a
project's instrument. It is typically accessed by looking up the instrument in
its parent song's ``instruments`` field.

Importing and Exporting Instruments
===================================

Instruments know how to import and export themselves. They export in what I'm
calling ``lsdinst`` format, which is really just a JSON encoding of the
instrument's data.

.. autoclass:: pylsdj.Instrument
   :members: import_from_file, export_to_file

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
   song.instruments[0x09].import_from_file("my_instrument.lsdinst")


Instrument Fields
=================

All instrument types have the following fields:

* ``name``: the instrument's name
* ``type``: the instrument's type (pulse, wave, noise, or kit)

Different instruments have different additional fields, corresponding to the
fields that an instrument has in LSDJ.

Pulse Instrument Fields
^^^^^^^^^^^^^^^^^^^^^^^

* ``envelope``: the pulse instrument's volume envelope (8-bit integer)
* ``phase_transpose``: detune pulse channel 2 this many semitones; in LSDJ, this is ``PU2 TUNE`` (8-bit integer)
* ``has_sound_length``: if ``False``, sound length is unlimited; otherwise, ``sound_length`` contains the sound's length
* ``sound_length``: the sound's length (6-bit integer)
* ``sweep``: modulates the sound's frequency; only works on pulse 1 (8-bit integer)
* ``automate``: if ``True``, turns on automation
* ``vibrato.type``: ``"hf"`` (for high frequency sine), ``"sawtooth"``, ``"saw"`` or ``"square"``
* ``vibrato.direction``: ``"down"`` or ``"up"``
* ``table``: a :py:class:`pylsdj.Table` referencing the instrument's table, or ``None`` if the instrument doesn't have a table
* ``wave``: the pulse's wave width; ``"12.5%"``, ``"25%"``, ``"50%"`` or ``"75%"``
* ``phase_finetune``: detune pulse channel 1 down, channel 2 up; in LSDJ, this is ``PU FINE`` (4-bit integer)
* ``pan``: sound panning; ``"L"``, ``"R"``, or ``"LR"``

Wave Instrument Fields
^^^^^^^^^^^^^^^^^^^^^^

* ``wave``: the sound's volume; 0 through 3
* ``synth``: the index of the wave's synth within its parent song's synths list
* ``repeat``: the synth sound's repeat point (4-bit integer)
* ``automate``: if ``True``, turns on automation
* ``vibrato.type``: ``"hf"`` (for high frequency sine), ``"sawtooth"``, ``"saw"`` or ``"square"``
* ``vibrato.direction``: ``"down"`` or ``"up"``
* ``table``: a :py:class:`pylsdj.Table` referencing the instrument's table, or ``None`` if the instrument doesn't have a table
* ``pan``: sound panning; ``"L"``, ``"R"``, or ``"LR"``
* ``play_type``: how to play the synth sound; ``"once"``, ``"loop"``, ``"ping-pong"``, or ``"manual"``
* ``steps``: length of the synth sound (4-bit integer)
* ``speed``: how fast the sound should be played back (4-bit integer)

Noise Instrument Fields
^^^^^^^^^^^^^^^^^^^^^^^

* ``envelope``: the noise instrument's volume envelope (8-bit integer)
* ``s_cmd``: ``"free"`` or ``"stable"``. When free, altering noise shape with
  the S command can sometimes mute the sound. When stable, sound will never be
  muted by accident. My understanding is that this setting exists for backwards-compatibility of behavior in old LSDJ instruments
* ``has_sound_length``: if ``False``, sound length is unlimited; otherwise, ``sound_length`` contains the sound's length
* ``sound_length``: the sound's length (6-bit integer)
* ``sweep``: modulates the sound's frequency; only works on pulse 1 (8-bit integer)
* ``automate``: if ``True``, turns on automation
* ``table``: a :py:class:`pylsdj.Table` referencing the instrument's table, or ``None`` if the instrument doesn't have a table
* ``pan``: sound panning; ``"L"``, ``"R"``, or ``"LR"``


Kit Instrument Fields
^^^^^^^^^^^^^^^^^^^^^

* ``volume``: the kit's volume; 0 to 3
* ``kit_1``: the index of the first kit in LSDJ's kit list
* ``kit_2``: the index of the second kit in LSDJ's kit list
* ``loop_1``: loop sample in kit 1 and start playing from an offset
* ``loop_2``: loop sample in kit 2 and start playing from an offset
* ``keep_attack_1``: loop sample in kit 1 and start playing from beginning
* ``keep_attack_2``: loop sample in kit 2 and start playing from beginning
* ``half_speed``: if ``True``, play the sample at half speed
* ``length_1``: the length of kit 1's sound (0 means "always play the sample to the end" and is displayed as ``AUT`` in LSDJ)
* ``length_2``: the length of kit 2's sound (0 means "always play the sample to the end" and is displayed as ``AUT`` in LSDJ)
* ``offset_1``: kit 1's loop start point (if ``loop_1`` is ``True`` and ``keep_attack_1`` is ``False``)
* ``offset_2``: kit 2's loop start point (if ``loop_2`` is ``True`` and ``keep_attack_2`` is ``False``)
* ``automate``: if ``True``, turns on automation
* ``vibrato.type``: ``"hf"`` (for high frequency sine), ``"sawtooth"``, ``"saw"`` or ``"square"``
* ``vibrato.direction``: ``"down"`` or ``"up"``
* ``table``: a :py:class:`pylsdj.Table` referencing the instrument's table, or ``None`` if the instrument doesn't have a table
* ``pan``: sound panning; ``"L"``, ``"R"``, or ``"LR"``
* ``pitch``: sample pitch shift (8-bit integer)
* ``dist_type``: algorithm used when two kits are mixed together; ``"clip"``, ``"shape"``, ``"shap2"`` or ``"wrap"``.
