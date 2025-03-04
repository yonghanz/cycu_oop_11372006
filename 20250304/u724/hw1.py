def product_of_odds_up_to_m(m):
    product = 1
    for number in range(1, m + 1, 2):
        product *= number
    return product

m = 11
print("從 1 到", m, "的奇數相積:", product_of_odds_up_to_m(m))

m = 21
print("從 1 到", m, "的奇數相積:", product_of_odds_up_to_m(m))

m = 51
print("從 1 到", m, "的奇數相積:", product_of_odds_up_to_m(m))

m = 101
print("從 1 到", m, "的奇數相積:", product_of_odds_up_to_m(m))