from .bread_spec import STEPS_PER_TABLE
from .vendor.six.moves import range

class TableFX(object):

    def __init__(self, params, table_index, fx_index):
        self._params = params
        self._table_index = table_index
        self._fx_index = fx_index

    @property
    def command(self):
        """the effect's command"""
        return self._params.fx[self._table_index][self._fx_index]

    @command.setter
    def command(self, value):
        self._params.fx[self._table_index][self._fx_index] = value

    @property
    def value(self):
        """the command's parameter"""
        return self._params.val[self._table_index][self._fx_index]

    @value.setter
    def value(self, val):
        self._params.val[self._table_index][self._fx_index] = val

    def __eq__(self, other):
        return hasattr(other, '_params') and self._params == other._params

class Table(object):

    """Each table is a sequence of transposes, commands, and amplitude
    changes that can be applied to any channel."""

    def __init__(self, song, index):
        self._song = song
        self._index = index

        self._fx1 = [TableFX(self._song.song_data.table_cmd1, self._index, i)
                     for i in range(STEPS_PER_TABLE)]
        self._fx2 = [TableFX(self._song.song_data.table_cmd2, self._index, i)
                     for i in range(STEPS_PER_TABLE)]

    def __eq__(self, other):
        return self._fx1 == other._fx1 and self._fx2 == other._fx2

    @property
    def song(self):
        """the table's parent Song"""
        return self._song

    @property
    def index(self):
        """the table's index within its parent song's table of macro tables"""
        return self._index

    @property
    def fx1(self):
        """a list of the table's first effects, represented as TableFX
        objects"""
        return self._fx1

    @property
    def fx2(self):
        """a list of the table's first effects, represented as TableFX
        objects"""
        return self._fx2

    @property
    def envelopes(self):
        """a list of the table's volume envelopes"""
        return self._song.song_data.table_envelopes[self._index]

    @property
    def transposes(self):
        """a list of the table's volume transposes"""
        return self._song.song_data.table_transposes[self._index]

    def export(self):
        export_struct = []

        for i in range(STEPS_PER_TABLE):
            export_struct.append({
                "volume": self.envelopes[i],
                "transpose": self.transposes[i],
                "cmd1": [self.fx1[i].command, self.fx1[i].value],
                "cmd2": [self.fx2[i].command, self.fx2[i].value]
            })

        return export_struct

    def import_lsdinst(self, lsdinst_struct):
        table_data = lsdinst_struct['table']

        for i, table_row in enumerate(table_data):
            self.envelopes[i] = table_row["volume"]
            self.transposes[i] = table_row["transpose"]
            self.fx1[i].command, self.fx1[i].value = table_row["cmd1"]
            self.fx2[i].command, self.fx2[i].value = table_row["cmd2"]
