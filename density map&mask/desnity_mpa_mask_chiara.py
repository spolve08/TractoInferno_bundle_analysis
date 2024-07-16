#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri giu 2 14:44:57 2023

@author: alberto and chiara

TODO:
- the script create density map and density mask of selected bundles. The chosen bundles are specified in the `keyword` array. The script iterates into the dataset path (specified in `dataset_path`) the one who begin with 'sub') trough specific folders (the ones who begin with `sub`) and within those check for file including the keywords (bundle name). If there's such files it create a density map and a binary mask of that bundle. These files are then saved in these locations:

mask --> dir_subj_out_mask = f'{dir_subj_out_mask_parent}/{subj_id}/'
map -->  dir_subj_out_map = f'{dir_subj_out_map_parent}/{subj_id}/'

Moreover, it creates a csv file with the following columns: 

keyword, subj_id, bundle, n_streamline, total_volume, aff.tolist(), dim.tolist(), voxel_sizes.tolist(), voxel_order, source 

and save it here:

csv --> csv_path = f"{home_path}/analysis_bundle_stats/tract_info.csv"





NB:
    - the .csv file should have column separated by comma "," not by ";". The file you shared with me has the columns separated by ";".
      the function to_csv() to save pandas dataframe saves files with columns correctly separated by comma ","
      https://en.wikipedia.org/wiki/Comma-separated_values#Basic_rules

      check that the file is always comma separated by ","
    
    - in general the decimal values must be always indicated with the . 

    - check why some bundles' volumes are really high

    - I inserted other comments that beginning with #CR ..

    - modify the variable run_on if the code is runned on alberto's machine
"""



import nibabel as nib
import numpy as np
import os
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.tracking.utils import density_map
import matplotlib.pylab as plt
import pandas as pd
from os.path import dirname as up
import math
import re
import csv
import json
#CR: imported the fct save_nifti defined in utils_data.py
import sys
script_fold = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_fold)

from utils_data import save_nifti


#CR: it is better to put all the inputs/outputs paths at the beginning

#CR: I inserted another variable indicating if the dataset path is reffered to alberto's file system, or to mine(chiara file system)
#moreover I defined home_path so that the output will be in the HOME path of the current file system
home_path=os.environ["HOME"]

#CR: modify this variable according to if it is runned on chiara or on alberto's machine
#run_on="chiara"
run_on="alberto"

dataset_path_run_on={"alberto":f"{home_path}/hd14tb/TractoInferno_Nilab_DetProb",
                    "chiara" : f"{home_path}/mnt/hd14TB_alberto/TractoInferno_Nilab_DetProb" }

dataset_path= dataset_path_run_on[run_on]

info_subject_dict = f'{dataset_path}/info_replic_original_tractograms.json'
dataset_path_replicated = f'{dataset_path}/derivatives/bundles_extracted_from_replicated_wbts_flipping'
dataset_path_original = f'{dataset_path}/derivatives/bundles_extracted_from_same_wbts'
dataset_anatomy = dataset_path


csv_path = f"{home_path}/analysis_bundle_stats/tract_info.csv"

#CR: I modfied the output path with the folder TractoINferno dataset derivatives
#(now you can write on the derivative folder)
dir_subj_out_mask_parent=f"{dataset_anatomy}/derivatives/bundles_masks/"
dir_subj_out_map_parent=f"{dataset_anatomy}/derivatives/bundles_density_map/"


path_subj_info={"replicated_tractograms":dataset_path_replicated,
		"original_tractograms": dataset_path_original }

cutoff = 1
#specify in this list the bundel you want to analyze. Simply write/delete the name of the bundles you've selected. 
keywords = ['AF_L', 'ILF_L', 'IFOF_L', 'FAT_L', 'PYT_L']

with open(info_subject_dict, 'r') as info_subjects_file:
    info_subjects = json.load(info_subjects_file)

#CR: add creation of output dir of csv file if it does not exists
dir_out_csv=os.path.dirname(csv_path)
if not os.path.exists(dir_out_csv):
    os.makedirs(dir_out_csv)

with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    header = ['subject_id','bundle_name','bundle_filename', 'n_streamline','bundle_Volume', 'affine', 'dimensions', 'voxel_sizes', 'voxel_order', 'source']
    writer.writerow(header)

#CR: it is better to define each variable only once
#header = ['bundle_name','subject_id','bundle_filename', 'n_streamline','bundle_Volume', 'affine', 'dimensions', 'voxel_sizes', 'voxel_order', 'source']

Data_array_list = []

#extracting the subject id


sub_id = []

dff=pd.DataFrame(columns=header)

info_subjects_trasformed = {}
for key, values in info_subjects.items():
    for value in values:
        info_subjects_trasformed[value] = key

subj_id_all = list(info_subjects_trasformed.keys())
for subj_id, source in info_subjects_trasformed.items():
        if info_subjects_trasformed[subj_id] == 'replicated_tractograms':
            dataset_path = dataset_path_replicated
        else:
            dataset_path = dataset_path_original       
            
        #CR: I modfied the output path with the folder TractoINferno dataset derivatives
        dir_subj_out_mask=f'{dir_subj_out_mask_parent}/{subj_id}/'
        dir_subj_out_map=f'{dir_subj_out_map_parent}/{subj_id}/'                        
        
        """
        dir_subj_out_mask=f'/home/alberto/hd14tb/alberto/mask/{subj_id}/'
        dir_subj_out_map=f'/home/alberto/hd14tb/alberto/map/{subj_id}/'
        """
        
        tract_path = f'{dataset_path}/{subj_id}'
        for bundle in os.listdir(tract_path):
            print(bundle)
            if bundle.endswith('.trk'):
                bundle_path = os.path.join(tract_path, bundle)
                if os.path.isfile(bundle_path):
                    for keyword in keywords:
                        if keyword in bundle_path:
                            #CR: in bids format: you put in the filename the subj_id at the beginning, and at the end the type of data saved (mask, density)
                            mask_bundle_path = f'{dir_subj_out_mask}/{subj_id}__{keyword}__mask.nii.gz'
                            density_bundle_path = f'{dir_subj_out_map}/{subj_id}__{keyword}__density.nii.gz' 
                            
                            
                            tract_all = nib.streamlines.load(bundle_path, lazy_load=False)
                            tract = np.array(tract_all.streamlines, dtype=object)

                            n_streamline = len(tract)
                            #n_streamline = tract.shape
                            # CR: the number of streamlines can be extracted with len(tract)  or tract.shape[0]
                            
                            aff = tract_all.affine
                            dim = tract_all.header['dimensions']
                            voxel_sizes = tract_all.header['voxel_sizes']
                            voxel_order = tract_all.header['voxel_order']
                            dens_map = density_map(tract, aff, dim) 
                            
                            
                            mask_bd= dens_map>=cutoff
                            mask_bd=mask_bd.astype(np.uint8)
                            total_voxel = np.sum(mask_bd)

                            #CR: check why for some subjects the volume is too big, by inspecting the values
                            total_volume = total_voxel * math.ceil(voxel_sizes[0]) * math.ceil(voxel_sizes[1]) * math.ceil(voxel_sizes[2])
                            file_basename=f"anat/{subj_id}__T1w.nii.gz"
                            reference_path = os.path.join(dataset_anatomy,subj_id,file_basename)
                        
                            reference_anatomy = nib.load(reference_path) 

                            #CR: the less you repeat lines of code the better. the saving of the nifti image 
                            #can be done with a function that you can re-use also in other scripts
                            #I saved the function in utils_data.py

                            save_nifti(np_array = mask_bd, aff=reference_anatomy.affine, headd= reference_anatomy.header, path_out= mask_bundle_path)
                            save_nifti(np_array = dens_map, aff=reference_anatomy.affine, headd= reference_anatomy.header,path_out= density_bundle_path )
                            
                            
                            """
                            if not os.path.exists(dir_subj_out_mask):
                                os.makedirs(dir_subj_out_mask)
                            if not os.path.exists(dir_subj_out_map):
                                os.makedirs(dir_subj_out_map)
                                
                            bdl_mask = nib.Nifti1Image(mask_bd, reference_anatomy.affine, reference_anatomy.header)
                            nib.save(bdl_mask, mask_bundle_path)
                            density = nib.Nifti1Image(dens_map, reference_anatomy.affine, reference_anatomy.header)
                            nib.save(density, density_bundle_path)
                            """


                            vector=[subj_id, keyword, bundle, n_streamline, total_volume, aff.tolist(), dim.tolist(), voxel_sizes.tolist(), voxel_order, source ]
                            Data_array_list.append(vector)
                            with open(csv_path, mode='a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([subj_id, keyword, bundle, n_streamline, total_volume, aff.tolist(), dim.tolist(), voxel_sizes.tolist(), voxel_order, source ])

                            #header = ['bundle_name','subject_id','bundle_filename', 'n_streamline','bundle_Volume', 'affine', 'dimensions', 'voxel_sizes', 'voxel_order', 'source']

                            #CR: alternative way to save data in a pandas dataframe: append each row to the dataframe row per row
                            dff = pd.concat([dff, pd.DataFrame({"subject_id": [subj_id],
                                                                "bundle_name":[keyword],
                                                                "bundle_filename":[bundle],
                                                                "n_streamline": [n_streamline],
                                                                "bundle_Volume": [total_volume],
                                                                "affine": [aff.tolist()],
                                                                "dimensions": [dim.tolist()],
                                                                "voxel_sizes":[ voxel_sizes.tolist()],
                                                                'voxel_order':  [voxel_order],                                                                 
                                                                'source': [source]})])
                            




#Data_array = np.array(Data_array_list)
# df = pd.DataFrame(Data_array, columns=header)

# df.to_csv(csv_path.replace('.csv','_df.csv'))

#CR: save the alternative dataframe
dff.to_csv(csv_path.replace('.csv','_dff.csv'),
            index=False) #to not have the indexes in the first column you should add index=False
       
       
       
"""            
# Prepare the CSV file and write the header
info_subjects_trasformed = {}
for key, values in info_subjects.items():
    for value in values:
        info_subjects_trasformed[value] = key



for subject, source in info_subjects_trasformed.items():
        if info_subjects_trasformed[subject] == 'replicated_tractograms':
            dataset_path = dataset_path_replicated
        else:
            dataset_path = dataset_path_original
        
        for item in os.listdir(dataset_path):
                        
                        
                        item_path = os.path.join(dataset_path, item)
                        if os.path.isdir(item_path) and item.startswith('sub'):       
                            subjs_id_all.append(item)
                            sub_id = item
                        subjs_id_all.sort()
                        print(sub_id)
                        
                        
                        
                        for id in subjs_id_all:
                            print(id)
                            dir_subj_out_mask=f'/home/alberto/hd14tb/alberto/mask/{id}/'
                            dir_subj_out_map=f'/home/alberto/hd14tb/alberto/map/{id}/'
                            tract_path = f'{dataset_path}/{id}'
                            for bundle in os.listdir(tract_path):
                                print(bundle)
                                if bundle.endswith('.trk'):
                                    bundle_path = os.path.join(tract_path, bundle)
                                    if os.path.isfile(bundle_path):
                                        for keyword in keywords:
                                            if keyword in bundle_path:
                                                mask_bundle_path = f'{dir_subj_out_mask}/mask_{keyword}_{id}.nii'
                                                density_bundle_path = f'{dir_subj_out_map}/density_{keyword}_{id}.nii' 
                                                tract_all = nib.streamlines.load(bundle_path, lazy_load=False)
                                                tract = np.array(tract_all.streamlines, dtype=object)
                                                n_streamline = tract.shape
                                                aff = tract_all.affine
                                                dim = tract_all.header['dimensions']
                                                voxel_sizes = tract_all.header['voxel_sizes']
                                                voxel_order = tract_all.header['voxel_order']
                                                dens_map = density_map(tract, aff, dim) 
                                                mask_bd= dens_map>=cutoff
                                                mask_bd=mask_bd.astype(np.uint8)
                                                total_voxel = np.sum(mask_bd)
                                                total_volume = total_voxel * voxel_sizes[0] * voxel_sizes[1] * voxel_sizes[2]
                                                file_basename=f"anat/{id}__T1w.nii.gz"
                                                reference_path = os.path.join(dataset_anatomy,id,file_basename)
                                            
                                                reference_anatomy = nib.load(reference_path)
                                                #/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/sub-1248/sub-1248__T1w.nii.gz
                                                #/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/sub-1000/anat/sub-1000__T1w.nii.gz
                                                if not os.path.exists(dir_subj_out_mask):
                                                    os.makedirs(dir_subj_out_mask)
                                                if not os.path.exists(dir_subj_out_map):
                                                    os.makedirs(dir_subj_out_map)
                                                bdl_mask = nib.Nifti1Image(mask_bd, reference_anatomy.affine, reference_anatomy.header)
                                                nib.save(bdl_mask, mask_bundle_path)
                                                density = nib.Nifti1Image(dens_map, reference_anatomy.affine, reference_anatomy.header)
                                                nib.save(density, density_bundle_path)

                                                vector=[keyword, id, bundle, n_streamline, total_volume, aff.tolist(), dim.tolist(), voxel_sizes.tolist(), voxel_order, source ]
                                                Data_array_list.append(vector)
                                                with open(csv_path, mode='a', newline='') as file:
                                                    writer = csv.writer(file)
                                                    writer.writerow([keyword, id, bundle, n_streamline, total_volume, aff.tolist(), dim.tolist(), voxel_sizes.tolist(), voxel_order, source ])





Data_array = np.array(Data_array_list)
df = pd.DataFrame(Data_array, columns=header)

df.to_csv(csv_path.replace('.csv','_df.csv'))




"""



