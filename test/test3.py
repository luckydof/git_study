"""
获取电价文件
"""
import os

file_list = [f for f in os.listdir("D:\static\dianjia") if f.endswith("pdf")]
print(file_list)
month = '202307'
year = month[:4] + "年"
mon = str(int(month[4:])) + '月'
temp = year + mon
file_name = [i for i in file_list if i.startswith(temp)][0]
print(file_name)

