import  sys
from ui import Ui_MainWindow
from PyQt5.QtWidgets import  *
from plot_figure import Figure_Canvas

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())