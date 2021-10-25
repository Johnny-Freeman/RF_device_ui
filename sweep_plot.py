import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class QMatplot_Static(FigureCanvas):
	def __init__(self, x_data, y_data, parent=None):
		fig, self.ax = plt.subplots()
		super().__init__(fig)
		self.setParent(parent)
		
		# ------------------------
		# Matplot Script
		# ------------------------
		
		# To access line object functions later
		self.line_objects, = self.ax.plot(x_data, y_data)
		
		self.ax.set(
			xlabel="x axis",
			ylabel="y axis",
			title="Demo Data",
		)
		
		self.ax.grid()

if __name__ == "__main__":
	from random import uniform
	from PyQt5 import QtCore
	
	def get_sweep_data(size):
		# monkey wrench
		x = [i for i in range(size)]
		y = [uniform(0.8*float(i), 1.2*float(i)) for i in range(size)]
		return x,y
	
	from PyQt5.QtWidgets import QApplication, QWidget
	class AppDemo(QWidget):
		def __init__(self):
			super().__init__()
			self.resize(800,600)
			
			self.size = 100
			x,y = get_sweep_data(100)
			self.graph = QMatplot_Static(x,y, parent=self )
			
			# test update
			self.LOOP()
		
		def LOOP(self):
			self.update_data()
			
			# End Loop
			QtCore.QTimer.singleShot(1000, self.LOOP)
		
		def update_data(self):
			# https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
			# self.size+=1 # growing data >> must also change axis size
			self.size=100
			x,y = get_sweep_data(self.size)
			self.graph.line_objects.set_xdata(x)
			self.graph.line_objects.set_ydata(y)
			
			# Redraw/display
			self.graph.draw()
			self.graph.flush_events()
			# print("beat")
			
	# run testapp
	app = QApplication([])
	
	o = AppDemo()
	o.show()
	
	app.exec_()