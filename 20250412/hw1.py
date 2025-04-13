import sympy as sp

# 定義符號
x, L, q, EI = sp.symbols('x L q EI')
c1, c2 = sp.symbols('c1 c2')

# 定義積分項（右手邊）
I1 = sp.integrate(sp.sin(sp.pi * x / L) * x**2, (x, 0, L))
I2 = sp.integrate(sp.sin(sp.pi * x / L) * x**3, (x, 0, L))

# M0 = q * L**2 / pi**4
pi = sp.pi
M0 = q * L**2 / pi**4

# 定義積分項（左手邊）
a11 = sp.integrate((2 * 2 * EI), (x, 0, L))
a12 = sp.integrate((2 * 6 * x * EI), (x, 0, L))
a21 = sp.integrate((2 * 6 * x * EI), (x, 0, L))
a22 = sp.integrate((6 * x * 6 * x * EI), (x, 0, L))

# 定義矩陣
matrix = sp.Matrix([
    [a11, a12],
    [a21, a22]
])

# 打印矩陣
print("積分矩陣為：")
sp.pprint(matrix)

# 定義右手邊的向量
rhs = sp.Matrix([
    q * I1 - 2 * L * M0,
    q * I2 - 3 * L**2 * M0
])

# 矩陣乘法
product_matrix = matrix * sp.Matrix([[c1], [c2]]) - rhs

print("矩陣乘法結果：")
sp.pprint(product_matrix)

# 解聯立方程式
solution = sp.solve(product_matrix, (c1, c2))

print("解為：")
sp.pprint(solution)

# 提取 c1 和 c2 的值
c1_value = solution[c1]
c2_value = solution[c2]

# 定義 w2(x)
w2= c1_value * x**2 + c2_value * x**3 

# 打印 w2(x)
print("w2(x) 為：")
sp.pprint(w2)