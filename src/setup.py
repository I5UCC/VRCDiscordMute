from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
packages = ["configparser", "keyboard", "zeroconf", "requests", "psutil", "openvr"]
file_include = ["config.ini", "app.vrmanifest"]

build_exe_options = {"packages": packages, "include_files": file_include}

setup(
    name="VRCDiscordMute",
    version="1.0",
    description="VRCDiscordMute",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", target_name="VRCDiscordMute.exe", base=False), Executable("main.py", target_name="VRCDiscordMute_NoConsole.exe", base="Win32GUI"), Executable("GetHotkeyName.py", target_name="GetHotkeyName.exe", base=False)],
)