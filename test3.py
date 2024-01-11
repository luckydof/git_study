# temp_dict = {"name": "tim"}
# print(temp_dict.get("nick_name", "ddd"))
# a = ""
# print(not a)
# print("name" in temp_dict)
# c = [1]
# d = [i for i in c if i != 1]
# print(d)
# print(not d)
import pickle as pk

with open("data/hangye_yongdian.pkl", 'rb') as file:
    data = pk.load(file)
print(data)
hangye = list(set(list(data.keys())))
yongdian = list(set(list(data.values())))

print(len(hangye))
print(len(yongdian))
