import os, shutil
from pathlib import Path


downloads_path = str( os.path.join(Path.home(), "Downloads") )
zwift_activity_dir = r"C:\Users\USER\Documents\Zwift\Activities"


def move_To_Uploaded_Activities_Folder(filename: str):
    source = os.path.join(zwift_activity_dir, "FixedActivities", filename)
    dest = os.path.join(zwift_activity_dir, "UploadedActivities")
    shutil.move(source, dest)

def move_To_Fixed_Activities_Folder(filename: str):
    source = os.path.join(downloads_path, filename)
    dest = os.path.join(zwift_activity_dir, "FixedActivities")
    shutil.move(source, dest)

def move_To_Temp_Folder(filename: str):
    source = os.path.join(zwift_activity_dir, filename)
    dest = os.path.join(zwift_activity_dir, "Temp")
    shutil.move(source, dest)

def rename_FitFile(newfilename: str, fitfilename: str = "fitfiletools.fit"):
    old_filename = os.path.join(downloads_path, fitfilename)
    new_filename = os.path.join(downloads_path, newfilename)
    os.rename(old_filename, new_filename)
