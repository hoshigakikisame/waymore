#!/usr/bin/env python

import os
import time
import re
import argparse

def auto_dedupe(substr: str, outdir: str):
    # Get the current working directory
    cwd = os.getcwd()
    # Get the list of files in the current working directory
    files = os.listdir(cwd)
    files = [file for file in files if substr in file]
    # custom callback function to sort the files
    files.sort(key=lambda x: int(re.findall(r'\d', x)[0]))
    # Iterate over the list of files
    if len(files) > 1:
        for file in files[:len(files)-1]:
            print(f'Deduping {file}')
            os.system(f'./dedupe.sh {file} {outdir} > /dev/null 2>&1')
    else:
        print('No files to dedupe')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto-dedupe wayback.urls files')
    parser.add_argument('--substr', type=str, help='Substring to match in the file name')
    parser.add_argument('--outdir', type=str, help='Output directory to store the deduped files')
    args = parser.parse_args()

    while True:
        auto_dedupe(args.substr, args.outdir)
        time.sleep(60*5) # Sleep for 5 minutes