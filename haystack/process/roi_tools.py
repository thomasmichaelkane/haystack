import os
import numpy as np
from rich.progress import track
from cellpose import io, utils

def save_from_seg(seg_data_list):
    
    # plot image with masks overlaid
    for seg_data in track(seg_data_list, description="Saving ROIs to text file..."):
    
        rois = utils.outlines_list_single(seg_data['masks'])
        roi_name = seg_data['filename'].replace('.tif', '')
        io.outlines_to_text(roi_name, rois)
    
def save_from_masks(masks_list, filenames):
    
    # plot image with masks overlaid
    for i, masks in track(enumerate(masks_list), description="Saving ROIs to text file..."):
    
        rois = utils.outlines_list_single(masks)
        roi_name = filenames[i].replace('.tif', '')
        io.outlines_to_text(roi_name, rois)

def import_from_text(roi_txt_path):
    """
    Read ROIs from a text file.

    Parameters:
    - text_file_path: Path to the text file containing ROI coordinates.

    Returns:
    - List of ROIs, where each ROI is a list of (x, y) coordinates.
    """
    rois = []

    with open(roi_txt_path, 'r') as file:
        for line in file:
            # Parse coordinates from the line
            entries = line.strip().split(',')
            roi_coordinates = [(int(entries[i]), int(entries[i+1])) for i in range(len(entries)) if i % 2 == 0]
        
            rois.append(roi_coordinates)

    return rois

def get_centres_of_mass(rois):
    
    centres_of_mass = []
    
    for roi in rois:
        x_coords, y_coords = zip(*roi)
        com = (int(np.mean(x_coords)), int(np.mean(y_coords)))

        centres_of_mass.append(com)
        
    return centres_of_mass

def import_and_stack(directory):
    
    rois_stack = []
    coms_stack = []
    
    text_files = [f for f in os.listdir(directory) if f.endswith('outlines.txt')]
    
    for text_file in text_files:
        
        path = os.path.join(directory, text_file)
        
        rois = import_from_text(path)
        rois_stack.append(rois)
        
        coms = get_centres_of_mass(rois)
        coms_stack.append(coms)
        
    return rois_stack, coms_stack

