import os
import json

from nose.tools import assert_equal

from .project import load_lsdsng
from .utils import temporary_file

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

def _test_load_store_instrument(source_lsdsng, lsdinst_path, original_index):
    proj = load_lsdsng(source_lsdsng)
    proj.song.instruments.import_from_file(0x2a, lsdinst_path)

    target_instr = proj.song.instruments[0x2a]
    original_instr = proj.song.instruments[original_index]

    assert_equal(original_instr, target_instr)

    with temporary_file() as tmpfile:
        original_instr.export_to_file(tmpfile)

        with open(tmpfile, 'r') as fp:
            saved_inst = json.load(fp)

        with open(lsdinst_path, 'r') as fp:
            original_inst = json.load(fp)

        assert_equal(original_inst, saved_inst)


def test_load_store_wave_instrument():
    _test_load_store_instrument(
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST.lsdsng'),
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST_0x00_wave.lsdinst'),
        0x00)

def test_load_store_pulse_instrument():
    _test_load_store_instrument(
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST.lsdsng'),
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST_0x03_pulse.lsdinst'),
        0x03)

def test_load_store_kit_instrument():
    _test_load_store_instrument(
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST.lsdsng'),
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST_0x16_kit.lsdinst'),
        0x16)

def test_load_store_noise_instrument():
    _test_load_store_instrument(
        os.path.join(SCRIPT_DIR, 'test_data', 'ANNARKTE.lsdsng'),
        os.path.join(SCRIPT_DIR, 'test_data', 'ANNARKTE_0x06_noise.lsdinst'),
        0x06)
