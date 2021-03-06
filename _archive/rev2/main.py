from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import os

from set_freq import QDialog_Set_Freq
from set_pwr import QDialog_Set_Power
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

# ==============================================
# Main Application
# ==============================================
b = import_widget4(path)
class main_menu(b):			
		def __init__(self, parent=None):
			super().__init__(parent)				
			# Situate Window
			self.window_setup()
			
			# Application State
			self.state = Echo_Session()
			
			# Style Sheets
			self.load_stylesheets()
			
		def load_stylesheets(self):
			# load tab style sheets
			# self.getChild('tabWidget').setStyleSheet("QTabBar::tab { height: 40px; width: 120px; }")
			
			# General stylesheet
			stylesheet = """
				QTabBar::tab { height: 40px; width: 120px; }
			"""
			self.setStyleSheet(stylesheet)
			
		def window_setup(self):
			# https://stackoverflow.com/questions/7021502/pyqt-remove-the-programs-title-bar
			# https://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
			self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # requires QtCore, but more control
			# self.showFullScreen()
			
		def ConnectSignalsAndSlots(self, *args, **kwargs):
			# Reserved PlaceHolder, override at will.
			# Programmically define click actions of children
			self.getChild('btn_exit').clicked.connect(self.close)
			
			
			# -------------------------
			# Generator
			# -------------------------
			# Toggle RF ON/OFF
			# clicked (not toggled) seems to work best for grouped buttons
			self.getChild('btn_rf_on').clicked.connect(self.toggle_rf_on_off)
			self.getChild('btn_rf_off').clicked.connect(self.toggle_rf_on_off)
			
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
			
			# 
			self.getChild('btn_sweep_start_freq').clicked.connect(self.set_detector_mode)
			self.getChild('btn_sweep_stop_freq').clicked.connect(self.set_detector_mode)
			self.getChild('btn_sweep_num_steps').clicked.connect(self.set_detector_mode)
			self.getChild('btn_sweep_pwr').clicked.connect(self.set_detector_mode)
			
			# -------------------------
			# Settings / Network
			# -------------------------
			self.getChild("rbtn_dynamic_ip").clicked.connect(self.set_network_mode)
			self.getChild("rbtn_static_ip").clicked.connect(self.set_network_mode)
		
		# =================================================
		# Generator
		# =================================================
		# -------------------------
		# Retreiving User input
		# -------------------------
		# frequency
		def input_user_freq(self):
			w = QDialog_Set_Freq(initial_value=self.state.generator.target_freq, freq_unit=self.state.generator.freq_unit)
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			obj_value = result[0][0]
			# obj_unit = result[0][1] # not used
				
			if bool_set:
				# Update generator targets
				self.state.generator.set_target_freq(obj_value)
				self.display_target_freq()
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
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			obj_value = result[0][0]
			# obj_unit = result[0][1] # not used
				
			if bool_set:
				# Update generator targets
				self.state.generator.set_target_power(obj_value)
				self.display_target_power()
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
		
		# -------------------------
		# Backend
		# -------------------------		
		def toggle_rf_on_off(self):
			if self.getChild('btn_rf_on').isChecked():
				self.state.generator.rf_on = True
			else:
				self.state.generator.rf_on = False
		
		# =================================================
		# Detector
		# =================================================
		def set_detector_mode(self):
			if self.getChild("btn_toggle_static_mode").isChecked():
				self.state.detector.mode = "STATIC"
				self.init_detector_static_mode()
			else:
				self.state.detector.mode = "SWEEP"
				self.init_detector_sweep_mode()
		
		def init_detector_static_mode(self):
			self.getChild("grp_sweep_controls").setEnabled(False)
		
		def init_detector_sweep_mode(self):
			self.getChild("grp_sweep_controls").setEnabled(True)
			
		
		# -------------------------
		# Sweep settings
		# -------------------------
		
		# =================================================
		# Settings / Network
		# =================================================
		def set_network_mode(self):
			if self.getChild("rbtn_dynamic_ip").isChecked():
				self.set_dynamic_ip()
			else: # static
				self.set_static_ip()
		
		def set_dynamic_ip(self):
			self.getChild("frame_network_input_settings").setEnabled(False)
			
		def set_static_ip(self):
			self.getChild("frame_network_input_settings").setEnabled(True)
			
		# -------------------------
		# static ip settings
		# -------------------------
		def set_ip_address(self):
			pass
		
		def set_netmask(self):
			pass
		
		def set_gateway(self):
			pass

def main():
	app = QApplication([])
	
	m = main_menu()
	m.show()
	
	app.exec_()

main()