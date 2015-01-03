Projects
--------

A project is a wrapper around a song that gives the song a name and a version.

In addition to the :py:class:`pylsdj.Project` object itself, the
:py:mod:`pylsdj.projects` module contains functions for loading projects from
``.srm`` and ``.lsdsng`` files.

Usage Examples
==============

.. code-block:: python

   from pylsdj import Project, load_srm, load_lsdsng

   # Load a .srm file
   srm_proj = load_srm("test1.srm")

   # Load a .lsdsng file
   lsdsng_proj = load_srm("test2.lsdsng")

   # Convert the .srm project to .lsdsng
   srm_proj.save("test1_conv.lsdsng")

   # Get the srm project's song
   song = srm_proj.song

API Documentation
=================

.. autofunction:: pylsdj.load_lsdsng

.. autofunction:: pylsdj.load_srm

.. autoclass:: pylsdj.Project
   :members:
