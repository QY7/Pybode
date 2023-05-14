import control as ct
import matplotlib.pyplot as plt

s = ct.TransferFunction([1, 0], [1])
sys = (s**2-3*s+3) / (s**2 + 2*s + 1)

nyquist_data,contour = ct.nyquist_plot(sys,plot=True,return_contour=True)
resp = sys(contour)
[x,y] = [resp.real.copy(),resp.imag.copy()]
plt.figure()
plt.plot(x,y)
plt.plot(x,-y,'--')
plt.show()
print(resp)