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
import MSM_PELE.test.test_helpers as thp



test_path = os.path.join(cs.DIR, "test/data")
SASA_ARGS = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "4", "--sasa", "0.5", "0.7", "--perc_sasa", "1", "0", "0", "--clust", "3", "--box_type", "fixed"]
SASA_ARGS_1 = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "4", "--sasa", "0.5", "0.7", "--perc_sasa", "0", "1", "0", "--clust", "3", "--box_type", "fixed"]
SASA_ARGS_2 = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "4", "--sasa", "0.5", "0.7", "--perc_sasa", "0", "0", "1", "--clust", "3", "--box_type", "fixed"]


@pytest.mark.parametrize("ext_args, sasa_min, sasa_int, test_type" , [
                         (SASA_ARGS, 0.5, 0.7, "lower_bound"),
                         (SASA_ARGS_1, 0.5, 0.7, "intermidiate_bound"),
                         (SASA_ARGS_2, 0.5, 0.7, "higher_bound"),
                         ])
def test_sasa_clustering(ext_args, sasa_min, sasa_int, test_type):

    thp.remove_folders(test_path)

    args = main.parse_args(ext_args)
    env = pele.EnviroBuilder.build_env(args) 

    ####FUNCTION TO TEST######
    with hp.cd(env.adap_ex_output):
        cluster_centers = cl.main(env.clusters, env.cluster_output, args.residue, "", env.cpus, env.topology, env.sasamin, env.sasamax, env.sasa, env.perc_sasa_min, env.perc_sasa_int)
    ####FUNCTION TO TEST######

    box, BS_sasa_min, BS_sasa_max = bx.create_box(cluster_centers, env) 
    ad.SimulationBuilder(env.pele_temp,  env.topology, cs.PELE_KEYWORDS, box, BS_sasa_min, BS_sasa_max)
    adaptive_long = ad.SimulationBuilder(env.ad_l_temp,  env.topology, cs.ADAPTIVE_KEYWORDS,
        cs.RESTART, env.adap_l_output, env.adap_l_input, args.cpus, env.pele_temp, args.residue, env.random_num, env.steps)
    adaptive_long.run_pele(env, limitTime=args.time)
    files = glob.glob(os.path.join(test_path, "L02_TEST/output_pele/0/report_*"))
    
    test_correct = True
    for file in files:
        with open(file, "r") as f:
            lines = f.readlines()
        sasa = float(lines[1].strip().split()[-1])
        if test_type == "lower_bound" and sasa > sasa_min:
            print("A")
            test_correct = False
        elif test_type == "intermidiate_bound" and (sasa < sasa_min or sasa > sasa_int):
            print("B")
            test_correct = False
        elif test_type == "higher_bound" and sasa < sasa_int:
            print("C")
            test_correct = False

    thp.remove_folders(test_path)

    assert test_correct

       
