# volume dice score

import nibabel as nib
import numpy as np
import os
import pandas as pd

header =['subj_id', 'bundle_name', 'volume_dice_score']

dff=pd.DataFrame(columns=header)
home_path=os.environ["HOME"]
bundle_mask = "/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/derivatives/bundles_masks/"
keywords = ['AF_L', 'ILF_L', 'IFOF_L', 'FAT_L', 'PYT_L']
csv_path = f"{home_path}/analysis_bundle_stats/volume_dice_score.csv"
Data_array_list = []
for subj_id in os.listdir(bundle_mask):
    for keyword in keywords:
        # Load the NIfTI file
        nifti_file_path_1= f'/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/derivatives/bundles_masks/{subj_id}/{subj_id}__{keyword}__mask.nii.gz'  # Adjust the path to your NIfTI file
        nifti_file_path_2= f'/home/alberto/hd14tb/TractoInferno_Nilab_DetProb/derivatives/bundles_masks_4algh/{subj_id}/{subj_id}__{keyword}__mask.nii.gz'  # Adjust the path to your NIfTI file
        if os.path.isfile(nifti_file_path_1) and os.path.isfile(nifti_file_path_2):
            nifti_img1 = nib.load(nifti_file_path_1)
            nifti_img2 = nib.load(nifti_file_path_2)
            # Get the data as a NumPy array
            binary_mask1 = nifti_img1.get_fdata()
            binary_mask1 = np.array(binary_mask1, dtype=np.int32)  # Ensure it is an integer array (0s and 1s)
            binary_mask2 = nifti_img2.get_fdata()
            binary_mask2 = np.array(binary_mask2, dtype=np.int32)  # Ensure it is an integer array (0s and 1s)
            # Check the shape of the array to confirm its dimensions
            print(binary_mask1.shape)
            print(binary_mask2.shape)
            def dice_score(mask1, mask2):
                """Calculate the Dice Coefficient between two binary masks."""
                intersection = np.sum(mask1 * mask2)
                total = np.sum(mask1) + np.sum(mask2)
                if total == 0:
                    return 1.0  # Both masks are empty, perfect similarity
                return 2. * intersection / total
            
            # Usage
            dice_coefficient = dice_score(binary_mask1, binary_mask2)
            dff = pd.concat([dff, pd.DataFrame({"subj_id": [subj_id],
                                                "bundle_name":[keyword],
                                                "volume_dice_score": [dice_coefficient],})])
                            
            print("Dice Score:", dice_coefficient)
dff.to_csv(csv_path,index=False)