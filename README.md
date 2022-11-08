# VRCDiscordMute
A simple python program that mutes you on discord whenever you are unmuted in VRChat.

It does this by using a ***Push to Mute*** Keybind in Discord. <br>
You'll have to set up that Keybind in discord first, under Settings>Keybinds, set the action to "Push To Mute" and ***set it to a key that can be pushed continuously without causing issues*** <br>
Then set that same hotkey in the config.ini file. <br>
If you are unsure what the key is called you can run ***GetHotkeyName.py/GetHotkeyName.exe*** to find it out quickly. <br><br>
This project is using the [Python Keyboard Package](https://github.com/boppreh/keyboard) <br><br>

On first startup of the program, the program will register its manifest into SteamVR to allow AutoStarting like any other Overlay application on SteamVR.
