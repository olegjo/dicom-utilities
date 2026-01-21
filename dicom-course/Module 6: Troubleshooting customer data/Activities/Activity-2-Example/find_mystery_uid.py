import glob, sys, pydicom, os
import pydicom.misc

def find_mystery_uid(input_dir):
    # All dicom files
    all_files = [filename for filename in glob.glob(f"{input_dir}/**/*", recursive=True) if os.path.isfile(filename) and pydicom.misc.is_dicom(filename)]
    for dicom_file in all_files:

        print(f"Checking file... {dicom_file}")
        os.system(f"dcmdump {dicom_file} | grep 1.3.46.670589.11.0.0.12.2")

if __name__ == "__main__":
    find_mystery_uid(sys.argv[1])
