import json
import os
import sys
import math
from nose.tools import assert_equal, assert_less

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(SCRIPT_DIR, os.path.pardir))

from . import filepack as filepack
from .project import Project, load_lsdsng, load_srm
from .utils import temporary_file


def test_save_load_lsdsng():
    sample_song_compressed = os.path.join(
        SCRIPT_DIR, "test_data", "UNTOLDST.lsdsng")

    proj = load_lsdsng(sample_song_compressed)

    expected_song_name = b"UNTOLDST"
    expected_song_version = 23

    assert_equal(proj.name, expected_song_name)
    assert_equal(proj.version, expected_song_version)

    tmp_abspath = None

    with temporary_file() as tmp_abspath:
        proj.save_lsdsng(tmp_abspath)

        read_project = load_lsdsng(tmp_abspath)

        assert_equal(proj, read_project)


def test_read_write_project():
    sample_song_compressed = os.path.join(
        SCRIPT_DIR, "test_data", "sample_song_compressed.json")

    with open(sample_song_compressed, "r") as fp:
        song_data_compressed = json.load(fp)

    song_data = filepack.decompress(song_data_compressed)
    song_name = "UNTOLDST"
    song_version = 23

    # 0xbadf00d for size in blocks is synthetic, since we don't really care
    # about its size for the purposes of this test
    bogus_size_blks = 0xbadf00d

    proj = Project(
        song_name, song_version, bogus_size_blks, song_data)

    assert_equal(proj.name, song_name)
    assert_equal(proj.version, song_version)

    raw_data = proj.get_raw_data()

    recompressed = filepack.compress(raw_data)

    assert_less(math.fabs(len(recompressed) - len(song_data_compressed)), 512)

    # Do comparison based on parsed object, since the actual input data can
    # contain noise
    proj_from_raw_data = Project(
        song_name, song_version, bogus_size_blks, raw_data)

    assert_equal(proj_from_raw_data._song_data, proj._song_data)


def test_block_remap_required():
    block_remap_song = os.path.join(SCRIPT_DIR, "test_data", "ANNARKTE.lsdsng")

    proj = load_lsdsng(block_remap_song)

    assert_equal(b"ANNARKTE", proj.name)
    assert_equal(3, proj.version)
    assert_equal(4, proj.size_blks)


def test_srm_load():
    srm_song = os.path.join(SCRIPT_DIR, "test_data", "sample.srm")

    proj = load_srm(srm_song)
    assert_equal("CLICK", proj.song.instruments[0].name)

    assert_equal(0x10, proj.song.sequence[0]['pu1'].index)
    assert_equal(0x05, proj.song.sequence[4]['noi'].index)



def test_save_load_srm():
    srm_song = os.path.join(SCRIPT_DIR, "test_data", "sample.srm")

    proj = load_srm(srm_song)

    with temporary_file() as tmp_proj_abspath:
        proj.save_srm(tmp_proj_abspath)
        read_proj = load_srm(tmp_proj_abspath)
        assert_equal(proj, read_proj)

if __name__ == "__main__":
    test_srm_load()
