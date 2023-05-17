from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 解决坐标轴中文显示问题
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号不显示的问题

class Figure_Canvas(FigureCanvas):
    """
    创建画板类
    """
    def __init__(self, width=3, height=5):
        self.fig = Figure(figsize=(width, height), dpi=100)
        super(Figure_Canvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)  # 111表示1行1列，第一张曲线图
        
    def add_line(self, x_data, y_data,x_min,x_max,y_min,y_max,xlog = False,ylog = False,style= '-'):
        self.line = Line2D(x_data, y_data)  # 绘制2D折线图
        self.ax.grid(True)  # 添加网格
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min,y_max)

        self.ax.add_line(self.line)
        self.line.set_linewidth(2)
        self.line.set_linestyle(style)
        self.line.set_color('r')
        if(xlog):
            self.ax.set_xscale('log')
        if(ylog):
            self.ax.set_yscale('log')

    def update_fig(self,**kwarg):
        if('x_data' in kwarg):
            self.line.set_xdata(kwarg['x_data'])
        if('y_data' in kwarg):
            self.line.set_ydata(kwarg['y_data'])
        if('x_min' in kwarg and 'x_max' in kwarg):
            self.ax.set_xlim([kwarg['x_min'],kwarg['x_max']])
        if('y_min' in kwarg and 'y_max' in kwarg):
            self.ax.set_ylim([kwarg['y_min'],kwarg['y_max']])
        self.draw()