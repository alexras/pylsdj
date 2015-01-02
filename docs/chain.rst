Chains
------

A chain is a list of phrases for a single channel.

A chain can have up to 16 phrases, each of which is associated with a transpose (how much the phrase's notes should be shifted up).

The :py:class:`pylsdj.chain.Chain` class is a convenience wrapper around one of a song's chains.

Usage Examples
==============

.. code-block:: python

   # Access the second transpose in chain $05
   song.chains[0x05].transposes[1]

   # Access the fifth phrase in chain $53
   song.chains[0x53].phrase[4]

API Reference
=============

.. autoclass:: pylsdj.chain.Chain
   :members:
