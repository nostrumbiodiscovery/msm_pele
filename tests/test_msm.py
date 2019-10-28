import pytest
import shutil
import sys
import os
import glob
import shutil
import msm_pele.main as main
import msm_pele.constants as cs


test_path = "data"
SIM_ARGS = [os.path.join(test_path, "L02.pdb"), "L02", "L", "--mae_lig", os.path.join(test_path, "L02_INIT.mae"), "--test", "--precision", "--iterations", "2", "--time", "240", "--steps", "100", "--solvent", "OBC", "--water", "M:1", "--water_temp", "2000", "--water_constr", "0.5", "--water_radius", "7", "--water_trials", "500"]
BOX_VALUES = ["11.662  7.469  11.464", "RADIUS 9", "3.648  4.900  8.275", "-4.367  2.331  5.086", 
  "-12.381  -0.237  1.897", "-20.395  -2.806  -1.293", "-28.410  -5.375  -4.482"]
PELE_VALUES = ["iteration2", "output_pele/1", 
#check constraints
   '"springConstant": 50, "equilibriumDistance": 0.0, "constrainThisAtom": "A:2112:_OW_"',
   '"springConstant": 0.5, "equilibriumDistance": 0.0, "constrainThisAtom": "A:871:_CA_"',
   '"springConstant": 5, "equilibriumDistance": 0.0, "constrainThisAtom": "A:888:_CA_" }',
#check water
   '''         "WaterPerturbation":
         {
             "Box" :
             {
                 "radius" : 7.0,
                 "fixedCenter": [3.109,-4.211,4.469],
                 "type" : "sphericalBox"
             },
             "watersToPerturb": { "links": { "ids": [ "M:1" ] } },
             "parameters":
             {
                 "temperature": 2000,
                 "numberOfStericTrials": 500,
                 "COMConstraintConstant": 0.5
             }
         },''',
#check precission
   '''                  { "ifAnyIsTrue": [ "rand3 <= 0.04 and sasaLig > 0.4" ],

                        "doThesechanges": { "Perturbation::parameters": {"steeringUpdateFrequency": 0, "numberOfTrials": 10 } },

                        "otherwise": { }''',
#check solvent
  '"solventType" : "OBC"'
]
ADAPTIVE_VALUES = ['"metricColumnInReport" : 7']
RESULTS_VALUES = ['0 3.029 0.233 0.141 0.165 M']


@pytest.mark.parametrize("ext_args", [
                         (SIM_ARGS),
                         ])
def test_msm(ext_args):
    errors = []
    #Clen data
    folders = glob.glob("L02_Pele*")
    for folder in folders:
        shutil.rmtree(folder)
    args = main.parse_args(ext_args)
    ####FUNCTION TO TEST######
    try:
        main.run(args) 
    except RuntimeError:
        errors = check_for_errors(errors)
        assert not errors
    ####FUNCTION TO TEST######

    errors = check_for_errors(errors)
    assert not errors


def check_for_errors(errors):
    folder = glob.glob("L02_Pele*")[0]
    if not folder:
        errors.append("Input folder not created. Problem preprocessing the pdb")
    errors = check_folder_count(folder, "output_adaptive_exit/iteration*", 2, errors)
    errors = check_folder_count(folder, "output_clustering/iteration*", 2, errors)
    errors = check_folder_count(folder, "output_clustering/iteration1/*_KMeans_allSnapshots.pdb", 1, errors)
    errors = check_folder_count(folder, "output_clustering/iteration1/*exit_path*.pdb", 1, errors)
    errors = check_folder_count(folder, "output_pele/MSM_*", 2, errors)
    errors = check_folder_count(folder, "results/result*", 1, errors)
    errors = check_folder_count(folder, "L02.log", 1, errors)
    errors = check_folder_count(folder, "box.pdb", 1, errors)
    errors = check_folder_count(folder, "ligand.pdb", 1, errors)
    errors = check_folder_count(folder, "receptor.pdb", 1, errors)
    errors = check_folder_count(folder, "*processed.pdb", 1, errors)
    errors = check_folder_count(folder, "Data", 1, errors)
    errors = check_folder_count(folder, "Documents", 1, errors)
    errors = check_folder_count(folder, "DataLocal/LigandRotamerLibs/L02.rot.assign", 1, errors)
    errors = check_folder_count(folder, "DataLocal/Templates/OPLS2005/HeteroAtoms/l02z", 1, errors)
    errors = check_folder_count(folder, "pele.conf", 1, errors)
    errors = check_folder_count(folder, "adaptive_exit.conf", 1, errors)
    check_file(folder, "box.pdb", BOX_VALUES, errors)
    check_file(folder, "pele.conf", PELE_VALUES, errors)
    check_file(folder, "adaptive_exit.conf", ADAPTIVE_VALUES, errors)
    check_file(folder, "results/results.txt", RESULTS_VALUES, errors)
    return errors

    

def check_folder_count(folder, folder_name, n, errors):
    folder_or_file = os.path.join(folder, "{}".format(folder_name))
    objects = glob.glob(folder_or_file)
    if not len(objects) == n:
        errors.append("{} problem".format(folder_name))
    return errors

def check_file(folder, filename, values, errors):
   filename = os.path.join(folder, filename)
   with open(filename, "r") as f:
      for value in values:
          lines = f.readlines()
          if value in lines:
              errors.append(filename) 
   return errors
