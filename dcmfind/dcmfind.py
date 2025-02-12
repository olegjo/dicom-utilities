import glob, sys, pydicom, os, glob
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

        return f"d{patient_name} -- {series_description} -- {self.dicom_file}"



def check_match(matches, check):
    for m in matches:
        if m == check:
            return True
    return False


def dcmfindseries(input_dir, search_tag, search_value, verbose=False, show_progress_bar=True):
    matches: list[MatchedSeries] = []

    # All files and directories ending with .txt and that don't begin with a dot:
    all_files = glob.glob(f"{input_dir}/**/*.dcm", recursive=True)

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

        if search_value in looked_up_value:
            ## Check if this series is already found
            already_found = check_match(matches, ds)

            if not already_found:
                matches.append(MatchedSeries(ds, dicom_file))
                if verbose:
                    print(f"FOUND: {dicom_file}")

    return matches

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("-m", "--match")
    parser.add_argument("-v", "--verbose", default=False)
    args = parser.parse_args()

    [query, value] = args.match.split("=")
    verbose = args.verbose

    matches = dcmfindseries(args.directory, query, value, verbose, True)

    print()
    print()
    for match in matches:
        print(match)
