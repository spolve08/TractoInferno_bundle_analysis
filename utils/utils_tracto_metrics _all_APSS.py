

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  28 9:01:26 2023

@author: chiara

Script to collect metrics functions to compute tracts metrics.
In particular the script thre is a function to compute DSC based on streamlines and based on voxels


NB: in the DSC based on voxel I remove the duplicates streamlines :)

TO run the script it is necessary to clone the repository git
    https://github.com/FBK-NILab/nilab.git

in the path
    ${HOME}/local/ 


"""
import json
import os
import sys
import numpy as np
import nibabel as nib 
import pandas as pd
from collections import defaultdict
home_path=os.environ["HOME"] 
repo_path=f"{home_path}/local/tracto_anomaly/"

path_nilab_repo = home_path + "/local/nilab/"
repo_utils_path=f"{repo_path}/utils/"

sys.path.append(repo_utils_path)
sys.path.append(path_nilab_repo)

from uitils_trk import map_trk_2_TRK_np_flipInvariant, rm_duplicates_streamlines_path_trk, rm_duplicates_streamlines_np, check_nps_is_the_same





def dsc_tracts_streamlines(tract_1_path, tract_2_path, distCutoff_sameStramline=0.01, check_rmDupl=False):

    #in the same tract, there can be duplicates streamlines!!!
    #same of the streamlines can be identical!

    #1. rm duplicates streamlines, streamline that overlap in the same bundle due to replication process.
    print("\nRm duplicates streamlines")
    np_unique_t1 = rm_duplicates_streamlines_path_trk(tract_1_path, sanity_check=check_rmDupl)
    np_unique_t2 = rm_duplicates_streamlines_path_trk(tract_2_path,  sanity_check=check_rmDupl)

    print("Compute dsc")
    #number of streamline in each tract
    len_t1, len_t2 = len(np_unique_t1), len(np_unique_t2)

    if len_t1>=len_t2:
        #if t1 has more streamlines than t2, or the number of streamlines is even 
        #use t1 to build kdtree
        T_np=np_unique_t1
        t_np=np_unique_t2
    else:
        #if t2 has more streamline than t1, use t2 to builf kdtree
        T_np=np_unique_t2
        t_np=np_unique_t1

    #gli indici di nearest neighbour nei due bundle T,t
    dists_nn, index_nn_in_T = map_trk_2_TRK_np_flipInvariant(T_np= T_np, 
                                                             t_np = t_np)


    intersec_streamlines_idx = index_nn_in_T [ np.array(dists_nn) < distCutoff_sameStramline]
    interserc_n_streamlines= len(intersec_streamlines_idx)

    duplic_corresp = len(intersec_streamlines_idx)- len(np.unique(intersec_streamlines_idx))
    if not duplic_corresp == 0:
        print(f"Warning there are streamlines assigned multiple times to the same streamlines in the two tracts!")
        print(f"There are {duplic_corresp} duplicates assignments out of  a total of {len(intersec_streamlines_idx)} intersecting streamlines")


    dsc_streamlines= (2* interserc_n_streamlines) / ( len_t1 +  len_t2)
    
    assert (0<= dsc_streamlines) and ( dsc_streamlines <=1)

    return dsc_streamlines, duplic_corresp

# Load JSON file
# json_path = "/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/info_replic_original_tractograms.json"
# with open(json_path, 'r') as file:
#     sub_dict = json.load(file)

# # Invert dictionary
# inverted_dict = {}
# for key, values in sub_dict.items():
#     for value in values:
#         # Assign original key as value in the new dictionary
#         inverted_dict[value] = key

# Prepare DataFrame
header = ['subj_id', 'bundle_name', 'volume_dice_score', 'source']
dff = pd.DataFrame(columns=header)

# Paths and keywords
csv_path = "/home/alberto/analysis_bundle_stats/tract_info_csv/dsc_streamline_APSS_&_subj_space.csv"

folder_APSS = "/home/alberto/myDataset/APSS_Bundles_Nilab/derivatives/register_to_t1_rigid"


folder_rbx = "/home/alberto/bundles_rbx_APSS"
#APSS_Bundles_Nilab/derivatives/skull_stripped_brain/10_MeGi/10_MeGi__skull_stripped_brain.nii.gz
folder_anat = "/home/alberto/myDataset/APSS_Bundles_Nilab/derivatives/skull_stripped_brain"

keywords = ['AF_L', 'ILF_L', 'IFOF_L', 'FAT_L', 'PYT_L']

source = 'APSS'

# Iterate over subjects and keywords
for sub in os.listdir(folder_rbx):
    for keyword in keywords:
            # value = inverted_dict[sub]
            # print(value)
            # # Conditional path selection based on 'sub' value
            # if value == 'replicated_tractograms':
            #     # Placeholder for specific path or operation for sub == 'your_specific_value_1'
            #     #/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/derivatives/register_to_MNI_affine/sub-1000/sub-1000__FAT_L__DET_PROB__affined_tract_DistCutoff_15.trk
            #     #/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/derivatives/register_to_MNI_affine/sub-1151/sub-1151__PYT_L__DET_PROB_affined_tract_DistCutoff_15.trk
            #     path_trk_1 = f"{folder_nilab2}/{sub}/{sub}__{keyword}__DET_PROB__DistCutoff_15.trk"
            #     print('daje')
            #     pass
            # elif value == 'original_tractograms':
            #     # Placeholder for specific path or operation for sub == 'your_specific_value_2'
            #     path_trk_1 = f"{folder_nilab1}/{sub}/{sub}__{keyword}__DET_PROB.trk"
            #     pass
            # print(path_trk_1)
            #Construct paths
            if keyword == "PYT_L":
                print(keyword)
                path_trk_1 = f"{folder_APSS}/{sub}/{sub}__PT_L__rigid_tract.trk"
                path_trk_2 = f"{folder_rbx}/{sub}/{sub}__{keyword}_cleaned.trk"
                path_anat = f"{folder_anat}/{sub}/{sub}__skull_stripped_brain.nii.gz"

            else:
                path_trk_1 = f"{folder_APSS}/{sub}/{sub}__{keyword}__rigid_tract.trk"
                path_trk_2 = f"{folder_rbx}/{sub}/{sub}__{keyword}_cleaned.trk"
                path_anat = f"{folder_anat}/{sub}/{sub}__skull_stripped_brain.nii.gz"
                # Check if paths exist
            if os.path.exists(path_trk_1) and os.path.exists(path_trk_2) and os.path.exists(path_anat):
                    print(path_trk_1)
                    print(path_trk_2)
                #Compute DSC between the corresponding tracts
                    dsc_same_streamlines, _ = dsc_tracts_streamlines(path_trk_1, path_trk_1, check_rmDupl=True)
                    dsc_streamlines, _ = dsc_tracts_streamlines(path_trk_1, path_trk_2)
                    assert dsc_same_streamlines
                    print(f"DSC between {path_trk_1} and {path_trk_2}")
                    print(f"DSC_Streamlines= {dsc_streamlines}")

                    # Update DataFrame
                    dff = pd.concat([dff, pd.DataFrame({"subj_id": [sub],
                                                        "bundle_name": [keyword],
                                                        "streamline_dice_score": [dsc_streamlines],
                                                        "source": [source]
                                                        })])
            else:
                    print("ouch!")

    # Save DataFrame to CSV
    dff.to_csv(csv_path, index=False)
    # if __name__=="__main__":
    #     sub="sub-1000"
    #     bundle="FAT_L"
    #     path_tractoinferno="/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/"
    #     #let's test the functions..

    #     path_trk_1=f"{path_tractoinferno}derivatives/bundles_extracted_from_replicated_wbts_flipping/{sub}/{sub}__FAT_L__DET_PROB__DistCutoff_15.trk"
    #     path_trk_2=f"{path_tractoinferno}derivatives/bundles_extracted_from_replicated_wbts_flipping/{sub}/{sub}__FAT_L__DET_PROB__DistCutoff_15.trk"
    #     path_anat=f"{path_tractoinferno}/{sub}/anat/{sub}__T1w.nii.gz"

        
    #     #compute dsc between the same tract
    #     dsc_same_streamlines, _=dsc_tracts_streamlines(path_trk_1, path_trk_1, check_rmDupl=True)
    #     assert dsc_same_streamlines 

        
    #     #compute dsc between tracts extracted with 10 dist cutoff or 15 dist cutoff
    #     dsc_streamlines, _=dsc_tracts_streamlines(path_trk_1, path_trk_2)

    #     print(f"DSC between {path_trk_1} and {path_trk_2}")
    #     print(f"DSC_Streamlines= {dsc_streamlines}")
        
        


