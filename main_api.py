import json
from check_master import check_master
import pickle as pk
from ocr_underline import ScreenShotRec
from flask import Flask, Response, request, send_file
from flask_cors import CORS
import pandas as pd
import traceback

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
CORS(app)


@app.route('/get_yw', methods=["GET", "POST"])
def get_yw_list():
    with open('data/ziduan_info.pkl', "rb") as f:
        data = pk.load(f)
    print(data)
    yw_list = list(data.keys())
    return json.dumps(yw_list, ensure_ascii=False)


@app.route('/upload', methods=["GET", "POST"])
def image_feed():
    # 接收图片
    # print(request)
    try:
        if 'file' not in request.files:
            return 'No file received', 400
        file = request.files['file']
        print(file)
        if file.filename == '':
            return 'No file selected', 400
        # 保存图片文件到本地
        file.save('images/' + file.filename)
        image_path = 'images/' + file.filename
        yewu = request.form.get("ziduan")
        print(yewu)
        res = ck_master.check(image_path, yewu)
        print(res)
        return json.dumps(res, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return json.dumps(str(e), ensure_ascii=False)


@app.route('/up_info', methods=["GET", "POST"])
def up_feed():
    # 接收图片
    # print(request)
    try:
        if 'file' not in request.files:
            return 'No file received', 400
        file = request.files['file']
        print(file)
        if file.filename == '':
            return 'No file selected', 400
        # 保存图片文件到本地
        file.save('images/' + file.filename)
        image_path = 'images/' + file.filename
        yewu = request.form.get("ziduan")
        print(yewu)
        res = ck_master.check(image_path, yewu)
        # print(res)
        return json.dumps(res, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return json.dumps(str(e), ensure_ascii=False)


if __name__ == "__main__":
    with open("data/ziduan_info.pkl", 'rb') as f:
        rule = dict(pk.load(f))
    with open("data/ziduan_tixing.pkl", 'rb') as f:
        tixing = dict(pk.load(f))
    with open("data/hangye_yongdian.pkl", 'rb') as f:
        hangye_yongdian = dict(pk.load(f))
    # with open("data/rule.pkl", 'rb') as f:
    #     rule = dict(pk.load(f))
    # with open("data/tixing.pkl", 'rb') as f:
    #     tixing = dict(pk.load(f))
    # 文本识别工具
    scr = ScreenShotRec()
    ck_master = check_master(scr, rule, tixing, hangye_yongdian)
    app.run(host='0.0.0.0', debug=True, port=6018)
