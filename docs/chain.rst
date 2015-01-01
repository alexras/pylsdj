Chains
------

A chain is a list of phrases for a single channel.

A chain can have up to 16 phrases, each of which is associated with a transpose (how much the phrase's notes should be shifted up).

The :py:class:`pylsdj.chain.Chain` class is a convenience wrapper around one of a song's chains. It has the following members:

* ``song``: a reference to the chain's parent song, as a :py:class:`pylsdj.song.Song` object
* ``index``: the chain's index in its parent song
* ``phrases``: a list of :py:class:`pylsdj.phrase.Phrase` objects, each of which refers to the phrase
* ``transposes``: a list of the chain's transposes, each of which is an integer

Usage Examples
==============

.. code-block:: python

   # Access the second transpose in chain $05
   song.chains[0x05].transposes[1]

   # Access the fifth phrase in chain $53
   song.chains[0x53].phrase[4]
