import os, shutil
from pathlib import Path
from read_config_file import *


def move_To_Uploaded_Or_Malformed_Activities_Folder(filename: str):
    source_dir = os.path.join(ZWIFT_ACTIVITY_DIR, "FixedActivities")
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
    dest_dir = os.path.join(ZWIFT_ACTIVITY_DIR, "UploadedOrMalformedActivities")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    source = os.path.join(source_dir, filename)
    dest = os.path.join(dest_dir, filename)
    shutil.move(source, dest)

def move_To_Fixed_Activities_Folder(filename: str):
    source_dir = os.path.join(Path.home(), "Downloads")
    dest_dir = os.path.join(ZWIFT_ACTIVITY_DIR, "FixedActivities")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    source = os.path.join(source_dir, filename)
    dest = os.path.join(dest_dir, filename)
    shutil.move(source, dest)

def move_To_Original_Activities_Folder(filename: str):
    dest_dir = os.path.join(ZWIFT_ACTIVITY_DIR, "OriginalActivities")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    source = os.path.join(ZWIFT_ACTIVITY_DIR, filename)
    dest = os.path.join(dest_dir, filename)
    shutil.move(source, dest)

def rename_FitFile(newfilename: str, fitfilename: str="fitfiletools.fit"):
    old_filename = os.path.join(Path.home(), "Downloads", fitfilename)
    new_filename = os.path.join(Path.home(), "Downloads", newfilename)
    os.rename(old_filename, new_filename)