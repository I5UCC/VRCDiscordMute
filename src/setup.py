from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
packages = ["pythonosc", "configparser", "keyboard"]
file_include = ["config.ini", "app.vrmanifest"]

build_exe_options = {"packages": packages, "include_files": file_include}

setup(
    name="VRCDiscordMute",
    version="0.2",
    description="VRCDiscordMute",
    options={"build_exe": build_exe_options},
    executables=[Executable("VRCDiscordMute.py", targetName="VRCDiscordMute.exe", base=False), Executable("VRCDiscordMute.py", targetName="VRCDiscordMute_NoConsole.exe", base="Win32GUI"), Executable("GetHotkeyName.py", targetName="GetHotkeyName.exe", base=False)],
)