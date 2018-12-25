from __future__ import absolute_import, division, print_function, unicode_literals
import os
import socket
import MSM_PELE.constants as cs

machine = socket.getfqdn()
print("MACHINE", machine)
PELE_EXECUTABLE = os.path.abspath(cs.PELE_BIN)
DATA_FOLDER = os.path.join(cs.PELE, "Data")
DOCUMENTS_FOLDER = os.path.join(cs.PELE, "Documents")
try:
    PYTHON = cs.PYTHON
except AttributeError:
    pass
inputFileTemplate = "{ \"files\" : [ { \"path\" : \"%s\" } ] }"
trajectoryBasename = "*traj*"

class AmberTemplates:
    forcefields = {"ff99SB": "oldff/leaprc.ff99SB", "ff14SB": "leaprc.protein.ff14SB"}
    antechamberTemplate = "antechamber -i $LIGAND -fi pdb -o $OUTPUT -fo mol2 -c bcc -pf y -nc $CHARGE"
    parmchk2Template = "parmchk2 -i $MOL2 -f mol2 -o $OUTPUT"
    tleapTemplate = "source oldff/leaprc.ff99SB\n" \
                    "source leaprc.gaff\n" \
                    "source leaprc.water.tip3p\n" \
                    "$MODIFIED_RES " \
                    "$RESNAME = loadmol2 $MOL2\n" \
                    "loadamberparams $FRCMOD\n" \
                    "COMPLX = loadpdb $COMPLEX\n" \
                    "$BONDS "\
                    "addions COMPLX Cl- 0\n" \
                    "solvatebox COMPLX TIP3PBOX $BOXSIZE\n" \
                    "saveamberparm COMPLX $PRMTOP $INPCRD\n" \
                    "savepdb COMPLX $SOLVATED_PDB\n" \
                    "quit"
    trajectoryTemplate = "trajectory_%d.%s"
    CheckPointReporterTemplate = "checkpoint_%d.chk"


class OutputPathConstants():
    """
        Class with constants that depend on the outputPath
    """
    def __init__(self, outputPath):
        self.originalControlFile = ""
        self.epochOutputPathTempletized = ""
        self.clusteringOutputDir = ""
        self.clusteringOutputObject = ""
        self.equilibrationDir = ""
        self.tmpInitialStructuresTemplate = ""
        self.tmpControlFilename = ""
        self.tmpInitialStructuresEquilibrationTemplate = ""
        self.tmpControlFilenameEqulibration = ""
        self.topologies = ""
        self.allTrajsPath = ""
        self.MSMObjectEpoch = ""
        self.buildConstants(outputPath)

    def buildConstants(self, outputPath):
        self.buildOutputPathConstants(outputPath)

        self.tmpFolder = "tmp_" + outputPath.replace("/", "_")

        self.buildTmpFolderConstants(self.tmpFolder)

    def buildOutputPathConstants(self, outputPath):
        self.originalControlFile = os.path.join(outputPath, "originalControlFile.conf")
        self.epochOutputPathTempletized = os.path.join(outputPath, "%d")
        self.clusteringOutputDir = os.path.join(self.epochOutputPathTempletized, "clustering")
        self.clusteringOutputObject = os.path.join(self.clusteringOutputDir, "object.pkl")
        self.MSMObjectEpoch = os.path.join(self.epochOutputPathTempletized, "MSM_object.pkl")
        self.topologies = os.path.join(outputPath, "topologies")
        self.equilibrationDir = os.path.join(outputPath, "equilibration")
        self.allTrajsPath = os.path.join(outputPath, "allTrajs")

    def buildTmpFolderConstants(self, tmpFolder):
        self.tmpInitialStructuresTemplate = tmpFolder+"/initial_%d_%d.pdb"
        self.tmpInitialStructuresEquilibrationTemplate = tmpFolder+"/initial_equilibration_%d.pdb"
        self.tmpControlFilename = tmpFolder+"/controlFile%d.conf"
        self.tmpControlFilenameEqulibration = tmpFolder+"/controlFile_equilibration_%d.conf"

md_supported_formats = set(["xtc", "dcd"])
formats_md_string = ", ".join(md_supported_formats)
