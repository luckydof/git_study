import pickle as pk
import re
from util.util import validate_id_card, validate_phone_number, edit_distance


# class check_master():
class check_master():
    def __init__(self, ocr, rule, tixing, hangye_yongdian):
        """
            校验器两个模块：
                1) 规则库
                2) 文本识别器
        """
        self.ocr = ocr
        self.rules = rule
        self.tixings = tixing
        self.hangye_yongdian = hangye_yongdian

    def get_content(self, img_path_list):
        for img_path in img_path_list:
            text = self.ocr.rec(img_path)

    def check(self, img_path, yw):
        """
        校验规则:
        一些业务需要具体处理，不能用通用规则校验
        1. 身份证号和手机号使用正则校验
        2. 其他字段暂时使用应填内容校验
        """
        text = self.ocr.rec(img_path)
        print(text)
        print("====================================")
        for i in text:
            print(i)
        print("====================================")

        # print(check_rules)
        # print(tixings)
        res = []
        # if yw == "居民充电桩":
        #     pass
        # if yw == "低压分布式电源新装增容":
        #     pass
        # if yw == "高压分布式电源新装增容":
        #     pass
        # if yw == "低压居民增容":
        #     pass
        # if yw == "低压非居民新装增容":
        #     pass
        # if yw == "居民更名":
        #     pass
        # if yw == "非居民更名":
        #     pass
        # if yw == "居民过户(线上受理）":
        #     pass
        # if yw == "非居民过户":
        #     pass
        # if yw == "改类":
        #     pass
        # if yw == "居民销户":
        #     pass
        # if yw == "非居民销户":
        #     pass
        # 所有需要校验的字段
        ziduan_list = list(self.rules[yw].keys())
        print(ziduan_list)
        # img_path = "test_image/test_121.png"
        text = self.ocr.rec(img_path)
        print(text)
        print("====================================")
        check_rules = self.rules[yw]
        tixings = self.tixings[yw]
        print("====================================")
        # 用户提交的截图中字段信息
        user_ziduan = []
        std_ziduan = []
        for i in text:
            # 编辑距离小于2,正常识别的,可能存在字段和内容为一个元素的情况
            min_s = edit_distance(i, ziduan_list)
            print(i)
            if min_s[1] < 2:
                user_ziduan.append(i)
                std_ziduan.append(min_s[0])
            temp_ziduan = [z for z in ziduan_list if i.startswith(z) and z not in user_ziduan]
            print("*********************")
            print(temp_ziduan)
            if temp_ziduan:
                user_ziduan.append(temp_ziduan[0])
                std_ziduan.append(temp_ziduan[0])
        print("====================================")
        print(user_ziduan)
        print(std_ziduan)
        res = []
        temp_dict = {}
        pipei_flag = False
        for i in range(len(user_ziduan)):
            u_ziduan = user_ziduan[i]
            s_ziduan = std_ziduan[i]
            temp = {"zidaun": "【" + s_ziduan + "】"}
            try:
                i_ziduan = text[text.index(u_ziduan) + 1]
            except Exception as e:
                i_ziduan = " "
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
                else:
                    pipei_flag = True
                    # print(i_ziduan)
                    # print(s_ziduan)
                    # temp_dict[s_ziduan] = i_ziduan
                    temp_dict[s_ziduan] = i_ziduan
        print(temp_dict)
        if yw == "居民充电桩":
            pass
        if yw == "低压分布式电源新装增容":
            if "投资模式" in temp_dict and "客户类型" in temp_dict:
                cus_type = temp_dict["客户类型"]
                mode = temp_dict["投资模式"]
                if cus_type == '同一法人':
                    flag = mode == "自投资"
                else:
                    flag = mode == "合同能源类型"
                if not flag:
                    temp_dict["投资模式"] = "客户类别为同一法人，则投资模式为自投资;客户类别为不同法人，则投资类别为合同能源管理或者其他。"
        if yw == "高压分布式电源新装增容":
            # dianliu = temp_dict.get("电流", "")
            # if dianliu == "0.015-0.075(6)A":
            #     # temp_dict.pop("电流")
            #     res = [i for i in text if "电流" not in i]
            z_dianliu = "0.015-0.075（6）A"
            y_dianliu = "0.015-0.075(6)A"
            temp_list = [i for i in text if z_dianliu in i or y_dianliu in text]
            if temp_list:
                pipei_flag = True
                print(res)
                res = [i for i in res if i["zidaun"] != "【电流】"]
                print(res)
                print("=--------=====")
        if yw == "低压居民增容":
            pass
        if yw == "低压非居民新装增容":
            pass
        if yw == "居民更名":
            pass
        if yw == "非居民更名":
            pass
        if yw == "居民过户(线上受理）":
            pass
        if yw == "非居民过户":
            pass
        if yw == "改类":
            pass
        if yw == "居民销户":
            pass
        if yw == "非居民销户":
            pass
        # 判断行业类别和用电类别的映射关系
        hangye = list(set(list(self.hangye_yongdian.keys())))
        yongdian = list(set(list(self.hangye_yongdian.values())))
        u_hangye = [i for i in hangye if i in text]
        u_yongdian = [i for i in yongdian if i in text]
        if u_hangye and u_yongdian:
            i_hangye = u_hangye[0]
            i_yongdian = u_yongdian[0]
            temp_dict['行业分类'] = i_hangye
            temp_dict['用电类别'] = i_yongdian
            print(i_hangye, i_yongdian)
        print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[")
        print(u_hangye)
        print(u_yongdian)

        if "行业分类" in temp_dict and "用电类别" in temp_dict:
            hangye = temp_dict['行业分类']
            yongdian_type = temp_dict['用电类别']
            s_type = self.hangye_yongdian[hangye]
            if s_type != yongdian_type:
                hangye_temp = {"zidaun": "【用电类别】", "info": f"{hangye}的用电类别应为{s_type}"}
                res.append(hangye_temp)
        print(pipei_flag)
        # if not pipei_flag:
        #     res = [{"zidaun": "校验失败", "info": ":未检测到字段信息"}]
        return res
