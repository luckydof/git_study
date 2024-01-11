# import pickle as pk
# with open('../data/hover_info.pkl', 'rb')as f:
#     data = pk.load(f)
# print(data)
std_1 = "std_1"
std_2 = "std_2"
std_3 = "std_3"
value = 0.9
info = std_1 if value == 0.9 else std_2 if value == 0.85 else std_3
print(info)
a = 2
if a == 1:
    print("ppp")
elif a == 2:
    print("pd")

a = "0.95"
b = "0.9"
c = "0.8"
print(b > c)
a = float(a)
print(a)
