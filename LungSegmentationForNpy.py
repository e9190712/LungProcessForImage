import numpy as np
from skimage import morphology
from skimage import measure
from sklearn.cluster import KMeans
import pydicom
from glob import glob
import skfuzzy as fuzz
from scipy import ndimage as ndi
import sys
import os
Inpath = "/home/mike/Documents/ISU_CTDATA1"
Outpath = "/home/mike/Desktop/MyProjectForAll/NpyOut"
select = int(input("Kmeans請輸入1,Cmeans請輸入2:"))
g = glob(Inpath + '/*.dcm')


def load_scan(path):
    slices = sorted([pydicom.read_file(s) for s in path],key=lambda x: int(x.InstanceNumber))
    #slices.sort(key=lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices

image = np.stack([s.pixel_array for s in load_scan(g)])
for i in range(len(image)):
    img = image[i]

    img = img - np.mean(img)
    img = img / np.std(img)

    middle = img[100:400, 100:400]
    mean = np.mean(middle)
    max_im = np.max(img)
    min_im = np.min(img)

    img[img == max_im] = mean
    img[img == min_im] = mean

    if select==1:
        kmeans = KMeans(n_clusters=2).fit(np.reshape(middle, [np.prod(middle.shape), 1]))
        centers = sorted(kmeans.cluster_centers_.flatten())
    if select==2:
        centers, u, u0, d, jm, p, fpc = fuzz.cmeans(np.reshape(middle, [np.prod(middle.shape), 1]), 2, 2, error=0.005,maxiter=1000, init=None)

    threshold = np.mean(centers)
    thresh_img = np.where(img < threshold, 1.0, 0.0)
    if select==1:
        eroded = morphology.erosion(thresh_img, np.ones([4, 4]))
        thresh_img = dilation = morphology.dilation(eroded, np.ones([10, 10]))

    labels = measure.label(thresh_img)
    #label_vals = np.unique(labels)
    regions = measure.regionprops(labels)
    good_labels = []
    for prop in regions:
        B = prop.bbox
        if B[2] - B[0] < 475 and B[3] - B[1] < 475 and B[0] > 40 and B[2] < 472:
            good_labels.append(prop.label)
    mask = np.ndarray([512, 512], dtype=np.int8)
    mask[:] = 0
    for N in good_labels:
        mask = mask + np.where(labels == N, 1, 0)
    if select==2:
        mask = ndi.binary_fill_holes(mask)
    elif select == 1:
        mask = morphology.dilation(mask, np.ones([10, 10]))
    image[i] = mask
np.save(Outpath + '/YourLungMask.npy',image)