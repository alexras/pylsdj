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

        self._song_data = bread.parse(data, spec.song)

        self.song = Song(self._song_data)
        """the song associated with the project"""

        self.size_blks = size_blks
        """the size of the song in filesystem blocks"""

        # Useful for applications tracking whether a project was modified since
        # it was loaded.
        self.modified = False

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

            preamble_data = bread.write(self._song_data)
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

    def __str__(self):
        return "<%s, %d>\n" % (self.name, self.version)
