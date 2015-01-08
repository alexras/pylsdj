import wave

import bread as b
from bread_spec import lsdj_rom_kits, KIT_SAMPLE_NAME_LENGTH, \
  SAMPLES_PER_KIT, KIT_NAME_LENGTH

from utils import fixed_width_string


SAMPLE_START_ADDRESS = 0x4060
EMPTY_SAMPLE_NAME = '\0--'

# WAVs are 4 bits/sample @ 11468 Hz in chunks of 16 bytes
# These are parameters passed to Wave_write objects during writing
WAVE_NUM_CHANNELS = 1
WAVE_SAMPLE_WIDTH = 1
WAVE_FRAMERATE = 11468
# WAVE_FRAMERATE = 5734

WAVE_PARAMS = (WAVE_NUM_CHANNELS, WAVE_SAMPLE_WIDTH, WAVE_FRAMERATE, 0,
               'NONE', 'not compressed')

class Kits(object):
    def __init__(self, rom_file):
        with open(rom_file, 'rb') as fp:
            self._data = b.parse(fp, lsdj_rom_kits)

        self._kits = map(lambda k: Kit(k), self._data.kits)

    def __getitem__(self, i):
        return self._kits[i]

class Kit(object):
    def __init__(self, data):
        self._data = data
        self._samples = map(lambda i: KitSample(self._data, i),
                            xrange(SAMPLES_PER_KIT))

    @property
    def name(self):
        return self._data.kit_name

    @name.setter
    def name(self, value):
        self._data.kit_name = fixed_width_string(value, KIT_NAME_LENGTH)

    @property
    def force_loops(self):
        return self._force_loops

    @property
    def samples(self):
        return self._samples

class KitSample(object):
    def __init__(self, data, index):
        self._data = data
        self.index = index

        # Because of data layout, indices for bits are
        #
        # 7, 6, 5, ..., 0, unused, 14, 13, ..., 8
        #
        # so the indexing logic is a little funky.

        if self.index < 8:
            self.force_loop_index = 7 - self.index
        else:
            self.force_loop_index = 15 - (self.index - 8)

        if self.index == 0:
            sample_start = 0
            sample_end = self._data.sample_ends[0]
        else:
            sample_start = self._data.sample_ends[self.index - 1]
            sample_end = self._data.sample_ends[self.index]

        sample_start = max(sample_start - SAMPLE_START_ADDRESS, 0)
        sample_end = max(sample_end - SAMPLE_START_ADDRESS, 0)

        self.sample_data =
            self._data.sample_data[sample_start:sample_end]

    @property
    def force_loop(self):
        return self._data.force_loop[self.force_loop_index]

    @force_loop.setter
    def force_loop(self, value):
        self._data.force_loop[self.force_loop_index] = value

    @property
    def name(self):
        return self._data.sample_names[self.index]

    @name.setter
    def name(self, value):
        self._data.sample_names[self.index] = fixed_width_string(
            value, KIT_SAMPLE_NAME_LENGTH, '-')

    def write_wave(self, filename):
        print self.name, len(self.sample_data)
        wave_output = None
        try:
            wave_output = wave.open(filename, 'w')
            wave_output.setparams(WAVE_PARAMS)
            wave_output.writeframes(self.sample_data)
        finally:
            if wave_output is not None:
                wave_output.close()

    def read_wave(self, filename):
        wave_input = None

        try:
            wave_input = wave.open(filename, 'r')
            self.sample_data = wave_input.readframes(
                wave_input.getnframes())
        finally:
            if wave_input is not None:
                wave_input.close()
