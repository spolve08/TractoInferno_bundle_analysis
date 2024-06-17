import nibabel as nib
import numpy as np
import os
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.tracking.utils import density_map
import matplotlib.pylab as plt
import pandas as pd
from os.path import dirname as up
import re
import csv

# AF_L 
# ILF_L
# IFOF_L
# FAT_L
# PYT_L
#/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/sub-1000/tractography/sub-1000__FAT_L.trk

cutoff = 1
#extracting the subject id
subjs_id_all = []
sub_id = []
keywords = ['AF_L', 'ILF_L', 'IFOF_L', 'FAT_L', 'PYT_L']
dataset_path = '/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/'
csv_path = '/home/alberto/analysis_bundle_stats/tract_info.csv'

# Prepare the CSV file and write the header
with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    header = ['bundle_name', 'subject_id', 'affine', 'dimensions', 'voxel_sizes', 'voxel_order']
    writer.writerow(header)

for item in os.listdir(dataset_path):
    item_path = os.path.join(dataset_path, item)
    if os.path.isdir(item_path) and item.startswith('sub'):       
        subjs_id_all.append(item)
        sub_id = item
subjs_id_all.sort()
for id in subjs_id_all:
    dir_subj_out=f'/home/alberto/analysis_bundle_stats/{id}/'
    tract_path = f'/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/{id}/tractography/'
    for bundle in os.listdir(tract_path):
        bundle_path = os.path.join(tract_path, bundle)
        if os.path.isfile(bundle_path):
            for keyword in keywords:
                if keyword in bundle_path:
                    mask_bundle_path = f'{dir_subj_out}/mask_{keyword}_{id}.nii'
                    density_bundle_path = f'{dir_subj_out}/density_{keyword}_{id}.nii' 
                    tract_all = nib.streamlines.load(bundle_path, lazy_load=False)
                    tract = np.array(tract_all.streamlines, dtype=object)
                    aff = tract_all.affine
                    dim = tract_all.header['dimensions']
                    voxel_sizes = tract_all.header['voxel_sizes']
                    voxel_order = tract_all.header['voxel_order']
                    dens_map = density_map(tract, aff, dim) 
                    mask_bd= dens_map>=cutoff
                    mask_bd=mask_bd.astype(np.uint8)
                    # if not os.path.exists(dir_subj_out):
                    #     os.makedirs(dir_subj_out)

                    # bdl_mask = nib.Nifti1Image(mask_bd, reference_anatomy.affine, reference_anatomy.header)
                    # nib.save(bdl_mask, mask_bundle_path)
                    # density = nib.Nifti1Image(dens_map, reference_anatomy.affine, reference_anatomy.header)
                    # nib.save(density, density_bundle_path)

                    with open(csv_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([bundle, id, aff.tolist(), dim.tolist(), voxel_sizes.tolist(), voxel_order])




















#mask_bundle_path = f'{dir_subj_out}/CC_Fr_mask_{sub_id}.nii'
#density_bundle_path = f'{dir_subj_out}/CC_Fr_density_{sub_id}.nii'
#p_trk=f"/home/alberto/TractoInferno_sample/{sub_id}/tractography/{sub_id}__CC_Fr_2.trk" #path of the bundle trk  

# reference_anatomy = nib.load(anat_path)
#tract_all = nib.streamlines.load(p_trk, lazy_load=False)
#print(len(tract_all.streamlines))
#tract_all = load_tractogram(p_trk, reference_anatomy)
# for i, item in enumerate(tract_all.streamlines):
# 	print(len(item))

# tract = np.array(tract_all.streamlines, dtype=object)
# aff = tract_all.affine
# dim = tract_all.header['dimensions']
# voxel_sizes = tract_all.header['voxel_sizes']
# voxel_order = tract_all.header['voxel_order']
# print(aff)
# print(dim)
# print(voxel_sizes)
# print(voxel_order)
# dens_map = density_map(tract, aff, dim) 

# mask_bd= dens_map>=cutoff
# mask_bd=mask_bd.astype(np.uint8)

#dir_out_mask = os.path.dirname(mask_bundle_path)
# if not os.path.exists(dir_subj_out):
#     os.makedirs(dir_subj_out)

# bdl_mask = nib.Nifti1Image(mask_bd, reference_anatomy.affine, reference_anatomy.header)
# nib.save(bdl_mask, mask_bundle_path)


# density = nib.Nifti1Image(dens_map, reference_anatomy.affine, reference_anatomy.header)
# nib.save(density, density_bundle_path)


# def plot_density_map(dens_map, slices=None):
#     if slices is None:
#         slices = [dens_map.shape[0] // 2, dens_map.shape[1] // 2, dens_map.shape[2] // 2]

#     fig, axes = plt.subplots(1, 3, figsize=(15, 5))
#     fig.suptitle('Density Map Slices')

#     # Plot the middle slice in each dimension
#     axes[0].imshow(dens_map[slices[0], :, :], cmap='gray')
#     axes[0].set_title(f'Slice {slices[0]} in X')
#     axes[0].axis('off')

#     axes[1].imshow(dens_map[:, slices[1], :], cmap='gray')
#     axes[1].set_title(f'Slice {slices[1]} in Y')
#     axes[1].axis('off')

#     axes[2].imshow(dens_map[:, :, slices[2]], cmap='gray')
#     axes[2].set_title(f'Slice {slices[2]} in Z')
#     axes[2].axis('off')

#     plt.show()

# # Call the plot function
# plot_density_map(dens_map)


