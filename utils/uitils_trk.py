

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Aug 28 9:17:59 2024

@author: chiara

Script to collect utils functions to analyse tractographies  

TO run the script it is necessary to clone the repository git
    https://github.com/FBK-NILab/nilab.git

in the path
    ${HOME}/local/ 

"""
import numpy as np
import sys
import os
from dipy.tracking.streamline import set_number_of_points
from scipy.spatial import KDTree
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.io.stateful_tractogram import Space, StatefulTractogram
import nibabel as nib
from dipy.tracking.utils import density_map
import gc


home_path=os.environ["HOME"] 
repo_path=f"{home_path}/local/tracto_anomaly/"
trk_bd_2_TRK_path=f"{repo_path}/preprocessing/trk_bundle__2___trk_WBTractography/"

path_nilab_repo = home_path + "/local/nilab/"
repo_utils_path=f"{repo_path}/utils/"

sys.path.append(repo_utils_path)
sys.path.append(path_nilab_repo)
sys.path.append(trk_bd_2_TRK_path)



#import from nilab
from load_trk_numba import load_streamlines 
from nearest_neighbors import streamlines_neighbors
#%%

N_RESAMPLE_Ps=40

def delete_from_mem(objects):
    if len(objects)==1:
        del ob 
    else:
        for ob in objects:
            #free some memory
            del ob 
    gc.collect()

def check_nps_is_the_same(np_1, np_2):
    #this function check if a numpy array is the same as another np array
    #the assumption is it has the same dimension

    assert len(np_1)== len(np_2)

    diff = np_1 - np_2
    sumDiff= np.sum(np.array([np.sum(d) for d in diff]))

    #if sumDiff is zero, then nps_is_the_same=True
    nps_is_the_same= not sumDiff

    return nps_is_the_same


def map_trk_2_TRK_np_flipInvariant(T_np, t_np, n_resample_p=N_RESAMPLE_Ps):
    """
    It returns the index in path_TRK that are nearest neighbours of each streamline in path_trk,
    and the distances,  by using KDtree.
    These nearest neighbours found are invariant to flipping.
    """
   
    n_fibers_T=len(T_np)
    print(f"N streamlines T_np:    {n_fibers_T}")

    n_fibers_t=len(t_np)
    print(f"N streamlines t_np:    {n_fibers_t}")

    #resample to the same numb of points (the reshaping in 2d is done internally by streamlines_neighbors )
    T_n40=np.array([set_number_of_points(s,n_resample_p) for s in T_np])    
    t_n40=np.array([set_number_of_points(s,n_resample_p) for s in t_np])
    
    delete_from_mem([T_np, t_np])

    dists_nn, index_nn_in_T = streamlines_neighbors(streamlines=t_n40, 
                                                    tractogram=T_n40, k=1, verbose=False)

    return dists_nn, index_nn_in_T



def rm_duplicates_streamlines_np(t_np,  distCutoff_sameStramline=0.01):
    """
    Function to return tractogram without duplicates. Its input and output are numpy array 
    """
    dists_nn, index_nn_in_T = map_trk_2_TRK_np_flipInvariant(T_np= t_np, 
                                                             t_np = t_np)

    #check all distance are zeros - it must be so since I am searching nearest neighbour comparing the tract with itself
    assert np.sum(np.array(dists_nn) < distCutoff_sameStramline) == len(t_np)
    
    index_t_unique = np.sort(np.unique(index_nn_in_T))
    t_np_unique = t_np[index_t_unique]

    return t_np_unique

def rm_duplicates_streamlines_path_trk(path_trk,  path_trk_unique=None, path_anatomy=None, distCutoff_sameStramline=0.01, sanity_check=False):
    """
    Function to return tractogram without duplicates. Its input are path of trk.
     THe output are a np.array or optionally can save the trk unique to file
     TODO: the saving of the filetered tract has to be tested yet
    """
    print("Remove duplicates in the same tract")
    t_np, t_header, t_lengths, t_idxs = load_streamlines(path_trk, container='array', verbose=False)
    t_np_unique = rm_duplicates_streamlines_np(t_np,  distCutoff_sameStramline=distCutoff_sameStramline)


    if sanity_check:
        #sanity check: if I rm again duplicates the result shoul not change
        print("\nRm duplicates streamlines sanity check")
        t_np_unique_check = rm_duplicates_streamlines_np(t_np_unique)
        assert check_nps_is_the_same(t_np_unique_check, t_np_unique)


    if path_trk_unique is not None:
        #TODO: to test
        assert path_anatomy is not None
        trk_sft = StatefulTractogram(t_np_unique, path_anatomy, Space.RASMM) 
        save_tractogram(trk_sft, path_trk_unique)
    

    return t_np_unique