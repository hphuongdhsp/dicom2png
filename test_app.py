
import os 
import pandas as pd
import numpy as np
from pydicom import dcmread
import png
import nibabel as nib
import cv2
import errno
import glob
import pydicom


def has_file_allowed_extension(filename, extensions):
    """Checks if a file is an allowed extension.
    Args:
        filename (string): path to a file
    Returns:
        bool: True if the filename ends with a known image extension
    """
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in extensions)

IMG_EXTENSIONS = ['.dcm']


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def get_all_items (path): 
    images = []  # list of images
    folder = glob.glob( path +'*') 
    while folder:
        f = folder[0]
        if os.path.isfile(f):
            images.append(f.replace(path, ''))
            folder.remove(f)
        else:
            folder+=glob.glob(f+'/*')
            folder.remove(f)
    return images

def dicom_2_png(PathDicom,output_path):
    '''
    input : dicom file 
    output: write the pixel array of dicom file as type os png as the output path 
    '''
    ds = pydicom.dcmread(PathDicom)
    shape = ds.pixel_array.shape
    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    # Write the PNG file
    with open(output_path, 'wb') as png_file:
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)

def dcm2img(input_folder, output_folder):
    error_list = []
    item_list = get_all_items(input_folder)
    for file in item_list: 
        if has_file_allowed_extension(file, IMG_EXTENSIONS):  ## except only cdm file 
            dicom_path  = input_folder +  file
            mkdir( output_folder + '/' + file.rpartition('/')[0])
            output_path = output_folder + '/' + file.replace('.dcm', '.png')
            try: 
                dicom_2_png(dicom_path,output_path)
            except: 
                error_list.append(dicom_path)
    df = pd.DataFrame(error_list,columns =['error_file'])
    df.to_csv(output_folder + '/' + 'error_list.csv')
    print('Done')
if __name__ == "__main__":
    
    input_folder = '/home/may-nov/Documents/spine/Torus Imagine'
    output_folder =  '/home/may-nov/Documents/spine/test1'

    mkdir(output_folder)
    dcm2img(input_folder, output_folder)