import glob, sys, pydicom, os
import pydicom.misc

def check_transfer_syntax(input_dir):
    # All dicom files
    all_files = [filename for filename in glob.glob(f"{input_dir}/**/*", recursive=True) if os.path.isfile(filename) and pydicom.misc.is_dicom(filename)]

    transfer_syntax_uids = []
    for dicom_file in all_files:
        ds = pydicom.dcmread(dicom_file)
        inst_uid = ds.file_meta.TransferSyntaxUID 
        if not inst_uid in transfer_syntax_uids:
            transfer_syntax_uids.append(inst_uid)
    
        print(f"Transfer syntax was {inst_uid} for file {dicom_file}")

    if len(transfer_syntax_uids) > 1:
        print("Some transfer syntaxes were different. This is a problem.")
    else:
        print("All transfer syntaxes were the same")

if __name__ == "__main__":
    check_transfer_syntax(sys.argv[1])
