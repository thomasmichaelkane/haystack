import sys

# from haystack.utils import parse

from haystack import Haystack, load_config, parse

def run():
    
    # parse command line arguments for stack/directory path, and whether previous rois are used
    PATH, ROIS_EXIST = parse_args()
    
    # load_config if using yaml file
    config = load_config()
    
    # initialize haystacl class
    hs = Haystack(PATH)
    
    # choose the desired colormap for detected cells
    hs.choose_colormap(config['clustering']['colormap'])
    
    # choose detection or roi load
    if ROIS_EXIST:
        # if cellpose has already been run, we can reload the rois directly
        hs.load_rois_directly()
    else:
        # if not then run cellpose on the stack
        hs.detect_cells(model_path=config['cellpose']['model_path'], 
                        cellprob_threshold=config['cellpose']['cellprob_threshold'],
                        channels=[config['cellpose']['channels']])
    
    # run clustering algorithm
    hs.cluster_cells(min_samples=config['clustering']['min_samples'], 
                     max_clustering_distance=config['clustering']['max_clustering_distance'])
    
    # show all processes
    hs.show_stack()
    hs.show_detections_stack()
    hs.show_detections_stack(on_frames=True)
    hs.show_cumulative_stack()
    hs.show_clustering()
    hs.show_clustered_cells()
    
    # save all processes and clustered cell coordinates
    hs.save_all_processing_images()
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

if __name__ == "__main__":
    run()