from vibrato import Vibrato

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

class VibratoMixin(object):
    @property
    def vibrato(self):
        """instrument's vibrato settings"""
        return Vibrato(self.data.vibrato)

    @staticmethod
    def import_lsdinst(obj, struct_data):
        Vibrato(obj.data.vibrato).import_lsdinst(struct_data)


class SoundLengthMixin(object):
    @property
    def sound_length(self):
        """"the instrument sound's length, a 6-bit integer or 'unlimited' if the
        sound plays forever"""
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
