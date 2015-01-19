from .vibrato import Vibrato


class EnvelopeMixin(object):

    @property
    def envelope(self):
        """the noise instrument's volume envelope (8-bit integer)"""
        return self.data.envelope

    @envelope.setter
    def envelope(self, value):
        self.data.envelope = value

    @staticmethod
    def import_lsdinst(obj, struct_data):
        obj.envelope = struct_data['data']['envelope']

    @staticmethod
    def equal(a, b):
        return (isinstance(a, EnvelopeMixin) and isinstance(b, EnvelopeMixin)
                and a.envelope == b.envelope)

class VibratoMixin(object):

    @property
    def vibrato(self):
        """instrument's vibrato settings"""
        return Vibrato(self.data.vibrato)

    @staticmethod
    def import_lsdinst(obj, struct_data):
        Vibrato(obj.data.vibrato).import_lsdinst(struct_data)

    @staticmethod
    def equal(a, b):
        return (isinstance(a, VibratoMixin) and isinstance(b, VibratoMixin)
                and a.vibrato == b.vibrato)



class SoundLengthMixin(object):

    @property
    def sound_length(self):
        """the instrument sound's length, a 6-bit integer or ``unlimited``
        if the sound plays forever"""
        if self.data.has_sound_length:
            return self.data.sound_length
        else:
            return 'unlimited'

    @sound_length.setter
    def sound_length(self, value):
        if value == 'unlimited':
            self.data.sound_length = 0
            self.data.has_sound_length = False
        else:
            self.data.sound_length = value

    @staticmethod
    def import_lsdinst(obj, struct_data):
        if struct_data['data']['has_sound_length']:
            obj.sound_length = struct_data['data']['sound_length']
        else:
            obj.sound_length = 'unlimited'

    @staticmethod
    def equal(a, b):
        return (isinstance(a, SoundLengthMixin)
                and isinstance(b, SoundLengthMixin)
                and a.sound_length == b.sound_length)

class SweepMixin(object):

    @property
    def sweep(self):
        """modulates the sound's frequency; only works on pulse 1
        (8-bit integer)"""
        return self.data.sweep

    @sweep.setter
    def sweep(self, value):
        self.data.sweep = value

    @staticmethod
    def import_lsdinst(obj, struct_data):
        obj.sweep = struct_data['data']['sweep']

    @staticmethod
    def equal(a, b):
        return (isinstance(a, SweepMixin) and isinstance(b, SweepMixin)
                and a.sweep == b.sweep)
