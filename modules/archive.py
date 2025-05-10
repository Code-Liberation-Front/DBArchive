import shutil
import os
from datetime import datetime

# file_name: Directory and File name for zipfile without .zip. Filename must include whole location
# file_directory: Root Directory of the folder you want to compress
def backup(file_name, file_directory):
    shutil.make_archive(file_name, 'zip', file_directory)

def backup_count(file_directory):
    files = os.listdir(file_directory)
    file_count = 0
    for file in files:
        if ".zip" in file:
            file_count += 1
    return file_count

def oldest_backup(file_directory):
    files = os.listdir(file_directory)
    filenames = []
    dates = []
    for file in files:
        if ".zip" in file:
            filenames.append(file)
            dates.append(time_from_filename(file))
    for counter, date in enumerate(dates):
        if date == min(dates):
            return os.path.join(file_directory, filenames[counter])

def newest_backup(file_directory):
    files = os.listdir(file_directory)
    filenames = []
    dates = []
    for file in files:
        if ".zip" in file:
            filenames.append(file)
            dates.append(time_from_filename(file))
    for counter, date in enumerate(dates):
        if date == max(dates):
            return os.path.join(file_directory, filenames[counter])

def time_from_filename(filename):
    time = filename.rstrip(".zip").split("_")[1:3]
    time[1] = ':'.join(time[1][i:i + 2] for i in range(0, len(time[1]), 2))
    time = f"{time[0]} {time[1]}"
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return time