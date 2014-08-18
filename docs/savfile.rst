.sav Files
----------

pylsdj manipulates .sav files through a :py:class:`pylsdj.SAVFile` object. This object can be used to load, store, and edit the contents of LSDJ's SRAM file.

Several methods of :py:class:`pylsdj.SAVFile` take a progress callback function that callers can use to notify callers of how far the operation has progressed. Callback functions take four arguments

* message: a message explaining what the step is doing
* step: the step that the operation is currently on
* total_steps: the total number of steps in the operation
* continuing: True if the operation is going to continue

The :py:class:`pylsdj.SAVFile` is described below. There's not a lot to it, since it's just a container for projects.

.. autoclass:: pylsdj.SAVFile
   :members:
   :special-members:
