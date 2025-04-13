import sympy as sp

# 定義符號
x, L, q, EI = sp.symbols('x L q EI')
c1 = sp.symbols('c1 ')

# 定義積分項（右手邊）
I1 = sp.integrate(sp.sin(sp.pi * x / L) * x**2, (x, 0, L))


# M0 = q * L**2 / pi**4
pi = sp.pi
M0 = q * L**2 / pi**4

# 定義積分項（左手邊）
a11 = sp.integrate((2 * 2 * EI), (x, 0, L))


# 定義矩陣
matrix = sp.Matrix([
    [a11]
])

# 打印矩陣
print("積分矩陣為：")
sp.pprint(matrix)

# 定義右手邊的向量
rhs = sp.Matrix([
    q * I1 - 2 * L * M0,
    
])

# 矩陣乘法
product_matrix = matrix * sp.Matrix([[c1]]) - rhs

print("矩陣乘法結果：")
sp.pprint(product_matrix)

# 解聯立方程式
solution = sp.solve(product_matrix, (c1))

print("解為：")
sp.pprint(solution)

# 提取 c1  的值
c1_value = solution[c1]

# 定義 w2(x)
w1= c1_value * x**2  

# 打印 w1(x)
print("w1(x) 為：")
sp.pprint(w1)