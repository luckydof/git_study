from check_master import check_master
import pickle as pk
from ocr_underline import ScreenShotRec

with open("data/rule.pkl", 'rb') as f:
    rule = dict(pk.load(f))
with open("data/tixing.pkl", 'rb') as f:
    tixing = dict(pk.load(f))
# 文本识别工具
scr = ScreenShotRec()
ck_master = check_master(scr, rule, tixing)
image_path = "test2.png"
yewu = "居民充电桩新装"
res = ck_master.check(image_path, yewu)
print(res)

# 字段提示
# with open('../data/ziduan_infodd.pkl', "rb") as f:
#     data = pk.load(f)
# print(data)
# print(type(data))
# word = "证件类型"
# res = []
# for key, tmp_dict in data.items():
#     # temp = tmp_dict.keys()
#     t_res = [i for i in tmp_dict.keys() if word in i]
#     if t_res:
#         temp_res = {"name": key, "trans": [tmp_dict[t_res[0]]]}
#         res.append(temp_res)
# print(res)
