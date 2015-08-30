import os
import tempfile

from nose.tools import assert_equal, raises

from .kits import Kits
from .utils import name_without_zeroes

def test_kit_used():
    test_rom = os.path.join(os.path.dirname(__file__), "test_data",
                            "lsdj_onlykits.gb")

    kits = Kits(test_rom)

    assert_equal(kits[4].samples[0].used, True)
    assert_equal(kits[4].samples[11].used, False)

def test_kit_reading():
    test_rom = os.path.join(os.path.dirname(__file__), "test_data",
                            "lsdj_onlykits.gb")

    kits = Kits(test_rom)

    # Expect LSDJ's built-in kits to be present

    expected_kit_names = [
        b'TR-606',
        b'TR-707',
        b'TR-727',
        b'TR-808',
        b'TR-909',
        b'CR-78 ',
        b'CR8000',
        b'DR-55 ',
        b'DR-110',
        b'DRUMUL',
        b'DMX   ',
        b'KR-55 ',
        b'LINNDR',
        b'RHYACE',
        b'TOM   ',
        b'ACIEED',
        b'GHETTO'
    ]

    for i, kit in enumerate(expected_kit_names):
        assert_equal(expected_kit_names[i], kits[i].name)

    # As a spot-check, test that the TR-707's samples are what we expect
    tr707_sample_names = [
        b'BD1', b'SD1', b'CHH', b'OHH', b'HT-', b'MT-', b'LT-', b'CCY', b'RCY',
        b'BD2', b'SD2', b'RIM', b'COW', b'TAM', b'CLP'
    ]

    for i, sample_name in enumerate(tr707_sample_names):
        assert_equal(sample_name, kits[1].samples[i].name)


def test_load_save_sample():
    test_rom = os.path.join(os.path.dirname(__file__), "test_data",
                            "lsdj_onlykits.gb")

    kits = Kits(test_rom)
    sample = kits[15].samples[3]

    temp_wav = tempfile.NamedTemporaryFile()

    sample.write_wav(temp_wav.name)

    read_sample = kits[15].samples[2]

    read_sample.read_wav(temp_wav.name)
    assert_equal(sample.sample_data, read_sample.sample_data)


@raises(Exception)
def test_load_save_too_large_sample():
    test_rom = os.path.join(os.path.dirname(__file__), "test_data",
                            "lsdj_onlykits.gb")

    kits = Kits(test_rom)
    sample = kits[15].samples[2]

    temp_wav = tempfile.NamedTemporaryFile()

    sample.write_wav(temp_wav)

    read_sample = kits[15].samples[3]

    read_sample.read_wav(temp_wav)

# Useful for diagnostic purposes, but not part of the regular test cycle
# def test_save_all_samples():
#     test_rom = os.path.join(os.path.dirname(__file__), "test_data",
#                             "lsdj_onlykits.gb")

#     for k, kit in enumerate(Kits(test_rom)):
#         for s, sample in enumerate(kit):
#             print(k, s, sample.index, sample.used)
#             sample.write_wav('/tmp/%s-%02d-%s.wav' % (
#                 name_without_zeroes(kit.name), sample.index, name_without_zeroes(sample.name)))

#     raise Exception('foo')
