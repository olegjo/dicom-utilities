import glob, sys, pydicom, os, glob, fnmatch
import progressbar, argparse

import pydicom.errors

class MatchedSeries:
    def __init__(self, ds: pydicom.Dataset, dicom_file):
        self.ds = ds
        self.dicom_file = dicom_file
        self.series_instance_uid = ds["SeriesInstanceUID"]
    
    def __eq__(self, other: pydicom.Dataset):
        return other["SeriesInstanceUID"] == self.series_instance_uid
    
    def __repr__(self):
        try:
            patient_name = self.ds['PatientName'].value
        except(KeyError):
            patient_name = "UNKNOWN PATIENT NAME"
        
        try:
            series_description = self.ds['SeriesDescription'].value
        except(KeyError):
            series_description = "UNKNOWN SERIES DESCRIPTION"

        return f"{patient_name} -- {series_description} -- {self.dicom_file}"

def check_match(matches, check):
    for m in matches:
        if m == check:
            return True
    return False

def dcmfindseries(input_dir, search_tag, search_value, case_insensitive, verbose=False, show_progress_bar=True):
    matches: list[MatchedSeries] = []

    # All files and directories in the given directory
    all_files = glob.glob(f"{input_dir}/**/*", recursive=True)

    # Filter out directories and keep only files. Can be any file type at this point. We'll filter on DICOM later.
    all_files = list(filter(lambda fname : os.path.isfile(fname), all_files))

    if show_progress_bar:
        # Setup progressbar
        pbar = progressbar.ProgressBar(max_value=len(all_files))
        pbar_i = 0

    for dicom_file in all_files:
        if show_progress_bar:
            pbar.update(pbar_i+1)
            pbar_i += 1

        try:
            ds = pydicom.dcmread(dicom_file)
        except(pydicom.errors.InvalidDicomError):
            continue

        try:
            looked_up_value = ds[search_tag].value
        except(KeyError):
            continue

        if case_insensitive:
            looked_up_value = str(looked_up_value).lower()
            search_tag = str(search_value).lower()

        # Look for the search value in the looked up value. Can have wildcards.
        if fnmatch.fnmatch(looked_up_value, search_value):
            ## Check if this series is already found
            already_found = check_match(matches, ds)

            if not already_found:
                matches.append(MatchedSeries(ds, dicom_file))
                if verbose:
                    print(f"\n\nFOUND: {dicom_file}\n\n")

    return matches

"""
Signatures
dcmfind -q "SeriesDescription==ABC" directory
dcmfind -q "SeriesDescription==*ABC*" directory
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("-q", "--query")
    parser.add_argument("--case-insensitive", default=False, action='store_true')
    parser.add_argument("-v", "--verbose", default=False, action='store_true')
    args = parser.parse_args()

    [search_term, search_value] = args.query.split("==")
    verbose = args.verbose
    case_insensitive = args.case_insensitive

    matches = dcmfindseries(args.directory, search_term, search_value, case_insensitive, verbose, True)

    print()
    print()
    for match in matches:
        print(match)
