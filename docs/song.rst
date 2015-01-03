Songs
-----

A song contains all the information about its notes and the instruments that
control how the notes sound. It also contains settings related to how LSDJ
should play the song.

Notes
=====

A song is defined by its *sequence*. A sequence consists of a number of
sequence **steps**. Each step specifies a chain for each of the Game Boy's four
audio channels (pulse 1, pulse 2, wave, and noise). See :doc:`chain` for more
information on how Chains are structured.

A song's sequence is stored in its ``sequence`` field as a two-dimensional
dictionary of chains.

Usage Examples
^^^^^^^^^^^^^^

.. code-block:: python

   from pylsdj import Sequence

   # Get the chain in step $3 of PU2 from the sequence
   curr_chain = song.sequence[Sequence.PU2][0x3]

   # Get that same chain from the global chains table
   curr_chain_another_way = song.chains[curr_chain.index]

   # Get chain $2D from the global chain table
   chain_two_d = song.chains[0x2d]

Instruments
===========

The sound of a note is determined by an instrument. An instrument can also
refer to a synth or a macro table to control how it behaves over time.

A song contains global tables for instruments, synths and macro tables. These
are stored in the song's ``instruments``, ``synths`` and ``tables`` fields,
resp.

Appearance and Playback Behavior
================================

Songs also have a number of fields that control the appearance of LSDJ and its
synchronization setting. A complete overview of what all these settings do is
out of this document's scope; see the API documentation below for a list of
supported settings.

API Documentation
=================

.. autoclass:: pylsdj.Song
   :members:
   :private-members:
