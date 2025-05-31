#!/usr/bin/env python

import os
import time
import re
import argparse

def auto_dedupe(substr: str, outdir: str, delresult: bool):
    # Get the current working directory
    cwd = os.getcwd()
    # Get the list of files in the current working directory
    files = os.listdir(cwd)
    files = [file for file in files if substr in file]
    # custom callback function to sort the files
    files.sort(key=lambda x: int(re.findall(r'\d', x)[0]))
    # Iterate over the list of files
    if len(files) > 0:
        print(files)
        for file in files:
            print(f'[+] Deduping {file}')
            cmd = f'cat {file} | urldedupe > "{outdir}/urldedupe.{file}" && rm -rf {file}'
            os.system(cmd)
            print(f'[+] Sending Notification')
            cmd = f'kabarin -f {outdir}/urldedupe.{file} -cs 500'
            os.system(cmd)
            if delresult:
                cmd = f'rm -rf {outdir}/urldedupe.{file}'
                os.system(cmd)
    else:
        print('No files to dedupe')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto-dedupe wayback.urls files')
    parser.add_argument('--substr', type=str, help='Substring to match in the file name')
    parser.add_argument('--outdir', type=str, help='Output directory to store the deduped files')
    parser.add_argument('--sleepdur', type=int, help='Minutes to wait for the next execution', default=5)
    parser.add_argument('--delresult', action=argparse.BooleanOptionalAction, help='Delete result upon storing file in telegram', default=True)
    args = parser.parse_args()

    while True:
        auto_dedupe(args.substr, args.outdir, args.delresult)
        print(f'[+] Sleeping for {args.sleepdur} min')
        time.sleep(60*args.sleepdur)
