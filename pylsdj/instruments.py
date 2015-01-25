import json

from .utils import assert_index_sane

from .wave_instrument import WaveInstrument
from .pulse_instrument import PulseInstrument
from .kit_instrument import KitInstrument
from .noise_instrument import NoiseInstrument

class Instruments(object):
    instrumentClasses = {
        "pulse": PulseInstrument,
        "wave": WaveInstrument,
        "kit": KitInstrument,
        "noise": NoiseInstrument
    }

    def __init__(self, song):
        self.song = song
        self.alloc_table = song.song_data.instr_alloc_table
        self.access_objects = []

        for index in range(len(self.alloc_table)):
            instr_type = self.song.song_data.instruments[index].instrument_type

            self.access_objects.append(
                self.instrumentClasses[instr_type](song, index))

    def _set_instrument_type(self, index, instrument_type):
        assert instrument_type in Instruments.instrumentClasses, (
            "Invalid instrument type '%s'" % (instrument_type))

        assert_index_sane(index, len(self.song.song_data.instruments))

        current_access_object = self.access_objects[index]

        # If this instrument is of a different type than we're currently
        # accessing, we've got to make a new access object of the
        # appropriate type
        if (current_access_object is None or
                current_access_object.type != instrument_type):

            self.access_objects[index] = (
                self.instrumentClasses[instrument_type](self.song, index))

            self.access_objects[index].type = instrument_type

    def __getitem__(self, index):
        assert_index_sane(index, len(self.alloc_table))

        if not self.alloc_table[index]:
            return None

        return self.access_objects[index]

    def as_list(self):
        return self.access_objects

    def allocate(self, index, instrument_type):
        self.alloc_table[index] = True
        self._set_instrument_type(index, instrument_type)

    def import_from_file(self, index, filename):
        """Import this instrument's settings from the given file. Will
        automatically add the instrument's synth and table to the song's
        synths and tables if needed.

        Note that this may invalidate existing instrument accessor objects.

        :param index: the index into which to import

        :param filename: the file from which to load

        :raises ImportException: if importing failed, usually because the song
          doesn't have enough synth or table slots left for the instrument's
          synth or table
        """

        with open(filename, 'r') as fp:
            self._import_from_struct(index, json.load(fp))

    def _import_from_struct(self, index, lsdinst_struct):
        instr_type = lsdinst_struct['data']['instrument_type']

        self.allocate(index, instr_type)

        instrument = self.song.instruments[index]
        instrument.name = lsdinst_struct['name']

        # Make sure we've got enough room for the table if we need it
        if 'table' in lsdinst_struct:
            table_index = self.song.tables.next_free()

            if table_index is None:
                raise ImportException(
                    "No available table slot in which to store the "
                    "instrument's table data")

            self.song.tables.allocate(table_index)
            instrument.table = self.song.tables[table_index]

        instrument.import_lsdinst(lsdinst_struct)
