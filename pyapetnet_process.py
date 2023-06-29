"""
pyapetnet_process.py
=============
Module to run pyapetnet (https://github.com/gschramm/pyapetnet) in mercure.

This scripts moves PET and MRI DICOM files into seperate input directories and runs pyapetnet.
"""

# Standard Python includes
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path


# Imports for loading DICOMs
import pydicom


def main(args=sys.argv[1:]):
    """
    Main entry function of the . 
    The module is called with two arguments from the function docker-entrypoint.sh:
    'testmodule [input-folder] [output-folder]'. The exact paths of the input-folder 
    and output-folder are provided by mercure via environment variables
    """
    # Print some output, so that it can be seen in the logfile that the module was executed
    print(f"Starting mercure-pyapetnet")

    # Check if the input and output folders are provided as arguments
    if len(sys.argv) < 3:
        print("Error: Missing arguments!")
        print("Usage: testmodule [input-folder] [output-folder]")
        sys.exit(1)

    # Check if the input and output folders actually exist
    in_folder = sys.argv[1]
    out_folder = sys.argv[2]
    if not Path(in_folder).exists() or not Path(out_folder).exists():
        print("IN/OUT paths do not exist")
        sys.exit(1)

    # Load the task.json file, which contains the settings for the processing module
    try:
        with open(Path(in_folder) / "task.json", "r") as json_file:
            task = json.load(json_file)
    except Exception:
        print("Error: Task file task.json not found")
        sys.exit(1)

    # Create default values for all module settings
    settings = {"trained_model": "S2_osem_b10_fdg_pe2i"}

    # Overwrite default values with settings from the task file (if present)
    if task.get("process", ""):
        settings.update(task["process"].get("settings", {}))

    
    # create directories for PET and MRI input files, and CNN output
    current_dir = os.getcwd()
    pet_input_path = os.path.join(current_dir, 'pet_input')
    if not os.path.exists(pet_input_path):
        os.makedirs(pet_input_path)

    mri_input_path = os.path.join(current_dir, 'mri_input')
    if not os.path.exists(mri_input_path):
        os.makedirs(mri_input_path)

    #create output dir for cnn
    cnn_output_path = os.path.join(current_dir, 'cnn_output')
    if not os.path.exists(cnn_output_path):
        os.makedirs(cnn_output_path)

    #read modality and move to relevant input directories
    series = []
    for entry in os.scandir(in_folder):
        if entry.name.endswith(".dcm") and not entry.is_dir():
            
            target_path = ''
            
            dcm_file_in = Path(in_folder) /  entry.name
            ds = pydicom.dcmread(dcm_file_in)
            
            series_number = ds.SeriesInstanceUID
            if series_number not in series:
                series.append(series_number)
                if len(series) >2:
                    print("Error: More than two series in input directory.")
                    sys.exit(1)

            modality = ds.Modality
            if modality=='MR':
                target_path =mri_input_path
                
            if modality=='PT':
                target_path=pet_input_path
                
            
            if (target_path):
                shutil.move(os.path.join(in_folder, entry.name), target_path)
            else:
                print("Error: Error copying files.")
                sys.exit(1)
    
    selected_model=settings["trained_model"]
    
    #run pyapetnet
    subprocess.run(["pyapetnet_predict_from_dicom", pet_input_path, mri_input_path, selected_model, "--output_dir", cnn_output_path])

    results_path = os.path.join(cnn_output_path, 'prediction_' + selected_model)
    

    if Path(results_path).exists():
        results_files = os.listdir(results_path)
        for f in results_files:
            shutil.move(os.path.join(results_path, f), out_folder)






if __name__ == "__main__":
    main()