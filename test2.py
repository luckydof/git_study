import pickle as pk
from text_ocr import TextOCR
from util.util import validate_id_card, validate_phone_number, edit_distance

# 字段提示
with open('data/ziduan_info.pkl', "rb") as f:
    data = pk.load(f)
print(data)

with open("data/ziduan_tixing.pkl", 'rb') as f:
    tixing = dict(pk.load(f))
print(tixing)
print("=====================")
print(tixing['低压非居民新装增容'])

# for key, value in data.items():
#     print(key)
#     print(value)
# print(list(data.keys()))

if __name__ == "__main__":
    yw = "高压分布式电源新装增容"
    # 所有需要校验的字段
    ziduan_list = list(data[yw].keys())
    print(ziduan_list)
    ocr = TextOCR()
    img_path = "test_image/test_121.png"
    text = ocr.rec(img_path)
    print(text)
    print("====================================")
    check_rules = data[yw]
    tixings = tixing[yw]
    print("====================================")
    # 用户提交的截图中字段信息
    user_ziduan = []
    std_ziduan = []
    for i in text:
        min_s = edit_distance(i, ziduan_list)
        print(i)
        if min_s[1] < 2:
            user_ziduan.append(i)
            std_ziduan.append(min_s[0])
    print("====================================")
    print(user_ziduan)
    print(std_ziduan)
    res = []
    temp_dict = {}
    for i in range(len(user_ziduan)):
        u_ziduan = user_ziduan[i]
        s_ziduan = std_ziduan[i]
        temp = {"zidaun": "【" + s_ziduan + "】"}
        i_ziduan = text[text.index(u_ziduan) + 1]
        if s_ziduan == "身份证号":
            id_res = validate_id_card(i_ziduan)
            if not id_res:
                # res.append(str(i) + "." + "身份证号格式有误")
                temp["info"] = "格式有误"
                res.append(temp)
        elif s_ziduan == "联系号码":
            phone_res = validate_phone_number(i_ziduan)
            if not phone_res:
                # res.append(str(i) + "." + "手机号格式有误")
                temp["info"] = "格式有误"
        else:
            temp_res = i_ziduan == str(check_rules[s_ziduan]) or i_ziduan in str(check_rules[s_ziduan]) or \
                       check_rules[s_ziduan] in text
            if not temp_res:
                temp["info"] = "字段内容可能存在问题," + str(tixings[s_ziduan])
                res.append(temp)
    print("校验结果===========================================")
    for r in res:
        print(r)
# if __name__ == "__main__":
#     with open("data/rule.pkl", 'rb') as f:
#         rule = dict(pk.load(f))
#     with open("data/tixing.pkl", 'rb') as f:
#         tixing = dict(pk.load(f))
#     print(rule)
#     print(tixing)
