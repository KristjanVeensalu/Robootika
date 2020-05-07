import os
import subprocess
import sys
import enchant
import tkinter as tk
from tkinter import filedialog
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter



def chooseFolder():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askdirectory()
    directory = file_path
    return directory


def install(package):
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    if package in installed_packages:
        pass
    else:
        import pip
        os.system("pip install --user "+ package)
        #subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def parseFolder(directory):
    fileList=[]
    for filename in os.listdir(directory):
        if filename.endswith(".txt") or filename.endswith(".doc"):
            fileList.append(os.path.join(directory, filename))
            continue
        else:
            continue
    return fileList

def printLine():
    print("\n")
    for x in range(0,50):
        print("-", end = " ")
    print("\n")