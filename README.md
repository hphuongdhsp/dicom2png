A simple code to convert dicom file to image (png).



Ubuntu/MacOS

## Installation

Open terminal then, 

```
$ git clone https://github.com/hphuongdhsp/dicom2png
```

Create a new envirement

```
$ conda create --name spine python=3.7 -y
```

Install the requirements

```
$ conda activate spine
$ cd dicom2png
$ pip install -r requirements.txt
$ conda install -c conda-forge gdcm -y
```

## Converting DICOM file to PNG 

To convert dicom folder (for example  "/Users/name_user/Desktop/input-folder") , to another folder (for example  "/Users/name_user/Desktop/output-folder") we use: 


```
$ python test_app.py -i /Users/name_user/Desktop/input-folder -o /Users/name_user/Desktop/output-folder -d True

```

All Dicom files will be converted to images and be stored in the "/Users/name_user/Desktop/output-folder".  All of the error files are stored in the CSV file "error_list.csv"


If you don't care about the error file, then we can use:


```
$ python test_app.py -i /Users/name_user/Desktop/input-folder -o /Users/name_user/Desktop/output-folder -d False

```



