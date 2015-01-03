.sav Files
----------

pylsdj manipulates .sav files through a :py:class:`pylsdj.SAVFile` object. This object can be used to load, store, and edit the contents of LSDJ's SRAM file.

Loading and Saving
==================

If you're writing an application using pylsdj, you'll probably want to load and store it.

Callback Functions
^^^^^^^^^^^^^^^^^^

Several methods of :py:class:`pylsdj.SAVFile` take a progress callback function that callers can use to notify callers of how far the operation has progressed. Callback functions take four arguments

* ``message``: a message explaining what the step is doing
* ``step``: the step that the operation is currently on
* ``total_steps``: the total number of steps in the operation
* ``continuing``: True if the operation is going to continue

Accessing and Editing a .sav File's Projects
============================================

A .sav file's ``project_list`` field contains an ordered list of that file's
projects. You can insert, modify and delete :py:class:`pylsdj.Project` objects
in this list to modify the .sav file's contents. Note that changes to the .sav
file will not persist unless it is saved.

Usage Examples
==============

.. code-block:: python


   from pylsdj import SAVFile

   # Load .sav file from lsdj.sav
   sav = SAVFile('lsdj.sav')

   # Load a .sav file, passing loading progress to a callback
   def my_callback(message, step, total_steps, continuing):
     print '%(m)s: %(s)d/%(t)d complete!' % { m: message, s: step, t: total_steps }

   sav = SAVFile('lsdj.sav', my_callback)

   # Get the file's project map (maps slot number to Project)
   projects = sav.projects

   # Save a savfile as lsdj_modified.sav, passing the same progress callback
   # from the above example
   sav.save('lsdj_modified.sav', my_callback)

API Documentation
=================

.. autoclass:: pylsdj.SAVFile
   :members:
