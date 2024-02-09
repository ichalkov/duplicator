import hashlib
import os
import sys
import time
from progress.bar import IncrementalBar
from pathlib import Path


def get_checksum(path_to_file):
    """Checksum calculation for a file"""
    BUF_SIZE = 65536
    md5 = hashlib.new("md5")
    with open(path_to_file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def add_checksum_to_dict(path_to_file, checksum_hash):
    """Adding a file path to a dictionary using a checksum key"""
    if checksum_hash in duplicates:
        duplicates[checksum_hash].append(path_to_file)
    else:
        duplicates[checksum_hash] = [path_to_file]


search_path = ''
if len(sys.argv) == 1:
    print('Path is not specified!')
    exit(1)
if len(sys.argv) > 1:
    search_path = sys.argv[1]
    if not os.path.isdir(search_path):
        print('Path not found!')
        exit(1)


# counting the number of files
folder = Path(search_path)
total_count = len(list(folder.rglob("*")))

# use progressbar
begin_time = time.time()
print('Finding for duplicates, please wait...')
bar = IncrementalBar('Progress:', max=total_count)

# file sizes dictionary
sizes = {}

# hashsum dictionary
duplicates = {}

for folder, folders, files in os.walk(search_path):
    for file in files:
        bar.next()

        path = os.path.join(folder, file)
        size = os.path.getsize(path)

        # check if this file already has been encountered
        if size in sizes:
            # calculate the hash for the file that is already in sizes, only once
            if len(sizes[size]) != 0:
                file2 = sizes[size]
                checksum = get_checksum(file2)
                add_checksum_to_dict(sizes[size], checksum)
                sizes[size] = ''  # reset value that it is no longer use
            # calculate the hash for the second and next files of the same size
            checksum = get_checksum(path)
            add_checksum_to_dict(path, checksum)
        else:
            sizes[size] = path


# Calculate statistic and displaying results
duplicate_count = 0

for hash_sum in duplicates:
    files = duplicates[hash_sum]
    if len(files) > 1:
        print("\n")
        duplicate_count += 1
        for file_name in files:
            try:
                print(hash_sum, file_name, sep="\t")
            except UnicodeEncodeError:
                print("!!!Bad filename")

if total_count == 0:
    print("Duplicates are not found ...")
else:
    end_time = time.time()
    print("")
    print(f"Total time:{round(end_time-begin_time, 2)} sec. Files: {total_count}. Total duplicates: {duplicate_count}")

bar.finish()
