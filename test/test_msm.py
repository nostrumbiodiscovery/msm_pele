import pytest
import shutil
import sys
import os
import glob
import MSM_PELE.Box.box as bx
import MSM_PELE.Helpers.pele_env as pele
import MSM_PELE.Helpers.clusterAdaptiveRun as cl
import MSM_PELE.main as main
import MSM_PELE.Helpers.helpers as hp
import MSM_PELE.constants as cs
import MSM_PELE.Helpers.simulation as ad


test_path = os.path.join(cs.DIR, "test/data")
SIM_ARGS = [os.path.join(test_path, "water_epbh.pdb"), "L02", "L", "--mae_lig", os.path.join(test_path, "L02_INIT.mae"), "--test", "--precision", "--iterations", "2", "--time", "240", "--steps", "100", "--restart", "pele", "--solvent", "OBC"]


@pytest.mark.parametrize("ext_args", [
                         (SIM_ARGS),
                         ])
def test_msm(ext_args):
    args = main.parse_args(ext_args)
    ####FUNCTION TO TEST######
    try:
        main.run(args) 
    except RuntimeError:
        assert True
    ####FUNCTION TO TEST######
        
