import  sys
from window import MainWindow
from PyQt5.QtWidgets import QApplication
import control as ct
import numpy as np
import matplotlib.pyplot as plt
_s = ct.tf('s')
bode_sys = ct.tf([1,2],[1,0])
nyquist_data = ct.nyquist_plot(bode_sys)

# ct.bode(bode_sys,omega = np.linspace(0.1,1e3,10000),plot=True)
# plt.show()
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	win.add_bode_line(bode_sys)
	win.plot_nyquist.ax = plt.gca()
	sys.exit(app.exec_())