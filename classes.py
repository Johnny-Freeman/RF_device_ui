from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

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

if __name__ == "__main__":
	i = import_widget4('test')