"""
This script can be used to modify tags in a directory of DICOM files such that 
the files will be interpreted as a new patient.

PLEASE USE A COPY OF THE OLD PATIENT AS THIS WILL OVERWRITE THE DICOM FILES WITHOUT BACKUP!

NOTE:
* The DICOM files have to have .dcm extension
"""
import glob, sys, pydicom, os
import progressbar, argparse

def modify_to_new_patient(input_dir):
    # All files and directories ending with .txt and that don't begin with a dot:
    all_files = glob.glob(f"{input_dir}/**/*.dcm", recursive=True)

    patient_names_map = {}
    patient_id_map = {}
    series_instance_uid_map = {}
    study_instance_uid_map = {}

    for dicom_file in all_files:
        ds = pydicom.dcmread(dicom_file)

        old_patient_name = ds["PatientName"].value
        if old_patient_name not in patient_names_map:
            print(f"Old patient name was '{old_patient_name}'")
            new_patient_name = input("What is the new patient name? ")
            patient_names_map[old_patient_name] = new_patient_name

            old_patient_id = ds["PatientID"].value
            print(f"Old patient ID was '{old_patient_id}'")
            new_patient_id = input("What is the new patient ID? ")
            patient_id_map[old_patient_name] = new_patient_id

    for dicom_file in all_files:
        ds = pydicom.dcmread(dicom_file)

        old_patient_name = ds["PatientName"].value
        new_patient_name = patient_names_map[old_patient_name]
        new_patient_id = patient_id_map[old_patient_name]
        
        old_series_instance_uid = ds["SeriesInstanceUID"].value
        if old_series_instance_uid not in series_instance_uid_map:
            new_series_instance_uid = pydicom.uid.generate_uid()
            series_instance_uid_map[old_series_instance_uid] = new_series_instance_uid
        else:
            new_series_instance_uid = series_instance_uid_map[old_series_instance_uid]
        
        old_study_instance_uid = ds["StudyInstanceUID"].value
        if old_study_instance_uid not in study_instance_uid_map:
            new_study_instance_uid = pydicom.uid.generate_uid()
            study_instance_uid_map[old_study_instance_uid] = new_study_instance_uid
        else:
            new_study_instance_uid = study_instance_uid_map[old_study_instance_uid]
        
        os.system(f'dcmodify --verbose --gen-inst-uid --no-backup --modify "(0010,0010)={new_patient_name}" --modify "(0010,0020)={new_patient_id}" --modify "(0020,000D)={new_study_instance_uid}" --modify "(0020,000E)={new_series_instance_uid}" "{dicom_file}"')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise NotADirectoryError("Second argument must be a directory")
    
    modify_to_new_patient(sys.argv[1])
