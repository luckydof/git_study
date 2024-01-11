import pickle as pk
import re
from util.util import validate_id_card, validate_phone_number, edit_distance


# class check_master():
class check_master():
    def __init__(self, ocr, rule, tixing):
        """
            校验器两个模块：
                1) 规则库
                2) 文本识别器
        """
        self.ocr = ocr
        self.rules = rule
        self.tixings = tixing

    def get_content(self, img_path_list):
        for img_path in img_path_list:
            text = self.ocr.rec(img_path)

    def check(self, img_path, yewu):
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
        check_rules = self.rules[yewu]
        tixings = self.tixings[yewu]
        # print(check_rules)
        # print(tixings)
        res = []
        # if yewu == "居民充电桩":
        #     pass
        # if yewu == "低压分布式电源新装增容":
        #     pass
        # if yewu == "高压分布式电源新装增容":
        #     pass
        # if yewu == "低压居民增容":
        #     pass
        # if yewu == "低压非居民新装增容":
        #     pass
        # if yewu == "居民更名":
        #     pass
        # if yewu == "非居民更名":
        #     pass
        # if yewu == "居民过户(线上受理）":
        #     pass
        # if yewu == "非居民过户":
        #     pass
        # if yewu == "改类":
        #     pass
        # if yewu == "居民销户":
        #     pass
        # if yewu == "非居民销户":
        #     pass
        for ziduan, content in check_rules.items():
            min_s = edit_distance(ziduan, text)
            if min_s[1] <= 1:
                flag = True
                temp = {"zidaun": "【" + ziduan + "】"}
                m_ziduan = min_s[0]
                # if ziduan in text:
                # 获取用户填写的字段内容
                i_ziduan = text[text.index(m_ziduan) + 1]
                if ziduan == "身份证号":
                    id_res = validate_id_card(i_ziduan)
                    if not id_res:
                        # res.append(str(i) + "." + "身份证号格式有误")
                        temp["info"] = "格式有误"
                        res.append(temp)
                elif ziduan == "联系号码":
                    phone_res = validate_phone_number(i_ziduan)
                    if not phone_res:
                        # res.append(str(i) + "." + "手机号格式有误")
                        temp["info"] = "格式有误"
                else:
                    temp_res = i_ziduan == str(check_rules[ziduan]) or i_ziduan in str(check_rules[ziduan]) or \
                               check_rules[ziduan] in text
                    if not temp_res:
                        temp["info"] = "字段内容可能存在问题," + str(tixings[ziduan])
                        res.append(temp)
                        # res.append(
                        #     str(i) + "." + ziduan + "字段内容可能存在问题,应为" + str(check_rules[ziduan]))
                        # print(ziduan)
            else:
                # res.append(str(i) + "." + "未检测到" + ziduan + "内容")
                pass
            # i += 1
        # res.insert(0, flag2 if not res else flag1)
        # return "\n".join(res)
        if not res and not flag:
            # print("校验res为[]")
            # print("结果为空,未检测到字段内容")
            res.append({"zidaun": "【未检测到】", "info": "字段信息"})
        # print("=====================")
        # print(res)
        # print("=====================")
        return res
