import os
import shutil

def remove_folders(test_path):
    if os.path.isdir(os.path.join(test_path, "L02_TEST/output_clustering")):
        shutil.rmtree(os.path.join(test_path, "L02_TEST/output_clustering"))
    if os.path.isdir(os.path.join(test_path, "L02_TEST/output_pele")):
        shutil.rmtree(os.path.join(test_path, "L02_TEST/output_pele"))
    if os.path.islink(os.path.join(test_path, "L02_TEST/Data")):
        os.unlink(os.path.join(test_path, "L02_TEST/Data"))
    if os.path.islink(os.path.join(test_path, "L02_TEST/Documents")):
        os.unlink(os.path.join(test_path, "L02_TEST/Documents"))
