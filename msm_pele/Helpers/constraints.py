import os
import sys
from string import Template
import argparse

AMINOACIDS = ["VAL", "ASN", "GLY", "LEU", "ILE",
              "SER", "ASP", "LYS", "MET", "GLN",
              "TRP", "ARG", "ALA", "THR", "PRO",
              "PHE", "GLU", "HIS", "HIP", "TYR",
              "CYS", "HID"]

IONS = ["CA", "MG", "ZN", "MN", "NA", "CL"]

TER_CONSTR = 5

HETATM_CONSTR = 50

BACK_CONSTR = 0.5

CONSTR_ATOM = '''{{ "type": "constrainAtomToPosition", "springConstant": {0}, "equilibriumDistance": 0.0, "constrainThisAtom": "{1}:{2}:{3}" }},'''

CONSTR_DIST = '''{{ "type": "constrainAtomsDistance", "springConstant": {}, "equilibriumDistance": {}, "constrainThisAtom": "{}:{}:{}", "toThisOtherAtom": "{}:{}:{}" }},'''

CONSTR_CALPHA = '''{{ "type": "constrainAtomToPosition", "springConstant": {2}, "equilibriumDistance": 0.0, "constrainThisAtom": "{0}:{1}:_CA_" }},'''


class ConstraintBuilder(object):

    def __init__(self, pdb, gaps, metals, dynamic_waters):
        self.pdb = pdb
        self.gaps = gaps
        self.metals = metals
        self.dynamic_waters = dynamic_waters

    def parse_atoms(self, interval=10):
        residues = []
        initial_res = None
        waters = []
        ions = []
        with open(self.pdb, "r") as pdb:
            for line in pdb:
                resname = line[16:21].strip()
                atomtype = line[11:16].strip()
                resnum = line[22:26].strip()
                chain = line[20:23].strip()
                if line.startswith("ATOM") and resname in AMINOACIDS and atomtype == "CA":
                    try:
                        if not initial_res:
                            initial = [chain, line[22:26].strip()]
                            initial_res = True
                            initial_resnum = line[22:26].strip()
                            continue
                        # Apply constraint every 10 residues
                        elif (int(resnum)-int(initial_resnum)) % interval == 0 and line.startswith("ATOM") and resname in AMINOACIDS and atomtype == "CA":
                            residues.append([resnum, chain])
                            terminal = [chain, line[22:26].strip()]
                    except ValueError:
                        continue
                elif line.startswith("HETATM") and resname == "HOH" and atomtype == "OW":
                    waters.append([atomtype, chain, resnum])
                elif line.startswith("HETATM") and resname in  IONS:
                    ions.append([atomtype, chain, resnum])
        return initial, residues, terminal, waters, ions

    def build_constraint(self, initial, residues, terminal, BACK_CONSTR=BACK_CONSTR, TER_CONSTR=TER_CONSTR, waters=[], constraint_water=HETATM_CONSTR, ions=[]):

        init_constr = ['''"constraints":[''', ]

        back_constr = [CONSTR_CALPHA.format(chain, resnum, BACK_CONSTR) for resnum, chain in residues if resnum.isdigit()]

        gaps_constr = self.gaps_constraints()

        metal_constr = self.metal_constraints()

        if waters:
            water_constr = self.create_constraints(waters, constraint_water)
        else:
            water_constr = []

       
        if ions:
            ions_constr = self.create_constraints(ions, constraint_water)
        else:
            ions_constr = []

        terminal_constr = [CONSTR_CALPHA.format(initial[0], initial[1], TER_CONSTR), CONSTR_CALPHA.format(terminal[0], terminal[1], TER_CONSTR).strip(",")]

        final_constr = ["],"]

        constraints = init_constr + back_constr + gaps_constr + metal_constr + ions_constr + water_constr + terminal_constr + final_constr

        return constraints

    def gaps_constraints(self):
        # self.gaps = {}
        gaps_constr = []
        for chain, residues in self.gaps.items():
            gaps_constr = [CONSTR_ATOM.format(TER_CONSTR, chain, terminal, "_CA_") for terminals in residues for terminal in terminals]
        return gaps_constr

    def metal_constraints(self):

        metal_constr = []
        for metal, ligands in self.metals.items():
            metal_name, chain, metnum = metal.split(" ")
            for ligand in ligands:
                ligand_info, bond_lenght = ligand
                resname, resnum, chain, ligname = ligand_info.split(" ")
                metal_constr.append(CONSTR_DIST.format(HETATM_CONSTR, bond_lenght, chain, resnum, ligname, chain, metnum, metal_name))
        return metal_constr

    def create_constraints(self, waters, constraint_water):
        water_constr = []
        for atom, chain, residue in waters:
            if "{}:{}".format(chain, residue) not in self.dynamic_waters:
                if atom == "OW":
                    water_constr.append(CONSTR_ATOM.format(constraint_water, chain, residue, "_"+atom+"_"))
                else:
                    water_constr.append(CONSTR_ATOM.format(constraint_water, chain, residue, atom+"__"))
        return water_constr


def retrieve_constraints(pdb_file, gaps, metal, back_constr=BACK_CONSTR, ter_constr=TER_CONSTR, interval=10,  dynamic_waters=[], constr_waters=HETATM_CONSTR):
    constr = ConstraintBuilder(pdb_file, gaps, metal, dynamic_waters)
    initial, residues, terminal, waters, ions = constr.parse_atoms(interval=interval)
    constraints = constr.build_constraint(initial, residues, terminal, back_constr, ter_constr, waters, constr_waters, ions)
    return constraints

class TemplateBuilder(object):

    def __init__(self, file, keywords):

        self.file = file
        self.keywords = keywords
        self.fill_in()

    def fill_in(self):
        """
        Fill the control file in
        """
        with open(os.path.join(self.file), 'r') as infile:
            confile_data = infile.read()

        confile_template = Template(confile_data)

        confile_text = confile_template.safe_substitute(self.keywords)

        with open(os.path.join(self.file), 'w') as outfile:
            outfile.write(confile_text)

def parseargs():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('pdb', type=str, help='pdb to create the contraints on')
    parser.add_argument('conf', help='Control file to fill in. It need to templetazide with $CONSTRAINTS')
    parser.add_argument('--interval', type=int, help="Every how many CA to constraint", default=10)
    parser.add_argument('--ca', type=float, help="Constraint value to use on backbone CA", default=BACK_CONSTR)
    parser.add_argument('--terminal', type=float, help="Constraint value to use on terminal CA", default=TER_CONSTR)
    parser.add_argument('--water', type=float, help="Constraint value to use on waters", default=HETATM_CONSTR)
    args = parser.parse_args()
    return os.path.abspath(args.pdb), os.path.abspath(args.conf), args.interval, args.conf, args.ca, args.terminal, args.water

if __name__ == "__main__":
    pdb, conf, interval, conf, back_constr, ter_constr, water = parseargs()
    constraints = retrieve_constraints(pdb, {}, {}, back_constr, ter_constr, interval, [], water)
    TemplateBuilder(conf, {"CONSTRAINTS": "\n".join(constraints)})
