from bottle import get, post, request, run
from threading import Thread
import os.path
import RPi.GPIO as io
import signal
from device import Device
from datetime import datetime

logged_in = False
STATUS_FILE = "status"

@get('/')
def login():
	return '''
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<form action="/" method="post">
			Enter pin: <input name="pin" type="password"/>
			<input value="Login" type="submit"/>
		</form>
	'''

@post('/')
def do_login():
	pin = request.forms.get('pin')

	if pin == '1234':
		global logged_in
		logged_in = True
		return sys_status()
	else:
		return login()

def status_file_exists():
	global STATUS_FILE
	return os.path.exists(STATUS_FILE)


def sys_status():

	if status_file_exists():
		current_status = "Armed"
	else:
		current_status = "Unarmed"

	if logged_in:
		html = '''<meta name="viewport" content="width=device-width, initial-scale=1.0">'''
		html +=	"<p> status=" + current_status + "</p>"
	
		if current_status == 'Unarmed':
			button = 'Arm'
		elif current_status == 'Armed':
			button = 'Unarm'
		else:
			print 'Unknown stat:' + current_status

		html += '''
			<form action="/status" method="post">
			<input name="status" type="submit" value=
		'''
		html += button
		html += ''' />
			</form>
		'''
		return html
	else:
		return login()

@post('/status')
def change_status():
	status = request.forms.get('status')
	
	if status == 'Arm':
		open(STATUS_FILE, 'w').close()
	else:
		os.remove(STATUS_FILE)

	return login()


def timestamp():
	return datetime.now().strftime("[%H:%M:%S %Y/%d/%m]")

def status(ch, device):
	ts = timestamp()
	status = device.on_status if io.input(ch) else device.off_status
	print '{} {} {}'.format(ts, device.name, status)

	if (status_file_exists() and (status == "Opened")):
		thread = Thread(target = sound_alarm)
		thread.start()
		thread.join()
		print "done sounding"

def sound_alarm():
 if status_file_exists():
	pass
	#keep sounding alarm



devices = [
	Device(26, "Front Door", "Opened", "Closed"),
	Device(24, "Garage Door", "Opened", "Closed"),
	Device(23, "Patio Door", "Opened", "Closed"),
	Device(22, "Living Room Window", "Opened", "Closed"),
	Device(21, "Den Window", "Opened", "Closed"),
	Device(19, "Kitchen Window", "Opened", "Closed"),
	Device(18, "Basement Window 1", "Opened", "Closed"),
	Device(16, "Basement Window 2", "Opened", "Closed")
]

io.setmode(io.BOARD)

for d in devices:
	io.setup(d.pin, io.IN, pull_up_down=io.PUD_DOWN)
	io.add_event_detect(d.pin, io.BOTH, callback=lambda ch: status(ch, d), bouncetime=1000)

try:
	run(host='192.168.0.200', port=8080)
except KeyboardInterrupt:
	print "Exiting..."
	io.cleanup()
