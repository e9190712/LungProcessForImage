import matplotlib.pyplot as plt
import pydicom
import numpy as np
from skimage.segmentation import clear_border
from skimage.measure import label,regionprops
from skimage.morphology import disk,binary_erosion,binary_closing
from skimage.filters import roberts
from scipy import ndimage as ndi
case_path = '/home/mike/Documents/ISU_CTDATA1/C+29.dcm'
pydicomimage = pydicom.read_file(case_path)
slice = pydicomimage.pixel_array
output_path = '/home/mike/Desktop/MyProjectForAll/NpyOut/'
mask_imags = np.load(output_path+'YourLungMask.npy')
#cmp_imags = np.load(output_path+'lungmask.npy')
def single(imgs):
    for i in range(len(imgs)):
        f, plots = plt.subplots(1, 1, figsize=(5, 5))
        plots.imshow(imgs[i], cmap='gray')
        plots.axis('off')
        plt.show()
def complex(imgs):
    for i in range(len(imgs)):
        f, plots = plt.subplots(1, 1, figsize=(5, 5))
        plots.imshow(imgs[i, 0], cmap='gray')
        plots.axis('off')
        plt.show()
def combine_(o_imags, imgs):
    for i in range(len(o_imags)):
        fig, ax = plt.subplots(2, 2, figsize=[12, 12])
        ax[0, 0].imshow(o_imags[i+40])
        ax[0, 1].imshow(imgs[i+40])
        plt.show()
def combine(pre_imags, imgs):
    for i in range(len(imgs)):
        fig, ax = plt.subplots(2, 2, figsize=[12, 12])
        ax[0, 0].imshow(pre_imags[i, 0], cmap='gray')
        ax[0, 1].imshow(imgs[i,0], cmap='gray')
        plt.show()
def ISU_LUNGMASK(imgs, masks):
    for i in range(len(imgs)):
        fig, ax = plt.subplots(2, 2, figsize=[12, 12])
        ax[0, 0].imshow(imgs[i+40], cmap='gray')
        ax[0, 1].imshow(masks[i+40, 0], cmap='gray')
        plt.show()
def get_segmented_lungs(im, plot=False):

        '''
        This funtion segments the lungs from the given 2D slice.
        '''
        if plot == True:
            f, plots = plt.subplots(2, 5, figsize=(10, 30))

            plots[0, 0].axis('off')
            plots[0, 0].imshow(im, cmap=plt.cm.gray)

        '''
        Step 1: Convert into a binary image. 
        '''
        binary = im < 604
        if plot == True:
            plots[0, 1].axis('off')
            plots[0, 1].imshow(binary, cmap=plt.cm.bone)
        '''
        Step 2: Remove the blobs connected to the border of the image.
        '''
        cleared = clear_border(binary)
        if plot == True:
            plots[0, 2].axis('off')
            plots[0, 2].imshow(cleared, cmap=plt.cm.bone)
        '''
        Step 3: Label the image.
        '''
        label_image = label(cleared)
        if plot == True:
            plots[0, 3].axis('off')
            plots[0, 3].imshow(label_image, cmap=plt.cm.bone)
        '''
        Step 4: Keep the labels with 2 largest areas.
        '''
        areas = [r.area for r in regionprops(label_image)]
        areas.sort()
        if len(areas) > 2:
            for region in regionprops(label_image):
                if region.area < areas[-2]:
                    for coordinates in region.coords:
                        label_image[coordinates[0], coordinates[1]] = 0
        binary = label_image > 0
        if plot == True:
            plots[1, 0].axis('off')
            plots[1, 0].imshow(binary, cmap=plt.cm.bone)
        '''
        Step 5: Erosion operation with a disk of radius 2. This operation is 
        seperate the lung nodules attached to the blood vessels.
        '''
        selem = disk(2)
        binary = binary_erosion(binary, selem)
        if plot == True:
            plots[1, 1].axis('off')
            plots[1, 1].imshow(binary, cmap=plt.cm.bone)
        '''
        Step 6: Closure operation with a disk of radius 10. This operation is 
        to keep nodules attached to the lung wall.
        '''
        selem = disk(10)
        binary = binary_closing(binary, selem)
        if plot == True:
            plots[1, 2].axis('off')
            plots[1, 2].imshow(binary, cmap=plt.cm.bone)
        '''
        Step 7: Fill in the small holes inside the binary mask of lungs.
        '''
        edges = roberts(binary)
        binary = ndi.binary_fill_holes(edges)
        if plot == True:
            plots[1,3].axis('off')
            plots[1,3].imshow(binary, cmap=plt.cm.bone)
        '''
        Step 8: Superimpose the binary mask on the input image.
        '''
        get_high_vals = binary == 0
        im[get_high_vals] = 0
        if plot == True:
            plots[1, 4].axis('off')
            plots[1, 4].imshow(im, cmap=plt.cm.bone)
        plt.show()
        return im
#get_segmented_lungs(slice, True)
single(mask_imags)
#complex(pre_imags)
#complex(eda_lung_mask)
#ISU_LUNGMASK(o_imags, pre_imags)
#combine_(o_imags, pre_imags)