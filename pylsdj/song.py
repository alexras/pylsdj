from .utils import assert_index_sane
from . import bread_spec

from .synth import Synth
from .table import Table
from .phrase import Phrase
from .chain import Chain
from .speech_instrument import SpeechInstrument

from .instruments import Instruments

from .bread_spec import INSTRUMENT_TYPE_CODE
from .filepack import DEFAULT_INSTRUMENT

from .clock import Clock, TotalClock

from .exceptions import ImportException

from .vendor.six.moves import range

# Number of channels
NUM_CHANNELS = 4


class AllocTable(object):

    def __init__(self, song, alloc_table, object_class):
        self.alloc_table = alloc_table

        self.access_objects = []

        for index in range(len(alloc_table)):
            self.access_objects.append(object_class(song, index))

    def __getitem__(self, index):
        assert_index_sane(index, len(self.alloc_table))

        if not self.alloc_table[index]:
            return None

        return self.access_objects[index]

    def allocate(self, index):
        self.alloc_table[index] = True

    def __len__(self):
        return len(self.alloc_table)

    def as_list(self):
        l = []
        for i in range(len(self.alloc_table)):
            if not self.alloc_table[i]:
                l.append(None)
            else:
                l.append(self.access_objects[i])

        return l

    def next_free(self):
        for i, occupied in enumerate(self.alloc_table):
            if not occupied:
                return i
        return None

class Grooves(object):

    def __init__(self, song):
        self.song = song

    def __getitem__(self, index):
        assert_index_sane(index, len(self.song.song_data.grooves))

        return self.song.song_data.grooves[index]


class Sequence(object):
    PU1 = "pu1"
    PU2 = "pu2"
    WAV = "wav"
    NOI = "noi"

    NO_CHAIN = 0xff

    def __init__(self, song):
        self.song = song

    def __getitem__(self, index):
        assert_index_sane(index, len(self.song.song_data.song))
        raw_chain = self.song.song_data.song[index]

        chain_objs = {}

        for channel in [Sequence.PU1,
                        Sequence.PU2,
                        Sequence.WAV,
                        Sequence.NOI]:
            chain_number = getattr(raw_chain, channel)

            if chain_number != Sequence.NO_CHAIN:
                chain = self.song.chains[chain_number]
                chain_objs[channel] = chain

        return chain_objs

    def __setitem__(self, index, value_dict):
        assert_index_sane(index, len(self.song.song_data.song))

        for channel in value_dict:
            assert (channel in [Sequence.PU1, Sequence.PU2, Sequence.WAV,
                                Sequence.NOI]), \
                ("Channel '%d' is not a valid channel" % (channel))

            chain = value_dict[channel]
            chain_number = chain.index

            assert_index_sane(chain_number,
                              len(self.song.song_data.chain_alloc_table))

            assert self.song.song_data.chain_alloc_table[chain_number], (
                "Assigning a chain (%d) that has not been allocated" % (
                    chain_number))

            setattr(self.song.song_data.song[index], channel, chain_number)

    def __str__(self):
        output_str = ''

        def add_line(line):
            output_str += line + '\n'


        add_line("   PU1 PU2 WAV NOI")

        for i, row in enumerate(self.song.song_data.song):
            add_line("%02x" % (i), end=' ')

            for channel in ["pu1", "pu2", "wav", "noi"]:
                chain_number = getattr(row, channel)

                if chain_number == Sequence.NO_CHAIN:
                    add_line(" --", end=' ')
                else:
                    add_line(" %02x" % (getattr(row, channel)), end=' ')
            add_line("")

        return output_str

class Synths(object):

    def __init__(self, song):
        self.song = song
        self.access_objects = []

        for index in range(bread_spec.NUM_SYNTHS):
            self.access_objects.append(Synth(self.song, index))

    def __getitem__(self, index):
        assert_index_sane(index, bread_spec.NUM_SYNTHS)

        return self.access_objects[index]

    def as_list(self):
        return self.access_objects


class Song(object):

    """A song consists of a sequence of chains, one per channel.
    """

    def __init__(self, song_data):
        # Check checksums
        assert song_data.mem_init_flag_1 == b'rb'
        assert song_data.mem_init_flag_2 == b'rb'
        assert song_data.mem_init_flag_3 == b'rb'

        # Everything we do to the song or any of its components should update
        # the song data object, so that we can rely on bread's writer to write
        # it back out in the right format
        self.song_data = song_data

        self._grooves = Grooves(self)
        self._speech_instrument = SpeechInstrument(self)
        self._synths = Synths(self)

        self._instruments = Instruments(self)

        # Stitch together allocated tables
        self._tables = AllocTable(
            song=self,
            alloc_table=self.song_data.table_alloc_table,
            object_class=Table)

        # Stitch together allocated phrases
        self._phrases = AllocTable(
            song=self,
            alloc_table=self.song_data.phrase_alloc_table,
            object_class=Phrase)

        # Stitch together allocated chains
        self._chains = AllocTable(
            song=self,
            alloc_table=self.song_data.chain_alloc_table,
            object_class=Chain)

        self._sequence = Sequence(self)

    def __str__(self):
        return str(self.sequence)

    @property
    def instruments(self):
        """the song's instrument table, represented as a list of
        Instrument objects"""
        return self._instruments

    @property
    def phrases(self):
        """the song's phrase table, represented as a list of Phrase objects"""
        return self._phrases

    @property
    def chains(self):
        """the song's chain table, represented as a list of Chain objects"""
        return self._chains

    @property
    def grooves(self):
        """the song's groove table"""
        return self._grooves

    @property
    def speech_instrument(self):
        """the song's speech instrument settings, represented as a
        SpeechInstrument object"""
        return self._speech_instrument

    @property
    def synths(self):
        return self._synths

    @property
    def clock(self):
        """the amount of time LSDJ has been used since the last memory
        reset, represented as a Clock object"""
        return Clock(self.song_data.clock)

    @property
    def global_clock(self):
        """the amount of time LSDJ has been used total, represented
        as a Clock object"""
        return TotalClock(self.song_data.total_clock)

    @property
    def song_version(self):
        """the song's version number"""
        return self.song_data.version

    @song_version.setter
    def song_version(self, version):
        self.song_data.version = version

    @property
    def sequence(self):
        """the song's sequence, showing the order in which chains are
        played on each of the four channels"""
        return self._sequence

    @property
    def tables(self):
        """the song's table of macro tables, represented as Table objects"""
        return self._tables

# For fields with a one-to-one correspondence with song data, we'll
# programmatically insert properties to avoid repetition
for field, doc in [("tempo", "the song's tempo"),
                   ("tune_setting", None),
                   ("key_delay", "the delay before key repeat is activated "
                    "for Game Boy buttons"),
                   ("key_repeat", "the key repeat speed for Game Boy buttons"),
                   ("font", "the selected LSDJ font"),
                   ("sync_setting", 'LSDJ\'s sync setting; one of ``"off"``, '
                    '``"slave"``, ``"master"``, ``"midi"``, ``"nano"``, and '
                    '``"keyboard"``'),
                   ("colorset", "the selected LSDJ colorset"),
                   ("clone", 'chain cloning depth; one of '
                    '``"deep"``, ``"slim"``'),
                   ("file_changed", "``1`` if the file has changed since last "
                    "save, ``0`` otherwise"),
                   ("power_save", None),
                   ("prelisten", "if non-zero, play notes and instruments "
                    "while entering them"),
                   ("bookmarks", "list of screen bookmarks"),
                   ("wave_synth_overwrite_locks", None)]:
    def field_getter(this):
        return getattr(this.song_data, field)

    def field_setter(this, value):
        setattr(this.song_data, field, value)

    setattr(Song, field, property(fset=field_setter, fget=field_getter,
                                  doc=doc))
