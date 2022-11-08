import keyboard

print("Press any combination of key/s to recieve its hotkey name:\n")
print("You pressed: " + keyboard.read_hotkey(suppress=True))
print("\nPress any key to close this...")
keyboard.read_key()