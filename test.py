import control

# 定义传递函数
num = [1]  # 分子多项式的系数
den = [1, 3, 2]  # 分母多项式的系数
sys = control.TransferFunction(num, den)

# 获取系统的零点和极点
zeros = control.zero(sys)
poles = control.pole(sys)

# 打印系统的零点和极点
print("系统的零点：", zeros)
print("系统的极点：", poles)

# 计算系统在零点和极点处的增益大小
for zero in zeros:
    gain_zero = control.evalfr(sys,zero)
    print("零点", zero, "处的增益大小：", gain_zero)

for pole in poles:
    gain_pole = control.evalfr(sys,pole)
    print("极点", pole, "处的增益大小：", gain_pole)