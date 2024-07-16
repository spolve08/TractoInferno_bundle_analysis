#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri giu 2 14:44:57 2023

@author: chiara


Some functions useful to work with neuroimaging data.

"""
import os
import nibabel as nib


def save_nifti(np_array , aff, headd, path_out):
    dir_out=os.path.dirname(path_out)
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)
                            
    nib_img = nib.Nifti1Image(np_array, aff, headd)
    nib.save(nib_img, path_out)
    print(f"Saved to file : {path_out}")
