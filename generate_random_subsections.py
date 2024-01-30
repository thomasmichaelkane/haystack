import sys

from lib.utils import parse
from lib.process import image_tools
from lib.utils.utils import *

def main():
    
    PATH, IS_DIR, NUM_SQUARES, SIZE = parse_args()
    
    # Get the parent directory
    output_directory, filename = create_output_dir(PATH)
    
    if IS_DIR:
        
        images = image_tools.read_img_folder(PATH)
    
    else: # using a tiff stack
        
        tiff_stack = image_tools.read_tiff_stack(PATH)
        images = image_tools.tiff_stack_to_list(tiff_stack)
        
    image_tools.random_sampling(images, NUM_SQUARES, SIZE, filename, output_directory)

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No images path specififed")
        
    elif len(sys.argv) == 2:
        
        path, is_dir = parse.path(sys.argv[1])
        num_squares = 1
        size = 300
    
    elif len(sys.argv) == 3:
        
        path, is_dir = parse.path(sys.argv[1])
        num_squares = parse.num_squares(sys.argv[2])
        size = 300
        
    elif len(sys.argv) == 4:
        
        path, is_dir = parse.path(sys.argv[1])
        num_squares = parse.num_squares(sys.argv[2])
        size = parse.size(sys.argv[3])
           
    else:
        
        raise KeyError("Too many input arguments")
    
    return path, is_dir, num_squares, size

main()
