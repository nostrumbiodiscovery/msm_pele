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
BOX_ARGS = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "1", "--box", os.path.join(test_path, "box_fixed.pdb")]
BOX_ARGS_1 = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "1", "--box", os.path.join(test_path, "box_multiple.pdb")]

BOX_FILE_RESULTS_CENTER = [[6.212,  13.757,  9.238],]
BOX_FILE_RESULTS_RADIUS = [9.52612422939, ]
BOX_FILE_RESULTS_CENTER_1 = [[7.917, 14.625, 8.740], [4.805, 22.695, 6.174]]
BOX_FILE_RESULTS_RADIUS_1 = [9.02238147652, 9.02238147652]

@pytest.mark.parametrize("ext_args, center, radius, boxtype", [
                         (BOX_ARGS, BOX_FILE_RESULTS_CENTER, BOX_FILE_RESULTS_RADIUS, "fixed"),
                         (BOX_ARGS_1, BOX_FILE_RESULTS_CENTER_1, BOX_FILE_RESULTS_RADIUS_1, "multiple"),
                         ])
def test_from_file(ext_args, center, radius, boxtype):

    thp.remove_folders(test_path)

    args = main.parse_args(ext_args)
    env = pele.EnviroBuilder.build_env(args) 
    ####FUNCTION TO TEST######
    with hp.cd(env.adap_ex_output):
        cluster_centers = cl.main(env.clusters, env.cluster_output, args.residue, "", env.cpus, env.topology, env.sasamin, env.sasamax, env.sasa, env.perc_sasa_min, env.perc_sasa_int)
    box, BS_sasa_min, BS_sasa_max = bx.create_box(cluster_centers, env) 
    #########################
    box = bx.BoxBuilder()

    thp.remove_folders(test_path)

    assert box.from_file(os.path.join(test_path, "L02_TEST/box.pdb")) == (center, radius, boxtype)
    
BOX_ARGS = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "1", "--user_center", "22", "22", "22", "--user_radius", "9"]
BOX_ARGS_1 = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "1", "--user_center", "22", "22", "22", "11", "11", "11", "--user_radius", "9", "5"]

BOX_FILE_RESULTS_CENTER = [[22, 22, 22],]
BOX_FILE_RESULTS_RADIUS = [9, ]
BOX_FILE_RESULTS_CENTER_1 = [[22, 22, 22], [11, 11, 11]]
BOX_FILE_RESULTS_RADIUS_1 = [9, 5]

@pytest.mark.parametrize("ext_args, center, radius, boxtype", [
                         (BOX_ARGS, BOX_FILE_RESULTS_CENTER, BOX_FILE_RESULTS_RADIUS, "fixed"),
                         (BOX_ARGS_1, BOX_FILE_RESULTS_CENTER_1, BOX_FILE_RESULTS_RADIUS_1, "multiple"),
                         ])
def test_from_list(ext_args, center, radius, boxtype):

    thp.remove_folders(test_path)

    args = main.parse_args(ext_args)
    env = pele.EnviroBuilder.build_env(args)
    ####FUNCTION TO TEST######
    with hp.cd(env.adap_ex_output):
        cluster_centers = cl.main(env.clusters, env.cluster_output, args.residue, "", env.cpus, env.topology, env.sasamin, env.sasamax, env.sasa, env.perc_sasa_min, env.perc_sasa_int)
    box, BS_sasa_min, BS_sasa_max = bx.create_box(cluster_centers, env)
    #########################
    box = bx.BoxBuilder()

    thp.remove_folders(test_path)

    assert box.from_file(os.path.join(test_path, "L02_TEST/box.pdb")) == (center, radius, boxtype)

BOX_ARGS = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "1",  "--box_type", "fixed"]
BOX_ARGS_1 = ["water_epbh.pdb", "L02", "L", "--mae_lig", "L02_INIT.mae",  "-wf", os.path.join(test_path, "L02_TEST"), "--restart", "pele", "--cpus", "1"]

BOX_FILE_RESULTS_CENTER = [[7.118, 17.952, 6.687],]
BOX_FILE_RESULTS_RADIUS = [22.999999999999996, ]
BOX_FILE_RESULTS_CENTER_1 = [[8.028, 14.518, 8.921], [4.989, 22.571, 6.329], [1.949, 30.623, 3.738], [-1.09, 38.676, 1.146]]
BOX_FILE_RESULTS_RADIUS_1 = [8.988649116745881, 8.988649116745881, 8.988649116745881, 8.988649116745881]

@pytest.mark.parametrize("ext_args, center, radius, boxtype", [
                         (BOX_ARGS, BOX_FILE_RESULTS_CENTER, BOX_FILE_RESULTS_RADIUS, "fixed"),
                         (BOX_ARGS_1, BOX_FILE_RESULTS_CENTER_1, BOX_FILE_RESULTS_RADIUS_1, "multiple"),
                         ])
def test_from_cluster(ext_args, center, radius, boxtype):

    thp.remove_folders(test_path)

    args = main.parse_args(ext_args)
    env = pele.EnviroBuilder.build_env(args)
    ####FUNCTION TO TEST######
    with hp.cd(env.adap_ex_output):
        cluster_centers = cl.main(env.clusters, env.cluster_output, args.residue, "", env.cpus, env.topology, env.sasamin, env.sasamax, env.sasa, env.perc_sasa_min, env.perc_sasa_int)
    box, BS_sasa_min, BS_sasa_max = bx.create_box(cluster_centers, env)
    #########################
    box = bx.BoxBuilder()

    thp.remove_folders(test_path)

    assert box.from_file(os.path.join(test_path, "L02_TEST/box.pdb")) == (center, radius, boxtype)
