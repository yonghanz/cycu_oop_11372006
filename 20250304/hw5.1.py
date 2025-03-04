def gcd(a, b) ->int :
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

# 測試範例
x = 56
y = 98
print(f"GCD of{x} and {y} is: {gcd(x, y)}")

x=7
y=49
print(f"GCD of{x} and {y} is: {gcd(x, y)}")