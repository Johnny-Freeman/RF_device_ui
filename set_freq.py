from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
import time, os

from classes import import_widget4

# ==============================================
# Globals that need to happento setup
# ==============================================
root_dir = """E:/projects_Python/RF_device_ui/"""
if not os.name == 'nt':
	root_dir = """/home/pi/Downloads/RF_device_ui/"""

path = root_dir + """/ui/set_freq.ui"""

# ==============================================
# Widget dialog to get freq input
# ==============================================
b = import_widget4(path)
class QDialog_Set_Freq(b):			
		def __init__(self, parent=None, input_value, freq_unit):
			super().__init__(parent)			
			# PlaceHolder
			self.ConnectSignalsAndSlots()
			
			# Situate Window
			self.windowsetup()
			self.load_stylesheets()
			
			# not sure if this is best method
			# depends on backend implimentation
			self.state = {
				"input_value"	: input_value,
				"freq_unit"	: , freq_unit,
				""	: ,
				""	: ,
				""	: ,
				""	: ,
				""	: ,
				""	: ,
			}
			
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
			self.getChild('btn_cancel').clicked.connect(self.close)
			
			WIP
			# clicked (not toggled) seems to work best for grouped buttons << WIP
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			
			# reset, canceling, setting
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			self.getChild('btn_').clicked.connect(self.click_btn_)
			
			# keyboard text input
			self.getChild('input_txt_num').textChanged.connect(self.keyboard_text_changed)
		
		def click_btn_(self):
			self.state["input_value"] += "" 
		
		def update_lbl_input_txt(self):
			self.
		
		def keyboard_text_input_changed(self):
			value = self.getChild('input_txt_num').get

if __name__ == "__main__":
	app = QApplication([])
	new_widget = QDialog_Set_Freq()
	new_widget.show()
	app.exec_()
	