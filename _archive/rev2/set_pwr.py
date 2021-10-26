from PyQt5 import QtCore
import os

from classes import import_widget4, Power, UNIT

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

path = _getRoot() + """/ui/set_pwr.ui"""

# ==============================================
# Widget dialog to get power input
# ==============================================
b = import_widget4(path)
class QDialog_Set_Power(b):			
		def __init__(self, parent=None, initial_value=Power(0, UNIT.DBM), power_unit=UNIT.DBM):
			super().__init__(parent)
			
			# Situate Window
			self.window_setup()
			self.load_stylesheets()
			
			# not sure if this is best method
			# depends on backend implimentation
			self.state = {
				"reset_value"	: str(initial_value.cast(power_unit)),
				"input_value"	: "0",
				"reset_unit"	: power_unit,
				"pwr_unit"		: power_unit,
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
			# WIP
			self.getChild('btn_dBm').clicked.connect(self.update_power_choice)
			self.getChild('btn_mW').clicked.connect(self.update_power_choice)
			self.getChild('btn_W').clicked.connect(self.update_power_choice)
		
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
			self.reset_power_choice()
		
		
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
		
		def reset_power_choice(self):
			self.state["freq_unit"] = self.state["reset_unit"]
			if self.state["freq_unit"] == UNIT.MIL:
				self.getChild("btn_mW").setChecked(True)
			elif self.state["freq_unit"] == UNIT.W:
				self.getChild("btn_W").setChecked(True)
			else: # dBm
				self.getChild("btn_dBm").setChecked(True)
			
			# update display
			self.update_power_choice()
		
		def update_display(self):
			self.getChild('input_txt_num').setText( self.state["input_value"] )
			self.update_power_choice()
		
		def update_power_choice(self):
			if self.getChild('btn_mW').isChecked():
				self.state["freq_unit"] = UNIT.MIL
			elif self.getChild('btn_W').isChecked():
				self.state["freq_unit"] = UNIT.W
			else: # dBm
				self.state["freq_unit"] = UNIT.DBM
			
			# last char is lowercase
			self.getChild('lbl_unit').setText( str(self.state["freq_unit"]) )
		
		# ------------------
		# Callback
		# ------------------
		def result(self):
			# this may not be the best method to do this
			# looked into QInputDialog's source code to see how they do it, but this is better
			result = super().result()
			if result:
				f = Power(float(self.state["input_value"]), self.state["freq_unit"])
				return ( f , self.state["freq_unit"]), True
			else:
				return (None, None), False


if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])
	
	new_widget = QDialog_Set_Power()
	new_widget.exec_()
	
	print(new_widget.result())
	
	# app.exec_() # to emulate calling window block