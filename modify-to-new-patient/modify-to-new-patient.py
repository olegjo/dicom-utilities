"""
This script can be used to modify tags in a directory of DICOM files such that 
the files will be interpreted as a new patient.

PLEASE USE A COPY OF THE OLD PATIENT AS THIS WILL OVERWRITE THE DICOM FILES WITHOUT BACKUP!

NOTE:
* The DICOM files have to have .dcm extension
"""
import glob, sys, pydicom, os
import progressbar, argparse

import pydicom.misc

def modify_to_new_patient(input_dir, dry_run):
    # All dicom files
    all_files = [filename for filename in glob.glob(f"{input_dir}/**/*", recursive=True) if os.path.isfile(filename) and pydicom.misc.is_dicom(filename)]

    patient_names_map = {}
    patient_id_map = {}
    patient_birthdate_map = {}
    series_instance_uid_map = {}
    study_instance_uid_map = {}

    print(f"{len(all_files)} DICOM files detected")

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

            old_patient_birth_date = ds["PatientBirthDate"].value
            print(f"Old PatientBirthDate was '{old_patient_birth_date}'")
            new_patient_birth_date = input("What is the new PatientBirthDate? ")
            patient_birthdate_map[old_patient_name] = new_patient_birth_date

    for dicom_file in all_files:
        ds = pydicom.dcmread(dicom_file)

        old_patient_name = ds["PatientName"].value
        new_patient_name = patient_names_map[old_patient_name]
        new_patient_id = patient_id_map[old_patient_name]
        new_patient_birth_date = patient_birthdate_map[old_patient_name]
        
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
        
        command = f'dcmodify --verbose --gen-inst-uid --no-backup --modify "(0010,0010)={new_patient_name}" --modify "(0010,0020)={new_patient_id}" --modify "(0010,0030)={new_patient_birth_date}" --modify "(0020,000D)={new_study_instance_uid}" --modify "(0020,000E)={new_series_instance_uid}" "{dicom_file}"'
        if dry_run:
            print(f"DRY RUN (not executed): {command}")
        else:
            os.system(command)
        

if __name__ == "__main__":
    parser_usagetext = """
This tool can be used to "move" a set of DICOM files to a new patient. The following DICOM tags will be modified in place:
* Patient name
* Patient ID
* Patient birth date
* Series instance UID
* Study instance UID

"""
    parser = argparse.ArgumentParser(prog="modify-to-new-patient", epilog=parser_usagetext, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory")
    parser.add_argument("--dry-run", default=False, action="store_true")
    args = parser.parse_args()

    directory = args.directory
    dry_run = args.dry_run

    # if len(sys.argv) != 2:
    #     raise NotADirectoryError("Second argument must be a directory")
    
    modify_to_new_patient(directory, dry_run)
