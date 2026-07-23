import sys
import os
import time

import sounddevice as sd
import soundfile as sf
from pynput import keyboard

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

data, samplerate = sf.read(resource_path("sounds/click.mp3"))

running = True


def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        return False

listener = keyboard.Listener(on_press=on_press)
listener.start()


if len(sys.argv) < 2:
    print("BPM not provided.")
    sys.exit(0)
if len(sys.argv) > 2:
    print("Too many arguments.")
    sys.exit(0)
bpm = sys.argv[1]
try:
    bpm = int(bpm)
except ValueError:
    print("Invalid BPM.")
    sys.exit(0)
print("Press ESC to exit.")

def sleep_interrupt(duration):
    step = 0.01
    end_time = time.time() + duration
    while running and time.time() < end_time:
        time.sleep(min(step, end_time - time.time()))

def main():
    try:
        while running:
            sd.play(data, samplerate)
            sleep_interrupt(60/bpm)
    except KeyboardInterrupt:
        pass
    sys.exit(0)
main()