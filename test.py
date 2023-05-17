import control as ct
import matplotlib.pyplot as plt

s = ct.TransferFunction([1], [1,2,11])

ct.nyquist_plot(s ,plot=True)
plt.xlim([-0.1,0.2])
plt.show()