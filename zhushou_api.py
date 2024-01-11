# -*- coding:utf-8 -*-
# 导入包
import os.path
from text_ocr import TextOCR
import pandas as pd
from flask import Flask, request
import json
from flask_cors import *
import pickle as pk
from util.util import hover, hover_info
import traceback

app = Flask(__name__)
app.config.from_object(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, supports_credentials=True)


# 只接受POST方法访问
# 搜索接口   展示图谱
@app.route("/liucheng_zhushou", methods=["GET", "POST"])
def faq_qa():
    # # data = pd.read_csv("./data/ziduan_info.csv", index_col=0)
    # with open('./data/ziduan_infodd.pkl', "rb")as f:
    #     data = pd.load(f)s
    # ziduan = request.args.get("ziduan")
    # print(ziduan)
    # temp = list(data[data['ziduan'].str.contains(ziduan)]['content'])
    # if len(temp) == 0:
    #     temp = ["知识库中未找到该字段相应说明"]
    # print(temp)
    #
    # res_dict = {}
    # res_dict["name"] = ziduan
    # res_dict["trans"] = temp
    #
    # res = [res_dict]
    # return json.dumps(res, enddsure_ascii=False)
    with open('data/ziduan_info.pkl', "rb") as f:
        data = pk.load(f)
    print(data)
    # print(data)
    # print(type(data))
    # word = "证件类型"
    ziduan = request.args.get("ziduan")
    print(ziduan)
    res = []
    for key, tmp_dict in data.items():
        # temp = tmp_dict.keys()
        # print(tmp_dict.keys())
        t_res = [i for i in tmp_dict.keys() if ziduan == i]
        if t_res:
            temp_res = {"name": key, "trans": [str(tmp_dict[t_res[0]])]}
            res.append(temp_res)
    print(res)
    if not res:
        res.append(
            {
                "name": "no_find",
                "trans": ["未找到字段"]
            }
        )

    return json.dumps(res, ensure_ascii=False)


@app.route("/up_info", methods=["GET", "POST"])
def up_data():
    # 页面全部信息
    info_dict = request.get_json()
    print(info_dict)
    with open("./data/hover_info.pkl", 'wb') as f:
        pk.dump(info_dict, f)
    return json.dumps("页面信息接收成功", ensure_ascii=False)


@app.route('/up_imginfo', methods=["GET", "POST"])
def image_feed():
    # 接收图片
    # print(request)
    try:
        if 'file' not in request.files:
            return 'No file received', 400
        # print(request.files)
        files = request.files.getlist("file")
        gl_yinshu = request.form.get("gl_yinshu")
        yougong = request.form.get("yougong")
        wugong = request.form.get("wugong")
        std = request.form.get("std")
        month = request.form.get("month")
        ave_dianjia = request.form.get("ave_dianjia")
        print(gl_yinshu, yougong, wugong, std, month, ave_dianjia)
        print("===================")
        text = []
        for file in files:
            if file.filename == '':
                return 'No file selected', 400
            # 保存图片文件到本地
            file.save('images/' + file.filename)
            res = "接收成功"
            # 开始图片解析
            c_list = text_ocr.rec('images/' + file.filename)
            print(c_list)
            if '9折优惠' in c_list:
                print(c_list)
                index = c_list.index("9折优惠")
                c_list[index] = c_list[index].replace('9折优惠', '九折优惠')
            text.append(c_list)
        res_dict = hover_info(text, gl_yinshu, yougong, wugong, std, month, ave_dianjia)
        return json.dumps(res_dict, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return json.dumps(str(e), ensure_ascii=False)


@app.route("/get_info", methods=["GET", "POST"])
def get_data():
    if not os.path.exists("./data/hover_info.pkl"):
        return json.dumps("未接收到完整页面信息,请先解析页面字段", ensure_ascii=False)
    req_info = request.get_json()
    ziduan_info = hover(req_info)
    return json.dumps(ziduan_info, ensure_ascii=False)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, port=6004)
    text_ocr = TextOCR()
    app.run(host='0.0.0.0', debug=True, port=6025)
