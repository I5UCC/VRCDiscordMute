import keyboard
import configparser
from pythonosc import dispatcher
from pythonosc import osc_server
import openvr
import os
import sys
import atexit

config = configparser.ConfigParser()
config.read('config.ini')

def resource_path(relative_path):
    """Gets absolute path from relative path"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

application = openvr.init(openvr.VRApplication_Utility)
appmanifest_path = resource_path(config["config"]["AppManifestFile"])

def handle_mute_event(addr, value):
  if not value:
    keyboard.press(config["config"]["PushMuteKey"])
  else:
    keyboard.release(config["config"]["PushMuteKey"])

def exit_handler():
  keyboard.release(config["config"]["PushMuteKey"])

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/avatar/parameters/MuteSelf", handle_mute_event)

server = osc_server.ThreadingOSCUDPServer((config["config"]["IP"], int(config["config"]["Port"])), dispatcher)
print(f"Listening to {server.server_address}\nPushMuteKey: {config['config']['PushMuteKey']}")
atexit.register(exit_handler)
server.serve_forever()
