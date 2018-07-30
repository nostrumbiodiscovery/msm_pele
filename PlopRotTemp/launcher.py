import os
import MSM_PELE.constants as cs
import subprocess
import MSM_PELE.Helpers.helpers as hp

def parametrize_miss_residues(args, env, syst):
    SPYTHON = os.path.join(cs.SCHRODINGER, "utilities/python")
    file_path = os.path.abspath(os.path.join(cs.DIR, "PlopRotTemp/main.py"))
    print(file_path)
    options = retrieve_options(args, env)
    if args.mae_lig:
        mae_charges = True
        subprocess.call("{} {} {} {} {} {}".format(SPYTHON, file_path, options, args.mae_lig, args.residue, env.pele_dir).split())
        hp.silentremove([syst.system])
    else:
        mae_charges = False
        subprocess.call("{} {} {} {} {} {}".format(SPYTHON, file_path, options, syst.lig, args.residue, env.pele_dir).split())
        hp.silentremove([syst.lig])


def retrieve_options(args, env):
    """
    Retrieve PlopRotTemp options from input arguments
    """

    options = []
    if args.core != -1:
        options.extend(["--core {}".format(args.core)])
    if args.mtor != 4:
        options.extend(["--mtor {}".format(args.mtor)])
    if args.n != 1000:
        options.extend(["--n {}".format(args.n)])
    if args.forcefield != "OPLS2005":
        options.extend(["--force {}".format(args.forcefield)])
    if args.mae_lig:
        options.extend(["--mae_charges"])
    if args.gridres != 10:
        options.extend(["--gridres {}".format(args.gridres)])
    return " ".join(options)

