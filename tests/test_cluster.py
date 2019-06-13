import pytest
import sys
import os
import shutil
import msm_pele.Box.box as bx
import msm_pele.Helpers.pele_env as pele
import msm_pele.Helpers.clusterAdaptiveRun as cl
import msm_pele.main as main
import msm_pele.Helpers.helpers as hp
import msm_pele.constants as cs
import msm_pele.test.test_helpers as thp

test_path = os.path.join(cs.DIR, "test/data")
CLUST_ARGS = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "1"]
@pytest.mark.parametrize("ext_args", [
                         (CLUST_ARGS),
                         ])
def test_kmeans(ext_args):

    thp.remove_folders(test_path)

    args = main.parse_args(ext_args)
    env = pele.EnviroBuilder.build_env(args) 
    ####FUNCTION TO TEST######
    with hp.cd(env.adap_ex_output):
        cluster_centers = cl.main(env.clusters, env.cluster_output, args.residue, "", env.cpus, env.topology, env.sasamin, env.sasamax, env.sasa, env.perc_sasa_min, env.perc_sasa_int)
    #########################

    assert True

