class Device:
	pin = 0
	name = ""
	trigger_on = ""
	trigger_off = ""

	def __init__(self, pin, name, trigger_on, trigger_off):
		self.pin = pin
		self.name = name
		self.trigger_on = trigger_on
		self.trigger_off = trigger_off
