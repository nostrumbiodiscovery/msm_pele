import os
import re
import MSM_PELE.Helpers.best_structs as bs


def silentremove(*args, **kwargs):
    for files in args:
        for filename in files:
            try:
                os.remove(filename)
            except OSError:
                pass


def is_exit_finish(path, test):
    return bs.main(path, test=test)

def change_output(inp_file, out_folder):
    with open(inp_file, "r") as f:
        lines = f.readlines()

    new_lines = [ '        "reportPath" : "{}",\n'.format(os.path.join(out_folder, "report"))  if "reportPath" in line else line for line in lines ]
    final_lines = [ '        "trajectoryPath" : "{}"\n'.format(os.path.join(out_folder, "trajectory.xtc"))  if "trajectoryPath" in line else line for line in new_lines ]

    with open(inp_file, "w") as f:
        f.write("".join(final_lines))

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def preproces_lines(lines):
    for i, line in enumerate(lines):
        line = re.sub(' +', ' ', line)
        line = line.strip('\n').strip().split()
        lines[i] = line
    return lines
