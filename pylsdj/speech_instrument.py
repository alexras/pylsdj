from instrument import Instrument
from utils import add_song_data_property

# Max. length of a word name
WORD_NAME_LENGTH = 4

def word_cleanup(word):
    return ''.join([chr(x) for x in word if x != 0]).ljust(WORD_NAME_LENGTH)

class Word(object):
    def __init__(self, song, index):
        self.song = song
        self.index = index

add_song_data_property(Word, 'name', ("word_names", ), use_index=True,
                       doc="the word's name")
add_song_data_property(Word, 'sounds', ("words", ), use_index=True,
                       doc="the sounds that make up the word")

class SpeechInstrument(object):
    def __init__(self, song):
        self._song = song

        self._words = [
            Word(self._song, i) for i in
            xrange(len(self._song.song_data.words))]

    @property
    def song(self):
        """the speech instrument's parent song"""
        return self._song

    @property
    def words(self):
        """the speech instrument's defined words"""
        return self._words
