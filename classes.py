from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from math import log
from enum import Enum

# ==============================================
# Interacting with Children, Signals and Slots
# ==============================================
def import_widget4(path):
	# Loads UI
	Widget_Ui, Widget_class = uic.loadUiType(path)
	class dummy(Widget_class):
		# -------------------------
		# Helpful widget functions
		# -------------------------
		def getChild(self, regex_name):
			# returns child, quick and simple
			# QWidget is the most basic of classes and will search through all widgets.
			return self.findChild(QWidget, regex_name)
		
		def getChildren(self, regex_name):
			# returns list of children, quick and simple
			# QWidget is the most basic of classes and will search through all widgets.
			return self.findChildren(QWidget, regex_name)
			
		def __init__(self, parent=None):
			super().__init__(parent)
			# Widget_class uses Widget_Ui to configure itself( passes Widget_Ui.setupUi(Widget_class) )
			# this method is composition
			ui = Widget_Ui()
			ui.setupUi(self)
			
			# PlaceHolder
			self.ConnectSignalsAndSlots()
			
		def ConnectSignalsAndSlots(self, *args, **kwargs):
			# Reserved PlaceHolder, override at will.
			# Programmically define click actions of children
			# self.findChild(QWidget, 'pushButton2').clicked.connect(self.print_funct)
			# self.getChild('pushButton2').clicked.connect(self.print_funct)
			pass
		
	return dummy #returns a class, not instance to use as inheritence later.


# ==============================================
# Storing freq (in Hz) and power (in mW)
# And converting between units
# ==============================================
class UNIT(Enum):
	# Frequency units
	HZ = "Hz"
	KHZ = "KHz"
	MHZ = "MHz"
	GHZ = "GHz"
	
	# Power units
	DBM = "dBm"
	MIL = "mW"
	W = "W"
	
	def __str__(self):
		return self.value
	
	def _export(self):
		return self.name
	
	@staticmethod
	def _import(input_string):
		return UNIT[input_string]

class Freq():
	@staticmethod
	def convert_to_Hz(value, unit):
		if unit == UNIT.HZ:
			return float(value)
		elif unit == UNIT.KHZ:
			return float(value)*1000.0
		elif unit == UNIT.MHZ:
			return float(value)*1000000.0
		elif unit == UNIT.GHZ:
			return float(value)*1000000000.0
		else:
			raise TypeError("input unit must be of UNIT() enum type")
	
	@staticmethod
	def convert_to_unit(hz_value, unit):
		if unit == UNIT.HZ:
			return float(hz_value)
		elif unit == UNIT.KHZ:
			return float(hz_value)/1000.0
		elif unit == UNIT.MHZ:
			return float(hz_value)/1000000.0
		elif unit == UNIT.GHZ:
			return float(hz_value)/1000000000.0
		else:
			raise TypeError("input unit must be of UNIT() enum type")
	
	def __init__(self, value, input_unit):
		self.hz_value = Freq.convert_to_Hz(value, input_unit)
	
	def get(self, desired_unit):
		return Freq.convert_to_unit(self.hz_value, desired_unit)
	read = cast = get
	
	def _export(self):
		return self.hz_value
	
	@staticmethod
	def _import(value):
		return Freq(value, UNIT.HZ)

class Power():
	# https://www.rapidtables.com/convert/power/Watt_to_dBm.html
	@staticmethod
	def convert_to_mW(value, unit):
		if unit == UNIT.MIL:
			return float(value)
		elif unit == UNIT.W:
			return float(value) *1000.0
		elif unit == UNIT.DBM:
			return pow(10.0, float(value)/10.0)
		else:
			raise TypeError("input unit must be of UNIT() enum type")


	@staticmethod
	def convert_to_unit(mil_value, unit):
		if unit == UNIT.MIL:
			return float(mil_value)
		elif unit == UNIT.W:
			return float(mil_value) /1000.0
		elif unit == UNIT.DBM:
			return 10.0 * log(float(mil_value),10.0)
		else:
			raise TypeError("input unit must be of UNIT() enum type")
	
	def __init__(self, value, input_unit):
		# Minimum value to handle negative infinity dBm
		if input_unit == UNIT.MIL:
			value = max(value, 0.001)
		
		self.mil_value = Power.convert_to_mW(value, input_unit)
	
	def get(self, desired_unit):
		return Power.convert_to_unit(self.mil_value, desired_unit)
	read = cast = get
	
	def _export(self):
		return self.mil_value
	
	@staticmethod
	def _import(value):
		return Power(value, UNIT.MIL)


# ==============================================
# Session managers
# ==============================================
class Generator_State():
	# Holds state of generator tab
	def __init__(self, config=None):
		# Defaults
		self.rf_on = False
		
		self.output_freq = Freq(0, UNIT.GHZ)
		self.output_power = Power(0, UNIT.DBM)
			
		self.vco_lock = False
		self.pll_lock = False
		
		# Profilable
		self.target_freq = Freq(0, UNIT.GHZ)
		self.freq_unit = UNIT.GHZ
		
		self.target_power = Power(0, UNIT.DBM)
		self.power_unit = UNIT.DBM
		
		if config:
			self._import(config)
	
	# --------------------------
	# Helper functions
	# --------------------------
	# Frequency
	def set_target_freq(self, value, freq_unit=None):
		if freq_unit:
			self.target_freq = Freq(value, freq_unit)
		
		elif type(value) in (float, int, str):
			raise TypeError("Numeric input values must be paired with freq_unit = <UNIT(enum)> type")
			
		else:
			self.target_freq = value
	
	def set_freq_unit(self, freq_unit):
		self.freq_unit = freq_unit
	
	def get_target_freq(self):
		return self.target_freq
	
	def get_freq_unit(self):
		return self.freq_unit
	
	def get_target_freq_string(self):
		return str( self.target_freq.cast(self.freq_unit) )+ " " + str(self.freq_unit)
	
	def get_output_freq_string(self):
		return str( self.output_freq.cast(self.freq_unit) )+ " " + str(self.freq_unit)
	
	# Power
	def set_target_power(self, value, power_unit=None):
		if power_unit:
			self.target_power = Power(value, power_unit)
		
		elif type(value) in (float, int):
			raise TypeError("Numeric input values must be paired with power_unit = <UNIT(enum)> type")
			
		else:
			self.target_power = value
	
	def set_power_unit(self, power_unit):
		self.power_unit = power_unit
	
	def get_target_power(self):
		return self.target_power
	
	def get_power_unit(self):
		return self.power_unit
	
	def get_target_power_string(self):
		return str( self.target_power.cast(self.power_unit) )+ " " + str(self.power_unit)
	
	def get_output_power_string(self):
		return str( self.output_power.cast(self.power_unit) )+ " " + str(self.power_unit)
	
	# --------------------------
	# import / export
	# --------------------------
	def _export(self):
		_dict = {
			"target_freq" : self.target_freq._export(),
			"freq_unit" : self.freq_unit._export(),
			
			"target_power" : self.target_power._export(),
			"power_unit" : self.power_unit._export(),
		}
		return _dict
		
	def _import(self, config):
		self.target_freq = Freq._import( config["target_freq"] )
		self.freq_unit = UNIT._import( config["freq_unit"] )
		
		self.target_power = Power._import( config["target_power"] )
		self.power_unit = UNIT._import( config["power_unit"] )

class Detector_State():
	# Holds state of detector tab
	def __init__(self, config=None):
		# Defaults
		self.mode = "STATIC" #STATIC/SWEEP
		
		self.start_freq = Freq(0, UNIT.GHZ)
		self.start_freq_unit = UNIT.GHZ
		
		self.stop_freq = Freq(0, UNIT.GHZ)
		self.stop_freq_unit = UNIT.GHZ
		
		self.num_steps = 0
		
		self.power = Power(0, UNIT.DBM)
		self.power_unit = UNIT.DBM
		
		if config:
			self._import(config)
	
	# --------------------------
	# Helper functions
	# --------------------------
	# start freq
	def set_sweep_start_freq(self, value, freq_unit):
		self.start_freq = value
		self.start_freq_unit = freq_unit
	
	def get_sweep_start_freq_string(self):
		return str(self.start_freq.cast(self.start_freq_unit)) + " " + str(self.start_freq_unit)
	
	# stop freq
	def set_sweep_stop_freq(self, value, freq_unit):
		self.stop_freq = value
		self.stop_freq_unit = freq_unit
		
	def get_sweep_stop_freq_string(self):
		return str(self.stop_freq.cast(self.stop_freq_unit)) + " " + str(self.stop_freq_unit)
	
	# sweep steps
	def set_sweep_num_steps(self, num_steps):
		self.num_steps = num_steps
	
	# sweep power
	def set_sweep_power(self, value, power_unit):
		self.power = value
		self.power_unit = power_unit
	
	def get_sweep_power_string(self):
		return str(self.power.cast(self.power_unit)) + " " + str(self.power_unit)
	
	# --------------------------
	# import / export
	# --------------------------
	def _export(self):
		_dict = {
			"mode" : self.mode,
			
			"start_freq" : self.start_freq._export(),
			"start_freq_unit" : self.start_freq_unit._export(),
			
			"stop_freq" : self.stop_freq._export(),
			"stop_freq_unit" : self.stop_freq_unit._export(),
			
			"num_steps" : self.num_steps,
			
			"power" : self.power._export(),
			"power_unit" : self.power_unit._export(),
		}
		return _dict
		
	def _import(self, config):
		self.mode = config["mode"]
		
		self.start_freq = Freq._import( config["start_freq"] )
		self.start_freq_unit = UNIT._import( config["start_freq_unit"] )
		
		self.stop_freq = Freq._import(config["stop_freq"])
		self.stop_freq_unit = UNIT._import(config["stop_freq_unit"] )
		
		self.num_steps = config["num_steps"]
		
		self.power = Power._import( config["power"])
		self.power_unit = UNIT._import(config["power_unit"] )

class Network_State():
	# Holds Network Settings
	def __init__(self, config = None):
		self.auto_ip = True
		self.ip_address = "192.168.1.1"
		self.netmask = "192.168.1.1"
		self.gateway = "192.168.1.1"
		
		if config:
			self._import(config)
	
	
	# --------------------------
	# Helper functions
	# --------------------------
	
	
	# --------------------------
	# import / export
	# --------------------------	
	def _export(self):
		_dict = {
			"auto_ip" : self.auto_ip,
			"ip_address" : self.ip_address,
			"netmask" : self.netmask,
			"gateway" : self.gateway,
		}
		return _dict
		
	def _import(self, config):
		self.auto_ip = config["auto_ip"]
		self.ip_address = config["ip_address"]
		self.netmask = config["netmask"]
		self.gateway = config["gateway"]
		

class Echo_Session():
	def __init__(self, config = None):
		self.generator = Generator_State()
		self.detector = Detector_State()
		self.network = Network_State()
		
		if config:
			self._import(config)
	
	def _export(self):
		_dict = {
			"generator" : self.generator._export(),
			"detector" : self.detector._export(),
			"network" : self.network._export(),
		}
		
		return _dict

	def _import(self, config):
		self.generator._import( config["generator"] )
		self.detector._import( config["detector"])
		self.network._import( config["network"] )

if __name__ == "__main__":
	# i = import_widget4('test')
	
	# s = Echo_Session()
	# s.network.ip_address = "1.1.1.1"
	# e = s._export()
	# ss = Echo_Session(e)
	# print(ss._export())
	pass