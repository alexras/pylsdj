class Vibrato(object):

    def __init__(self, data):
        self._data = data

    @property
    def type(self):
        """ ``hf`` (for high frequency sine), ``sawtooth``,
        ``saw`` or ``square``"""
        return self._data.type

    @type.setter
    def type(self, value):
        self._data.type = value

    @property
    def direction(self):
        """'down' or 'up'"""
        return self._data.direction

    @direction.setter
    def direction(self, value):
        self._data.direction = value

    def import_lsdinst(self, struct_data):
        self.direction = struct_data['data']['vibrato']['direction']
        self.type = struct_data['data']['vibrato']['type']

    def __eq__(self, other):
        return (isinstance(other, Vibrato)
                and self.type == other.type
                and self.direction == other.direction)
