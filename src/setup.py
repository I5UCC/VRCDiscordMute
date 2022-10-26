import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
packages = ["pythonosc", "configparser", "keyboard"]
exclude = ["tkinter", "html", "http", "lib2to3", "multiprocessing", "test", "unittest", "xmlrpc", "os", "traceback", "openvr", "sys", "time", "argparse"]
file_include = ["config.ini"]
bin_excludes = ["_bz2.pyd", "_decimal.pyd", "_hashlib.pyd", "_lzma.pyd", "_queue.pyd", "_ssl.pyd", "libcrypto-1_1.dll", "libssl-1_1.dll", "ucrtbase.dll", "VCRUNTIME140.dll"]

build_exe_options = {"packages": packages, "excludes": exclude, "include_files": file_include, "bin_excludes": bin_excludes}

setup(
    name="ThumbParamsOSC",
    version="0.3.1",
    description="ThumbParamsOSC",
    options={"build_exe": build_exe_options},
    executables=[Executable("VRCDiscordMute.py", targetName="VRCDiscordMute.exe", base=False), Executable("VRCDiscordMute.py", targetName="VRCDiscordMute_NoConsole.exe", base="Win32GUI")],
)