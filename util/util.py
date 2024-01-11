import re
import Levenshtein
import pandas as pd
import os
import pickle as pk


def validate_phone_number(phone_number):
    pattern = r'^1[3456789]\d{9}$'
    return re.match(pattern, phone_number) is not None


def validate_id_card(id_card):
    pattern = r'^\d{17}[\dXx]$'
    return re.match(pattern, id_card) is not None


def edit_distance(query, str_list):
    cmp_res = {}
    for s in str_list:
        score = Levenshtein.distance(query, s)
        cmp_res[s] = score
    min_s = sorted(cmp_res.items(), key=lambda x: x[1])
    return min_s[0]


def hover_info(ocr_list, *info):
    file_list = ['2023年10月代理购电价格公示表（20230927）.pdf', '2023年1月代理购电测算公示表（20221228）.pdf',
                 '2023年2月代理购电测算公示表.pdf', '2023年3月代理购电测算公示表.pdf',
                 '2023年4月代理购电测算公示表.pdf', '2023年5月代理购电价格公示表.pdf',
                 '2023年6月代理购电公示表（20230526）.pdf', '2023年7月代理购电价格公示表（20230625）.pdf',
                 '2023年8月代理购电价格公示表（20230728）.pdf', '2023年9月代理购电价格公示表（20230828）.pdf',
                 '2023年11月代理购电价格公示表（20231027）.pdf']

    # file_list = ['2023年10月代理购电价格公示表（20230927）.xlsx', '2023年11月代理购电价格公示表（20231027）.xlsx',
    #              '2023年1月代理购电测算公示表（20221228）.xlsx', '2023年2月代理购电测算公示表.xlsx',
    #              '2023年3月代理购电测算公示表.xlsx', '2023年4月代理购电测算公示表.xlsx',
    #              '2023年5月代理购电价格公示表.xlsx', '2023年6月代理购电公示表（20230526）.xlsx',
    #              '2023年7月代理购电价格公示表（20230625）.xlsx', '2023年8月代理购电价格公示表（20230728）.xlsx',
    #              '2023年9月代理购电价格公示表（20230828）.xlsx']

    print(info)
    gl_yinshu = float(info[0])
    yougong = info[1]
    wugong = info[2]
    std = float(info[3])
    time = info[4]
    year = time[:4] + "年"
    mon = str(int(time[4:])) + '月'
    file_name = [i for i in file_list if i.startswith(year + mon)][0]
    ave_dianjia = info[5]
    print("---------***********************")
    print(ave_dianjia)
    print(std)
    print(type(std))
    res_dict = {"电价": rf"http://10.131.251.186:6004/dianjia/{file_name}",
                "本月份应付账款": "每路电源当月应付电费的总和",
                "减已结算之账款": "当月6、16、26日已收取的分次预收电费总和",
                "本月应付尾差或溢付": "本月份应付账款-已结算账款", "结算金额": "6日结算金额=本月应付尾差或溢付+分次预收金额； \
         16日结算金额 = 分次预收金额；\
         26日结算金额 = 分次预收金额。\
         注：分次预收金额 =（当月电费 * 系数） / 3",
                "《关于进一步规范本市非电网直供电价格的通知》": "若您存在向租户（终端用户）收取电费的行为，请遵守：终端用户用电价格 =“基准电价＋上浮幅度”本路电源的“基准电价”为“提取的平均电价值”“上浮幅度”由主体用户与终端用户自行商定，最大上浮幅度不得超过10％；涉及终端用户的合理线损等已经通过物业费、租金等其他途径解决的，电价不再上浮；存在多层主体用户供电情况的，各层终端用户用电价格上浮幅度合计不得超过10％。".replace(
                    "“提取的平均电价值”", ave_dianjia),
                "功率因数": f"功率因数=有功电量({yougong})/视在电量\n视在电量=有功电量√<span style='TEXT-DECORATION: overline'>有功电量({yougong})的平方+无功电量({wugong})的平方</span>"}

    # 0.9对应标准
    std_1 = "功率因数标准0.90，适用于160千伏安以上的高压供电工业用户（包括社队工业用户）、装有带负荷调整电压装置的高压供电电力用户和3200千伏安及以上的高压供电电力排灌站。"
    # 0.85对应标准
    std_2 = "功率因数标准0.85，适用于100千伏安（千瓦）及以上的其他工业用户（包括社队工业用户），100千伏安（千瓦）及以上的非工业用户和100千伏安（千瓦）及以上的电力排灌站。"
    # 0.8对应标准
    std_3 = "功率因数标准0.80，适用于100千伏安（千瓦）及以上的农业用户和趸售用户，但大工业用户未划由电业直接管理的趸售用户，功率因数标准应为0.85。"
    res_dict["标准"] = std_1 if std == 0.9 else std_2 if std == 0.85 else std_3
    res_dict["功率因数调整百分数"] = "功率因数超过标准，奖励。" if gl_yinshu > std else "功率因数刚达标，不奖不罚。" \
        if gl_yinshu == std else "功率因数未达标，罚款。"

    # 图片内容解析
    # img_path = "images/u7fuyc.png"
    month = int(time[4:])
    print(time, month)
    t_list = ocr_list[0] + ocr_list[1]
    if "尖峰" in t_list and "峰" in t_list:
        if month in [7, 8, 9]:
            f_info = "尖峰时段：12:00-14:00 \n\
                峰时段：8:00-12:00、14:00-15:00、18:00-21:00\n\
                平时段：6:00-8:00、15:00-18:00、21:00-22：00\n\
                谷时段：22:00-次日6:00"
        elif month in [1, 12]:
            f_info = "尖峰时段：19:00-21:00\n \
            峰时段：8:00-11:00、18:00-19:00\n\
            平时段：6:00-8:00、11:00-18:00、21:00-22：00\n\
            谷时段：22:00-次日6:00"
        else:
            f_info = "尖峰时段：归入峰时段\n\
            峰时段：8:00-11:00、18:00-21:00\n\
            平时段：6:00-8:00、11:00-18:00、21:00-22：00\n\
            谷时段：22:00-次日6:00"
    else:
        f_info = "峰时段：6:00-22:00\n\
        谷时段：22:00-次日6:00"

    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')  # 匹配汉字的正则表达式
    ocr_result = []
    print(ocr_list)
    for temp_list in ocr_list:
        result = []
        for item in temp_list:
            if chinese_pattern.match(item):  # 如果当前元素是汉字，则添加到结果列表
                result.append([item])
            else:  # 否则添加到结果列表的最后一个子列表中
                result[-1].append(item)
        ocr_result.append(result)
    print(ocr_result)
    h1 = "户总容量超315kVA的工商业用户，执行两部制电价。您是35kV及以下供电的两部制工商业客户，按最大需量计收基本电费。当您选择“实际最大需量”方式，基本电费=当月最大需量值*40.8元当您选择“合约最大需量”方式，基本电费=需量和定制（契约限额）*40.8元"
    h2 = "户总容量超315kVA的工商业用户，执行两部制电价。您是110kV及以上供电的两部制工商业客户，按最大需量计收基本电费。当您选择“实际最大需量”方式，基本电费=当月最大需量值*38.4元当您选择“合约最大需量”方式，基本电费=需量和定制（契约限额）*38.4元"
    h3 = "户总容量超315kVA的工商业用户，执行两部制电价。您是35kV及以下供电的两部制工商业客户，按容量计收基本电费。基本电费=容量*25.5元"
    h4 = "户总容量超315kVA的工商业用户，执行两部制电价。您是110kV及以上供电的两部制工商业客户，按容量计收基本电费。基本电费=容量*24元"
    h5 = "您是35kV及以下供电的两部制工商业客户，按“合约最大需量（契约限额）”计收基本电费。您本月使用的最大需量，超过了“合约最大需量（契约限额）”，超出部分价格翻倍收取。基本电费2=（当月最大需量-合约最大需量*1.05）*81.6元"
    h6 = "您是110kV及以上供电的两部制工商业客户，按“合约最大需量（契约限额）”计收基本电费。您本月使用的最大需量，超过了“合约最大需量（契约限额）”，超出部分价格翻倍收取。基本电费2=（当月最大需量-合约最大需量*1.05）*76.8元"
    for result in ocr_result:
        i = 0
        dianfei1 = ""
        dianfei2 = ""
        dianjia = ""
        xiaoji = ""
        lilv_adj = ""
        for res in result:
            if res[0] in ['尖峰', '峰', '平', '谷']:
                res_dict["imgC" + str(i)] = f_info
            if res[0] in ['基本电费', '基本电费1']:
                dianjia = res[2]
                info = h1 if dianjia == "40.800" else h2 if dianjia == "38.400" else h3 if dianjia == "25.500" else h4
                res_dict["imgD" + str(i)] = info
                dianfei1 = res[3]
            if res[0] == '基本电费2':
                dianjia = res[2]
                info = h5 if dianjia == "81.6" else h6
                res_dict["imgD" + str(i)] = info
                dianfei2 = res[3]
            if res[0] == '小计':
                xiaoji = res[1]
            if res[0] == '力率调整':
                lilv_adj = res[1]
                res_dict['平均电价'] = f"平均电价=电费/电量=（{xiaoji}+{lilv_adj}）/{yougong}"
            if res[0] == '九折优惠':
                # print(dianfei1)
                base_dianfei = float(dianfei1) if dianfei1 else 0
                base_dianfei2 = float(dianfei2) if dianfei2 else 0
                t_dianfei = base_dianfei + base_dianfei2
                info = f"您是按需量计收基本电费的两部制工商业用户。您本月户总有功电量/合同容量≧260，可享受基本电费9折优惠。9折优惠金额={t_dianfei}*（-10%）"
                res_dict["imgD" + str(i)] = info
            i += 1
    # print(dianjia)

    return res_dict


def hover(select_info):
    ziduan = select_info['label']
    value = select_info['value']
    data_path = '/'.join(os.path.abspath(__file__).split('\\')[:-2])
    print(data_path)
    with open(os.path.join(data_path, "data/hover_info.pkl"), 'rb') as f:
        info_dict = pk.load(f)
    data = pd.read_excel(os.path.join(data_path, "data/zhangdan_hover.xlsx"), index_col=0)
    info = ""
    if ziduan not in data["停留位置"].tolist():
        print(ziduan, "字段不在本次规则内")
    else:
        if ziduan in ["电价"
                      ",本月份应付账款",
                      "减已结算之账款",
                      "本月应付尾差或溢付",
                      "结算金额"]:
            info = data[data["停留位置"] == ziduan]["显示内容"].values[0]
        elif ziduan == "功率因数":
            yougong = info_dict["yougong"]
            wugong = info_dict["wugong"]
            info = "有功电量/视在电量"
        elif ziduan == "标准":
            # 0.9对应标准
            std_1 = "功率因数标准0.90，适用于160千伏安以上的高压供电工业用户（包括社队工业用户）、装有带负荷调整电压装置的高压供电电力用户和3200千伏安及以上的高压供电电力排灌站。"
            # 0.85对应标准
            std_2 = "功率因数标准0.85，适用于100千伏安（千瓦）及以上的其他工业用户（包括社队工业用户），100千伏安（千瓦）及以上的非工业用户和100千伏安（千瓦）及以上的电力排灌站。"
            # 0.8对应标准
            std_3 = "功率因数标准0.80，适用于100千伏安（千瓦）及以上的农业用户和趸售用户，但大工业用户未划由电业直接管理的趸售用户，功率因数标准应为0.85。"
            info = std_1 if value == '0.9' else std_2 if value == '0.85' else std_3
        elif ziduan == "功率因数调整百分数":
            gonglvyinshu = float(info_dict["gl_yinshu"])
            gonglvyinshu_std = float(info_dict["std"])
            info = "功率因数超过标准，奖励。" if gonglvyinshu > gonglvyinshu_std else "功率因数刚达标，不奖不罚。" \
                if gonglvyinshu == gonglvyinshu_std else "功率因数未达标，罚款。"
        elif ziduan == "电价":
            month = info_dict["month"]
            info = "提示" + month + "电价表,随后补充"
        elif ziduan == "《关于进一步规范本市非电网直供电价格的通知》":
            ave_dianjia = info_dict["ave_dianjia"]
            info = data[data["停留位置"] == ziduan]["显示内容"].values[0].replace("“提取的平均电价值”", ave_dianjia)
        return info


if __name__ == "__main__":
    std = "0.9"
    res = 2 if std == '0.9' else 1 if std == '0.85' else 3
    print(res)
    # phone_number = "15729575914"
    # id_number = "14232619950726141x"
    # res1 = validate_phone_number(phone_number)
    # res2 = validate_id_card(id_number)
    # print(res1, res2)
    # cmp_res = ['hello', "world", "tim", "dig", "dog"]
    # print(edit_distance("dog", cmp_res))
    # import os
    #
    # print(os.path.abspath(__file__))
    # current_dir = os.path.abspath(os.getcwd())
    # print(current_dir)
    # print(type(current_dir))
    # print("-------------")
    # print(current_dir.split('\\'))
    # print(current_dir.split('\\')[:-1])
    # print(os.path.abspath(__file__))
    # cur_dir = '/'.join(os.path.abspath(__file__).split('\\')[:-2])
    # print(cur_dir)
