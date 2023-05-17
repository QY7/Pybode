import control

# 定义传递函数
num = [1]  # 分子多项式的系数
den = [1, 2, 1]  # 分母多项式的系数
sys = control.TransferFunction(num, den)

# 获取零频率下的响应大小
response_at_zero = abs(control.evalfr(sys, 0))

print("零频率下的响应大小为:", response_at_zero)