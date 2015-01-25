import os
from nose.tools import assert_equal

from .project import load_lsdsng

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


def test_read_clocks():
    proj = load_lsdsng(
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST.lsdsng'))

    project_clock = proj.song.clock
    total_clock = proj.song.global_clock

    print(project_clock)
    print(total_clock)
    print((total_clock.checksum))

    assert_equal(5, project_clock.hours)
    assert_equal(47, project_clock.minutes)

    assert_equal(57, total_clock.days)
    assert_equal(1, total_clock.hours)
    assert_equal(11, total_clock.minutes)


def test_set_local_clock():
    proj = load_lsdsng(
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST.lsdsng'))

    project_clock = proj.song.clock

    project_clock.hours = 2
    project_clock.minutes = 22

    assert_equal(2, proj.song.clock.hours)
    assert_equal(22, proj.song.clock.minutes)


def test_set_global_clock():
    proj = load_lsdsng(
        os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST.lsdsng'))

    proj.song.global_clock.days = 5
    proj.song.global_clock.hours = 14
    proj.song.global_clock.minutes = 20

    assert_equal(5, proj.song.global_clock.days)
    assert_equal(14, proj.song.global_clock.hours)
    assert_equal(20, proj.song.global_clock.minutes)

    assert_equal(39, proj.song.global_clock.checksum)
