# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def otsu(gray, delta=0):
    pixel_number = gray.shape[0] * gray.shape[1]
    mean_weigth = 1.0/pixel_number
    intensity_arr = np.arange(256)
    his, bins = np.histogram(gray, np.arange(0,257))
    final_thresh = -1
    final_value = -1
    
    for t in bins[1:-1]:
        pcb = np.sum(his[:t])
        pcf = np.sum(his[t:])
        Wb = pcb * mean_weigth
        Wf = pcf * mean_weigth
        
        mub = np.sum(intensity_arr[:t]*his[:t]) / float(pcb)
        muf = np.sum(intensity_arr[t:]*his[t:]) / float(pcf)
        
        value = Wb * Wf * (mub - muf) ** 2
        
        if value > final_value:
            final_thresh = t
            final_value = value
    
    final_thresh += delta
    final_img = gray.copy()
#    print('Otsu threshold: ', final_thresh)
    final_img[gray >= final_thresh] = 255
    final_img[gray < final_thresh] = 0
    return final_img

def im_threshold(gray,t):
    final_img = gray.copy()
    final_img[gray > t] = 255
    final_img[gray <= t] = 0
    return final_img    

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def rgb2meangray(rgb):
    return np.dot(rgb[...,:3], [0.8, 0.1, 0.1])

def make_image(arr, f_name, resize_fact=1, dpi=200, plt_show=True):
    """
    Export array as figure in original resolution
    :param arr: array of image to save in original resolution
    :param f_name: name of file where to save figure
    :param resize_fact: resize facter wrt shape of arr, in (0, np.infty)
    :param dpi: dpi of your screen
    :param plt_show: show plot or not
    """
    fig = plt.figure(frameon=False)
    fig.set_size_inches(arr.shape[1]/dpi, arr.shape[0]/dpi)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(arr, cmap='gray')
    plt.savefig(f_name, dpi=(dpi * resize_fact))
    if plt_show:
        plt.show()
    else:
        plt.close()