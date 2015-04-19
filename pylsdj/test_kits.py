import os

from nose.tools import assert_equal

from .kits import Kits

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
