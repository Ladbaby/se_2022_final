dic = {"a": 1, "b": 2}

try:
    dic["c"]
except KeyError:
    print("fuck")
