import sys

from haystack import SubsectionGenerator, parse

def run():
    
    PATH, NUM_SQUARES, SIZE = parse_args()
    
    generator = SubsectionGenerator(PATH, SIZE)
    generator.make_samples(NUM_SQUARES)

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No images path specififed")
        
    elif len(sys.argv) == 2:
        
        path = parse.path(sys.argv[1])
        num_squares = 1
        size = 300
    
    elif len(sys.argv) == 3:
        
        path = parse.path(sys.argv[1])
        num_squares = parse.num_squares(sys.argv[2])
        size = 300
        
    elif len(sys.argv) == 4:
        
        path = parse.path(sys.argv[1])
        num_squares = parse.num_squares(sys.argv[2])
        size = parse.size(sys.argv[3])
           
    else:
        
        raise KeyError("Too many input arguments")
    
    return path, num_squares, size

if __name__ == "__main__":
    run()
