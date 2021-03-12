
import os 
import pandas as pd
import numpy as np
import png
import errno
import glob
import pydicom
from tqdm import tqdm
import multiprocessing as mp


def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

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


def dicom_2_png(input_folder, file , output_folder):
    '''
    input : dicom file 
    output: write the pixel array of dicom file as type os png as the output path 
    '''
    if has_file_allowed_extension(file, IMG_EXTENSIONS):
        try:
            PathDicom = input_folder +  file
            mkdir(output_folder + '/' + file.rpartition('/')[0])
            output_path = output_folder + '/' + file.replace('.dcm', '.png')
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
        except:
            pass
    
def dcm2img(input_folder, output_folder):
    pool = mp.Pool(mp.cpu_count())
    item_list = get_all_items(input_folder)
    import time
    t0 = time.time()
    pool.starmap(dicom_2_png, [(input_folder, file , output_folder) for file in item_list])

    print(time.time()-t0)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='dicom2png app python ')
    parser.add_argument('-i', '--input_dir', type=str, default='/Users/nguyenphuong/Desktop/input-folder', help='the dicom path')
    parser.add_argument('-o', '--output_dir', type=str, default='/Users/nguyenphuong/Desktop/output-folder', help='the png path')
    args = parser.parse_args()
    
    mkdir(args.output_dir)
    dcm2img(args.input_dir, args.output_dir)

