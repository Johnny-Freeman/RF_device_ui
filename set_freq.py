from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
import time, os

from classes import import_widget4

# ==============================================
# Globals that need to happento setup
# ==============================================
root_dir = """D:/projects_Python/RF_device_ui/"""
if not os.name == 'nt':
	root_dir = """/home/pi/Downloads/RF_device_ui/"""

path = root_dir + """/ui/set_freq.ui"""

# ==============================================
# Widget dialog to get freq input
# ==============================================
b = import_widget4(path)
class QDialog_Set_Freq(b):			
		def __init__(self, parent=None, input_value=0, freq_unit="HZ"):
			super().__init__(parent)			
			# PlaceHolder
			# self.ConnectSignalsAndSlots() # OMG << this is reserved namespace, (causes double click issues)
			
			# Situate Window
			self.windowsetup()
			self.load_stylesheets()
			
			# not sure if this is best method
			# depends on backend implimentation
			self.state = {
				"reset_value"	: str(input_value),
				"input_value"	: str(input_value),
				"freq_unit"		: freq_unit,
			#	""	: ,
			#	""	: ,
			#	""	: ,
			#	""	: ,
			#	""	: ,
			}
			
			# Initial Values
			self.getChild('input_txt_num').setText(str(self.state["input_value"]))
			
		def load_stylesheets(self):
			pass
			
		def windowsetup(self):
			# https://stackoverflow.com/questions/7021502/pyqt-remove-the-programs-title-bar
			# https://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
			self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # requires QtCore, but more control
			# self.showFullScreen()
			
		def ConnectSignalsAndSlots(self, *args, **kwargs):
			# PlaceHolder, override at will.
			# Programmically define click actions of children
			# using built-in reject/accept, this also sets self.result() and handles other nuances
			self.getChild('btn_cancel').clicked.connect(self.reject)
			self.getChild('btn_set').clicked.connect(self.accept)
			
			# clicked (not toggled) seems to work best for grouped buttons << WIP
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
		
		# Keypad
		def click_btn_num_1(self):
			test_value = self.state["input_value"] + "1"
			self.keypad_update(test_value)
		
		def click_btn_num_2(self):
			test_value = self.state["input_value"] + "2" 
			self.keypad_update(test_value)
		
		def click_btn_num_3(self):
			test_value = self.state["input_value"] + "3" 
			self.keypad_update(test_value)
		
		def click_btn_num_4(self):
			test_value = self.state["input_value"] + "4" 
			self.keypad_update(test_value)
		
		def click_btn_num_5(self):
			test_value = self.state["input_value"] + "5" 
			self.keypad_update(test_value)
		
		def click_btn_num_6(self):
			test_value = self.state["input_value"] + "6" 
			self.keypad_update(test_value)
		
		def click_btn_num_7(self):
			test_value = self.state["input_value"] + "7" 
			self.keypad_update(test_value)
		
		def click_btn_num_8(self):
			test_value = self.state["input_value"] + "8" 
			self.keypad_update(test_value)
		
		def click_btn_num_9(self):
			test_value = self.state["input_value"] + "9" 
			self.keypad_update(test_value)
		
		def click_btn_num_0(self):
			test_value = self.state["input_value"] + "0" 
			self.keypad_update(test_value)
		
		def click_btn_num_00(self):
			test_value = self.state["input_value"] + "00" 
			self.keypad_update(test_value)
		
		def click_btn_num_000(self):
			test_value = self.state["input_value"] + "000" 
			self.keypad_update(test_value)
		
		def click_btn_num_decimal(self):
			test_value = self.state["input_value"] + "." 
			self.keypad_update(test_value)
		
		def click_btn_num_back(self):
			test_value = self.state["input_value"][:-1]
			self.keypad_update(test_value)
		
		def click_btn_num_CC(self):
			test_value = self.state["input_value"] = "0"
			self.keypad_update(test_value)
		
		def click_btn_reset(self):
			self.keypad_update(self.state["reset_value"])
		
		
		# ------------------
		# Updates
		# ------------------
		def keypad_update(self, test_string):
			if test_string == "":
				self.state["input_value"] = "0"
			
			else:
				try:
					float(test_string)
					
					# remove leading zero
					if float(test_string) >= 1.0 and test_string[0] == "0":
						test_string = test_string[1:]
					
					self.state["input_value"] = test_string
				except:
					pass
			
			# update label
			self.getChild('input_txt_num').setText(str(self.state["input_value"]))
		
		def keyboard_text_input_changed(self):
			# str_value<str>
			str_value = self.getChild('input_txt_num').text()
			if str_value == self.state["input_value"]:
				# check duplicate loop
				return
			
			# else test input if valid float
			self.keypad_update(str_value)
		
		# ------------------
		# Callback
		# ------------------
		def result(self):
			# this may not be the best method to do this
			# looked into QInputDialog's source code to see how they do it, but this is better
			result = super().result()
			if result:
				return (self.state["input_value"], self.state["freq_unit"]), True
			else:
				return None, False

if __name__ == "__main__":
	app = QApplication([])
	new_widget = QDialog_Set_Freq()
	new_widget.exec_()
	
	print(new_widget.result())
	
	app.exec_()
	