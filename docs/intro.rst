Introduction
------------

What is LSDJ?
=============

Little Sound DJ (or LSDJ) is a program for the Nintendo Game Boy that turns the humble Game Boy into a music workstation. More information about LSDJ can be found at `the LSDJ website`_ and `the LSDJ wiki`_.

What is pylsdj?
===============

pylsdj is a suite of tools for reading, writing and editing LSDJ's save data, which includes the user's saved songs and instruments.

Why?
====

Before pylsdj, the suite of tools available for interacting with LSDJ's save data was sparse and fragmented. People who wanted to share and re-use instruments between songs or move songs between saves were met with partial solutions at best. pylsdj endeavors to be a one-stop solution for save data reading, writing and editing.

How Can I Help?
===============

First and foremost, use it! You can also try out LSMC_, which is really just a GUI on top of many of pylsdj's functions.

Second, if you find a bug, file it. I know I haven't hit all the potential use cases for this in tests, and your input will help me find and squash bugs.

Third, if you're a developer, write some tests. If you find a feature pylsdj doesn't have and you want to take a crack at it, fork the code and send me a pull request. I'm ready and willing to receive contributions from the community.

Known Limitations
=================

pylsdj only works on save data for LSDJ versions 3.0.0 and above. Given that version 3.0.0 came out back in 2006 and marked a significant change in file structure, I feel like this is a reasonable point at which to freeze backwards-compatibility.

Terminology Primer
------------------

LSDJ's save data is stored in the Game Boy's battery RAM. LSDJ's file manager can hold up to 32 songs. Songs are stored in the file manager in a compressed form and a song is expanded into memory when it's being worked on.

The Game Boy has four audio channels: two pulse wave generators, a PCM 4-bit wave sample, and a noise generator. A song consists of a sequence of **chains**, one for each channel. Each chain consists of a sequence of **phrases**, and a phrase contains up to 16 notes.

The sound of each note is determined by the **instrument** used to play the note. This instrument controls the sound produced by one of the channels when the note is played. While the sound produced by each channel is simple, LSDJ provides a variety of means to vary the sound over time, allowing for a wide range of timbres as well as effects like arpeggio and vibrato.

.. _`the LSDJ website`: http://www.littlesounddj.com/lsd/
.. _`the LSDJ wiki`: http://littlesounddj.wikia.com/wiki/Little_Sound_Dj
.. _`LSMC`: https://www.github.com/alexras/lsmc
