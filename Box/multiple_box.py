import numpy as np
import MSM_PELE.Box.box_helpers as mbp


def build_box(cluster_centers, env):

    # Calculate binding site point
    BS_location = mbp.get_binding_site_position(cluster_centers, env)

    # Calculate centroid
    centroid = mbp.find_centroid(cluster_centers)

    # Get center and radius along the exit path
    center, radius = get_centers(BS_location, centroid)

    return center, radius, "multiple"

def get_centers(BS_location, centroid, radius=5):
    # Equation to get the radius of one sphere if we want
    # to fit n spheres in a segment of distance d
    # radius=d/(2n-2)
    current_point = BS_location
    final_point = BS_location + 2*(centroid-BS_location)
    distance = np.linalg.norm(final_point-current_point)
    distance_centroid = np.linalg.norm(final_point-centroid)
    number_spheres = int(distance/(2*radius)+1) if int(distance/(2*radius)+1) > 1 else 2
    radius = distance/(2*number_spheres-2)
    exit_func = lambda x: BS_location + x * (centroid-BS_location)/np.linalg.norm(centroid-BS_location)
    radius = radius if 100 > radius > 4 else 5
    alpha = radius
    centers = []
    # Check the distance to the centroid because we want to pass the centroid
    # and go two times that distance.
    while np.linalg.norm(centroid-current_point) <= 2*distance_centroid:
        current_point = exit_func(alpha)
        centers.append(current_point)
        alpha += radius
        print("Point {}".format(current_point))
        print("Next distance {}".format(np.linalg.norm(centroid-current_point)))
    radius = [radius]*len(centers)
    return centers, radius
