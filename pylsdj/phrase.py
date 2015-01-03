from utils import add_song_data_property, assert_index_sane, ObjectLookupDict

class Phrase(object):
    """A phrase is a sequence of notes for a single channel.
    """
    def __init__(self, song, index):
        self._song = song
        self._index = index
        self._instruments = ObjectLookupDict(
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

for property_name, doc in [
        ("notes", "a list of the phrase's notes, one byte per note"),
        ("fx", "a list of the phrase's effects, one byte per effect"),
        ("fx_val", "a list of the phrase's effect parameters, "
         "one byte per effect")]:
    add_song_data_property(Phrase, property_name, ("phrase_" + property_name,),
                           use_index = True, doc=doc)
