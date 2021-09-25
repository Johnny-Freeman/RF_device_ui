from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget


root_dir = """E:/projects_Python/RF_device_ui/"""


# ==============================================
# Globals that need to happento setup
# ==============================================
path = root_dir + "helloworld_1.ui"
app = QApplication([])


# ==============================================
# Importing and Initializing Widgets
# ==============================================
def import_widget(path, parent=None):
	# Loads UI
	Widget_Ui, Widget_class = uic.loadUiType(path)
	class dummy(Widget_class, Widget_Ui):
		def __init__(self, parent):
			super().__init__(parent)
			# Widget_class uses Widget_Ui to configure itself( passes Widget_Ui.setupUi(Widget_class) )
			# this method is slightly cleaner (uses inheritence and seldf initializes), with both ui and widget pulled from same file
			self.setupUi(self)
	
	return dummy(parent)
	
def import_widget2(path, parent=None):
	# Loads UI
	Widget_Ui, Widget_class = uic.loadUiType(path)
	# print(Widget_Ui, Widget_class)
	class dummy(Widget_class):
		def __init__(self, parent):
			super().__init__(parent)
			# Widget_class uses Widget_Ui to configure itself
			# this method is more composition-like as it assumes seperate Widget_class and Ui_layout files
			uic.loadUi(path, self)
	
	return dummy(parent)

def import_widget3(path, parent=None):
	# Loads UI
	Widget_Ui, Widget_class = uic.loadUiType(path)
	class dummy(Widget_class):
		def __init__(self, parent):
			super().__init__(parent)
			# Widget_class uses Widget_Ui to configure itself( passes Widget_Ui.setupUi(Widget_class) )
			# this method is composition
			ui = Widget_Ui()
			ui.setupUi(self)

	return dummy(parent)

def import_widget4(path):
	# Loads UI
	# This method is prefered
	#	Returns a parent_class for inheritence
	#	Loads helpful general use methods
	#	Allows initial configuration of class such as modal
	
	# Use case:
	#b = import_widget4(path)
	#class dummy(b):			
	#		def __init__(self, parent=None):
	#			super().__init__(parent)	
	#		def Foobar(self):
	#			pass
		
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



# ==============================================
# Interacting with Children, Signals and Slots
# ==============================================
def import_widget4(path, parent=None):
	# Loads UI
	Widget_Ui, Widget_class = uic.loadUiType(path)
	class dummy(Widget_class):
		def getChild(self, regex_name):
			# returns child, quick and simple
			# QWidget is the most basic of classes and will search through all widgets.
			return self.findChild(QWidget, regex_name)
		
		def getChildren(self, regex_name):
			# returns list of children, quick and simple
			# QWidget is the most basic of classes and will search through all widgets.
			return self.findChildren(QWidget, regex_name)
			
		def __init__(self, parent):
			super().__init__(parent)
			# Widget_class uses Widget_Ui to configure itself( passes Widget_Ui.setupUi(Widget_class) )
			# this method is composition
			ui = Widget_Ui()
			ui.setupUi(self)
			
			# ConnectSignalsAndSlots (programmically)
			# programmically define click actions of children
			# self.findChild(QWidget, 'pushButton2').clicked.connect(self.print_funct)
			
			self.counter = 1
		
		def pushbutton_slot_test_1(self):
			# one way to interact is by overriding slot in the dialog.
			
			# setting values
			# self.getChild('textEdit1').setText('yo' + str(self.counter))
			
			# reading values
			# print(self.getChild('textEdit1').toPlainText())
			
			self.counter +=1
			# print(self.counter)
		
		def print_funct(self):
			print('yo')

	return dummy(parent)


d = import_widget4(path)
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