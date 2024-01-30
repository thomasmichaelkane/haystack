import os
import numpy as np
from sklearn.cluster import DBSCAN

def get_clusters(coordinates_stack, min_samples, max_clustering_distance):
    
    coordinates = [coord for stack in coordinates_stack for coord in stack]

    # Convert coordinates to a NumPy array
    data = np.array(coordinates)

    # Adjust the eps parameter based on your data
    dbscan = DBSCAN(eps=max_clustering_distance, min_samples=min_samples)  # Increase or decrease eps as needed
    labels = dbscan.fit_predict(data)

    # Get unique labels (including noise labeled as -1)
    unique_labels = np.unique(labels)

    # Create a list of tuples with the reduced coordinates and counts
    reduced_coordinates = []
    for label in unique_labels:
        if label == -1:
            continue  # Skip noise points
        cluster_points = data[labels == label]
        centroid = np.mean(cluster_points, axis=0)
        count = len(cluster_points)
        
        reduced_coordinates.append((int(round(centroid[0])), int(round(centroid[1])), count))
        
    return reduced_coordinates

def save(coords, directory, min_samples, max_clustering_distance, count=False):
    
    if count is False:
        coords = [(str(coord[0]), str(coord[1])) for coord in coords]
    else:
        coords = [(str(coord[0]), str(coord[1]), str(coords[2])) for coord in coords]
    
    name = "cells_from_clusters_min-samp-" + str(min_samples) + "_max-dist-" + str(max_clustering_distance) + ".txt" 
    
    path = os.path.join(directory, name)
    
    with open(path, 'w') as file:
        for coord in coords:
            for point in coord:
                file.write(point)
                file.write('\t')
            file.write('\n')
            
