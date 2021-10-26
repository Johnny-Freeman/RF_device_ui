from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import os

from set_freq import QDialog_Set_Freq
from set_pwr import QDialog_Set_Power
from set_num import QDialog_Set_Number
from set_ip import QDialog_Set_IP
from sweep_plot import QMatplot_Static
from classes import import_widget4, Echo_Session, UNIT

# ==============================================
# Globals that need to happento setup
# ==============================================
# root_dir = """D:/projects_Python/RF_device_ui/"""
# if not os.name == 'nt':
# 	root_dir = """/home/pi/Downloads/RF_device_ui/"""
import inspect
def _getRoot(relative=True):
	# John's special, any system, any terminal, relative to THIS file
	# Realtive = True	returns calling python script's parent directory
	# Realtive = False	returns main(master) python sciptt's parent directory
	
	# Default stack location
	frame = inspect.stack()[1]
	if not relative:
		# absolute main python call
		frame = inspect.stack()[-1]
	
	module = inspect.getmodule(frame[0])
	root = os.path.dirname(os.path.abspath(module.__file__))
	return root

path = _getRoot() + """/ui/main_1.ui"""

# WIP - for Dev/monkey wrench purpsoes
from classes import Power

# ==============================================
# Backend Data? TBD on how to grab data
# ==============================================
from random import uniform
def get_sweep_data():
	# monkey wrench
	x = [i for i in range(100)]
	y = [uniform(0.8*float(i), 1.2*float(i)) for i in range(100)]
	return x,y


# ==============================================
# Main Application
# ==============================================
def get_stylesheet(*paths):
	full_string = ""
	
	for path in paths:
		ofile = open(path,"r")
		lines = ofile.read()
		full_string = full_string + "\n" + lines
	
	return full_string

b = import_widget4(path)
class main_menu(b):			
		def __init__(self, parent=None):
			super().__init__(parent)				
			# Situate Window
			self.window_setup()
			
			# Application State
			self.state = Echo_Session()
			self.RELOAD()
			
			# Style Sheets
			self.load_stylesheets()
			
			# Initiate Loops
			self.LOOP()
			
		def load_stylesheets(self):
			# load tab style sheets
			# self.getChild('tabWidget').setStyleSheet("QTabBar::tab { height: 40px; width: 120px; }")
			
			# General stylesheet
			self.setStyleSheet(get_stylesheet( _getRoot()+"/css/theme.css", _getRoot()+"/css/override.css" ))
			
		def window_setup(self):
			# https://stackoverflow.com/questions/7021502/pyqt-remove-the-programs-title-bar
			# https://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
			self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # requires QtCore, but more control
			self.setStatusBar(None)
			
			# WIP MVP: remove and hardcode on prod
			if not os.name == 'nt':
				self.showFullScreen()
			
			# Adding matplotlib Graph
			x,y = get_sweep_data()
			self.figure = QMatplot_Static(x,y, parent=self.getChild('frame_detector_sweep') )
		
		
		# =================================================
		# Signals, Tabs, Slots
		# =================================================		
		def RELOAD(self):
			# Called to refresh modes/state options across application
			self.load_generator_state()
			self.load_detector_state()
			self.load_network_state()
		
		def DISPLAY(self):
			# Called to refresh display labels across application
			self.display_generator()
			self.display_detector()
			self.display_network()
		
		# General Interface
		def ConnectSignalsAndSlots(self, *args, **kwargs):
			# Reserved PlaceHolder, override at will.
			# Programmically define click actions of children
			self.getChild('btn_exit').clicked.connect(self.close)
			
			# -------------------------
			# Generator
			# -------------------------
			# Toggle RF ON/OFF
			# clicked (not toggled) seems to work best for grouped buttons
			self.getChild('btn_rf_on').clicked.connect(self.toggle_generator_rf_on_off)
			self.getChild('btn_rf_off').clicked.connect(self.toggle_generator_rf_on_off)
			
			# Set target frequency/power
			self.getChild('btn_set_freq').clicked.connect(self.input_user_freq)
			self.getChild('btn_set_pwr').clicked.connect(self.input_user_power)
			
			# Toggle between frequency units
			self.getChild('btn_Hz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_KHz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_MHz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_GHz').clicked.connect(self.update_frequency_choice)
			
			# Toggle between power units
			self.getChild('btn_mW').clicked.connect(self.update_power_choice)
			self.getChild('btn_W').clicked.connect(self.update_power_choice)
			self.getChild('btn_dBm').clicked.connect(self.update_power_choice)
			
			# -------------------------
			# Detector
			# -------------------------
			# Toggle between Static and Sweep mode
			self.getChild('btn_toggle_static_mode').clicked.connect(self.set_detector_mode)			
			self.getChild('btn_toggle_sweep_mode').clicked.connect(self.set_detector_mode)
			
			# Power options
			self.getChild('btn_detector_dBm').clicked.connect(self.update_detector_power_choice)
			self.getChild('btn_detector_mW').clicked.connect(self.update_detector_power_choice)
			self.getChild('btn_detector_W').clicked.connect(self.update_detector_power_choice)
			
			# Static options
			self.getChild('btn_static_generator_rf_on').clicked.connect(self.toggle_detector_rf_on_off)
			self.getChild('btn_static_generator_rf_off').clicked.connect(self.toggle_detector_rf_on_off)
			self.getChild('btn_static_generator_set_freq').clicked.connect(self.input_user_freq)
			self.getChild('btn_static_generator_set_pwr').clicked.connect(self.input_user_power)
			
			# Sweep options
			self.getChild('btn_sweep_start_freq').clicked.connect(self.set_sweep_start_freq)
			self.getChild('btn_sweep_stop_freq').clicked.connect(self.set_sweep_stop_freq)
			self.getChild('btn_sweep_num_steps').clicked.connect(self.set_sweep_num_steps)
			self.getChild('btn_sweep_pwr').clicked.connect(self.set_sweep_power)
			
			# -------------------------
			# Settings / Network
			# -------------------------
			# Static / Dynamic Toggle
			self.getChild("rbtn_dynamic_ip").clicked.connect(self.set_network_mode)
			self.getChild("rbtn_static_ip").clicked.connect(self.set_network_mode)
			
			# Userset
			self.getChild("btn_set_ip_address").clicked.connect(self.set_ip_address)
			self.getChild("btn_set_netmask").clicked.connect(self.set_netmask)
			self.getChild("btn_set_gateway").clicked.connect(self.set_gateway)
		
		# =================================================
		# Generator
		# =================================================
		def toggle_generator_rf_on_off(self):
			if self.getChild('btn_rf_on').isChecked():
				self.state.generator.rf_on = True
			else:
				self.state.generator.rf_on = False
			
			self.RELOAD()
				
		def load_generator_state(self):
			# radio on/off
			if self.state.generator.rf_on:
				self.getChild('btn_rf_on').setChecked(True)
			else:
				self.getChild('btn_rf_off').setChecked(True)
		
		# -------------------------
		# Retreiving User input
		# -------------------------
		# frequency
		def input_user_freq(self):
			w = QDialog_Set_Freq(initial_value=self.state.generator.target_freq, freq_unit=self.state.generator.freq_unit)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			obj_value = result[0][0]
			# obj_unit = result[0][1] # not used
				
			if bool_set:
				# Update generator targets
				self.state.generator.set_target_freq(obj_value)
				self.DISPLAY() # global_app << self.display_target_freq()
			else:
				pass
		
		def update_frequency_choice(self):
			if self.getChild('btn_Hz').isChecked():
				unit = UNIT.HZ
			elif self.getChild('btn_KHz').isChecked():
				unit = UNIT.KHZ
			elif self.getChild('btn_MHz').isChecked():
				unit = UNIT.MHZ
			else: # GHZ
				unit = UNIT.GHZ
			self.state.generator.set_freq_unit(unit)
			
			# update displays
			self.display_target_freq()
			self.display_output_freq()
		
		# power
		def input_user_power(self):
			w = QDialog_Set_Power(initial_value=self.state.generator.target_power, power_unit=self.state.generator.power_unit)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			obj_value = result[0][0]
			# obj_unit = result[0][1] # not used
				
			if bool_set:
				# Update generator targets
				self.state.generator.set_target_power(obj_value)
				self.DISPLAY() # global_app << self.display_target_power()
			else:
				pass
		
		def update_power_choice(self):
			if self.getChild('btn_mW').isChecked():
				unit = UNIT.MIL
			elif self.getChild('btn_W').isChecked():
				unit = UNIT.W
			else: # dBm
				unit = UNIT.DBM
			self.state.generator.set_power_unit(unit)
			
			# update displays
			self.display_target_power()
			self.display_output_power()
		
		# -------------------------
		# Display generator outputs
		# -------------------------
		def display_target_freq(self):
			target_freq_string = self.state.generator.get_target_freq_string()
			self.getChild('lbl_target_freq').setText(target_freq_string)
		
		def display_target_power(self):
			target_power_string = self.state.generator.get_target_power_string()
			self.getChild('lbl_target_power').setText(target_power_string)
			
		def display_output_freq(self):
			output_freq_string = self.state.generator.get_output_freq_string()
			self.getChild('lbl_output_freq').setText(output_freq_string)
		
		def display_output_power(self):
			output_power_string = self.state.generator.get_output_power_string()
			self.getChild('lbl_output_power').setText(output_power_string)
		
		def display_generator(self):
			self.display_target_freq()
			self.display_target_power()
			self.display_output_freq()
			self.display_output_power()
		
		# =================================================
		# Detector
		# =================================================
		def load_detector_state(self):
			# radio on/off
			if self.state.generator.rf_on:
				self.getChild('btn_static_generator_rf_on').setChecked(True)
			else:
				self.getChild('btn_static_generator_rf_off').setChecked(True)
			
			# misc
			self.set_detector_mode()
		
		def toggle_detector_rf_on_off(self):
			if self.getChild('btn_static_generator_rf_on').isChecked():
				self.state.generator.rf_on = True
			else:
				self.state.generator.rf_on = False
			
			self.RELOAD()
				
		def set_detector_mode(self):
			if self.getChild("btn_toggle_static_mode").isChecked():
				self.state.detector.mode = "STATIC"
				self.init_detector_static_mode()
			else:
				self.state.detector.mode = "SWEEP"
				self.init_detector_sweep_mode()
		
		def update_detector_power_choice(self):
			if self.getChild('btn_detector_mW').isChecked():
				unit = UNIT.MIL
			elif self.getChild('btn_detector_W').isChecked():
				unit = UNIT.W
			else: # dBm
				unit = UNIT.DBM
			self.state.detector.set_power_display_unit(unit)
			
			# update displays
			self.display_detector_static_read_power
		
		def init_detector_static_mode(self):
			# enable static components
			self.getChild("frame_detector_static").setEnabled(True)
			self.getChild("frame_detector_static").setVisible(True)
			
			self.getChild("grp_static_generator_controls").setEnabled(True)
			self.getChild("grp_static_generator_controls").setVisible(True)
			
			# disable sweep components
			self.getChild("frame_detector_sweep").setEnabled(False)
			self.getChild("frame_detector_sweep").setVisible(False)
			
			self.getChild("grp_sweep_controls").setEnabled(False)
			self.getChild("grp_sweep_controls").setVisible(False)
		
		def init_detector_sweep_mode(self):
			# disable static components
			self.getChild("frame_detector_static").setEnabled(False)
			self.getChild("frame_detector_static").setVisible(False)
			
			self.getChild("grp_static_generator_controls").setEnabled(False)
			self.getChild("grp_static_generator_controls").setVisible(False)
			
			# enable sweep components
			self.getChild("frame_detector_sweep").setEnabled(True)
			self.getChild("frame_detector_sweep").setVisible(True)
			
			self.getChild("grp_sweep_controls").setEnabled(True)
			self.getChild("grp_sweep_controls").setVisible(True)
		
		# -------------------------
		# Sweep settings
		# -------------------------
		def set_sweep_start_freq(self):
			w = QDialog_Set_Freq(initial_value=self.state.detector.start_freq, freq_unit=self.state.detector.start_freq_unit)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			obj_value = result[0][0]
			obj_unit = result[0][1]
				
			if bool_set:
				# Update detector
				self.state.detector.set_sweep_start_freq(obj_value, obj_unit)
				self.display_detector_sweep_settings()
			else:
				pass
			
		def set_sweep_stop_freq(self):
			w = QDialog_Set_Freq(initial_value=self.state.detector.stop_freq, freq_unit=self.state.detector.stop_freq_unit)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			obj_value = result[0][0]
			obj_unit = result[0][1]
				
			if bool_set:
				# Update detector
				self.state.detector.set_sweep_stop_freq(obj_value, obj_unit)
				self.display_detector_sweep_settings()
			else:
				pass
		
		def set_sweep_num_steps(self):
			w = QDialog_Set_Number(initial_value=self.state.detector.num_steps)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			int_value = result[0]
				
			if bool_set:
				# Update detector
				self.state.detector.set_sweep_num_steps(int_value)
				self.display_detector_sweep_settings()
			else:
				pass
		
		def set_sweep_power(self):
			w = QDialog_Set_Power(initial_value=self.state.detector.power, power_unit=self.state.detector.power_unit)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			obj_value = result[0][0]
			obj_unit = result[0][1]
				
			if bool_set:
				# Update detector
				self.state.detector.set_sweep_power(obj_value, obj_unit)
				self.display_detector_sweep_settings()
			else:
				pass
		
		# -------------------------
		# Display Detector Outputs
		# -------------------------
		def display_detector_sweep_settings(self):
			self.getChild('lbl_sweep_start_freq').setText(self.state.detector.get_sweep_start_freq_string())
			self.getChild('lbl_sweep_stop_freq').setText(self.state.detector.get_sweep_stop_freq_string())
			self.getChild('lbl_sweep_num_steps').setText(str(self.state.detector.num_steps))
			self.getChild('lbl_sweep_pwr').setText(self.state.detector.get_sweep_power_string())
		
		def display_detector_static_target_freq(self):
			self.getChild('lbl_static_generator_target_freq').setText(self.state.generator.get_target_freq_string() )
		
		def display_detector_static_target_power(self):
			self.getChild('lbl_static_generator_target_power').setText(self.state.generator.get_target_power_string() )
		
		def display_detector_static_read_power(self):
			self.getChild('lbl_detector_static_big_readout').setText(self.state.detector.get_static_read_power_string() )
		
		def display_detector(self):
			self.display_detector_sweep_settings()
			self.display_detector_static_target_freq()
			self.display_detector_static_target_power()
			self.display_detector_static_read_power()
		
		# =================================================
		# Settings / Network
		# =================================================
		def load_network_state(self):
			pass
		
		def set_network_mode(self):
			if self.getChild("rbtn_dynamic_ip").isChecked():
				self.set_dynamic_ip()
			else: # static
				self.set_static_ip()
		
		def set_dynamic_ip(self):
			self.getChild("frame_network_input_settings").setEnabled(False)
			self.state.network.auto_ip = True
			
		def set_static_ip(self):
			self.getChild("frame_network_input_settings").setEnabled(True)
			self.state.network.auto_ip = False
			
		# -------------------------
		# static ip settings
		# -------------------------
		def set_ip_address(self):
			w = QDialog_Set_IP(initial_value=self.state.network.ip_address)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			str_value = result[0]
				
			if bool_set:
				# Update network
				self.state.network.ip_address = str_value
				self.display_network_settings()
			else:
				pass
		
		def set_netmask(self):
			w = QDialog_Set_IP(initial_value=self.state.network.netmask)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			str_value = result[0]
				
			if bool_set:
				# Update network
				self.state.network.netmask = str_value
				self.display_network_settings()
			else:
				pass
		
		def set_gateway(self):
			w = QDialog_Set_IP(initial_value=self.state.network.gateway)
			w.setStyleSheet(self.styleSheet())
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			str_value = result[0]
				
			if bool_set:
				# Update network
				self.state.network.gateway = str_value
				self.display_network_settings()
			else:
				pass
		
		# -------------------------
		# Display Network Settings
		# -------------------------
		def display_network_settings(self):
			self.getChild("txt_ip_address").setText(self.state.network.ip_address)
			self.getChild("txt_netmask").setText(self.state.network.netmask)
			self.getChild("txt_gateway").setText(self.state.network.gateway)
		
		def display_network(self):
			self.display_network_settings()

		# -------------------------
		# Loops
		# -------------------------
		def LOOP(self):
			# Check if features are enabled before updating
			if self.state.detector.mode == "SWEEP":
				self.update_sweep_data()
			else:
				self.update_static_data()
			
			# End Loop
			QtCore.QTimer.singleShot(250, self.LOOP)
		
		def update_sweep_data(self):
			x,y = get_sweep_data()
			self.figure.line_objects.set_xdata(x)
			self.figure.line_objects.set_ydata(y)
			
			# Redraw/display
			self.figure.draw()
			self.figure.flush_events()
			# print("sweep beat")
		
		def update_static_data(self):
			# monkey wrench
			x,y = get_sweep_data()
			num = y[-1]
			self.state.detector.read_power = Power(num, UNIT.DBM)
			
			# display
			self.display_detector_static_read_power()
		
		# -------------------------
		# Get monkey data
		# -------------------------
		def update_information(self):
			# something about downloading and storing fake data
			pass
			
class Future_Socket_Class():
	pass

def main():
	app = QApplication([])
	
	m = main_menu()
	m.show()
	
	# Nope, polling outside of show doesn't seem to work
	# import time
	# x = 1
	# while(1):
	# 	print(str(x))
	# 	x+=1
	# 	time.sleep(1)
	
	app.exec_()

main()