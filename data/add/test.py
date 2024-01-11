import pickle as pk

with open('../ziduan_info.pkl', "rb") as f:
    data = pk.load(f)
for key, value in data.items():
    print(key)
    print(value)
