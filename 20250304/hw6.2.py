def absolute_value_extra_return(x):
    if x < 0:
        return -x
    else:
        return x
    
    return 'This is dead code.'


def is_divisible(x, y):
    if x % y == 0:
        return True
    else:
        return False
    
def is_divisible(x, y):
    return x % y == 0

# 測試範例
print(is_divisible(10, 2))  # 輸出: True
print(is_divisible(10, 3))  # 輸出: False
     