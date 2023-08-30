# -*- coding: utf-8 -*-
"""
@author: Guilherme Esgario
"""

import os
import sys
import imageio
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.transform import resize
from utils.measures import ChlMeasures
from utils.plot import plot_multiple_indices
from utils.seg_methods import im_threshold

import warnings

warnings.filterwarnings("ignore")

IMG_SIZE = (512, 512)
PATH = "dataset"
BACKGROUND = "natural_bg"  # natural_bg or white_bg
CSV_PATH = os.path.join(PATH, "spad_502_measures.csv")
PLANT_NAME = ("golden papaya", "tainung papaya")

# open dataset csv
dataset = pd.read_csv(CSV_PATH, encoding="UTF-8")

# golden papaya
spad_gp = dataset[dataset["plant"] == PLANT_NAME[0]]
spad_gp = spad_gp["spad_measure"].values

# tainung papaya
spad_tp = dataset[dataset["plant"] == PLANT_NAME[1]]
spad_tp = spad_tp["spad_measure"].values


def load_images(IMG_PATH):
    files = os.listdir(IMG_PATH)

    images = np.zeros((len(files), IMG_SIZE[0], IMG_SIZE[1], 3), dtype=np.uint8)
    leaf_masks = np.zeros((len(files), IMG_SIZE[0], IMG_SIZE[1]), dtype=np.bool)
    bg_masks = np.zeros((len(files), IMG_SIZE[0], IMG_SIZE[1]), dtype=np.bool)

    for i in range(len(files)):
        sys.stdout.write("\rLoading images: %d%%" % (100 * (i + 1) / len(files)))

        # reading image
        img = imageio.imread(os.path.join(IMG_PATH, files[i]))
        img = resize(img, IMG_SIZE, mode="constant", preserve_range=True)

        # convert to HSV color space
        img_hsv = matplotlib.colors.rgb_to_hsv(img)

        # generate a new component combining 'saturation' and 'blue' channels
        img_new = img_hsv[:, :, 1] * 255 + 255 - img[:, :, 2]
        img_new = (img_new - img_new.min()) / (img_new.max() - img_new.min())

        #  segmentation
        leaf_mask = im_threshold(img_new, 0.8)
        leaf_mask = np.invert(np.array(leaf_mask, dtype=bool))

        bg_mask = im_threshold(img_new, 0.2)
        bg_mask = np.array(bg_mask, dtype=bool)

        images[i] = img
        leaf_masks[i] = leaf_mask
        bg_masks[i] = bg_mask

    #        plt.imshow(images[i])
    #        plt.show()
    #        plt.imshow(bg_mask, cmap='gray')
    #        plt.show()
    #        plt.imshow(leaf_mask, cmap='gray')
    #        plt.show()

    print("\n")
    return images, leaf_masks, bg_masks


# Golden papaya
images, leaf_masks, bg_masks = load_images(PATH + "/golden/" + BACKGROUND)
cme = ChlMeasures(
    images,
    leaf_masks,
    bg_masks,
    white_balance=(True if BACKGROUND == "white_bg" else False),
)
result_gp, index_names = cme.compute_all_indices()

# Tainung papaya
images, leaf_masks, bg_masks = load_images(PATH + "/tainung/" + BACKGROUND)
cme.set_images(images, leaf_masks, bg_masks)
result_tp, index_names = cme.compute_all_indices()

# select_indices = ( 10, 26 )
select_indices = list(range(27))

results = (result_gp[:, select_indices], result_tp[:, select_indices])
spad_measures = (spad_gp, spad_tp)
index_names_new = [index_names[i] for i in select_indices]

# Plotting results
plot_multiple_indices(
    results, spad_measures, index_names_new, (16, 20), ("gp", "tp"), 0
)
