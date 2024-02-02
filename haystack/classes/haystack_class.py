import os
import numpy as np
from cellpose import models, io

from haystack.process import display, roi_tools, image_tools, clustering
from haystack.utils import parse, logging
from haystack.utils.util_functions import *

class Haystack():
    
    def __init__(self, path):
        
        self.path = path
        self.roi_path = self.path
        
        self.parent_directory = os.path.dirname(self.path)
        self.output_directory = create_directory(self.parent_directory, "haystack", timestamp=True)
        
        if parse.tiff(self.path):
            self.load_from_stack()
            self.is_stack = True
        elif parse.dir(self.path):
            self.load_from_dir()
            self.is_stack = False
        else:
            raise FileNotFoundError
        
        self.background = image_tools.create_background(self.shape)
        self.middle_frame = image_tools.convert_to_color(self.images[int(round(self.length/2))])
        
        self.has_raw_images = False
        self.cells_detected = False
        self.cells_clustered = False
        self.colormap = "jet"
    
    def choose_colormap(self, cm):
        
        self.colormap = cm
        
    def load_from_stack(self):
        
        self.raw = io.imread(self.path)
        self.images = [image for image in self.raw]
        
        self.shape = self.images[0].shape
        self.length = len(self.images)
        
        self.has_raw_images = True
        
        logging.update('Loaded {} images from tiff stack'.format(self.length))
    
    def load_from_dir(self):
        
        self.files = io.get_image_files(self.path, '_masks')
        self.images = [io.imread(file) for file in self.files]
        self.raw = np.array(self.images)
        
        self.shape = self.images[0].shape
        self.length = len(self.images)
        
        self.has_raw_images = True
        
        logging.update('Loaded {} images from directory'.format(self.length))
    
    def load_rois_directly(self, roi_path=None):
        
        if roi_path is None and self.is_stack is True:
            raise Exception("No path for ROIS was specified. A path to ROIS must be suppplied to this function, as this instance was built from a tiff stack, not a directory.")
        
        elif roi_path is not None: 
            self.roi_path = roi_path
        
        self.analyse_rois()
        
        logging.update('Loaded {} rois directly'.format(self.length))
             
    def write_images_dir(self):
        
        tiff_name = os.path.splitext(os.path.basename(self.path))[0]
        
        self.path = self.roi_path = create_directory(self.parent_directory, tiff_name)
        
        for i, image in enumerate(self.images):
            
            img_name = tiff_name + "_" + str(i).zfill(3) + ".tif"
            save_image(image, self.path, img_name)
        
        self.files = io.get_image_files(self.path, '_masks')
        
        logging.update('Writing images to a directory for cellpose')
    
    def detect_cells(self, model_path, cellprob_threshold, channels):
        
        if self.is_stack:
            self.write_images_dir()
            
        logging.update('Starting cellpose detection...')
        
        self.model = models.CellposeModel(pretrained_model=model_path)
        
        # Run Cellpose
        self.masks, self.flows, _ = self.model.eval(self.images,
                                                    channels=channels,
                                                    cellprob_threshold=cellprob_threshold)
    
        io.masks_flows_to_seg(self.images,
                              self.masks,
                              self.flows,
                              self.model.diam_labels*np.ones(len(self.masks)),
                              self.files,
                              channels)
    
        # if create_roi_txts: 
        roi_tools.save_from_masks(self.masks, self.files)
        
        self.analyse_rois()
        
        logging.update('Cellpose detection complete')
         
    def analyse_rois(self):
        
        _, self.coms_stack = roi_tools.import_and_stack(self.roi_path)
        
        self.cells_detected = True
        self.cells_clustered = False
    
        self.cell_detection_stack = image_tools.make_detections_stack(self.coms_stack, self.background.copy(), colormap=self.colormap)
        self.cell_detection_stack_on_frames = image_tools.make_detections_stack(self.coms_stack, self.raw, sequence=True, point_size=4, colormap=self.colormap)
        self.cumulative_detection_stack = image_tools.make_detections_stack(self.coms_stack, self.background.copy(), cumulative=True, colormap=self.colormap)
    
    def cluster_cells(self, min_samples, max_clustering_distance):
        
        self.min_samples = min_samples
        self.max_clustering_distance = max_clustering_distance
        
        if self.cells_detected:
        
            self.cells_from_clustering = clustering.get_clusters(self.coms_stack, min_samples, max_clustering_distance)
            self.clustering_image = image_tools.add_points(self.cells_from_clustering, self.cumulative_detection_stack[-1].copy(), radius=8, fill=False)
            self.clustered_cells_image = image_tools.add_points(self.cells_from_clustering, self.background.copy())
    
        self.cells_clustered = True
        
        logging.update('Clustering complete')
        logging.line()
        logging.update('{} cells were identified through clustering'.format(len(self.cells_from_clustering)))
    
    def show_stack(self, fps=8):
        
        display.stack(self.raw, fps, name="Raw sequence")
    
    def show_detections_stack(self, on_frames=False, fps=8):
        
        stack = self.cell_detection_stack_on_frames if on_frames else self.cell_detection_stack
        
        display.stack(stack, fps, name="Cell detections")
        
    def show_cumulative_stack(self, fps=8):
        
        display.stack(self.cumulative_detection_stack, fps, name="Cumulative detections") 
        
    def show_clustering(self):
        
        display.image(self.clustering_image, name="Clustering process")
        
    def show_clustered_cells(self):
        
        display.image(self.clustered_cells_image, name="Cells from clusters")

    def save_raw(self):
        
        save_image(self.raw, self.output_directory, "original.tif")
    
    def save_detections_stack(self):
        
        save_image(self.cell_detection_stack, self.output_directory, "detections_raw.tif")

    def save_detections_stack_on_frames(self):
        
        save_image(self.cell_detection_stack_on_frames, self.output_directory, "detections_on_frames.tif")
        
    def save_cumulative_stack(self):
        
        save_image(self.cumulative_detection_stack, self.output_directory, "detections_cumulative.tif")
        
    def save_clustering_image(self):
        
        save_image(self.clustering_image, self.output_directory, "clustering.tif")
        
    def save_clustered_cells_image(self):
        
        save_image(self.clustered_cells_image, self.output_directory, "cells_from_clusters.tif")

    def save_all_processing_images(self, save_raw=False):

        if save_raw: self.save_raw()
        self.save_detections_stack()
        self.save_detections_stack_on_frames()
        self.save_cumulative_stack()
        self.save_clustering_image()
        self.save_clustered_cells_image()

    def save_cells_as_coords(self):
        
        clustering.save(self.cells_from_clustering, 
                        self.output_directory,
                        self.min_samples, 
                        self.max_clustering_distance)
        
        logging.update('Saving coordinates of cells from clusters')
        
        
