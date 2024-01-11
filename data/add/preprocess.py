import pandas as pd
import pickle as pk


# xls = pd.ExcelFile("【整合】流程助手-提示及校验模板-光伏.xlsx")
# # 遍历每个工作表
# for sheet_name in xls.sheet_names:
#     # 读取当前工作表的数据
#     df = pd.read_excel("【整合】流程助手-提示及校验模板-光伏.xlsx", sheet_name=sheet_name)[['问题', '答案']]


def preprocess_ziduan_info():
    """
    选中提示涉及到的数据
    :return:
    """
    res = {}
    yw_list = ["电梯充电桩", "低压分布式电源新装增容", "高压分布式电源新装增容"]
    for yw in yw_list:
        data = pd.read_excel("jiaoyan.xlsx", sheet_name=yw, index_col=None)
        temp_dict = dict(zip(data["ziduan"], data["content"]))
        # print(temp_dict)
        res[yw] = temp_dict
    # 存储字段信息
    with open("ziduan_info.pkl", "wb") as f:
        pk.dump(res, f)


# 字段选中提示
def preprocess_ziduan_data():
    """
      选中提示涉及到的数据,新增了好多专业业务数据
      :return:
    """
    res = {}
    sheets = pd.read_excel('jiaoyan_1114.xlsx', sheet_name=None)
    for sheet_name, df in sheets.items():
        # print("sheet name:", sheet_name)
        # print(df)
        if not df.empty:
            ziduan = df['字段名']
            content = df['应填写的内容']
            temp = dict(zip(ziduan, content))
            res[sheet_name] = temp
    with open("ziduan_info.pkl", "wb") as f:
        pk.dump(res, f)
    return res


# 字段提醒内容
def preprocess_tixing_data():
    """
      选中提示涉及到的数据,新增了好多专业业务数据
      :return:
    """
    res = {}
    sheets = pd.read_excel('jiaoyan_1114.xlsx', sheet_name=None)
    for sheet_name, df in sheets.items():
        # print("sheet name:", sheet_name)
        # print(df)
        if not df.empty:
            ziduan = df['字段名']
            content = df['提醒内容']
            temp = dict(zip(ziduan, content))
            res[sheet_name] = temp
    print(res)
    with open("ziduan_tixing.pkl", "wb") as f:
        pk.dump(res, f)
    return res


# 行业分类和用电类别关系
def preprocess_liandong_data():
    """
      行业分类、用电类别联动校验
      :return:
    """
    res = {}
    sheets = pd.read_excel('hangye_yongdian.xlsx', sheet_name=None)
    for sheet_name, df in sheets.items():
        # print("sheet name:", sheet_name)
        # print(df)
        if not df.empty:
            ziduan = df['营销行业分类名称']
            content = df['对应营销用电类别']
            res = dict(zip(ziduan, content))
    print(res)
    with open("hangye_yongdian.pkl", "wb") as f:
        pk.dump(res, f)
    return res


#
# res = preprocess_ziduan_data()
# for key, value in res.items():
#     print(key)
#     print(value)
# print("=====================================")
# res = preprocess_tixing_data()
# for key, value in res.items():
#     print(key)
#     print(value)
# print("=====================================")
res = preprocess_liandong_data()
for key, value in res.items():
    print(key, ":", value)
temp = res.values()
print(len(list(set(temp))))