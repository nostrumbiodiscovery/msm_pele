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


class OutputPathConstants():
    """
        Class with constants that depend on the outputPath
    """
    def __init__(self, outputPath):
        self.originalControlFile = ""
        self.epochOutputPathTempletized = ""
        self.clusteringOutputDir = ""
        self.clusteringOutputObject = ""
        self.tmpInitialStructuresTemplate = ""
        self.tmpControlFilename = ""
        self.tmpInitialStructuresEquilibrationTemplate = ""
        self.tmpControlFilenameEqulibration = ""
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
        self.topologyFile = os.path.join(outputPath, "topology.pdb")

    def buildTmpFolderConstants(self, tmpFolder):
        self.tmpInitialStructuresTemplate = tmpFolder+"/initial_%d_%d.pdb"
        self.tmpInitialStructuresEquilibrationTemplate = tmpFolder+"/initial_equilibration_%d.pdb"
        self.tmpControlFilename = tmpFolder+"/controlFile%d.conf"
        self.tmpControlFilenameEqulibration = tmpFolder+"/controlFile_equilibration_%d.conf"
