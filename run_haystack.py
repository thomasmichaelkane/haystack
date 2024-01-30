import sys

from lib.utils import parse
from lib.utils.utils import load_config
from lib.obj.haystack import Haystack

def main():
    
    PATH, ROIS_EXIST = parse_args()
    
    config = load_config()
    
    hs = Haystack(PATH)
    
    hs.choose_colormap(config['clustering']['colormap'])
    
    if ROIS_EXIST:
        hs.load_rois_directly()
    else:
        hs.detect_cells(model_path=config['cellpose']['model_path'], 
                        cellprob_threshold=config['cellpose']['cellprob_threshold'],
                        channels=[config['cellpose']['channels']])
    
    hs.cluster_cells(min_samples=config['clustering']['min_samples'], 
                     max_clustering_distance=config['clustering']['max_clustering_distance'])
    
    hs.show_stack()
    hs.show_detections_stack()
    hs.show_detections_stack(on_frames=True)
    hs.show_cumulative_stack()
    hs.show_clustering()
    hs.show_clustered_cells()
    
    hs.save_all_processing()
    hs.save_cells_as_coords()
    
def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No directory specififed")
        
    elif len(sys.argv) == 2:
        
        path = parse.path(sys.argv[1])
        rois_exist = False
        
    elif len(sys.argv) == 3:
        
        path = parse.path(sys.argv[1])
        rois_exist = parse.rois_exist(sys.argv[2])
           
    else:
        
        raise KeyError("Too many input arguments")
    
    return path, rois_exist

main()