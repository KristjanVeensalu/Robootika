import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import sys

root = tk.Tk()
root.withdraw()

file_path = filedialog.askdirectory()
directory = file_path

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

def install(package):
    if package in installed_packages:
        pass
    else:
        import pip
        os.system("pip install --user "+ package)
        #subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def parseFolder():
    fileList=[]
    for filename in os.listdir(directory):
        if filename.endswith(".txt") or filename.endswith(".doc"):
            fileList.append(os.path.join(directory, filename))
            continue
        else:
            continue
    return fileList