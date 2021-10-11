from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
import time, os

# ==============================================
# Globals that need to happento setup
# ==============================================
root_dir = """E:/projects_Python/RF_device_ui/"""
if not os.name == 'nt':
	root_dir = """/home/pi/Downloads/RF_device_ui/"""

path = root_dir + """/ui/main_1.ui"""
app = QApplication([])

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
			# PlaceHolder, override at will.
			# Programmically define click actions of children
			# self.findChild(QWidget, 'pushButton2').clicked.connect(self.print_funct)
			# self.getChild('pushButton2').clicked.connect(self.print_funct)
			pass
		
	return dummy #returns a class, not instance to use as inheritence later.


b = import_widget4(path)
class main_menu(b):			
		def __init__(self, parent=None):
			super().__init__(parent)			
			# PlaceHolder
			self.ConnectSignalsAndSlots()
			
			# Situate Window
			self.windowsetup()
			
			
			# not sure if this is best method
			# depends on backend implimentation
			self.state = {
				"rf_on_off" : True,
			}
			
			self.load_stylesheets()
			
						
		def load_stylesheets(self):
			# load tab style sheets
			# self.getChild('tabWidget').setStyleSheet("QTabBar::tab { height: 40px; width: 120px; }")
			
			# general stylesheet
			stylesheet = """
				#tabWidget {
					QTabBar::tab { height: 40px; width: 120px; }
				}
			"""
			self.setStyleSheet(stylesheet)
			
		def windowsetup(self):
			# https://stackoverflow.com/questions/7021502/pyqt-remove-the-programs-title-bar
			# https://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
			self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # requires QtCore, but more control
			# self.showFullScreen()
			
		def ConnectSignalsAndSlots(self, *args, **kwargs):
			# PlaceHolder, override at will.
			# Programmically define click actions of children
			self.getChild('btn_exit').clicked.connect(self.close)
			
			# clicked (not toggled) seems to work best for grouped buttons
			self.getChild('btn_rf_on').clicked.connect(self.update_checkbox_labels)
			self.getChild('btn_rf_off').clicked.connect(self.update_checkbox_labels)
			self.getChild('btn_rf_on_2').clicked.connect(self.update_checkbox_labels)
			
		def update_checkbox_labels(self):
			print("toggled") # looks grouped buttons have a double click to them.
			# if self.getChild('btn_rf_on').isChecked():
			# 	# ON
			# 	self.getChild('lbl_status').setText("RF is ON")
			# elif self.getChild('btn_rf_off').isChecked():
			# 	#OFF
			# 	self.getChild('lbl_status').setText("RF is OFF")
			# else:
			# 	# Whoops
			# 	self.getChild('lbl_status').setText("What have you done.")



m = main_menu()
m.show()

app.exec_()

"""
# ==============================================
# Globals that need to happento setup
# ==============================================
app = QApplication([])

# Loads UI
Widget_Ui, Widget_class = uic.loadUiType(root_dir + "helloworld.ui")

widget = Widget_class()


# some global decorator that's required for loading UI.
ui_handle = Widget_Ui()
ui_handle.setupUi(widget)

print(dir(widget.children))

widget.show() # exec() also works but then app is still running without exit() command

#block can this be down at the bottom or does it have to be at the top? >> yes app is global
# QT just requires the app wrapper
app.exec_()
"""
