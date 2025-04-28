import shutil
import os

# file_name: Directory and File name for zipfile without .zip. Already includes base directory/Backups
# file_directory: Root Directory of the folder you want to compress
def backup(file_name, file_directory):
    shutil.make_archive(f"{str(os.getcwd())}/Backups/{file_name}", 'zip', file_directory)