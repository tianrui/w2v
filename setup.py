import sys
from cx_Freeze import setup, Executable
import scipy
import os

scipyf = []
#scipyp = os.path.dirname(scipy.__file__)
#scipyp = "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/scipy"
scipyp = "/Library/Python/2.7/site-packages/scipy"
scipyf.append(scipyp)
print scipyf
print sys.path
raw_input("press enter")

includes = ["scipy"]
build_exe_options = {"packages": ["os", "gensim", "nltk.data"], "include_files": [scipyp], "excludes": ["tkinter", "tcl", "Tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
setup(
        name = "UGift w2v",
        version = "0.0.1",
        description = "Model for tag matching",
        options = {"build_exe": build_exe_options},
        executables = [Executable("test.py", base=base)]
        )

