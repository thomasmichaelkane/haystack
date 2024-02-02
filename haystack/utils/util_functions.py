import os
from datetime import datetime
import yaml
from tifffile import imwrite

def load_config():
    
    with open('config.yaml') as config:
        settings = yaml.load(config.read(), Loader=yaml.Loader)
        
    return settings

def save_image(img, directory, name):
    
    path = os.path.join(directory, name)
    imwrite(path, img)
    
def save_images(img_list, directory, name):
    
    for img in img_list:
        save_image(img, directory, name)

def create_directory(parent, name, timestamp=False):
    
    if timestamp:
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d-%H%M%S_")
        name = date_str + name
    
    output_directory = os.path.join(parent, name)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    return output_directory