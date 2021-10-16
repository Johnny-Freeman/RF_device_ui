from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

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
# Session managers
# ==============================================
class Generator_State():
	# Holds state of generator tab
	def __init__(self, config=None):
		# Defaults
		self.rf_on = False
		
		self.freq = 0 # always in Hz
		self.freq_unit = "HZ"
		
		self.pwr = 0
		self.pwr_unit = "W"
		
		self.vco_lock = False
		self.pll_lock = False
		
		if config:
			self._import(config)
	
	# --------------------------
	# Helper functions
	# --------------------------
	def set_target_freq(self, value, freq_unit):
		if freq_unit.upper() == "HZ":
			self.freq = float(value)
		elif freq_unit.upper() == "KHZ":
			self.freq = float(value * 1000.0)
		elif freq_unit.upper() == "MHZ":
			self.freq = float(value * 1000000.0)
		else: #GHZ
			self.freq = float(value * 1000000000.0)
	
	def set_freq_unit(self, freq_unit):
		self.freq_unit = freq_unit.upper()
	
	def get_target_freq(self):
		value = self.freq
		if self.freq_unit.upper() == "HZ":
			pass
		elif self.freq_unit.upper() == "KHZ":
			value/=1000.0
		elif self.freq_unit.upper() == "MHZ":
			value/=1000000.0
		else: #GHZ
			value/=1000000000.0
		
		return value, self.freq_unit.upper()
	
	def get_target_freq_string(self):
		value, freq_unit = self.get_target_freq()
		return str(value)+ " " + freq_unit[:-1] + freq_unit[-1].lower()
	
	# --------------------------
	# import / export
	# --------------------------
	def _export(self):
		_dict = {
			"freq" : self.freq,
			"freq_unit" : self.freq_unit,	
			
			"pwr" : self.pwr,
			"pwr_unit" : self.pwr_unit,
		}
		return _dict
		
	def _import(self, config):
		self.freq = config["freq"]
		self.freq_unit = config["freq_unit"]
		
		self.pwr = config["pwr"]
		self.pwr_unit = config["pwr_unit"]

class Detector_State():
	# Holds state of detector tab
	def __init__(self, config=None):
		# Defaults
		self.mode = "STATIC" #STATIC/SWEEP
		
		self.start_freq = 0
		self.start_freq_unit = "HZ"
		
		self.stop_freq = 0
		self.stop_freq_unit = "HZ"
		
		self.step_size = 0
		self.step_size_unit = "HZ"
		
		self.pwr = 0
		self.pwr_unit = "W"
		
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
			"mode" : self.mode,
			
			"start_freq" : self.start_freq,
			"start_freq_unit" : self.start_freq_unit,
			
			"stop_freq" : self.stop_freq,
			"stop_freq_unit" : self.stop_freq_unit,
			
			"step_size" : self.step_size,
			"step_size_unit" : self.step_size_unit,
			
			"pwr" : self.pwr,
			"pwr_unit" : self.pwr_unit,
		}
		return _dict
		
	def _import(self, config):
		self.mode = config["mode"]
		
		self.start_freq = config["start_freq"]
		self.start_freq_unit = config["start_freq_unit"]
		
		self.stop_freq = config["stop_freq"]
		self.stop_freq_unit = config["stop_freq_unit"]
		
		self.step_size = config["step_size"]
		self.step_size_unit = config["step_size_unit"]
		
		self.pwr = config["pwr"]
		self.pwr_unit = config["pwr_unit"]

class Network_State():
	# Holds Network Settings
	def __init__(self, config = None):
		self.auto_ip = True
		self.ip_address = "0.0.0.0"
		self.netmask = "0.0.0.0"
		self.gateway = "0.0.0.0"
		
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