from ui import Ui_MainWindow
from PyQt5.QtWidgets import  *
from plot_figure import Figure_Canvas
import numpy as np
import control as ct
import matplotlib.pyplot as plt

from PyQt5.QtCore import *
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']# 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

INF_VALUE = float('inf')

class PyBode(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(PyBode, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.fig_bode_mag   = Figure_Canvas()
        self.fig_bode_phase = Figure_Canvas()
        self.fig_step_resp  = Figure_Canvas()
        self.fig_nyquist    = Figure_Canvas()
        self.ct_gain = ct.tf([100],[1,2,10])
        self.freq_min = 0.01
        self.freq_max = 100000
        self.bode_mag_plot.addWidget(self.fig_bode_mag)
        self.bode_phase_plot.addWidget(self.fig_bode_phase)
        self.step_resp_plot.addWidget(self.fig_step_resp)
        self.nyquist_plot.addWidget(self.fig_nyquist)
        cid = self.fig_bode_mag.mpl_connect('button_press_event', self.add_pole_zero)
        self.shift_state = False
        self.ctrl_state = False
        self.pole_arr = []
        self.zero_arr = [100]
        self.wcp = float('inf')
        self.wcp = float('inf')
        self.gm = float('inf')
        self.pm = float('inf')
        self.stable = False
        self.refresh_figure()

    @property
    def freq_min(self):
        return self._freq_min
    
    @freq_min.setter
    def freq_min(self,val):
        self._freq_min = float(val)

    @property
    def freq_max(self):
        return self._freq_max
    
    @freq_max.setter
    def freq_max(self,val):
        self._freq_max = float(val)

    @property
    def ct_sys(self):
        sys_tmp = self.ct_gain
        for item in self.pole_arr:
            if(item == 0):
                tmp_blk = ct.tf([1],[1,0])
            else:
                tmp_blk = ct.tf([1],[1/item,1])
            sys_tmp = ct.series(sys_tmp,tmp_blk)
        for item in self.zero_arr:
            if(item == 0):
                tmp_blk = ct.tf([1,0],[1])
            else:
                tmp_blk = ct.tf([1/item,1],[1])
            sys_tmp = ct.series(sys_tmp,tmp_blk)
        return sys_tmp
    

    def set_freq_range(self):
        try:
            self.freq_min = float(self.edit_freq_min.text())
            self.freq_max = float(self.edit_freq_max.text())
            self.refresh_figure()
        except:
            return

    def refresh_nyquist(self):
        try:
            _,nyquist_contour = ct.nyquist(self.ct_sys,plot=False,return_contour=True)
            nyq_resp = self.ct_sys(nyquist_contour)
            nyq_x,nyq_y = nyq_resp.real.copy(),nyq_resp.imag.copy()
            self.fig_nyquist.ax.clear()
            self.fig_nyquist.update_line(
                idx = 0,
                x_data = nyq_x,
                y_data = nyq_y
            )
            self.fig_nyquist.update_line(
                idx = 1,
                x_data = nyq_x,
                y_data = -nyq_y,
                linestyle= '--'
            )
            resp_0Hz = abs(ct.evalfr(self.ct_sys, 0))
            self.fig_nyquist.ax.plot(resp_0Hz,0,'ko')

            x_min = min(nyq_x)
            x_max = max(nyq_x)
            x_min = x_min*0.8 if x_min>0 else x_min*1.2
            x_max = x_max*1.2 if x_max>0 else x_max*0.8

            y_max = max(max(nyq_y),max(-nyq_y))*1.2
            self.fig_nyquist.refresh_fig(
                x_min= x_min,
                x_max = x_max,
                y_min = -y_max,
                y_max = y_max,
                title = "Nyquist plot"
            )
        except Exception as e:
            print(e)
            pass
        
    def refresh_margin(self):
        gm, pm, wcg, wcp = ct.margin(self.ct_sys)
        self.gm = gm
        self.pm = pm
        self.wcg = wcg
        self.wcp = wcp
        self.mag_margin_label.setText(f"{gm:.1f}")
        self.phase_margin_label.setText(f"{pm:.1f}")
        self.wcg_label.setText(f"{wcg:.1f}")
        self.wcp_label.setText(f"{wcp:.1f}")
        if(gm > 1 and pm > 0):
            self.stable_label.setText("Stable")
        else:
            self.stable_label.setText("Unstable")

    def refresh_step(self):
        step_time,step_resp = ct.step_response(self.ct_sys)
        self.fig_step_resp.update_line(
            idx = 0,
            x_data = step_time,
            y_data = step_resp,
            
        )
        y_min = min(step_resp)
        y_max = max(step_resp)

        y_min = y_min*0.8 if y_min>0 else y_min*1.2
        y_max = y_max*1.2 if y_max>0 else y_max*0.8
        self.fig_step_resp.refresh_fig(
            x_min= min(step_time),
            x_max = max(step_time),
            y_min = y_min,
            y_max = y_max,
            title = "Step response"
        )

    def refresh_bode(self):
        zeros = ct.zero(self.ct_sys)
        poles = ct.pole(self.ct_sys)
        poles = np.abs(poles)
        zeros = np.abs(zeros)
        gain_at_poles = 20*np.log(np.array([abs(ct.evalfr(self.ct_sys,x*1j)) for x in poles]))
        gain_at_zeros = 20*np.log(np.array([abs(ct.evalfr(self.ct_sys,x*1j)) for x in zeros]))
        self.fig_bode_mag.ax.clear()
       
        mag,phase,omega = ct.bode(
            self.ct_sys,
            plot=False,
            omega = np.geomspace(self.freq_min,self.freq_max,100000)
        )
        phase = phase*180/np.pi
        phase %= 360  # 将角度限制在0到360之间
        phase[phase > 0] -= 360
        mag = 20*np.log(mag)
        self.fig_bode_mag.update_line(
            idx = 0,
            x_data = omega,
            y_data = mag,
        )

        self.fig_bode_phase.update_line(
            idx = 0,
            x_data = omega,
            y_data = phase,
            
        )
        self.fig_bode_mag.ax.plot(poles,gain_at_poles,'g*',linestyle='None')
        self.fig_bode_mag.ax.plot(zeros,gain_at_zeros,'g',marker='o',linestyle='None', fillstyle='none')
        self.fig_bode_mag.refresh_fig(
            x_min=self.freq_min,
            x_max=self.freq_max,
            y_min = min(mag)-10,
            y_max = max(mag)+10,
            x_scale = 'log',
            title = "Bode-mag"
        )
        self.fig_bode_phase.refresh_fig(
            x_min=self.freq_min,
            x_max=self.freq_max,
            y_min = - 360,
            y_max =   360,
            x_scale = 'log',
            title = "Bode-phase"
        )

    def refresh_figure(self):
        self.refresh_margin()
        self.refresh_bode()
        self.refresh_nyquist()
        self.refresh_step()
        

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
            if(event.xdata != None):
                print(f"Adding pole at {event.xdata}")
                self.pole_arr.append(event.xdata)
        elif(self.ctrl_state):
            if(event.xdata != None):
                print(f"Adding zero at {event.xdata}")
                self.zero_arr.append(event.xdata)
        self.refresh_figure()
        
    def load_num_den(self):
        try:
            num_arr = [float(x) for x in self.num_input.text().strip().replace('[','').replace(']','').split(',')]
            den_arr = [float(x) for x in self.den_input.text().strip().replace('[','').replace(']','').split(',')]
            self.ct_gain = ct.tf(num_arr,den_arr)
            self.refresh_figure()
        except ValueError:
            return