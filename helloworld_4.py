from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget

import time, os

# ==============================================
# Globals that need to happento setup
# ==============================================
root_dir = """E:/projects_Python/RF_device_ui/"""
if not os.name == 'nt':
	root_dir = """/home/pi/Downloads/RF_device_ui/"""

path = root_dir + """/ui/helloworld_4.ui"""
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
class dummy(b):			
		def __init__(self, parent=None):
			super().__init__(parent)			
			# PlaceHolder
			self.ConnectSignalsAndSlots()
			
			# full screen
			self.windowsetup()
			
		def windowsetup(self):
			# https://stackoverflow.com/questions/7021502/pyqt-remove-the-programs-title-bar
			# https://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
			self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # requires QtCore, but more control
			self.showFullScreen()
			
		def ConnectSignalsAndSlots(self, *args, **kwargs):
			# PlaceHolder, override at will.
			# Programmically define click actions of children
			self.getChild('btn_exit').clicked.connect(self.close)
			pass

d = dummy()
d.show()

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
