

a = [[1,2]]
b = [["x", "y"]]


combined = [list(pair[0] + pair[1]) for pair in zip(a, b)]
print(combined)

