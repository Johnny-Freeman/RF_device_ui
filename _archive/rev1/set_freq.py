from PyQt5 import QtCore
import time, os

from classes import import_widget4

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

path = _getRoot() + """/ui/set_freq.ui"""

# ==============================================
# Widget dialog to get frequency input
# ==============================================
b = import_widget4(path)
class QDialog_Set_Freq(b):			
		def __init__(self, parent=None, initial_value=0, freq_unit="HZ"):
			super().__init__(parent)
			
			# Situate Window
			self.window_setup()
			self.load_stylesheets()
			
			# not sure if this is best method
			# depends on backend implimentation
			self.state = {
				"reset_value"	: str(initial_value),
				"input_value"	: "0",
				"reset_unit"	: freq_unit.upper(),
				"freq_unit"		: "HZ",
			}
			
			# display zeros
			self.update_display()
			
		def load_stylesheets(self):
			pass
			
		def window_setup(self):
			# https://stackoverflow.com/questions/7021502/pyqt-remove-the-programs-title-bar
			# https://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
			self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # requires QtCore, but more control
			# self.showFullScreen()
			
		def ConnectSignalsAndSlots(self, *args, **kwargs):
			# PlaceHolder, override at will.
			# Programmically define click actions of children
			# using built-in reject/accept, this also sets self.result() and handles other nuiances
			self.getChild('btn_cancel').clicked.connect(self.reject)
			self.getChild('btn_set').clicked.connect(self.accept)
			
			# clicked (not toggled) seems to work best for grouped buttons
			self.getChild('btn_num_1').clicked.connect(self.click_btn_num_1)
			self.getChild('btn_num_2').clicked.connect(self.click_btn_num_2)
			self.getChild('btn_num_3').clicked.connect(self.click_btn_num_3)
			self.getChild('btn_num_4').clicked.connect(self.click_btn_num_4)
			self.getChild('btn_num_5').clicked.connect(self.click_btn_num_5)
			self.getChild('btn_num_6').clicked.connect(self.click_btn_num_6)
			self.getChild('btn_num_7').clicked.connect(self.click_btn_num_7)
			self.getChild('btn_num_8').clicked.connect(self.click_btn_num_8)
			self.getChild('btn_num_9').clicked.connect(self.click_btn_num_9)
			self.getChild('btn_num_0').clicked.connect(self.click_btn_num_0)
			self.getChild('btn_num_00').clicked.connect(self.click_btn_num_00)
			self.getChild('btn_num_000').clicked.connect(self.click_btn_num_000)
			self.getChild('btn_num_decimal').clicked.connect(self.click_btn_num_decimal)
			self.getChild('btn_num_back').clicked.connect(self.click_btn_num_back)
			self.getChild('btn_num_CC').clicked.connect(self.click_btn_num_CC)
			
			# reset
			self.getChild('btn_reset').clicked.connect(self.click_btn_reset)
			
			# keyboard text input
			self.getChild('input_txt_num').textChanged.connect(self.keyboard_text_input_changed)
			
			# Radio buttons, freq choice
			self.getChild('btn_Hz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_KHz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_MHz').clicked.connect(self.update_frequency_choice)
			self.getChild('btn_GHz').clicked.connect(self.update_frequency_choice)
		
		# ------------------
		# Keypad
		# ------------------
		def click_btn_num_1(self):
			test_value = self.state["input_value"] + "1"
			self.value_update(test_value)
		
		def click_btn_num_2(self):
			test_value = self.state["input_value"] + "2" 
			self.value_update(test_value)
		
		def click_btn_num_3(self):
			test_value = self.state["input_value"] + "3" 
			self.value_update(test_value)
		
		def click_btn_num_4(self):
			test_value = self.state["input_value"] + "4" 
			self.value_update(test_value)
		
		def click_btn_num_5(self):
			test_value = self.state["input_value"] + "5" 
			self.value_update(test_value)
		
		def click_btn_num_6(self):
			test_value = self.state["input_value"] + "6" 
			self.value_update(test_value)
		
		def click_btn_num_7(self):
			test_value = self.state["input_value"] + "7" 
			self.value_update(test_value)
		
		def click_btn_num_8(self):
			test_value = self.state["input_value"] + "8" 
			self.value_update(test_value)
		
		def click_btn_num_9(self):
			test_value = self.state["input_value"] + "9" 
			self.value_update(test_value)
		
		def click_btn_num_0(self):
			test_value = self.state["input_value"] + "0" 
			self.value_update(test_value)
		
		def click_btn_num_00(self):
			test_value = self.state["input_value"] + "00" 
			self.value_update(test_value)
		
		def click_btn_num_000(self):
			test_value = self.state["input_value"] + "000" 
			self.value_update(test_value)
		
		def click_btn_num_decimal(self):
			test_value = self.state["input_value"] + "." 
			self.value_update(test_value)
		
		def click_btn_num_back(self):
			test_value = self.state["input_value"][:-1]
			self.value_update(test_value)
		
		def click_btn_num_CC(self):
			test_value = "0"
			self.value_update(test_value)
		
		def click_btn_reset(self):
			self.value_update(self.state["reset_value"])
			self.reset_frequency_choice()
		
		
		# ------------------
		# Updates
		# ------------------
		def value_update(self, test_string):
			# automatic zero
			if test_string == "":
				self.state["input_value"] = "0"
			
			else:
				try:
					float(test_string)
					
					# remove leading zeros
					if float(test_string) >= 1.0 and test_string[0] == "0":
						test_string = test_string.lstrip("0")
					
					self.state["input_value"] = test_string
				except:
					pass
			
			# update display
			self.update_display()
		
		def keyboard_text_input_changed(self):
			# str_value<str>
			str_value = self.getChild('input_txt_num').text()
			if str_value == self.state["input_value"]:
				# check duplicate loop
				return
			
			# else test input if valid float
			self.value_update(str_value)
			
		def reset_frequency_choice(self):
			self.state["freq_unit"] = self.state["reset_unit"]
			if self.state["freq_unit"] == "HZ":
				self.getChild("btn_Hz").setChecked(True)
			elif self.state["freq_unit"] == "KHZ":
				self.getChild("btn_KHz").setChecked(True)
			elif self.state["freq_unit"] == "MHZ":
				self.getChild("btn_MHz").setChecked(True)
			else: # GHz
				self.getChild("btn_GHz").setChecked(True)
			
			# update display
			self.update_frequency_choice()
		
		def update_display(self):
			self.getChild('input_txt_num').setText(str(self.state["input_value"]))
			self.update_frequency_choice()
		
		def update_frequency_choice(self):
			if self.getChild('btn_Hz').isChecked():
				self.state["freq_unit"] = "HZ"
			elif self.getChild('btn_KHz').isChecked():
				self.state["freq_unit"] = "KHZ"
			elif self.getChild('btn_MHz').isChecked():
				self.state["freq_unit"] = "MHZ"
			else: # GHz
				self.state["freq_unit"] = "GHZ"
			
			# last char is lowercase
			self.getChild('lbl_unit').setText( self.state["freq_unit"][:-1] + self.state["freq_unit"][-1].lower() )
		
		# ------------------
		# Callback
		# ------------------
		def result(self):
			# this may not be the best method to do this
			# looked into QInputDialog's source code to see how they do it, but this is better
			result = super().result()
			if result:
				return (float(self.state["input_value"]), self.state["freq_unit"]), True
			else:
				return (None, None), False

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])
	
	new_widget = QDialog_Set_Freq()
	new_widget.exec_()
	
	print(new_widget.result())
	
	# app.exec_() # to emulate calling window block
	