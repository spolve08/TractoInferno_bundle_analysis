#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 20:24:07 2024

@author: chiara
"""

import os
import sys
import numpy as np
import nibabel as nib 

home_path=os.environ["HOME"] 
repo_path=f"{home_path}/local/tracto_anomaly/"

path_nilab_repo = home_path + "/local/nilab/"
repo_utils_path=f"{repo_path}/utils/"

sys.path.append(repo_utils_path)
sys.path.append(path_nilab_repo)

from utils_trk import map_trk_2_TRK_np_flipInvariant, rm_duplicates_streamlines_path_trk, rm_duplicates_streamlines_np, check_nps_is_the_same


def sensitivity_tracts_streamlines(tract_pred, tract_gt, distCutoff_sameStramline=0.01, check_rmDupl=False):

    #in the same tract, there can be duplicates streamlines!!!
    #same of the streamlines can be identical!
    #important: you can't switch gt and pred
    #it computes the number of 
            #TP/ (TP + FN) =  TP/TOT_positive = true positive / total number of streamlines of ground truth

    #1. rm duplicates streamlines
    print("\nRm duplicates streamlines")
    np_unique_pred = rm_duplicates_streamlines_path_trk(tract_pred, sanity_check=check_rmDupl)
    np_unique_gt = rm_duplicates_streamlines_path_trk(tract_gt,  sanity_check=check_rmDupl)

    print("Compute dsc")

    len_pred, len_gt = len(np_unique_pred), len(np_unique_gt)

    if len_pred>=len_gt:
        #if t1 has more streamlines than t2, or the number of streamlines is even 
        #use t1 to build kdtree
        T_np=np_unique_pred
        t_np=np_unique_gt
    else:
        #if t2 has more streamline than t1, use t2 to builf kdtree
        T_np=np_unique_gt
        t_np=np_unique_pred


    dists_nn, index_nn_in_T = map_trk_2_TRK_np_flipInvariant(T_np= T_np, 
                                                             t_np = t_np)


    intersec_streamlines_idx = index_nn_in_T [ np.array(dists_nn) < distCutoff_sameStramline]
    interserc_n_streamlines= len(intersec_streamlines_idx) #true positive
    
                    #True positive / total positive
    sensitivity = interserc_n_streamlines / len_gt  
    
    assert (0<= sensitivity) and ( sensitivity <=1)

    return sensitivity




if __name__=="__main__":
    sub="sub-1000"
    bundle="FAT_L"
    path_tractoinferno="/home/chiara/datasets/TractoInferno_Nilab/"
    #let's test the functions..

    path_trk_1=f"{path_tractoinferno}//derivatives/bundles_extracted_from_replicated_wbts_flipping/{sub}/{sub}__FAT_L__DET_PROB__DistCutoff_15.trk"
    path_trk_2=f"{path_tractoinferno}//derivatives/bundles_extracted_from_replicated_wbts_flipping/{sub}/{sub}__FAT_L__DET_PROB__DistCutoff_10.trk"
    path_anat=f"{path_tractoinferno}/{sub}/anat/{sub}__T1w.nii.gz"
    
    #compute sensitivity between the same bundle    
    sens_same_bdl = sensitivity_tracts_streamlines(path_trk_1, path_trk_1, check_rmDupl=True)
    assert sens_same_bdl
    
    sens_bdl = sensitivity_tracts_streamlines(path_trk_1, path_trk_2, check_rmDupl=True)

    print(f"sensitivity between PRED {path_trk_1} and  GT {path_trk_2}")
    print(f"sensitivity_streamlines= {sens_bdl}")
    #%%
    sens_bdl = sensitivity_tracts_streamlines(path_trk_2, path_trk_1, check_rmDupl=True)
 
    print(f"sensitivity between PRED {path_trk_2} and  GT {path_trk_1}")
    print(f"sensitivity_streamlines= {sens_bdl}")
   
    