import cv2
import numpy as np

def stack(stack, fps, name='stack'):
    
    show = True
    delay = int(round(1000/fps)) 
    
    while show:
        
        for frame in stack:
        
            cv2.imshow(name, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(delay) == ord('q'):
                show = False
                break
            
    cv2.destroyAllWindows()
    
def image(img, name='image'):
    
    cv2.imshow(name, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def rois(rois, image, color=(0, 0, 255), show=True):
    """
    Display ROIs on a blank background using OpenCV.

    Parameters:
    - rois: List of ROIs, where each ROI is a list of (x, y) coordinates.
    - image_shape: Tuple representing the shape of the image (height, width).
    """
    
    for roi in rois:
        # Convert ROI coordinates to NumPy array
        roi_np = np.array(roi, dtype=np.int32)
        roi_np = roi_np.reshape((-1, 1, 2))

        # Draw the ROI on the blank image
        cv2.polylines(image, [roi_np], isClosed=True, color=color, thickness=2)

    # Display the image with centers of mass
    if show:
        cv2.imshow('ROIs', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return image
        