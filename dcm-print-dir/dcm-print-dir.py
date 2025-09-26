import glob, sys, pydicom, os
import progressbar
from tabulate import tabulate

import pydicom.misc

def get_tag_value(ds: pydicom.Dataset, tag: str):
    try:
        ret = str(ds[tag].value)
    except(KeyError):
        ret = "NOT FOUND"
    return ret

def print_dicom_meta_in_dir(input_dir, output_format):
    # dicom_tags_to_get = ["SeriesInstanceUID"]
    dicom_tags_to_get = ["PatientName", "PatientSex", "SeriesDescription", "SeriesDescription", "Manufacturer", "ImageType", "Rows", "Columns", "SpacingBetweenSlices", "SliceThickness", "PixelSpacing", "RepetitionTime", "EchoTime", "FlipAngle", "SOPClassUID", "NumberOfFrames", "MagneticFieldStrength", "Modality", "NUMBER_OF_FILES", "FILE_PATH"]

    # All dicom files
    all_files = [filename for filename in glob.glob(f"{input_dir}/**/*", recursive=True) if os.path.isfile(filename) and pydicom.misc.is_dicom(filename)]

    series_instance_uid_map = {}

    # Setup progressbar
    pbar = progressbar.ProgressBar(max_value=len(all_files))
    pbar_i = 0

    for dicom_file in all_files:
        pbar.update(pbar_i+1)
        pbar_i += 1
        
        ds = pydicom.dcmread(dicom_file)
        
        try:
            series_instance_uid = ds["SeriesInstanceUID"].value
            if series_instance_uid in series_instance_uid_map:
                series_instance_uid_map[series_instance_uid]["NUMBER_OF_FILES"] += 1
                continue

            series_instance_uid_map[series_instance_uid] = {
                "NUMBER_OF_FILES": 0,
                "FILE_PATH": dicom_file
            }

        except(KeyError):
            continue

        
        for tag in dicom_tags_to_get:
            if tag in ["NUMBER_OF_FILES", "FILE_PATH"]:
                continue
            series_instance_uid_map[series_instance_uid][tag] = get_tag_value(ds, tag)
        
        series_instance_uid_map[series_instance_uid]["NUMBER_OF_FILES"] += 1
    

    if "CSV" in output_format:
        s = ";".join(dicom_tags_to_get)
        for uid in series_instance_uid_map:
            s += "\n"
            s += ";".join([f"{series_instance_uid_map[uid][key]}" for key in dicom_tags_to_get])
        print(s)

    if "pretty_print" in output_format:
        table = []
        for uid in series_instance_uid_map:
            table.append([f"{series_instance_uid_map[uid][key]}" for key in dicom_tags_to_get])

        print(tabulate(table, headers=dicom_tags_to_get, tablefmt="fancy_grid"))
        
if __name__ == "__main__":
    output_format = "pretty_print|CSV" # CSV or pretty_print
    print_dicom_meta_in_dir(sys.argv[1], output_format)
