import RPi.GPIO as io
import signal

from common import *
from time import sleep
from threading import Thread
from device import Device


def dev_status(ch, device):
    triggered = False

    state = device.trigger_on if io.input(ch) else device.trigger_off

    if io.input(ch):
        state = device.trigger_on
        triggered = True
    else:
        state = device.trigger_off

    log_msg(device.name + ' ' + state)

    if check_if_armed() and triggered:
        log_msg('Alarm triggered.')
        sound_alarm()

def sound_alarm():
    while check_if_armed():
        sleep(2)
        #sound alarm

    log_msg('Alarm stopped')

devices = [
	# Device(26, "Front Door", "Opened", "Closed"),
	# Device(24, "Garage Door", "Opened", "Closed"),
	# Device(23, "Patio Door", "Opened", "Closed"),
	# Device(22, "Living Room Window", "Opened", "Closed"),
	# Device(21, "Den Window", "Opened", "Closed"),
	# Device(19, "Kitchen Window", "Opened", "Closed"),
	# Device(18, "Basement Window 1", "Opened", "Closed"),
	# Device(16, "Basement Window 2", "Opened", "Closed")
     Device(11, "Basement Window 2", "Opened", "Closed")
]

io.setmode(io.BOARD)

for d in devices:
    # CHANGE THIS LATER
	io.setup(d.pin, io.IN, pull_up_down=io.PUD_DOWN)
	io.add_event_detect(d.pin, io.BOTH, callback=lambda ch: dev_status(ch, d), bouncetime=1000)

try:
  signal.pause()
except KeyboardInterrupt:
  log_msg('Existing system.py...')
  io.cleanup()
