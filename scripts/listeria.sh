#!/bin/bash

# General Options
scripts_directory="scripts/" # this project's scripts directory
work_directory="/tmp/"
output_directory="/tmp/"
queue_size=4
profile="docker"

# GAS Nomenclature Nextflow Pipeline
gas_repo="phac-nml/gasnomenclature"
gas_version="0.3.0"
gas_params="https://raw.githubusercontent.com/phac-nml/schedule-pipelines/refs/heads/main/config/gasnomenclature-listeria.json"
gas_input="https://raw.githubusercontent.com/phac-nml/schedule-pipelines/refs/heads/main/test/data/samplesheet_gasnomenclasture.csv"
gas_work_directory="$work_directory/gasnomenclature/work/"
gas_output_directory="$output_directory/gasnomenclature/output/"
gas_irida_json="$gas_output_directory/iridanext.output.json.gz"

# Update Sample Sheet Python Script
update_script="$scripts_directory/update-samplesheet.py"
update_output="$output_directory/updated_samplesheet.csv"

# Arborator Nextflow Pipeline
arborator_detection_repo="phac-nml/arboratornf"
arborator_detection_version="0.3.2"
arborator_detection_params="https://raw.githubusercontent.com/phac-nml/schedule-pipelines/refs/heads/main/config/arboratornf-detection-listeria.json"
arborator_detection_samplesheet="test/data/samplesheet_arborator.csv"
arborator_detection_work_directory="$work_directory/arborator_detection/work/"
arborator_detection_output_directory="$output_directory/arborator_detection/output/"

# Post-Processing Python Script
post_script="$scripts_directory/post-processing.py"
post_output="$output_directory/post/"

nextflow run $gas_repo -r $gas_version --input $gas_input -w $gas_work_directory -profile $profile -params-file $gas_params -queue-size $queue_size --outdir $gas_output_directory
python $update_script --json $gas_irida_json --samplesheet $arborator_detection_samplesheet --output $update_output
nextflow run $arborator_detection_repo -r $arborator_detection_version --input $update_output -w $arborator_detection_work_directory -profile $profile -params-file $arborator_detection_params -queue-size $queue_size --outdir $arborator_detection_output_directory
python $post_script --gasnomenclature $gas_output_directory --arborator $arborator_detection_output_directory --output $post_output
