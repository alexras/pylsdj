from .instrument import Instrument
from .instrument_mixins import VibratoMixin


class KitInstrument(Instrument, VibratoMixin):

    def __init__(self, song, index):
        super(KitInstrument, self).__init__(song, index)

    @property
    def volume(self):
        """the kit's volume; 0 to 3"""
        return self.data.volume

    @volume.setter
    def volume(self, value):
        self.data.volume = value

    @property
    def kit_1(self):
        """the index of the first kit in LSDJ's kit list"""
        return self.data.kit_1

    @kit_1.setter
    def kit_1(self, value):
        self.data.kit_1 = value

    @property
    def loop_1(self):
        """loop sample in kit 1 and start playing from an offset"""
        return self.data.loop_1

    @loop_1.setter
    def loop_1(self, value):
        self.data.loop_1 = value

    @property
    def keep_attack_1(self):
        """loop sample in kit 1 and start playing from beginning"""
        return self.data.keep_attack_1

    @keep_attack_1.setter
    def keep_attack_1(self, value):
        self.data.keep_attack_1 = value

    @property
    def length_1(self):
        """the length of kit 1's sound (0 means 'always play the sample to
        the end' and is displayed as AUT in LSDJ)"""
        return self.data.length_1

    @length_1.setter
    def length_1(self, value):
        self.data.length_1 = value

    @property
    def offset_1(self):
        """ kit 1's loop start point (if loop_1 is True and keep_attack_1 is
        False)"""
        return self.data.offset_1

    @offset_1.setter
    def offset_1(self, value):
        self.data.offset_1 = value

    @property
    def kit_2(self):
        """the index of the second kit in LSDJ's kit list"""
        return self.data.kit_2

    @kit_2.setter
    def kit_2(self, value):
        self.data.kit_2 = value

    @property
    def loop_2(self):
        """loop sample in kit 2 and start playing from an offset"""
        return self.data.loop_2

    @loop_2.setter
    def loop_2(self, value):
        self.data.loop_2 = value

    @property
    def keep_attack_2(self):
        """loop sample in kit 2 and start playing from beginning"""
        return self.data.keep_attack_2

    @keep_attack_2.setter
    def keep_attack_2(self, value):
        self.data.keep_attack_2 = value

    @property
    def length_2(self):
        """the length of kit 2's sound (0 means 'always play the sample to
        the end' and is displayed as AUT in LSDJ)"""
        return self.data.length_2

    @length_2.setter
    def length_2(self, value):
        self.data.length_2 = value

    @property
    def offset_2(self):
        """ kit 2's loop start point (if loop_2 is True and keep_attack_2 is
        False)"""
        return self.data.offset_2

    @offset_2.setter
    def offset_2(self, value):
        self.data.offset_2 = value

    @property
    def pitch(self):
        """sample pitch shift (8-bit integer)"""
        return self.data.pitch

    @pitch.setter
    def pitch(self, value):
        self.data.pitch = value

    @property
    def dist_type(self):
        """algorithm used when two kits are mixed together; ``clip``, ``shape``,
        ``shap2`` or ``wrap``"""
        return self.data.dist_type

    @dist_type.setter
    def dist_type(self, value):
        self.data.dist_type = value

    @property
    def half_speed(self):
        """if true, play samples at half their normal speed"""
        return self.data.half_speed

    @half_speed.setter
    def half_speed(self, value):
        self.data.half_speed = value

    def import_lsdinst(self, lsdinst_struct):
        super(KitInstrument, self).import_lsdinst(lsdinst_struct)

        self.volume = lsdinst_struct['data']['volume']

        self.kit_1 = lsdinst_struct['data']['kit_1']
        self.loop_1 = lsdinst_struct['data']['loop_1']
        self.keep_attack_1 = lsdinst_struct['data']['keep_attack_1']
        self.length_1 = lsdinst_struct['data']['length_1']
        self.offset_1 = lsdinst_struct['data']['offset_1']

        self.kit_2 = lsdinst_struct['data']['kit_2']
        self.loop_2 = lsdinst_struct['data']['loop_2']
        self.keep_attack_2 = lsdinst_struct['data']['keep_attack_2']
        self.length_2 = lsdinst_struct['data']['length_2']
        self.offset_2 = lsdinst_struct['data']['offset_2']

        self.pitch = lsdinst_struct['data']['pitch']
        self.dist_type = lsdinst_struct['data']['dist_type']

        VibratoMixin.import_lsdinst(self, lsdinst_struct)
