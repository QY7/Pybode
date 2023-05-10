from ui import Ui_MainWindow
from PyQt5.QtWidgets import  *
from plot_figure import Figure_Canvas
import numpy as np
import control as ct

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.plot_fig_bode_mag = Figure_Canvas()
        self.plot_fig_bode_phase = Figure_Canvas()
        self.plot_step_response = Figure_Canvas()
        self.plot_nyquist = Figure_Canvas()
        self.bodeLayout.addWidget(self.plot_fig_bode_mag)
        self.bodeLayout.addWidget(self.plot_fig_bode_phase)
        self.responseLayout.addWidget(self.plot_step_response)
        self.responseLayout.addWidget(self.plot_nyquist)

    def add_bode_line(self,ct_sys):
        mag,phase,omega = ct.bode(ct_sys,omega = np.linspace(0.1,1e3,10000))
        self.plot_fig_bode_mag.add_line(omega,20*np.log(mag),xlog=True,ylog=False)
        self.plot_fig_bode_phase.add_line(omega,phase*180/np.pi,xlog=True)

    def add_step_response_plot(self,ct_sys):
        resp = ct.step_response(ct_sys)
        self.plot_step_response.add_line(resp.time,resp.outputs)
        nyquist_resp = ct.nyquist_plot(ct_sys)

        