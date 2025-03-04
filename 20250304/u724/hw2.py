def sum_of_odds_up_to_m(m):
    total = 0
    for number in range(1, m + 1, 2):
        total += number
    return total

# 測試範例
m = 11
print("從 1 到", m, "的奇數總和:", sum_of_odds_up_to_m(m))

m = 21
print("從 1 到", m, "的奇數總和:", sum_of_odds_up_to_m(m))

m = 51
print("從 1 到", m, "的奇數總和:", sum_of_odds_up_to_m(m))

m = 101
print("從 1 到", m, "的奇數總和:", sum_of_odds_up_to_m(m))