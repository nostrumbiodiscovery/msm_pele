import os
import re
import random
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

    new_lines = []
    for line in lines:
        if "reportPath" in line:
            new_lines.append('        "reportPath" : "{}",\n'.format(os.path.join(out_folder, "report")))
        elif "trajectoryPath" in line:
            new_lines.append('        "trajectoryPath" : "{}"\n'.format(os.path.join(out_folder, "trajectory.xtc")))
        elif "seed" in line:
            new_lines.append('        "RandomGenerator" : {{ "seed" : {} }},\n'.format(random.randint(1,10000)))
        else:
            new_lines.append(line)

    with open(inp_file, "w") as fout:
        fout.write("".join(new_lines))

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
