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

    def add_line(self, x_data, y_data,xlog = False,ylog = False):
        pass
        # self.line = Line2D(x_data, y_data)  # 绘制2D折线图
        # self.ax.grid(True)  # 添加网格
        # self.ax.set_title('采样波形')  # 设置标题

        # # 设置xy轴最大最小值,找到x_data, y_data最大最小值
        # self.ax.set_xlim(min(x_data), max(x_data))
        # self.ax.set_ylim(min(y_data)*0.8,max(y_data)*1.2)  # y轴稍微多一点，会好看一点

        # self.ax.add_line(self.line)
        # self.line.set_linewidth(2)
        # self.line.set_color('r')
        # if(xlog):
        #     self.ax.set_xscale('log')
        # if(ylog):
        #     self.ax.set_yscale('log')