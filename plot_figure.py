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
        
    def insert_line(self,x_data,y_data):
        self.update_line(idx = len(self.get_children()),x_data= x_data,y_data=y_data)
        return len(self.get_children())-1
    
    def refresh_fig(self,**kwargs):
        # 全局的样式设置
        self.ax.grid(True)  # 添加网格
        if('y_min' in kwargs and 'y_max' in kwargs):
            self.ax.set_ylim([kwargs['y_min'],kwargs['y_max']])
        if('x_scale' in kwargs):
            self.ax.set_xscale(kwargs['x_scale'])
        if('y_scale' in kwargs):
            self.ax.set_xscale(kwargs['y_scale'])
        if('x_min' in kwargs and 'x_max' in kwargs):
            self.ax.set_xlim([kwargs['x_min'],kwargs['x_max']])
        if('title' in kwargs):
            self.ax.set_title(kwargs['title'])
        self.draw()

    def get_children(self):
        return self.ax._children
    
    def update_line(self,idx,x_data,y_data,linestyle = '-'):
        if(idx == len(self.get_children())):
            line = Line2D(x_data,y_data)
            line.set_linewidth(2)
            line.set_color('r')
            line.set_linestyle(linestyle)
            self.ax.add_line(line)
        else:
            self.ax._children[idx].set_xdata(x_data)
            self.ax._children[idx].set_ydata(y_data)
    