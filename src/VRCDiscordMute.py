import keyboard
import configparser
from pythonosc import dispatcher
from pythonosc import osc_server
from tinyoscquery.queryservice import OSCQueryService
from tinyoscquery.utility import get_open_tcp_port, get_open_udp_port, check_if_tcp_port_open, check_if_udp_port_open
from threading import Thread
import openvr
import os
import sys
import atexit
import time
import traceback

enabled = True

def resource_path(relative_path):
    """Gets absolute path from relative path"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def handle_mute_event(addr, value):
  global enabled
  
  if not value and enabled:
    keyboard.press(PushToMuteKey)
  else:
    keyboard.release(PushToMuteKey)


def set_enabled(addr, value):
  global enabled

  if value:
    enabled = False
    handle_mute_event(None, True)
  else:
    enabled = True


def osc_server_serve():
  print(f"Starting OSC client on {osc_server_ip}:{osc_server_port}:{http_port}")
  server.serve_forever(2)


config = configparser.ConfigParser()
config.read(resource_path('config.ini'))
PushToMuteKey = config["config"]["PushMuteKey"]

# Init openvr
try:
  application = openvr.init(openvr.VRApplication_Utility)
  appmanifest_path = resource_path(config["config"]["AppManifestFile"])
  openvr.VRApplications().addApplicationManifest(appmanifest_path)
except Exception:
  pass

try:
  osc_server_ip = config["config"]["IP"]
  osc_server_port = int(config["config"]["Port"])
  http_port = int(config["config"]["HTTPPort"])
  if osc_server_port != 9001:
    print("OSC Server port is not default, testing port availability and advertising OSCQuery endpoints")
    if osc_server_port <= 0 or not check_if_udp_port_open(osc_server_port):
      osc_server_port = get_open_udp_port()
    if http_port <= 0 or not check_if_tcp_port_open(http_port):
      http_port = osc_server_port if check_if_tcp_port_open(osc_server_port) else get_open_tcp_port()
  else:
    print("OSC Server port is default.")

  handle_mute_event(None, True)
  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/avatar/parameters/MuteSelf", handle_mute_event)
  dispatcher.map("/avatar/parameters/DisableDiscordMute", set_enabled)
  server = osc_server.ThreadingOSCUDPServer((osc_server_ip, osc_server_port), dispatcher)
  Thread(target=osc_server_serve, daemon=True).start()

  oscqs = OSCQueryService("AvatarParameterSync", http_port, osc_server_port)
  oscqs.advertise_endpoint("/avatar/parameters/MuteSelf", access="readwrite")
  oscqs.advertise_endpoint("/avatar/parameters/DisableDiscordMute", access="readwrite")

  print(f"Listening to {server.server_address}\nPushMuteKey: {config['config']['PushMuteKey']}")
  atexit.register(lambda: handle_mute_event(None, True))
  while True:
    time.sleep(1)
except Exception:
  traceback.print_exc()
  handle_mute_event(None, True)
