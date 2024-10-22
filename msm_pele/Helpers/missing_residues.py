import os
import shutil
import msm_pele.PlopRotTemp.launcher as plop
import msm_pele.Helpers.system_prep as sp
import msm_pele.Helpers.helpers as hp


def create_template(args, env):
    template_dir = os.path.join(env.pele_dir, "DataLocal/Templates/{}/HeteroAtoms/".format(env.forcefield))
    rotamers_dir = os.path.join(env.pele_dir, "DataLocal/LigandRotamerLibs")
    output_pdb = os.path.join(env.pele_dir, "miss_residue.pdb")
    syst = sp.SystemBuilder.build_system(env.system_fix, None, env.residue, env.pele_dir, output=output_pdb)
    plop.parametrize_miss_residues(args, env, syst)
