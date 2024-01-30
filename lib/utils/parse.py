import os

def rois_exist(arg):
    
    if arg == "1":
        return True
    
    elif arg == "0":
        return False
    
    else:
        raise ValueError("Argument for whether ROIs already exist should be either 1 (True) or 0 (False)")
        

def tiff(arg):
    
    return True if arg.endswith('.tiff') or arg.endswith('.tif') else False
        
def dir(arg):
    
    return True if os.path.isdir(arg) else False

def path(arg):
    
    if os.path.exists(arg):
        
        return arg
            
    else:
        raise FileNotFoundError
    
def num_squares(arg):
    
    try:
        num_squares = int(arg)
        
        if num_squares > 0:
            return num_squares
        else:
            raise ValueError("Needs to be 1 or more")
            
    except ValueError:
        
        raise NameError("Needs to be an integer")

def cellprob(arg):

    try:
        cellprob = float(arg)
        
        if -6 < cellprob < 6:
            return cellprob
        else:
            raise ValueError("Needs to be between -6 and 6")
            
    except ValueError:
        
        raise NameError("Needs to be a number")

def size(arg):
    
    try:
        size = int(arg)
        
        if 50 <= size <= 1000:
            return size
        else:
            raise ValueError("Needs to within range 50-1000")
            
    except ValueError:
        
        raise NameError("Needs to be an integer")
