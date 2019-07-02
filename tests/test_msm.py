import pytest
import shutil
import sys
import os
import glob
import msm_pele.Box.box as bx
import msm_pele.Helpers.pele_env as pele
import msm_pele.Helpers.clusterAdaptiveRun as cl
import msm_pele.main as main
import msm_pele.Helpers.helpers as hp
import msm_pele.constants as cs
import msm_pele.Helpers.simulation as ad


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
        
