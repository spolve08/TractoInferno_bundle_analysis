#!/bin/bash
atlas_rbx_path="/home/alberto.spolverato/mnt/myDataset/atlas_RBX/atlas_v1.1/atlas_v1.1"
atlas_anat_mni="mnt/myDataset/atlas_RBX/atlas_v1.1/mni_masked.nii.gz"
config_path="mnt/myDataset/atlas_RBX/atlas_v1.1/config_v2.2/config_ind_copy.json"
rbx_main_path="/home/alberto.spolverato/local/rbx_flow/main_copy.nf"
container_scilus_path="/home/alberto.spolverato/mnt/container_scilus/scilus_1.5.0.sif"
dataset_path="/home/alberto.spolverato/mnt/myDataset/TractoInferno/derivatives/input_rbX/batch3"
out_dir="/home/alberto.spolverato/mnt/Experiments/batch3"
mkdir -p $out_dir
cd $out_dir
log_file="${out_dir}/log_rbx_originalAtlas_rf.txt"
nextflow run $rbx_main_path -with-singularity $container_scilus_path -resume --input $dataset_path --atlas_directory $atlas_rbx_path --atlas_config $config_path --atlas_anat $atlas_anat_mni --rbx_processes 10 --processes 1 -profile large_dataset,cbrain  &>> $log_file
