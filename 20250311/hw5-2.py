# 反轉字串並轉換為列表
reversed_list = list(reversed('parrot'))
print(reversed_list)  # 輸出: ['t', 'o', 'r', 'r', 'a', 'p']

# 反轉字串並轉換為字串
reversed_string = ''.join(reversed('parrot'))
print(reversed_string)  # 輸出: 'torrap'

# 直接反轉字串並轉換為字串
print(''.join(reversed('parrot')))  # 輸出: 'torrap'

def is_palindrome(word):
    return word == word[::-1]

def reverse_word(word):
    return ''.join(reversed(word))

word_list = ['parrot', 'racecar', 'level', 'python', 'madam', 'rotator', 'deified']

for word in word_list:
    if len(word) >= 7 and is_palindrome(word):
        print(word)