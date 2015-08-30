import wave

import bread as b

from .vendor.six.moves import range

from .bread_spec import lsdj_rom_kits, KIT_SAMPLE_NAME_LENGTH, \
    SAMPLES_PER_KIT, KIT_NAME_LENGTH, SAMPLE_START_ADDRESS, MAX_SAMPLE_LENGTH
from .utils import fixed_width_string


EMPTY_SAMPLE_NAME = '\0--'

# WAVs are 8 bits/sample PCM-encoded @ 11468 Hz
# These are parameters passed to Wave_write objects during writing
WAVE_NUM_CHANNELS = 1
WAVE_SAMPLE_WIDTH = 1
WAVE_FRAMERATE = 11468

WAVE_PARAMS = (WAVE_NUM_CHANNELS, WAVE_SAMPLE_WIDTH, WAVE_FRAMERATE, 0,
               'NONE', 'not compressed')


class Kits(object):
    """A wrapper for an LSDJ ROM's kits"""

    def __init__(self, rom_file):
        """Load kits from the provided LSDJ ROM

        :param rom_file: path to the LSDJ ROM to load
        """
        with open(rom_file, 'rb') as fp:
            self._data = b.parse(fp, lsdj_rom_kits)

        # Don't include the last four kits in the kit list, which are reserved
        # for the speech synthesizer
        self._kits = list(map(lambda k: Kit(k), self._data.kits[:-4]))

    def __getitem__(self, i):
        return self._kits[i]

    def __str__(self):
        return '\n'.join(map(str, self._kits))

    def __iter__(self):
        for kit in self._kits:
            yield kit


class Kit(object):
    """An individual sample kit"""

    def __init__(self, data):
        self._data = data

        if self._data.magic_number != [0x60, 0x40]:
            raise Exception(
                'Expected magic number to be 0x60, 0x40, '
                'but was %s' % (', '.join(map(hex, self._data.magic_number))))

        self._samples = list(map(lambda i: KitSample(self._data, i),
                                 range(SAMPLES_PER_KIT)))

    @property
    def name(self):
        """the kit's name"""
        return self._data.kit_name

    @name.setter
    def name(self, value):
        self._data.kit_name = fixed_width_string(value, KIT_NAME_LENGTH)

    @property
    def samples(self):
        """the samples that comprise the kit, each of which is a KitSample"""
        return self._samples

    def __str__(self):
        kit_str = "Kit %s\n" % (self.name)
        kit_str += '\n'.join(map(lambda sample: '  %s' % (sample), self.samples))

        return kit_str

    def __iter__(self):
        for sample in self._samples:
            if sample.used:
                yield sample


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

    def _sample_used(self, index):
        return (self._data.sample_ends[index] > 0)

    def _get_sample_data_bounds(self, index=None, sample_ends=None):
        if index is None:
            index = self.index

        if sample_ends is None:
            sample_ends = self._data.sample_ends

        if index == 0:
            sample_start = 0
            sample_end = sample_ends[0]
        else:
            sample_start = sample_ends[index - 1]
            sample_end = sample_ends[index]

        # Sample end addresses are relative to the start of the kit's sample memory
        sample_start = sample_start - SAMPLE_START_ADDRESS
        sample_end = sample_end - SAMPLE_START_ADDRESS

        # Multiply all sample bounds by two since we're dealing with nibbles
        # and the offsets are stored as bytes
        sample_start = sample_start * 2
        sample_end = sample_end * 2

        sample_start = max(sample_start, 0)
        sample_end = max(sample_end, 0)

        return (sample_start, sample_end)

    def _get_sample_length(self, index):
        if not self._sample_used(index):
            return 0
        else:
            sample_start, sample_end = self._get_sample_data_bounds(index)

            return (sample_end - sample_start + 1)

    def _get_sample_data(self, index):
        if not self._sample_used(index):
            return None

        sample_start, sample_end = self._get_sample_data_bounds(index)

        return bytearray(self._data.sample_data[sample_start:sample_end])

    @property
    def force_loop(self):
        """true if the sample will loop, false otherwise"""
        return self._data.force_loop[self.force_loop_index]

    @force_loop.setter
    def force_loop(self, value):
        self._data.force_loop[self.force_loop_index] = value

    @property
    def name(self):
        """the sample's name"""
        return self._data.sample_names[self.index]

    @name.setter
    def name(self, value):
        self._data.sample_names[self.index] = fixed_width_string(
            value, KIT_SAMPLE_NAME_LENGTH, '-')

    @property
    def used(self):
        """True if the sample's memory is in use, false otherwise"""
        return self._sample_used(self.index)

    @property
    def sample_data(self):
        """The raw hex nibbles that comprise the sample"""
        return self._get_sample_data(self.index)

    @sample_data.setter
    def sample_data(self, sample_data):
        # For simplicity, we'll just pack samples into their new locations and
        # overwrite the sample memory for the kit.

        new_sample_ends = []

        new_sample_data = []

        for i in range(SAMPLES_PER_KIT):
            if not self._sample_used(i) and i != self.index:
                # We've found the first unused sample; since samples are
                # presumed to be contiguous, this means we're done moving
                # samples
                break

            if i == self.index:
                new_sample_data.extend(sample_data)
            else:
                current_sample_data = self._get_sample_data(i)

                if current_sample_data is not None:
                    new_sample_data.extend(current_sample_data)

            new_sample_ends.append(int(len(new_sample_data) / 2))

        if len(new_sample_ends) < SAMPLES_PER_KIT:
            new_sample_ends.extend([0] * (SAMPLES_PER_KIT - len(new_sample_ends)))

        if len(new_sample_data) < MAX_SAMPLE_LENGTH * 2:
            new_sample_data.extend([0] * ((MAX_SAMPLE_LENGTH * 2) - len(new_sample_data)))
        elif len(new_sample_data) > MAX_SAMPLE_LENGTH * 2:
            raise Exception('Not enough sample memory to add this sample to its kit')

        self._data.sample_data = new_sample_data
        self._data.sample_ends = new_sample_ends

    def __str__(self):
        sample_start, sample_end = self._get_sample_data_bounds()
        return '%s [0x%04x - 0x%04x]' % (self.name, sample_start, sample_end)

    @property
    def length(self):
        """the length of the sample, in bytes"""
        sample_start, sample_end = self._get_sample_data_bounds()
        return (sample_end - sample_start + 1) * 4

    def write_wav(self, filename):
        """Write this sample to a WAV file.

        :param filename: the file to which to write
        """

        wave_output = None
        try:
            wave_output = wave.open(filename, 'w')

            wave_output.setparams(WAVE_PARAMS)

            frames = bytearray([x << 4 for x in self.sample_data])

            wave_output.writeframes(frames)
        finally:
            if wave_output is not None:
                wave_output.close()

    def read_wav(self, filename):
        """Read sample data for this sample from a WAV file.

        :param filename: the file from which to read
        """
        wave_input = None

        try:
            wave_input = wave.open(filename, 'r')
            wave_frames = bytearray(
                wave_input.readframes(wave_input.getnframes()))

            self.sample_data = [x >> 4 for x in wave_frames]

        finally:
            if wave_input is not None:
                wave_input.close()
