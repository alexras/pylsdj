import os
from nose.tools import assert_false, assert_true

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

from .project import load_lsdsng

def test_wave_synth_overwrite_locks():
    test_project = os.path.join(SCRIPT_DIR, 'test_data', 'UNTOLDST.lsdsng')

    project = load_lsdsng(test_project)
    project.song.synths[4].phase_type = 'resync2'
    assert_false(project.song.wave_synth_overwrite_locks[0xf - 4],
                 "Expected wave synth overwrite lock to be disabled "
                 "after modifying synth parameters")
    assert_false(project.song.synths[4].wave_synth_overwrite_lock)

    project.song.synths[4].waves[5][3] = 0xd
    assert_true(project.song.wave_synth_overwrite_locks[0xf - 4],
                "Expected wave synth overwrite lock to be enabled "
                "after modifying wave frames")
    assert_true(project.song.synths[4].wave_synth_overwrite_lock)
