from .instrument import Instrument
from .instrument_mixins import SoundLengthMixin, EnvelopeMixin, SweepMixin

MIXINS = [SoundLengthMixin, EnvelopeMixin, SweepMixin]


class NoiseInstrument(Instrument, SoundLengthMixin, EnvelopeMixin, SweepMixin):

    def __init__(self, song, index):
        super(NoiseInstrument, self).__init__(song, index)

    @property
    def s_cmd(self):
        """``free`` or ``stable``. When free, altering noise shape with the
        S command can sometimes mute the sound. When stable, sound will never
        be muted by accident. My understanding is that this setting exists for
        backwards-compatibility of behavior in old LSDJ instruments"""
        return self.data.s_cmd

    @s_cmd.setter
    def s_cmd(self, value):
        self.data.s_cmd = value

    def import_lsdinst(self, struct_data):
        super(NoiseInstrument, self).import_lsdinst(struct_data)

        self.s_cmd = struct_data['data']['s_cmd']

        for mixin in MIXINS:
            mixin.import_lsdinst(self, struct_data)
