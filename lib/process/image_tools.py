import os
import cv2
import tifffile
import random
import numpy as np
import cmapy as cm

def read_tiff_stack(tiff_file_path):
    """
    Read a TIFF stack using tifffile.

    Parameters:
    - tiff_file_path: Path to the TIFF file.

    Returns:
    - NumPy array representing the TIFF stack.
    """
    tiff_stack = tifffile.imread(tiff_file_path)
    
    return tiff_stack

def tiff_stack_to_list(tiff_stack):

    images = [tiff for tiff in tiff_stack]
    
    return images

def read_img_folder(img_folder_path):
    
    images = []

    for filename in os.listdir(img_folder_path):
        
        #todo add all image format functionality
        if filename.endswith(".tif") or filename.endswith(".tiff"):
            image_path = os.path.join(img_folder_path, filename)
            
            # Read TIFF image
            images.append(cv2.imread(image_path))
            
    return images

def create_background(image_shape):
    
    # Create a blank image
    background = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.uint8)
    
    return background

def convert_to_color(frame):
    
    frame_color = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    
    return frame_color
            
def cut_random_squares(image, num_squares, square_size):
    height, width, _ = image.shape
    random_squares = []

    for _ in range(num_squares):
        start_x = random.randint(0, width - square_size)
        start_y = random.randint(0, height - square_size)

        square = image[start_y:start_y+square_size, start_x:start_x+square_size, :]
        random_squares.append(square)

    return random_squares

def random_sampling(images, num_squares, square_size, basename, output_directory):
    
    # Cut out squares
    for i, image in enumerate(images):    

        cuts = cut_random_squares(image, num_squares, square_size)

        # Save cut images
        for j, cut in enumerate(cuts):
            output_filename = f"{os.path.splitext(basename)[0]}_slice_{i+1}_cut_{j+1}.png"
            cv2.imwrite(os.path.join(output_directory, output_filename), cut)
            

def add_points(points, img, color=(0, 255, 255), radius=3, fill=True, add_numbering=False):
    """
    Display points on an image using OpenCV.

    Parameters:
    - rois: List of ROIs, where each ROI is a list of (x, y) coordinates.
    - image_shape: Tuple representing the shape of the image (height, width).
    """
    
    for point in points:

        thickness = -1 if fill is True else 1
        cv2.circle(img, (point[0], point[1]), radius=radius, color=color, thickness=thickness)
        
        # if add_numbering: 
        #     try:
        #         cv2.addText(image, str(point[2]), (point[0]-10, point[1]+10), color=color)
        #     except:
        #         print("number-fail")
    
    return img

def make_detections_stack(coms_stack, background, cumulative=False, sequence=False, point_size=3, colormap="jet"):
    
    detections_list = []
    
    if sequence is False: img = background.copy()
    
    for i, coms_slice in enumerate(coms_stack):
        
        if sequence is True: 
            img = convert_to_color(background[i].copy())
        elif cumulative is True:
            img = img.copy()
        else:
            img = background.copy()
        
        color = cm.color(colormap, random.randrange(0, 256), rgb_order=True)

        img = add_points(coms_slice, img, color=color, radius=point_size)

        detections_list.append(img)
        
    stack_detections = np.array(detections_list)
        
    return stack_detections


