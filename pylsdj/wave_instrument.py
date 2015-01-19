from .instrument import Instrument
from .instrument_mixins import VibratoMixin
from .exceptions import ImportException

from . import bread_spec

from .synth import Synth

from .vendor.six.moves import range

class WaveInstrument(Instrument, VibratoMixin):

    def __init__(self, song, index):
        super(WaveInstrument, self).__init__(song, index)

    @property
    def volume(self):
        """the sound's volume; 0 through 3"""
        return self.data.volume

    @volume.setter
    def volume(self, value):
        self.data.volume = value

    @property
    def synth(self):
        """the wave's synth settings"""
        return self.song.synths[self.data.synth]

    @synth.setter
    def synth(self, value):
        self.data.synth = value.index

    @property
    def repeat(self):
        """the synth sound's repeat point (4-bit integer)"""
        return self.data.repeat

    @repeat.setter
    def repeat(self, value):
        self.data.repeat = value

    @property
    def play_type(self):
        """how to play the synth sound; ``once``, ``loop``, ``ping-pong``,
        or ``manual``"""
        return self.data.play_type

    @play_type.setter
    def play_type(self, value):
        self.data.play_type = value

    @property
    def steps(self):
        """length of the synth sound (4-bit integer)"""
        return self.data.steps

    @steps.setter
    def steps(self, value):
        self.data.steps = value

    @property
    def speed(self):
        """how fast the sound should be played back (4-bit integer)"""
        return self.data.speed

    @speed.setter
    def speed(self, value):
        self.data.speed = value

    def _get_open_synth_index(self):
        available_synths = set(range(bread_spec.NUM_SYNTHS))

        for instrument in self.song.instruments.as_list():
            if instrument is not None and instrument.type == 'wave':
                available_synths.discard(instrument.synth.index)

        if len(available_synths) == 0:
            return None
        else:
            return available_synths.pop()

    def import_lsdinst(self, lsdinst_struct):
        super(WaveInstrument, self).import_lsdinst(lsdinst_struct)

        # Make sure we've got enough space for the synth if we need one
        synth_index = self._get_open_synth_index()

        if synth_index is None:
            raise ImportException(
                "No available synth slot in which to store the instrument's "
                "synth data")

        synth = Synth(self.song, synth_index)
        synth.import_lsdinst(lsdinst_struct['synth'])

        self.synth = synth

        VibratoMixin.import_lsdinst(self, lsdinst_struct)

    def export_struct(self):
        export_struct = super(WaveInstrument, self).export_struct()

        export_struct['synth'] = Synth(self.song, self.synth.index).export()

        return export_struct
