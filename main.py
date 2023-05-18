import  sys
from pybode import PyBode
from PyQt5.QtWidgets import QApplication
import control as ct
import numpy as np
import matplotlib.pyplot as plt
# plt.show()
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = PyBode()
	win.show()
	sys.exit(app.exec_())