import logging
import time
import keyboard
from tinyoscquery.query import OSCQueryBrowser, OSCQueryClient
from psutil import process_iter
import os
import sys
import configparser
import openvr

AVATAR_CHANGE_PARAMETER = "/avatar/change"
PARAMETER_PREFIX = "/avatar/parameters/"
MUTESELF_PARAMETER = PARAMETER_PREFIX + "MuteSelf"
VOICE_PARAMETER = PARAMETER_PREFIX + "Voice"

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")


def resource_path(relative_path):
    """Gets absolute path from relative path"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def wait_get_oscquery_client():
    service_info = None
    logging.info("Waiting for VRChat to be discovered.")
    while service_info is None:
        browser = OSCQueryBrowser()
        time.sleep(2)  # Wait for discovery
        service_info = browser.find_service_by_name("VRChat")
    logging.info("VRChat discovered!")
    client = OSCQueryClient(service_info)
    logging.info("Waiting for VRChat to be ready.")
    while client.query_node(AVATAR_CHANGE_PARAMETER) is None:
        time.sleep(2)
    logging.info("VRChat ready!")
    return client


def is_running() -> bool:
    """Checks if VRChat is running."""
    _proc_name = "VRChat.exe" if os.name == 'nt' else "VRChat"
    return _proc_name in (p.name() for p in process_iter())


def press_key(key: str):
    """Presses a key."""
    keyboard.press(key)
    time.sleep(0.05)
    keyboard.release(key)


def main_loop():
    state = None
    last_state = None
    key = str(config["config"]["ToggleMuteKey"])
    poll_interval = float(config["config"]["PollInterval"])

    logging.info("Waiting for VRChat to start.")
    while not is_running():
        time.sleep(3)
    logging.info("VRChat started!")

    qclient = wait_get_oscquery_client()
    while not state:
        state = qclient.query_node(MUTESELF_PARAMETER)
        if state and not state.value[0]:
            logging.warn("Waiting for user to Mute...")
        else:
            logging.info("User is Muted!")
        time.sleep(1)
    last_state = state

    while is_running():
        state = qclient.query_node(MUTESELF_PARAMETER)
        if state and state.value[0] != last_state.value[0]:
            logging.info(
                "User is Muted!" if state.value[0] else "User is Unmuted!")
            press_key(key)
            last_state = state
        time.sleep(poll_interval)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(resource_path('config.ini'))
    appmanifest_path = resource_path(config["config"]["AppManifestFile"])

    # Init openvr
    try:
        application = openvr.init(openvr.VRApplication_Utility)
        openvr.VRApplications().addApplicationManifest(appmanifest_path)
    except Exception:
        pass

    main_loop()
