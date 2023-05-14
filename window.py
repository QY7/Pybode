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
        self.plot_bode_mag = Figure_Canvas()
        self.plot_bode_phase = Figure_Canvas()
        self.plot_step_response = Figure_Canvas()
        self.plot_nyquist = Figure_Canvas()
        self.bodeLayout.addWidget(self.plot_bode_mag)
        self.bodeLayout.addWidget(self.plot_bode_phase)
        self.responseLayout.addWidget(self.plot_step_response)
        self.responseLayout.addWidget(self.plot_nyquist)
        s = ct.tf('s')
        self.ct_sys = 1/(s+1)
        self.refresh_figure()

    @property
    def ct_sys(self):
        return self._ct_sys
    
    @ct_sys.setter
    def ct_sys(self,sys_str):
        self._ct_sys = sys_str

    def refresh_figure(self):
        ct_sys = self.ct_sys
        mag,phase,omega = ct.bode(ct_sys,omega = np.linspace(0.1,10e3,10000))
        _,nyquist_contour = ct.nyquist(ct_sys,plot=False,return_contour=True)
        nyq_resp = ct_sys(nyquist_contour)
        nyq_x,nyq_y = nyq_resp.real.copy(),nyq_resp.imag.copy()

        step_time,step_resp = ct.step_response(ct_sys)
        self.plot_bode_mag.add_line(omega,20*np.log(mag),x_min=0.1,x_max = 10e3,y_min=-100,y_max = 10,xlog=True,ylog=False)
        self.plot_bode_phase.add_line(omega,phase*180/np.pi,xlog=True,x_min = 0.1,x_max = 10e3,y_min =-200,y_max = 200)
        self.plot_nyquist.add_line(nyq_x,nyq_y,x_min = -1.2,x_max = 1.2,y_min=-1.2,y_max = 1.2)
        self.plot_nyquist.add_line(nyq_x,-nyq_y,x_min = -1.2,x_max = 1.2,y_min=-1.2,y_max = 1.2,style='--')
        self.plot_step_response.add_line(step_time,
                                         step_resp,
                                         x_min= min(step_time),
                                         x_max = max(step_time),
                                         y_min = 0,
                                         y_max = 10
                                         )

        