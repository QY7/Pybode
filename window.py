from ui import Ui_MainWindow
from PyQt5.QtWidgets import  *
from plot_figure import Figure_Canvas
import numpy as np
import control as ct
import matplotlib.pyplot as plt

from PyQt5.QtCore import *

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.fig_bode_mag   = Figure_Canvas()
        self.fig_bode_phase = Figure_Canvas()
        self.fig_step_resp  = Figure_Canvas()
        self.fig_nyquist    = Figure_Canvas()
        s = ct.tf('s')
        self.ct_gain = ct.tf([1],[1])
        self.ct_sys = self.ct_gain
        self.freq_min = 0.01
        self.freq_max = 100000
        self.bode_mag_plot.addWidget(self.fig_bode_mag)
        self.bode_phase_plot.addWidget(self.fig_bode_phase)
        self.step_resp_plot.addWidget(self.fig_step_resp)
        self.nyquist_plot.addWidget(self.fig_nyquist)
        self.shift_state = False
        self.ctrl_state = False
        self.pole_arr = [100]
        self.zero_arr = []
        self.draw_figure()

    @property
    def freq_min(self):
        return self._freq_min
    
    @freq_min.setter
    def freq_min(self,val):
        self._freq_min = float(val)
        print(val)

    @property
    def freq_max(self):
        return self._freq_max
    
    @freq_max.setter
    def freq_max(self,val):
        self._freq_max = float(val)
        print(val)

    @property
    def ct_sys(self):
        return self._ct_sys
    
    @ct_sys.setter
    def ct_sys(self,sys_str):
        self._ct_sys = sys_str

    def set_freq_range(self):
        try:
            self.freq_min = float(self.edit_freq_min.text())
            self.freq_max = float(self.edit_freq_max.text())
            self.refresh_figure()
        except:
            return

    def draw_figure(self):
        ct_sys = self.ct_sys
        mag,phase,omega = ct.bode(
            ct_sys,
            plot=False,
            omega = np.geomspace(self.freq_min,self.freq_max,100000)
        )
        try:
            _,nyquist_contour = ct.nyquist(ct_sys,plot=False,return_contour=True)
            nyq_resp = ct_sys(nyquist_contour)
            nyq_x,nyq_y = nyq_resp.real.copy(),nyq_resp.imag.copy()
            self.fig_nyquist.add_line(
                nyq_x,
                nyq_y,
                x_min = -10,
                x_max = 10,
                y_min=-10,
                y_max = 10
            )
            self.fig_nyquist.add_line(
                nyq_x,
                -nyq_y,
                x_min = -10,
                x_max = 10,
                y_min=-10,
                y_max = 10,
                style='--'
            )
        except:
            pass
        step_time,step_resp = ct.step_response(ct_sys)
        self.fig_bode_mag.add_line(
            omega,20*np.log(mag),
            x_min=self.freq_min,
            x_max = self.freq_max,
            y_min=-100,
            y_max = 100,
            xlog=True,
            ylog=False
        )
        self.fig_bode_phase.add_line(
            omega,phase*180/np.pi,
            xlog=True,
            x_min = self.freq_min,
            x_max = self.freq_max,
            y_min =-200,
            y_max = 200
        )

        self.fig_step_resp.add_line(
            step_time,
            step_resp,
            x_min= min(step_time),
            x_max = max(step_time),
            y_min = 0,
            y_max = 10
        )
        cid = self.fig_bode_mag.mpl_connect('button_press_event', self.add_pole_zero)
        self.refresh_figure()

    def refresh_figure(self):
        self.ct_sys = self.ct_gain
        for item in self.pole_arr:
            tmp_blk = ct.tf([1],[1/item,1])
            self.ct_sys = ct.series(self.ct_sys,tmp_blk)
        for item in self.zero_arr:
            tmp_blk = ct.tf([1/item,1],[1])
            self.ct_sys = ct.series(self.ct_sys,tmp_blk)

        mag,phase,omega = ct.bode(
            self.ct_sys,
            plot=False,
            omega = np.geomspace(self.freq_min,self.freq_max,100000)
        )
        mag = 20*np.log(mag)
        phase = phase+2*np.pi
        self.fig_bode_mag.update_fig(
            x_min=self.freq_min,
            x_max=self.freq_max,
            x_data = omega,
            y_data = mag
        )

        self.fig_bode_phase.update_fig(
            x_min=self.freq_min,
            x_max=self.freq_max,
            y_min = - np.pi*2,
            y_max =   np.pi*2,
            x_data = omega,
            y_data = phase
        )
    # 检测键盘回车按键，函数名字不要改，这是重写键盘事件
    def keyPressEvent(self, event):
        print(event.key())
        if(event.key() == 16777248):
            self.shift_state = True
        elif(event.key() == 16777249):
            self.ctrl_state = True

    def keyReleaseEvent(self,event):
        if(event.key() == 16777248):
            self.shift_state = False
        elif(event.key() == 16777249):
            self.ctrl_state = False

    def add_pole_zero(self,event):
        if self.shift_state:
            print(f"Adding pole at {event.xdata}")
            self.pole_arr.append(event.xdata)
        elif(self.ctrl_state):
            print(f"Adding zero at {event.xdata}")
            self.zero_arr.append(event.xdata)
        self.refresh_figure()