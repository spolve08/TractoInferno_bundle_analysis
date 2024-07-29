#!/bin/bash

execute_and_print() {
  local command="$1"
  # Print the command
  echo "Executing: $command"
  
  # Execute the command
  $command
  
  # Print a separator for readability
  echo "---------------------------"
  echo ""
}

atlas_rbx_path="/home/alberto.spolverato/mnt/myDataset/atlas_RBX/atlas_v1.1/atlas_v1.1"
atlas_anat_mni="/home/alberto.spolverato/mnt/myDataset/atlas_RBX/atlas_v1.1/mni_masked.nii.gz"
config_path="/home/alberto.spolverato/mnt/myDataset/atlas_RBX/atlas_v1.1/config_v2.2/config_ind_copy.json"
rbx_main_path="/home/alberto.spolverato/local/rbx_flow/main.nf"
container_scilus_path="/home/alberto.spolverato/mnt/container_scilus/scilus_1.5.0.sif"

vector=("3" "6" "7") 
for i in "${vector[@]}"
do
    dataset_path="/home/alberto.spolverato/mnt/myDataset/TractoInferno/derivatives/input_rbX/batch${i}"
    out_dir="/home/alberto.spolverato/mnt/Experiments/batch${i}"

    mkdir -p $out_dir

    cd $out_dir

    log_file="${out_dir}/log_rbx_originalAtlas_rf.txt"

    echo 'start' >> $log_file

    nextflow_cmd="nextflow run ${rbx_main_path} -with-singularity ${container_scilus_path} -resume --input ${dataset_path} --atlas_directory ${atlas_rbx_path} --atlas_config ${config_path} --atlas_anat ${atlas_anat_mni} --rbx_processes 10 --processes 1 -profile large_dataset,cbrain &> ${log_file}"

    execute_and_print "${nextflow_cmd}"
    echo 'end' >> $log_file

    pwd
done
#"8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "23" "24" "25" "26"
