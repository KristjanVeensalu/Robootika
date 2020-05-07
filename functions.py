import os
import subprocess
import sys
import enchant
import tkinter as tk
from tkinter import filedialog
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter

def chooseFile():
    root = tk.Tk()
    root.withdraw()
    file_path = ""
    while file_path == '':
        print("No file chosen, press ENTER to choose.")
        input()
        file_path = filedialog.askopenfilename()
    print("File chosen: " + file_path)
    directory = file_path
    return directory


#Runs tkinter filedialog to open folder select for user, returns path to folder
def chooseFolder():
    root = tk.Tk()
    root.withdraw()
    file_path = ''
    while file_path == '':
        print("No folder chosen, press ENTER to choose.")
        input()
        file_path = filedialog.askdirectory()
    print("Folder chosen: " + file_path)
    directory = file_path
    return directory

#Check user installed packages and install any that are missing
def install(package):
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    if package in installed_packages:
        pass
    else:
        import pip
        os.system("pip install --user "+ package)

#List all of the useable files in the selected folder, return a list of paths
def parseFolder(directory):
    fileList=[]
    for filename in os.listdir(directory):
        if filename.endswith(".txt") or filename.endswith(".doc"):
            fileList.append(os.path.join(directory, filename))
            continue
        else:
            continue
    return fileList

#Tool to print lines for visual aid
def printLine():
    print("\n")
    for x in range(0,50):
        print("-", end = " ")
    print("\n")