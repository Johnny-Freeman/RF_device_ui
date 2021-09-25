from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

import time

root_dir = """E:/projects_Python/RF_device_ui/"""


# ==============================================
# Globals that need to happento setup
# ==============================================
path = root_dir + "helloworld_2.ui"
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
			self.counter = 1
		
		def pushbutton_slot_test_1(self):
			# one way to interact is by overriding slot in the dialog.
			
			# setting values
			self.getChild('textEdit1').setText('yo' + str(self.counter))
			
			# reading values
			print(self.getChild('textEdit1').toPlainText())
			
			self.counter +=1
			# print(self.counter)
		
		def pushbutton_restyle(self):
			# -------------------------
			# Style sheets
			# -------------------------
			# https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html
			# https://doc.qt.io/qt-5/stylesheet-syntax.html#selector-types
			# https://stackoverflow.com/questions/22504421/how-to-apply-style-sheet-to-a-custom-widget-in-pyqt
			
			print("setting....")
			time.sleep(1)
			
			# That's rather annoying, # >> means search by ID, otherwise the name is taken as class/widget_space
			# Otherwise you could use QPushButton#pushButton3
			# Would be worth while to write a simple to use regex qt_stylesheet library or find one.
			style_sheet_test = """
				#pushButton3 {
					background-color: rgb(0, 0, 100);
				}
			"""
			self.setStyleSheet(style_sheet_test)
			
			# This works, but is bulky if we want to focus on style sheet
			# self.getChild('textEdit1').setStyleSheet("""	background-color: rgb(0, 0, 100);""")
			# self.getChild('pushButton3').setStyleSheet("""	background-color: rgb(0, 0, 100);""")
			
			
		def export_style_sheet(self)
			return self.styleSheet()

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