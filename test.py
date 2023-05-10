import control as ct
import matplotlib.pyplot as plt

s = ct.TransferFunction([1, 0], [1])
sys = 1 / (s**2 + 2*s + 1)

nyquist_data = ct.nyquist_plot(sys)
ax = plt.gca()
l1 = list(ax.get_lines())[0]
l2 = list(ax.get_lines())[3]
plt.figure()
plt.plot(l1.get_data()[0],l1.get_data()[1])
plt.plot(l2.get_data()[0],l2.get_data()[1])
plt.show()