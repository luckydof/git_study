import pandas as pd
import pickle as pk


# 悬浮提示
# data1 = pd.read_excel("content.xlsx", sheet_name="电梯充电桩", index_col=None)
# temp1 = dict(zip(data1.iloc[:, 0], data1.iloc[:, 1]))
# print(temp1)
# data2 = pd.read_excel("content.xlsx", sheet_name="光伏", index_col=None)


def preprocess_ziduan_info():
    """
    校验涉及到的数据
    :return:
    """
    res = {}
    yw_list = ["电梯充电桩", "光伏"]
    for yw in yw_list:
        data = pd.read_excel("content.xlsx", sheet_name=yw, index_col=None)
        temp_dict = dict(zip(data["ziduan"], data["content"]))
        # print(temp_dict)
        res[yw] = temp_dict
    # 存储字段信息
    with open("ziduan_infodd.pkl", "wb") as f:
        pk.dump(res, f)


def jiaoyan():
    """校验规则,校验内容字段
    """
    data = pd.read_excel("jiaoyan_rule.xlsx", sheet_name="居民充电桩")
    # print(data.head())
    rule_dict = {}
    tixing_dict = {}
    yewu_list = list(set(data['业务名称'].tolist()))
    print(yewu_list)
    """
    校验规则:
    1. 身份证号和手机号使用正则校验
    2. 其他字段暂时使用应填内容校验
    """
    for yewu in yewu_list:
        info_df = data[data['业务名称'] == yewu]
        # print(info_df)
        # 应填写内容
        content_dict = dict(zip(info_df['字段名'], info_df['应填内容']))
        # 提示内容
        warn_dict = dict(zip(info_df['字段名'], info_df['提醒内容']))
        rule_dict[yewu] = content_dict
        tixing_dict[yewu] = warn_dict
    with open("rule.pkl", "wb") as f:
        pk.dump(rule_dict, f)
    with open("tixing.pkl", "wb") as f:
        pk.dump(tixing_dict, f)


def hover():
    # pass
    """
    悬停:
    """
    data = pd.read_excel("./zhangdan_hover.xlsx")[""]
    print(data)


# jiaoyan()
# hover()
if __name__ == "__main__":
    with open("ziduan_infodd.pkl", 'rb') as f:
        data = pk.load(f)
        print(data)
        print(data["电梯充电桩"]["【用电户分类】"])
    # preprocess_ziduan_info()
