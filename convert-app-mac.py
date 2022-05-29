from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os 
import pandas as pd
import numpy as np
root = os.getcwd()
import png
import pydicom
import errno
import glob
import multiprocessing as mp
from tkinter import messagebox

gui = Tk()
gui.geometry("400x400")
gui.title("DCM2PNG")

IMG_EXTENSIONS = ['.dcm']

class FolderSelect(Frame):
    def __init__(self,parent=None,folderDescription="",**kw):
        Frame.__init__(self,master=parent,**kw)
        self.folderPath = StringVar()
        self.lblName = Label(self, text=folderDescription)
        self.lblName.grid(row=0,column=0)
        self.entPath = Entry(self, textvariable=self.folderPath)
        self.entPath.grid(row=0,column=1)
        self.btnFind = ttk.Button(self, text="Click",command=self.setFolderPath)
        self.btnFind.grid(row=0,column=2)
    def setFolderPath(self):
        folder_selected = filedialog.askdirectory()
        self.folderPath.set(folder_selected)
    @property
    def folder_path(self):
        return self.folderPath.get()

folderPath = StringVar()
directory1Select = FolderSelect(gui,"Input folder ")
directory1Select.grid(row=0)
directory2Select = FolderSelect(gui,"Output folder")
directory2Select.grid(row=1)


def has_file_allowed_extension(filename, extensions):
    """Checks if a file is an allowed extension.
    Args:
        filename (string): path to a file
    Returns:
        bool: True if the filename ends with a known image extension
    """
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in extensions)


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

def dcm2img():
    pool = mp.Pool(mp.cpu_count())
    input_folder = directory1Select.folder_path   #get input path
    output_folder = directory2Select.folder_path  #get output path
    item_list = get_all_items(input_folder)
    pool.starmap(dicom_2_png, [(input_folder, file , output_folder) for file in item_list])
    print('Done')
    messagebox.showinfo('finish','Done')

def main():
    c = ttk.Button(gui, text="Convert", command = dcm2img)
    c.grid(row=4,column=0)
    gui.mainloop()

if __name__ == "__main__":

    main()
