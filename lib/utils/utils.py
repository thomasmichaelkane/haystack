import os
import json
from datetime import datetime
import yaml
from tifffile import imwrite

def load_config():
    
    with open('config.yaml') as config:
        settings = yaml.load(config.read(), Loader=yaml.Loader)
        
    return settings

def save_stack(stack, directory, name, as_dir=False):
    
    path = os.path.join(directory, name)
    imwrite(path, stack)

def save_image(img, directory, name):
    
    path = os.path.join(directory, name)
    imwrite(path, img)

def save_settings(filename, settings):

    with open(filename, 'w') as file:
        file.write(json.dumps(settings))

def get_output_directory(parent, name, timestamp=False):
    
    if timestamp:
        
        now = datetime.now() # current date and time
        date_str = now.strftime("%Y-%m-%d-%H%M%S_")
        directory_name = date_str + name
    
    directory_path = os.path.join(parent, directory_name)
        
    return directory_path

def create_directory(parent, name, timestamp=False):
    
    if timestamp:
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d-%H%M%S_")
        name = date_str + name
    
    output_folder = os.path.join(parent, name)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    return output_folder

def create_output_dir(input_path):
    
    parent = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    
    output_name = os.path.splitext(filename)[0].strip() + "_random_samples"
    
    output_folder = os.path.join(parent, output_name)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    return output_folder, filename