import glob, sys, pydicom, os, glob, fnmatch
import progressbar, argparse
from typing import Optional

import pydicom.errors

class MatchedSeries:
    def __init__(self, ds: pydicom.Dataset):
        self.ds = ds
        self.series_instance_uid = ds["SeriesInstanceUID"]
        try:
            self.patient_name = ds["PatientName"].value
        except(KeyError):
            self.patient_name = "UNKNOWN"

        self.file_paths = []
    
    def __eq__(self, other: pydicom.Dataset):
        try:
            patient_name = other["PatientName"].value
        except(KeyError):
            patient_name = "UNKNOWN"

        return other["SeriesInstanceUID"] == self.series_instance_uid and patient_name == self.patient_name
    
    def __repr__(self):        
        try:
            series_description = self.ds['SeriesDescription'].value
        except(KeyError):
            series_description = "UNKNOWN SERIES DESCRIPTION"

        ret = "="*100
        ret += f"\nPatientName         {self.patient_name}"
        ret += f"\nSeriesDescription   {series_description}"
        ret += f"\nFound in the following locations:"

        unique_dirnames = []
        for f in self.file_paths:
            dirname = os.path.abspath(os.path.dirname(f))
            if dirname not in unique_dirnames:
                unique_dirnames.append(dirname)
        
        for dirname in unique_dirnames:
            ret += f"\n\t\t- {dirname}"
        return ret
    
    def add_file(self, path):
        self.file_paths.append(path)

def check_match(matches, check) -> Optional[MatchedSeries]:
    for m in matches:
        if m == check:
            return m
    return None

def dcmfindseries(input_dir, search_tag, search_value, case_insensitive, show_progress_bar=True):
    matches: list[MatchedSeries] = []

    if case_insensitive:
        search_value = str(search_value).lower()

    # All files and directories in the given directory
    all_files = glob.glob(f"{input_dir}/**/*", recursive=True)

    # Filter out directories and keep only files. Can be any file type at this point. We'll filter on DICOM later.
    all_files = list(filter(lambda fname : os.path.isfile(fname), all_files))

    if show_progress_bar:
        # Setup progressbar
        pbar = progressbar.ProgressBar(max_value=len(all_files))
        pbar_i = 0
    
    # Loop through all dicom files and check if query is fulfilled
    for dicom_file in all_files:
        if show_progress_bar:
            pbar.update(pbar_i+1)
            pbar_i += 1

        try:
            ds = pydicom.dcmread(dicom_file)
        except(pydicom.errors.InvalidDicomError):
            continue

        try:
            looked_up_value = str(ds[search_tag].value)
        except(KeyError) as e:
            continue

        if case_insensitive:
            looked_up_value = str(looked_up_value).lower()

        # Look for the search value in the looked up value. Can have wildcards.
        if fnmatch.fnmatch(looked_up_value, search_value):
            ## Check if this series is already found
            already_found = check_match(matches, ds)

            if already_found is None:
                m = MatchedSeries(ds)
                m.add_file(dicom_file)
                matches.append(m)
            else:
                m.add_file(dicom_file)

    return matches

"""
Signatures
dcmfind -q "SeriesDescription==ABC" directory
dcmfind -q "SeriesDescription==*ABC*" directory
"""

if __name__ == "__main__":
    parser_usagetext = """
This tool can be used to find DICOM files or directories containing DICOM files that fulfil a given search query.
For example, if you have a folder structure that contains DICOM files, and you are looking for all DICOM files 
where the SeriesDescription equals "My_series_description", you can search like this:

\t>> dcmfind -q "SeriesDescription==My_series_description" /path/to/folder

The dcmfind tool will recursively find all files in /path/to/folder that fulfils the search criterion.

You may also use wildcards:

\t>> dcmfind -q "SeriesDescription==*_series_" /path/to/folder

This will return all folders that contain DICOM files, who's Series Descriptions match the wildcard query *_series_*

"""
    parser = argparse.ArgumentParser(prog="dcmfind", epilog=parser_usagetext, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory")
    parser.add_argument("-q", "--query")
    parser.add_argument("--case-insensitive", default=False, action='store_true')
    args = parser.parse_args()

    [search_term, search_value] = args.query.split("==")
    case_insensitive = args.case_insensitive

    matches = dcmfindseries(args.directory, search_term, search_value, case_insensitive, True)

    print()
    print()
    for match in matches:
        print(match)
