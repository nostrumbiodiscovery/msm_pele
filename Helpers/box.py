import os
import prody as pd
from scipy.spatial import distance
import shutil
import numpy as np
from string import Template
import argparse
import math
import MSM_PELE.Helpers.best_structs as best_structs
import MSM_PELE.Helpers.template_builder as tb
import MSM_PELE.Helpers.helpers as hp
import MSM_PELE.Helpers.center_of_mass as cm
import MSM_PELE.Helpers.plotMSMAdvancedInfo as pm
import MSM_PELE.constants as cs

__author__ = "Daniel Soler Viladrich"
__email__ = "daniel.soler@nostrumbiodiscovery.com"

# BOX CONSTANTS
KEYWORDS = ["MODEL", "RADIUS", "CENTER_X", "CENTER_Y", "CENTER_Z", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"]
COORD = "{:>11.3f}{:>8.3f}{:>8.3f}"
CENTER = "{:.3f}"


def parseargs():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('bs', type=int, nargs='+', help='an integer for the accumulator')
    parser.add_argument('--points', '-p', type=str, help='File where to find all coord')
    args = parser.parse_args()
    return args.bs, args.points


def create_box(cluster_centers, args, env):
    #Check exit simulation is properly finished
    BS_sasa_min, BS_sasa_max = is_exit_finish(env.adap_ex_output, args.test)
    #Retrieve info from file
    if args.box:
        center, radius = retrieve_box_info(args.box, env.clusters_output)
    #Retrieve info from user
    elif args.user_center and args.user_radius:
        center = [ args.user_center[i*3:i*3+3] for i in range(len(args.user_center)) ]
        radius = args.user_radius
        args.box_type = "multiple" if len(center) > 3 else "fixed" 
    #Create single box
    elif args.box_type == "fixed":
        center_mass = cm.center_of_mass(env.ligand_ref)
        center, radius = build_box(env.adap_ex_input, env.clusters_output, center_mass)
    #Create multiple box
    elif args.box_type == "multiple":
        center, radius = create_multiple_centers(cluster_centers, args,env)
    #Build box image
    initialize(env.box_temp)
    for i, (c,r) in enumerate(zip(center, radius), 1):
        box_to_pdb(c, r, env.box_temp, model=i)
    #Build box string for simulation
    box_string = string_builder(center, radius, args.box_type)
    #Ensure box connectivity
    points = get_points(env.clusters_output)
    remove_clusters_out_of_box(env.cluster_output, center, radius, points)
    return box_string, BS_sasa_min, BS_sasa_max


def build_box(system, clusters, bs):

    points = get_points(clusters)
    centroid = find_centroid(points)
    center = find_non_contact_points(system, centroid, bs) 
    radius = (distance.euclidean(bs, center) + 10) 
    return [center, ], [radius, ]

def remove_clusters_out_of_box(cluster_directory, centers, radiuses, points):
    """
    Remove clusters out of the exploration
    boxes. (They won't move on the simulation
    aggregating noise).
    """
    for i, point in enumerate(points):
        out_of_box = True
        for center, radius in zip(centers, radiuses):
            cx, cy, cz = center
            x,y,z = point
            if ((x-cx)**2 + (y-cy)**2 + (z-cz)**2) <= (radius**2):
                out_of_box = False
        if out_of_box:
            try:
                os.remove(os.path.join(cluster_directory, "initial_{}.pdb".format(i)))
            except OSError:
                pass


def find_non_contact_points(system, centroid, bs):
    """
        Find 0 contact point with protein
        in the direction produced by the 
        points of the binding side and the 
        centroide.
    """

    direction = np.array(centroid, dtype=float) - np.array(bs, dtype=float)
    directior_unitary = direction / np.linalg.norm(direction)
    atoms = pd.parsePDB(system)
    contacts = pd.measure.Contacts(atoms)

    point=np.array(bs, dtype=float)
    number_of_contacts = False
    while number_of_contacts > 0 or number_of_contacts is False:
        number_of_contacts = contacts. select(5, point)
        point = np.array(point, dtype=float) + directior_unitary
    return point.tolist()

def get_sasa_points(path, max_sasa_structs):
    points = []
    for _, info in max_sasa_structs.items():
        epoch, report, value, model = info
        coord_file = os.path.join(path, "{}/extractedCoordinates/coord_{}.dat".format(epoch, report))
        with open(coord_file, 'r') as f:
                lines = f.readlines()
        coord = [float(crd) for crd in lines[model].split()[1:]]
        points.append(coord)
    return points


def get_points(pdb):
    with open(pdb, 'r') as f:
        lines = [line.split() for line in f if line.startswith("HETATM")]
        points = [[float(line[6]), float(line[7]), float(line[8])] for line in lines]
        return points


def find_centroid(points):
    x, y, z = decompose(points)
    n_points = len(points)
    centroid = (sum(x) / n_points, sum(y) / n_points, sum(z) / n_points)
    return centroid


def decompose(points):
    crd_x = [x for x, y, z in points]
    crd_y = [y for x, y, z in points]
    crd_z = [z for x, y, z in points]
    return crd_x, crd_y, crd_z


def find_angle_lenght(bs, centroid, points):
    point_angle_lenght = []
    bs_centroid = [final - initial for initial, final in zip(bs, centroid)]
    point_centroid = []
    for point in points:
        point_centroid.append([final - initial for initial, final in zip(centroid, point)])
    for point, vector in zip(points, point_centroid):
        scalar = 0
        for initial, final in zip(vector, bs_centroid):
            scalar += initial * final
        magnitude_bs_cent = math.sqrt((bs_centroid[0])**2 + (bs_centroid[1])**2 + (bs_centroid[2])**2)
        magnitude_point_cent = math.sqrt((vector[0])**2 + (vector[1])**2 + (vector[2])**2)
        angle = math.acos(scalar / (magnitude_point_cent * magnitude_bs_cent))
        point_angle_lenght.append([point, angle, distance.euclidean(centroid, point)])
    return point_angle_lenght


def WireframeSphere(centre, radius, n_meridians=20, n_circles_latitude=None):
    """
    Create the arrays of values to plot the wireframe of a sphere.

    """
    if n_circles_latitude is None:
        n_circles_latitude = max(n_meridians / 2, 4)
    u, v = np.mgrid[0:2 * np.pi:n_meridians * 1j, 0:np.pi:n_circles_latitude * 1j]
    sphere_x = centre[0] + radius * np.cos(u) * np.sin(v)
    sphere_y = centre[1] + radius * np.sin(u) * np.sin(v)
    sphere_z = centre[2] + radius * np.cos(v)
    return sphere_x, sphere_y, sphere_z

def retrieve_box_info(box, clusters):
    with open(box, 'r') as f:
        lines = hp.preproces_lines(f.readlines()) 
        try:
            center = [[float(line[5]), float(line[6]), float(line[7])] for line in lines if "CENTER" in line]            
            radius = [ float(line[2]) for line in lines if "RADIUS" in line ]
        except ValueError:
            raise ValueError("{} not valid. Check the file is not a template.")
    print(center, radius)
    return center, radius

def box_to_pdb(center, radius, file, model=1):

    cx, cy, cz = center
    v1 = COORD.format(cx - radius, cy - radius, cz - radius)
    v2 = COORD.format(cx + radius, cy - radius, cz - radius)
    v3 = COORD.format(cx + radius, cy - radius, cz + radius)
    v4 = COORD.format(cx - radius, cy - radius, cz + radius)
    v5 = COORD.format(cx - radius, cy + radius, cz - radius)
    v6 = COORD.format(cx + radius, cy + radius, cz - radius)
    v7 = COORD.format(cx + radius, cy + radius, cz + radius)
    v8 = COORD.format(cx - radius, cy + radius, cz + radius)
    cx = CENTER.format(cx)
    cy = CENTER.format(cy)
    cz = CENTER.format(cz)

    values = [model, radius, cx, cy, cz, v1, v2, v3, v4, v5, v6, v7, v8]

    replace = {keyword: value for keyword, value in zip(KEYWORDS, values)}

    box_tmp = Template(cs.BOX)

    box = box_tmp.safe_substitute(replace)

    with open(file, "a") as f:
        f.write(box)


def initialize(file):
    with open(file, "w") as f:
        f.write("")


def create_multiple_centers(cluster_centers, args, env):
    #Calculate binding site point
    BS_location = get_binding_site_position(cluster_centers, args, env)
    #Calculate centroid
    centroid = find_centroid(cluster_centers)

    #Get center and radius along the exit path
    centers, radius = get_multiple_box_centers(BS_location, centroid)

    return centers, [radius]*len(centers)


def get_binding_site_position(cluster_centers, args, env):
    minpos = pm.get_min_Pos(env.system_fix, env.residue)
    distances = np.linalg.norm(cluster_centers-minpos, axis=1)
    min_distance = np.argmin(distances)
    BS_location = cluster_centers[min_distance]
    return BS_location


def get_multiple_box_centers(BS_location, centroid, radius=5):
    #Equation to get the radius of one sphere if we want
    #to fit n spheres in a segment of distance d 
    #radius=d/(2n-2)
    alpha = 0
    current_point = BS_location
    final_point = BS_location +  2*(centroid-BS_location)
    distance = np.linalg.norm(final_point-current_point)
    distance_centroid =  np.linalg.norm(final_point-centroid)
    number_spheres = int(distance/(2*radius)+1) if int(distance/(2*radius)+1)>1 else 2
    radius = distance/(2*number_spheres-2)
    chosen_clusters = []
    exit_func = lambda x : BS_location + x * (centroid-BS_location)/np.linalg.norm(centroid-BS_location)
    radius = radius if 100  > radius > 4 else 5
    #Check the distance to the centroid because we want to pass the centroid
    #and go two times that distance.
    while np.linalg.norm(centroid-current_point) <= 2*distance_centroid:
        current_point = exit_func(alpha)
        chosen_clusters.append(current_point)
        alpha += 2*radius
        print("Point {}".format(current_point))
        print("Next distance {}".format(np.linalg.norm(centroid-current_point)))
    return chosen_clusters, radius+3




def ensure_connectivity_clusters(spheres, radius):
    connected = False
    while not connected:
        connected = check_connectivity(spheres, radius) 
        radius += 1
    return radius

def check_connectivity(spheres, radius):
    overlap = []
    for sphere in spheres:
        for other_sphere in spheres:
            if not np.array_equal(sphere, other_sphere):
                overlap = is_overlap(sphere, other_sphere, radius, radius)
                if overlap:
                    return True
    

def is_overlap(center1, center2, radius1, radius2): 
    distance = np.linalg.norm(center2-center1)
    radius_sum = radius1 + radius2
    if (distance >= radius_sum): 
        return False
    else: 
        return True

def string_builder(centers, radiuses, type_box):
    string = []
    print(centers, radiuses)
    if type_box == "fixed":
        string.append('"type": "sphericalBox",\n')
    elif type_box == "multiple":
        string.append('"type": "multiSphericalBox",\n"listOfSpheres":[')
    for center, radius in zip(centers, radiuses):
        string.append('{{\n"radius": {},\n"fixedCenter":[{}]\n}},'.format(radius, ",".join([str(coord) for coord in center])))
    string[-1] = string[-1].strip(",")
    string.append(']')
    return "\n".join(string)

def is_exit_finish(path, test):
    return best_structs.main(path, test=test)
