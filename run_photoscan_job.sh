#/bin/bash
#$ -pe smp 16
#Prefer the RSE qeueu
#$ -P rse
#$ -l h_rt=24:00:00
agisoft_dir=~/photoscan/photoscan-pro
input_dir=/shared/ddcf2/Shared/Group3

(time $agisoft_dir/photoscan.sh -r ./run_agisoft_workflow.py $input_dir) 2>&1 | tee photoscan_output.txt

