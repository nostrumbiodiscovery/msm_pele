from itertools import islice
import sys
import os
import glob
import numpy as np
import argparse
from MSM_PELE.AdaptivePELE.utilities import utilities
from MSM_PELE.AdaptivePELE.freeEnergies import cluster, extractCoords
from MSM_PELE.AdaptivePELE.analysis import splitTrajectory
import MSM_PELE.constants as cs
import pandas as pd

def parseArgs():
    parser = argparse.ArgumentParser(description="Script that reclusters the Adaptive clusters")
    parser.add_argument('nClusters', type=int)
    parser.add_argument("ligand_resname", type=str, help="Name of the ligand in the PDB")
    parser.add_argument("-atomId", nargs="*", default="", help="Atoms to use for the coordinates of the conformation, if not specified use the center of mass")
    parser.add_argument('-o', type=str, help="Output folder", default="None")
    args = parser.parse_args()
    return args.nClusters, args.ligand_resname, args.atomId, args.o


def writePDB(pmf_xyzg, title="clusters.pdb"):
    templateLine = "HETATM%s  H%sCLT L 502    %s%s%s  0.75%s           H\n"

    content = ""
    for j, line in enumerate(pmf_xyzg):
        number = str(j).rjust(5)
        number3 = str(j).ljust(3)
        x = ("%.3f" % line[0]).rjust(8)
        y = ("%.3f" % line[1]).rjust(8)
        z = ("%.3f" % line[2]).rjust(8)
        g = 0
        content += templateLine % (number, number3, x, y, z, g)

    with open(title, 'w') as f:
        f.write(content)


def writeInitialStructures(centers_info, filename_template, topology=None):
    for i, cluster_num in enumerate(centers_info):
        epoch_num, traj_num, snap_num = map(int, centers_info[cluster_num]['structure'])
        trajectory = "%d/trajectory_%d.xtc" % (epoch_num, traj_num) if topology else "%d/trajectory_%d.pdb" % (epoch_num, traj_num)
        snapshots = utilities.getSnapshots(trajectory, topology=topology)
        if not topology:
            with open(filename_template % i, "w") as fw:
                fw.write(snapshots[snap_num])
        else:
            splitTrajectory.main("", [trajectory, ], topology, [snap_num+1,],template=filename_template % cluster_num)

def split_by_sasa(centers_info, topology=None):
    sasas = {}
    for cluster_num in centers_info:
        epoch_num, traj_num, snap_num = map(int, centers_info[cluster_num]['structure'])
        sasa = get_sasa(epoch_num, traj_num, snap_num)
        sasas[cluster_num] = sasa
    sasa_max, sasa_int, sasa_min = sasa_classifier(sasas)
    print("Sasa magnitude has been classified in the next clusters: Min: {}, Int: {}, Max: {}".format(sasa_max, sasa_int, sasa_min))
    clusters = update_cluster(centers_info, sasa_max, sasa_int, sasa_min)
    return {i: value for i, (key, value) in enumerate(clusters.iteritems())}

def get_sasa(epoch_num, traj_num, snap_num):
    report = os.path.join(str(epoch_num), "report_{}".format(traj_num))
    report_data = pd.read_csv(report, sep='    ', engine='python')
    return report_data[cs.CRITERIA].values.tolist()[snap_num]

def sasa_classifier(sasas):
    sasas_max = {}
    sasas_int = {}
    sasas_min = {}

    sasa_values = [ value for key, value in sasas.iteritems() ]
    sasa_max = max(sasa_values)
    sasa_min = min(sasa_values)
    sasa_threshold_min = (sasa_max - sasa_min) * 0.3 + sasa_min
    sasa_threshold_max = (sasa_max - sasa_min) * 0.6 + sasa_min
    for cluster_num, sasa in sasas.iteritems():
        if sasa > sasa_threshold_max:
            sasas_max[cluster_num] = sasa
        elif sasa_threshold_max > sasa > sasa_threshold_min:
            sasas_int[cluster_num] = sasa
        elif sasa < sasa_threshold_min:
            sasas_min[cluster_num] = sasa
    return sasas_max, sasas_int, sasas_min 
    
def update_cluster(centers_info, sasa_max,sasa_int, sasa_min):
    total_of_clusters = len(centers_info) / 2
    extra_clust = len(centers_info)
    number_sasa_min_clust = round(total_of_clusters * 0.60)
    number_sasa_int_clust = round(total_of_clusters * 0.30)
    number_sasa_max_clust = total_of_clusters - number_sasa_min_clust - number_sasa_int_clust

    chosen_clusters = {}
    sasa_max = take(number_sasa_max_clust, sasa_max.iteritems())
    sasa_int = take(number_sasa_int_clust, sasa_int.iteritems())
    sasa_min = take(number_sasa_min_clust, sasa_min.iteritems())

    chosen_clusters.update(sasa_max)
    if len(chosen_clusters) != number_sasa_max_clust:
        chosen_clusters, centers_info, extra_clust = repite_clusters(centers_info, chosen_clusters, sasa_min, number_sasa_max_clust-len(chosen_clusters), extra_clust)

    chosen_clusters.update(sasa_int)
    if len(chosen_clusters) != (number_sasa_max_clust+number_sasa_int_clust):
        chosen_clusters, centers_info, extra_clust = repite_clusters(centers_info, chosen_clusters, sasa_min, (number_sasa_max_clust+number_sasa_int_clust)-len(chosen_clusters), extra_clust)

    chosen_clusters.update(sasa_min)
    if len(chosen_clusters) != (total_of_clusters):
        chosen_clusters, centers_info, extra_clust = repite_clusters(centers_info, chosen_clusters, sasa_min, total_of_clusters-len(chosen_clusters), extra_clust)

    for cluster_num in centers_info.copy():
        for chosen_cluster_number in chosen_clusters.iteritems():
            if cluster_num not in list(chosen_clusters.keys()):
                centers_info.pop(cluster_num, None)
    return centers_info

def repite_clusters(centers_info, chosen_clusters, sasa_min, limit_clusters, extra_clust):
    for i in range(limit_clusters):
        chosen_clusters[extra_clust] = sorted(sasa_min, key=lambda x: x[1])[i][1]
        centers_info[extra_clust] = centers_info[sorted(sasa_min, key=lambda x: x[1])[i][0]]
        extra_clust +=1
    return chosen_clusters, centers_info, extra_clust

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def get_centers_info(trajectoryFolder, trajectoryBasename, num_clusters, clusterCenters):
    centersInfo = {x: {"structure": None, "minDist": 1e6, "center": None} for x in xrange(num_clusters)}

    trajFiles = glob.glob(os.path.join(trajectoryFolder, trajectoryBasename))
    for traj in trajFiles:
        _, epoch, iTraj = os.path.splitext(traj)[0].split("_", 3)
        trajCoords = np.loadtxt(traj)
        if len(trajCoords.shape) < 2:
            trajCoords = [trajCoords]
        for snapshot in trajCoords:
            nSnap = snapshot[0]
            snapshotCoords = snapshot[1:]
            dist = np.sqrt(np.sum((clusterCenters-snapshotCoords)**2, axis=1))
            for clusterInd in xrange(num_clusters):
                if dist[clusterInd] < centersInfo[clusterInd]['minDist']:
                    centersInfo[clusterInd]['minDist'] = dist[clusterInd]
                    centersInfo[clusterInd]['structure'] = (epoch, int(iTraj), nSnap)
                    centersInfo[clusterInd]['center'] = snapshotCoords
    return centersInfo


def main(num_clusters, output_folder, ligand_resname, atom_ids, cpus, topology=None):
    #extractCoords.main(lig_resname=ligand_resname, non_Repeat=True, atom_Ids=atom_ids, nProcessors=cpus, parallelize=False, topology=topology)
    trajectoryFolder = "allTrajs"
    trajectoryBasename = "traj*"
    stride = 1
    clusterCountsThreshold = 0
    folders = utilities.get_epoch_folders(".")
    folders.sort(key=int)
    original_clust = num_clusters
    num_clusters *= 2
    clusteringObject = cluster.Cluster(num_clusters, trajectoryFolder,
                                       trajectoryBasename, alwaysCluster=False,
                                       stride=stride)
    clusteringObject.clusterTrajectories()
    clusteringObject.eliminateLowPopulatedClusters(clusterCountsThreshold)
    clusterCenters = clusteringObject.clusterCenters
    centersInfo = get_centers_info(trajectoryFolder, trajectoryBasename, num_clusters, clusterCenters)
    centersInfo = split_by_sasa(centersInfo,  topology=topology)
    COMArray = [centersInfo[i]['center'] for i in centersInfo]
    if output_folder is not None:
        outputFolder = os.path.join(output_folder, "")
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
    else:
        outputFolder = ""
    writePDB(COMArray, outputFolder+"clusters_%d_KMeans_allSnapshots.pdb" % original_clust)
    writeInitialStructures(centersInfo, outputFolder+"initial_%d.pdb", topology=topology)

if __name__ == "__main__":
    n_clusters, lig_name, atom_id, output = parseArgs()
    main(n_clusters, output, lig_name, atom_id)
