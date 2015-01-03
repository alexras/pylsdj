Speech Instrument
-----------------

LSDJ has a speech instrument (loaded into instrument slot $40) that can
synthesize words from allophones.

If you're looking for a way to break down words into allophones, `the CMU Pronouncing Dictionary`_ is a good place to start.

Speech Instrument Structure
===========================

The speech instrument consists of a list of **words**. Each word has a name,
and a list of **sounds**. Each sound consists of an allophone and a length.

Usage Examples
==============

.. code-block:: python

   # Get word $5 defined in the speech instrument
   word = song.speech_instrument.words[0x5]

   # Extract the word's allophones
   allophones = [sound.allophone for sound in word.sounds]

   # Change the fifth allophone to 'OY'
   word.sounds[4].allophone = 'OY'

   # Change the length of the 10th allophone to 5
   word.sounds[9].length = 5

   # Change the 3rd word's name to 'WORD'
   word.sounds[2].name = 'WORD'

API Documentation
=================

.. autoclass:: pylsdj.SpeechInstrument
   :members:
   :private-members:

.. autoclass:: pylsdj.Word
   :members:
   :private-members:

.. _the CMU Pronouncing Dictionary:  http://www.speech.cs.cmu.edu/cgi-bin/cmudict
