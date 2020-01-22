#!/usr/bin/env python
# coding: utf-8

# # Initalizaion

# In[60]:



#https://docs.fast.ai/vision.image.html#ImagePoints

get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')
#from fastai.vision import *
import openpyxl
#from fastai.callbacks.hooks import *
#from fastai.metrics import error_rate
from PIL import Image
from imutils import paths
import argparse
import cv2
import os
# import the necessary packages
import skimage
from skimage import measure
import matplotlib.pyplot as plt
import numpy as np

bs = 3

#from tkinter import Tk
#from tkinter.filedialog import askdirectory
#path = askdirectory(title='Select Folder') # shows dialog box and return the path
#print(path)  


def nosignalcheck(image):
    path="/home/shaomtuser/.fastai/data/aran_errors/NoSignal.png"
    img = cv2.imread(str(path))
    s = measure.compare_ssim(img, image,multichannel=True)
    return(s)




#path = untar_data(URLs.MNIST_SAMPLE); path
#print(path)
#tfms = get_transforms(do_flip=False)
#data = ImageDataBunch.from_folder(path, ds_tfms=tfms, size=26)
#data.show_batch(rows=3, figsize=(5,5))

#path='/home/shaomtuser/.fastai/data/aran_errors'
#tfms = get_transforms(do_flip=False)
#data = ImageDataBunch.from_folder(path, ds_tfms=tfms, size=26)
#data.show_batch(rows=3, figsize=(5,5))


# # Scan through files in folder and write excel file with errors

# In[101]:



#ask for directory
#from tkinter import Tk
#from tkinter.filedialog import askdirectory
#path = askdirectory(title='Select Folder') # shows dialog box and return the path
#print(path) 

directory_in_str="/home/shaomtuser/.fastai/data/aran_errors/testset"
directory = os.fsencode(directory_in_str)

wb=openpyxl.load_workbook('/home/shaomtuser/.fastai/data/aran_errors/arantest.xlsx')
sheet=wb.get_sheet_by_name('Sheet1')
cellnum=3
sheet['B1']=(directory)
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".PNG") or filename.endswith(".jpg"): 
        img = cv2.imread(str(directory.decode())+'/'+str(file.decode()))#decode removes the b prefex of string
        
        #if nosignalcheck(img)>.9: #no signal check
         #   sheet['A'+str(cellnum)]=(filename)
          #  sheet['B'+str(cellnum)]='No Signal'
        
        if variance_of_laplacian(img)<1000: #blurry check
            sheet['A'+str(cellnum)]=(filename)
            sheet['B'+str(cellnum)]='blurry'
            cellnum=cellnum+1 
                
        continue
     else:
         continue
wb.save('/home/shaomtuser/.fastai/data/aran_errors/aran_errors.xlsx')


# # No signal check

# In[35]:







img = cv2.imread(str(path))
s=nosignalcheck(img)

if s > .9:
    print("No signal")


# # Blur check

# In[36]:



 
def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()


if variance_of_laplacian(img)<1000:
   print("blurry")
 


# # Overexposed

# In[ ]:


grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hist = cv.calcHist([img],[0],None,[256],[0,256])

