import os, shutil, yaml
from pathlib import Path


dir = os.path.dirname(__file__)
CONFIG_FILE_PATH = os.path.abspath( os.path.join(dir, '..', 'configfile', 'user_config.yml') )
with open(CONFIG_FILE_PATH, 'r') as f:
    config = yaml.safe_load(f)
    

downloads_path = str( os.path.join(Path.home(), "Downloads") )
zwift_activity_dir = config["zwift_activity_dir"]


def move_To_Uploaded_Activities_Folder(filename: str):
    source = os.path.join(zwift_activity_dir, "FixedActivities", filename)
    dest_dir = os.path.join(zwift_activity_dir, "UploadedActivities")
    dest = os.path.join(dest_dir, os.path.basename(source))
    shutil.move(source, dest)

def move_To_Fixed_Activities_Folder(filename: str):
    source = os.path.join(downloads_path, filename)
    dest_dir = os.path.join(zwift_activity_dir, "FixedActivities")
    dest = os.path.join(dest_dir, os.path.basename(source))
    shutil.move(source, dest)

def move_To_Original_Activities_Folder(filename: str):
    source = os.path.join(zwift_activity_dir, filename)
    dest_dir = os.path.join(zwift_activity_dir, "OriginalActivities")
    dest = os.path.join(dest_dir, os.path.basename(source))
    shutil.move(source, dest)

def rename_FitFile(newfilename: str, fitfilename: str = "fitfiletools.fit"):
    old_filename = os.path.join(downloads_path, fitfilename)
    new_filename = os.path.join(downloads_path, newfilename)
    os.rename(old_filename, new_filename)
