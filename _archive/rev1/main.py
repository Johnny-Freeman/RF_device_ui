from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
import time, os

from set_freq import QDialog_Set_Freq
from set_pwr import QDialog_Set_Pwr
from classes import import_widget4, Echo_Session 

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
app = QApplication([])


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
			self.getChild('btn_set_pwr').clicked.connect(self.input_user_pwr)
			
			# Toggle between frequency units
			self.getChild('btn_Hz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_KHz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_MHz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_GHz').clicked.connect(self.update_frequency_choice)
			
			
			# -------------------------
			# Detector
			# -------------------------
			self.getChild('btn_toggle_static_mode').clicked.connect(self.set_detector_mode)			
			self.getChild('btn_toggle_sweep_mode').clicked.connect(self.set_detector_mode)	
			
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
		def input_user_freq(self):
			w = QDialog_Set_Freq(initial_value=self.state.generator.freq, freq_unit=self.state.generator.freq_unit)
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			value = result[0][0]
			unit = result[0][1]
				
			if bool_set:
				# Update generator targets
				self.state.generator.set_target_freq(value, unit)
				self.display_set_freq()
			else:
				pass
		
		def update_frequency_choice(self):
			if self.getChild('btn_Hz').isChecked():
				unit = "HZ"
			elif self.getChild('btn_KHz').isChecked():
				unit = "KHZ"
			elif self.getChild('btn_MHz').isChecked():
				unit = "MHZ"
			else: # GHZ
				unit = "GHZ"
			self.state.generator.set_freq_unit(unit)
			
			# update displays
			self.display_set_freq()
		
		def input_user_pwr(self): #WIP
			w = QDialog_Set_Pwr(initial_value=self.state.generator.pwr, pwr_unit=self.state.generator.pwr_unit)
			w.exec_()
						
			result = w.result()
			bool_set = result[1]
			value = result[0][0]
			unit = result[0][1]
				
			if bool_set:
				# Update generator targets
				# self.state.generator.set_target_freq(value, unit)
				# self.display_set_freq()
				#WIP
				pass
			else:
				pass
		
		# -------------------------
		# Display generator outputs
		# -------------------------
		def display_set_freq(self):
			target_freq_string = self.state.generator.get_target_freq_string()
			self.getChild('lbl_freq_target').setText(target_freq_string)
		
		# -------------------------
		# Backend
		# -------------------------		
		def toggle_rf_on_off(self):
			if self.getChild('btn_rf_on').isChecked():
				self.state["generator"]["rf_on"] = True
			else:
				self.state["generator"]["rf_on"] = False
		
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

def main():
	m = main_menu()
	m.show()
	
	app.exec_()

main()