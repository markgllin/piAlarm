import os.path
import RPi.GPIO as io
import signal
import time

from common import *
from device import Device

global pin_count
pin_count = 0

def increment_pin(pin):
    global pin_count
    print "before: " + pin_count
    pin_count = pin_count + 1
    print "after: " + pin_count


def arm(pin):
    global pin_count
    log_msg('Arming system...')

    if pin_count == 3:
        open("status", 'w').close()
        log_msg('System armed.')
    else:
        log_msg('Incorrect pin entered to arm system.')

    pin_count = 0

def unarm(pin):
    global pin_count
    log_msg('Disarming system...')

    if pin_count == 3:
        os.remove("status")
        log_msg('System disarmed.')
    else:
        log_msg('Incorrect pin entered to disarm system.')

    pin_count = 0


def arm_status(pin):
    unarm(pin) if check_if_armed() else arm(pin)

io.setmode(io.BOARD)
io.setup(23, io.IN, pull_up_down=io.PUD_DOWN)
io.add_event_detect(23, io.RISING)
io.add_event_callback(23, callback=arm_status)
io.add_event_callback(23, callback=increment_pin)

try:
  signal.pause()
except KeyboardInterrupt:
  log_msg('Exiting arm.py...')
  io.cleanup()
