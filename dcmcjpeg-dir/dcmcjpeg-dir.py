import glob, sys, os, glob

input_dir = sys.argv[1]

# All files and directories in the given directory
all_files = glob.glob(f"{input_dir}/**/*", recursive=True)

for file in all_files:
    os.system(f"dcmcjpeg -v {file} {file}")