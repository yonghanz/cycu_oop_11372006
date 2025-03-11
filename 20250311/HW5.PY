


def is_palindrome(word):
    return word == word[::-1]

def reverse_word(word):
    return ''.join(reversed(word))

word_list = ['parrot', 'racecar', 'level', 'python', 'madam', 'rotator', 'deified']

for word in word_list:
    if len(word) >= 7 and is_palindrome(word):
        print(word)