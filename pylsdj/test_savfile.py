import os
import sys
from nose.tools import assert_equal, with_setup

from .project import load_lsdsng
from .utils import temporary_file

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.append(
    os.path.dirname(os.path.abspath(os.path.join(__file__, os.path.pardir))))

from . import savfile as savfile

SAV_IN = os.path.join(os.path.dirname(__file__), "test_data", "lsdj.sav")

def test_project_save_load():

    with temporary_file() as SAV_OUT:
        sav = savfile.SAVFile(SAV_IN)
        sav.save(SAV_OUT)

        new_sav = savfile.SAVFile(SAV_OUT)

        assert_equal(sav, new_sav)

def test_set_project():
    sample_song_compressed = os.path.join(
        SCRIPT_DIR, "test_data", "UNTOLDST.lsdsng")

    proj = load_lsdsng(sample_song_compressed)

    sav = savfile.SAVFile(SAV_IN)

    sav.projects[5] = proj
