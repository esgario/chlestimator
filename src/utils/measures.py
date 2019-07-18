# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 10:16:34 2018

@author: Guilherme
"""

import numpy as np
import math
import sys
import matplotlib.pyplot as plt

class ChlMeasures:
    def __init__(self, img=None, leaf_mask=None, bg_mask=None, white_balance=True):
        
        self.white_balance = white_balance
        
        if img is not None:
            self.set_images(img, leaf_mask, bg_mask)
        
    def set_images(self, _images, _leaf_masks=None, _bg_masks=None):
        
        self.total_images = len(_images)
        
        self.R = np.zeros(self.total_images)
        self.G = np.zeros(self.total_images)
        self.B = np.zeros(self.total_images)
        self.H = np.zeros(self.total_images)
        self.S = np.zeros(self.total_images)
        self.I = np.zeros(self.total_images)
        self.r = np.zeros(self.total_images)
        self.g = np.zeros(self.total_images)
        self.b = np.zeros(self.total_images)
        self.hue = np.zeros(self.total_images)
        self.sat = np.zeros(self.total_images)
        self.bri = np.zeros(self.total_images)
        
        for i in range(self.total_images):
            if _leaf_masks is not None:
                image = np.ma.zeros(_images.shape)
                bg = np.ma.zeros(_images.shape)
                
                if _bg_masks is None:
                    _bg_masks = np.invert(_leaf_masks)
                
                for j in range(3):
                    image[i,:,:,j] = np.ma.masked_array(_images[i,:,:,j], _leaf_masks[i])
                    bg[i,:,:,j] = np.ma.masked_array(_images[i,:,:,j], _bg_masks[i])
                    
            else:
                image[i] = _images[i]
                bg = None
            
            self.R[i] = np.mean(image[i,:,:,0])
            self.G[i] = np.mean(image[i,:,:,1])
            self.B[i] = np.mean(image[i,:,:,2])
            
            # White balance
            if (self.white_balance is True) & (bg is not None):
                Rw = np.mean(bg[i,:,:,0])
                Gw = np.mean(bg[i,:,:,1])
                Bw = np.mean(bg[i,:,:,2])
                
                self.R[i] = self.R[i] - Rw + 255
                self.G[i] = self.G[i] - Gw + 255
                self.B[i] = self.B[i] - Bw + 255
    
            m = (self.R[i] + self.G[i] + self.B[i])
            
            self.H[i] = math.acos( (((self.R[i] - self.G[i]) + (self.R[i] - self.B[i])) / 2) /
                               math.sqrt((self.R[i] - self.G[i])**2 + (self.R[i] - self.B[i])*(self.G[i] - self.B[i])) )
            self.S[i] = 1 - (3 / m) * min([self.R[i], self.G[i], self.B[i]])
            self.I[i] = (1 / 3) * (m)
            
            self.r[i] = self.R[i]/m
            self.g[i] = self.G[i]/m
            self.b[i] = self.B[i]/m
            
            self.hue[i], self.sat[i], self.bri[i] = self.rgb2hsb(i)
    
    def compute_index(self, n=None):
        
        switcher = {
            0 : [ lambda x, i : x.R[i], 'R' ],
            1 : [ lambda x, i : x.G[i], 'G' ],
            2 : [ lambda x, i : x.B[i], 'B' ],
            3 : [ lambda x, i : x.H[i], 'H' ],
            4 : [ lambda x, i : x.S[i], 'S' ],
            5 : [ lambda x, i : x.I[i], 'I' ],
            6 : [ lambda x, i : x.r[i], 'NR' ],
            7 : [ lambda x, i : x.g[i], 'NG' ],
            8 : [ lambda x, i : x.b[i], 'NB' ],
            9 : [ lambda x, i : x.R[i]-x.G[i], 'R-G' ],
            10 : [ lambda x, i : x.R[i]-x.B[i], 'R-B' ],
            11 : [ lambda x, i : x.G[i]-x.B[i], 'G-B' ],
            12 : [ lambda x, i : x.G[i]/x.R[i], 'G/R' ],
            13 : [ lambda x, i : x.R[i]/x.B[i], 'R/B' ],
            14 : [ lambda x, i : x.G[i]/x.B[i], 'G/B' ],
            15 : [ lambda x, i : (x.R[i]-x.G[i])/(x.R[i]+x.G[i]), 'R-G/R+G' ],
            16 : [ lambda x, i : (x.R[i]-x.B[i])/(x.R[i]+x.B[i]), 'R-B/R+B' ],
            17 : [ lambda x, i : (x.G[i]-x.B[i])/(x.G[i]+x.B[i]), 'G-B/G+B' ],
            18 : [ lambda x, i : (x.R[i]-x.G[i])/(x.R[i]+x.G[i]+x.B[i]), 'R-G/R+G+B' ],
            19 : [ lambda x, i : (x.R[i]-x.B[i])/(x.R[i]+x.G[i]+x.B[i]), 'R-B/R+G+B' ],
            20 : [ lambda x, i : (x.G[i]-x.B[i])/(x.R[i]+x.G[i]+x.B[i]), 'G-B/R+G+B' ],
            21 : [ lambda x, i : 1.4*x.r[i]-x.g[i], 'ExR' ],
            22 : [ lambda x, i : 2*x.g[i]-x.r[i]-x.b[i], 'ExG' ],
            23 : [ lambda x, i : 1.4*x.b[i]-x.g[i], 'ExB' ],
            24 : [ lambda x, i : (2*x.g[i]-x.r[i]-x.b[i])-(1.4*x.r[i]-x.g[i]), 'ExGR' ],
            25 : [ lambda x, i : (x.g[i]-x.r[i])/(x.g[i]+x.r[i]), 'NGRDI' ],
            26 : [ lambda x, i : ( ((x.hue[i]-60)/60) + (1-x.sat[i]) + (1-x.bri[i]) )/3, 'DGCI' ]
        }
        
        result = np.zeros(self.total_images)
                
        for i in range(self.total_images):
            result[i] = switcher[n][0](self, i)
            sys.stdout.write("\r%s - IMG[%d/%d]" % (switcher[n][1], i+1 , self.total_images))
            sys.stdout.flush()
            
        print('')
        
        return result, switcher[n][1]
    
    def compute_all_indices(self):
        
        result = np.zeros([self.total_images, 27])
        
        index_names = []
    
        print("Calculating indices...")
    
        for j in range(27):
            result[:,j], index_name = self.compute_index(j)
            index_names.append(index_name)
            
        return result, index_names
    
    def rgb2hsb(self, i):

        R = self.R[i]/255; G = self.G[i]/255; B = self.B[i]/255;
        
        max_RGB = max([R,G,B])
        max_i = [R,G,B].index(max_RGB)
        
        min_RGB = min([R,G,B])
        
        if max_i == 0:
            Hue = 60 * ( (G-B)/(max_RGB-min_RGB) )
        elif max_i == 1:
            Hue = 60 * ( 2 + ((B-R)/(max_RGB-min_RGB)) )
        else:
            Hue = 60 * ( 4 + ((R-G)/(max_RGB-min_RGB)) )        
        
        Saturation = (max_RGB - min_RGB)/max_RGB
        
        Brightness = max_RGB
    
        return Hue, Saturation, Brightness;