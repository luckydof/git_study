import pickle as pk

with open("ziduan_info.pkl", 'rb')as f:
    data = pk.load(f)
for i in data.keys:
    print(i)