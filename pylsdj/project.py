import math
import bread
from . import bread_spec as spec
from .song import Song
from . import filepack
from . import blockutils
from .blockutils import BlockReader, BlockWriter, BlockFactory


def load_lsdsng(filename):
    """Load a Project from a ``.lsdsng`` file.

    :param filename: the name of the file from which to load
    :rtype: :py:class:`pylsdj.Project`
    """

    # Load preamble data so that we know the name and version of the song
    with open(filename, 'rb') as fp:
        preamble_data = bread.parse(fp, spec.lsdsng_preamble)

    with open(filename, 'rb') as fp:
        # Skip the preamble this time around
        fp.seek(int(len(preamble_data) / 8))

        # Load compressed data into a block map and use BlockReader to
        # decompress it
        factory = BlockFactory()

        while True:
            block_data = bytearray(fp.read(blockutils.BLOCK_SIZE))

            if len(block_data) == 0:
                break

            block = factory.new_block()
            block.data = block_data

        remapped_blocks = filepack.renumber_block_keys(factory.blocks)

        reader = BlockReader()
        compressed_data = reader.read(remapped_blocks)

        # Now, decompress the raw data and use it and the preamble to construct
        # a Project
        raw_data = filepack.decompress(compressed_data)

        name = preamble_data.name
        version = preamble_data.version
        size_blks = int(math.ceil(
            float(len(compressed_data)) / blockutils.BLOCK_SIZE))

        return Project(name, version, size_blks, raw_data)


def load_srm(filename):
    """Load a Project from an ``.srm`` file.

    :param filename: the name of the file from which to load
    :rtype: :py:class:`pylsdj.Project`
    """

    # .srm files are just decompressed projects without headers

    # In order to determine the file's size in compressed blocks, we have to
    # compress it first
    with open(filename, 'rb') as fp:
        raw_data = fp.read()

    compressed_data = filepack.compress(raw_data)

    factory = BlockFactory()
    writer = BlockWriter()
    writer.write(compressed_data, factory)

    size_in_blocks = len(factory.blocks)

    # We'll give the file a dummy name ("SRMLOAD") and version, since we know
    # neither
    name = "SRMLOAD"
    version = 0

    return Project(name, version, size_in_blocks, raw_data)


class Project(object):

    def __init__(self, name, version, size_blks, data):
        self.name = name
        """the project's name"""

        self.version = version
        """the project's version (incremented on every save in LSDJ)"""

        self.size_blks = size_blks
        """the size of the song in filesystem blocks"""

        # Useful for applications tracking whether a project was modified since
        # it was loaded.
        self.modified = False

        # Since parsing the song is expensive, we'll load it lazily from the
        # raw data on-demand
        self.__song_data = None
        self._song = None
        self._raw_bytes = data

    @property
    def _song_data(self):
        if self.__song_data is None:
            self.__song_data = bread.parse(self._raw_bytes, spec.song)

        return self.__song_data

    @_song_data.setter
    def _song_data(self, value):
        self.__song_data = value

    @property
    def song(self):
        """the song associated with the project"""
        if self._song is None:
            self._song = Song(self._song_data)

        return self._song

    @song.setter
    def song(self, value):
        self._song = value

    def get_raw_data(self):
        return bread.write(self._song_data, spec.song)

    def save(self, filename):
        """Save a project in .lsdsng format to the target file.

        :param filename: the name of the file to which to save

        :deprecated: use ``save_lsdsng(filename)`` instead
        """
        with open(filename, 'wb') as fp:
            writer = BlockWriter()
            factory = BlockFactory()

            preamble_dummy_bytes = bytearray([0] * 9)
            preamble = bread.parse(
                preamble_dummy_bytes, spec.lsdsng_preamble)
            preamble.name = self.name
            preamble.version = self.version

            preamble_data = bread.write(preamble)
            raw_data = self.get_raw_data()
            compressed_data = filepack.compress(raw_data)

            writer.write(compressed_data, factory)

            fp.write(preamble_data)

            for key in sorted(factory.blocks.keys()):
                fp.write(bytearray(factory.blocks[key].data))

    def save_lsdsng(self, filename):
        """Save a project in .lsdsng format to the target file.

        :param filename: the name of the file to which to save
        """
        return self.save(filename)

    def save_srm(self, filename):
        """Save a project in .srm format to the target file.

        :param filename: the name of the file to which to save
        """
        with open(filename, 'wb') as fp:
            raw_data = bread.write(self._song_data, spec.song)
            fp.write(raw_data)

    def __eq__(self, other):
        return self._song_data == other._song_data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "<%s, %d>\n" % (self.name, self.version)
