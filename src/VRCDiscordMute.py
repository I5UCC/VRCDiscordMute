import keyboard
import configparser
from pythonosc import dispatcher
from pythonosc import osc_server

config = configparser.ConfigParser()
config.read('config.ini')

def handle_mute_event(addr, value):
  if not value:
    keyboard.press(config["config"]["PushMuteKey"])
  else:
    keyboard.release(config["config"]["PushMuteKey"])

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/avatar/parameters/MuteSelf", handle_mute_event)

server = osc_server.ThreadingOSCUDPServer((config["config"]["IP"], int(config["config"]["Port"])), dispatcher)
print(f"Listening to {server.server_address}\nPushMuteKey: {config['config']['PushMuteKey']}")
server.serve_forever()
