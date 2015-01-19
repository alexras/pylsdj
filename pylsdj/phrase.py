from .utils import ObjectLookupDict

# Need to define a custom lookup dict so that index=255 is treated as unset and
# doesn't throw an exception
class InstrumentLookupDict(ObjectLookupDict):
    def __getitem__(self, index):
        if self.id_list[index] == 255:
            return None

        return super(InstrumentLookupDict, self).__getitem__(index)

class Phrase(object):

    """A phrase is a sequence of notes for a single channel.
    """

    def __init__(self, song, index):
        self._song = song
        self._index = index
        self._instruments = InstrumentLookupDict(
            self._song.song_data.phrase_instruments[index],
            self._song.instruments)

    @property
    def song(self):
        """a reference to the phrase's parent song"""
        return self._song

    @property
    def index(self):
        """the phrase's index within its parent song's phrase table"""
        return self._index

    @property
    def instruments(self):
        """a list of Instruments, None where no instrument is defined"""
        return self._instruments

    @property
    def notes(self):
        """a list of the phrase's notes, one byte per note"""
        return self.song.song_data.phrase_notes[self._index]

    @property
    def fx(self):
        """a list of the phrase's effects, one byte per effect"""
        return self.song.song_data.phrase_fx[self._index]

    @property
    def fx_val(self):
        """a list of the phrase's effect parameters, one byte per effect"""
        return self.song.song_data.phrase_fx_val[self._index]
