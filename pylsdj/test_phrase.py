import os

from nose.tools import assert_equal

from .project import load_lsdsng

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

def test_phrase_load():
    proj = load_lsdsng(os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST.lsdsng'))

    phrase = proj.song.phrases[0x24]

    assert_equal('C 4', phrase.notes[0x0])
    assert_equal('K', phrase.fx[0x3])
    assert_equal('L', phrase.fx[0xc])
    assert_equal(1, phrase.fx_val[0xc])
    assert_equal(None, phrase.instruments[1])
    assert_equal(2, phrase.instruments[4].index)
