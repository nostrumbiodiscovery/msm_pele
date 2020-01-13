import os
import re
import random
import msm_pele.Helpers.best_structs as bs


INPUT_LINE = '{{ "files" : [ {{ "path" : "{}" }} ] }},\n'


def silentremove(*args, **kwargs):
    for files in args:
        for filename in files:
            try:
                os.remove(filename)
            except OSError:
                pass


def is_exit_finish(path, test, criteria="7"):
    return bs.main(path, criteria=criteria, test=test)

def change_output(inp_file, out_folder, i, inputs):
    with open(inp_file, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # When Multicomplex is present all input lines
        if "MultipleComplex" in line:
            new_lines.append('"MultipleComplex": [\n')
            for i, input in enumerate(inputs):
                new_line =  input + ",\n" if i!=len(inputs)-1 else input + "],\n"
                new_lines.append(new_line)
        #Input lines from last iterations are removed
        elif '"files" : [ { "path"' in line:
            pass
        elif "reportPath" in line:
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


def find_coords(pdb, resnum, chain, atom="OW"):
    with open(pdb, "r") as f:
        for line in f:
            if line:
                if line.startswith("HETATM") and line[22:26].strip() == resnum and line[21:22] == chain:
                    return [float(coord) for coord in line[30:54].split()]


def find_centroid(points):
    x = [cx for cx, cy, cz in points]
    y = [cy for cx, cy, cz in points]
    z = [cz for cx, cy, cz in points]
    n_points = len(points)
    centroid = (sum(x) / n_points, sum(y) / n_points, sum(z) / n_points)
    return centroid

