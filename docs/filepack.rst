Compression and Decompression
-----------------------------

Game Boys don't have a lot of RAM (128KB tops); in order for LSDJ to deal with
such a limited amount of space, it has to pack files in pretty tight. To do
this, it uses an algorithm referred to on the `LSDJ wiki`_ as the "file pack
algorithm".

pylsdj includes functions that will compress and decompress lists of bytes
using the file pack algorithm.

Typically you don't need to do this: .sav files compress themselves on save and
decompress themselves on load automatically. If your application needs to do
something fancy with LSDJ's filesystem, however, you can use the compression
and decompression functions by themselves.

Usage Examples
==============

.. code-block:: python

   from pylsdj import filepack

   # Here's a list of bytes
   bytes = [0x12, 0x12, 0x12, 0x15, 0x15, 0x10]

   # We can compress those bytes
   compressed = filepack.compress(bytes)

   # ... and then decompress them again
   decompressed = filepack.decompress(compressed)


API Documentation
=================

.. automodule:: pylsdj.filepack
   :members: compress, decompress

.. _LSDJ wiki: http://littlesounddj.wikia.com/wiki/Little_Sound_Dj
