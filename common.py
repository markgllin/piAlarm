import os.path
from datetime import datetime

def timestamp():
    return datetime.now().strftime("[%H:%M:%S %Y/%d/%m]")

def check_if_armed():
    return os.path.exists("status")

def log_msg(msg):
    print '{} {}'.format(timestamp(), msg)
