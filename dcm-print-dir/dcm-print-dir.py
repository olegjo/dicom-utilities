import glob, sys, pydicom, os
import progressbar

import pydicom.misc

def get_tag_value(ds: pydicom.Dataset, tag: str):
    try:
        ret = str(ds[tag].value)
    except(KeyError):
        ret = "NOT FOUND"
    return ret

def print_dicom_meta_in_dir(input_dir):
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
                continue
        except(KeyError):
            continue

        # dicom_tags_to_get = ["SeriesInstanceUID"]
        dicom_tags_to_get = ["PatientName", "SeriesDescription"]

        series_instance_uid_map[series_instance_uid] = {}
        for tag in dicom_tags_to_get:
            series_instance_uid_map[series_instance_uid][tag] = get_tag_value(ds, tag)
        
    s = ";".join(dicom_tags_to_get)
    
    for uid in series_instance_uid_map:
        s += "\n"
        s += ";".join([series_instance_uid_map[uid][key] for key in dicom_tags_to_get])

    print(s)
        
if __name__ == "__main__":
    print_dicom_meta_in_dir(sys.argv[1])
