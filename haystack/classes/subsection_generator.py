from haystack.utils import parse, logging
from haystack.process import image_tools
from haystack.utils.util_functions import *

class SubsectionGenerator():
    def __init__(self, path, square_size):
    
        self.path = path
        self.square_size = square_size
        
        self.parent_directory, filename = os.path.split(self.path)
        self.name = os.path.splitext(filename)[0]
        self.output_directory = create_directory(self.parent_directory, self.name+"_subsections", timestamp=True)
        
        if parse.tiff(self.path):
            self.load_from_stack()
            self.is_stack = True
        elif parse.dir(self.path):
            self.load_from_dir()
            self.is_stack = False
        else:
            raise FileNotFoundError
        
        self.test_img = self.images[0]
        
        self.smaller_dim = min(self.test_img.shape[0], self.test_img.shape[1])
        parse.square_vs_image_size(self.smaller_dim, self.square_size)
        
        self.check_if_color()
    
    def check_if_color(self):
        
        if len(self.test_img.shape) == 2:
            self.is_color = False
        elif len(self.test_img.shape) == 3:
            self.is_color = True
        else:
            raise Exception("Input image shape error")
    
    def load_from_stack(self):
        
        stack = image_tools.read_tiff_stack(self.path)
        self.images = [slice for slice in stack]
        
    def load_from_dir(self):    
        
        self.images = image_tools.read_img_folder(self.path)
        
    def make_samples(self, squares_per_slice):
        
        image_tools.random_sampling(self.images, self.is_color, squares_per_slice, self.square_size, self.name, self.output_directory)

        logging.update('Created {} random subsections per slice from {} slice stack'.format(squares_per_slice, len(self.images)))
