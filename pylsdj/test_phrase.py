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

def test_arduinoboy_phrase_load():
    proj = load_lsdsng(os.path.join(SCRIPT_DIR, 'test_data', 'ARDBOYxx.lsdsng'))
    phrase = proj.song.phrases[0]

    assert_equal('C 3', phrase.notes[0])
    assert_equal('C#3', phrase.notes[1])
    assert_equal('D 3', phrase.notes[2])
    assert_equal('D#3', phrase.notes[3])

    assert_equal('N', phrase.fx[0])
    assert_equal(0x18, phrase.fx_val[0])

    assert_equal('X', phrase.fx[1])
    assert_equal(0x12, phrase.fx_val[1])

    assert_equal('Q', phrase.fx[2])
    assert_equal(0xf7, phrase.fx_val[2])

    assert_equal('Y', phrase.fx[3])
    assert_equal(0xd8, phrase.fx_val[3])
