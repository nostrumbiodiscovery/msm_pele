import pytest
import sys
import os
import shutil
import MSM_PELE.Box.box as bx
import MSM_PELE.Helpers.pele_env as pele
import MSM_PELE.Helpers.clusterAdaptiveRun as cl
import MSM_PELE.main as main
import MSM_PELE.Helpers.helpers as hp
import MSM_PELE.constants as cs
import MSM_PELE.test.test_helpers as thp

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

