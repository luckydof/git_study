# -*- coding:utf-8 -*-
# 导入包
import random
import requests
import jieba.analyse
import warnings
import json
import pandas as pd
import traceback
from flask import Flask, request
from flask_cors import *
from datetime import datetime
from configs.config import tool, graph

app = Flask(__name__)
app.config.from_object(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, supports_credentials=True)
warnings.filterwarnings("ignore")


@app.route('/download_num', methods=["GET", "POST"])
def download_num():
    try:
        tool.connect()
        request_data = request.get_json()
        file = request_data.get('file')
        req_files = [i['file_name'] for i in file]
        print(file)
        print(type(file))
        file_list = ["'" + i['file_name'] + "'" for i in file]
        file_param = '(' + ','.join(file_list) + ')'
        print(file_list)
        if not file:
            res = {"code": 401, "info": "参数解析异常"}
            return json.dumps(res, ensure_ascii=False)
        select_sql = f"SELECT file_name,count(*) as count FROM yuntu_files,file_download_history" \
                     f" where file_download_history.file_id = yuntu_files.file_id  and file_name in {file_param}" \
                     f" group by file_name"
        # select_sql = f"SELECT count(*) as count FROM yuntu_files,file_download_history" \
        #              f" where file_download_history.file_id = yuntu_files.file_id  and file_name = '{file_name}'"
        print(select_sql)
        info = tool.select_data(select_sql)
        info_dict = dict(zip([i[0] for i in info], [i[1] for i in info]))
        print(info_dict)
        res = []
        for file_name in req_files:
            # temp_dict = {file_name: info_dict.get(file_name, 0)}
            # res.append(temp_dict)
            temp_num = info_dict.get(file_name, 0)
            res.append(temp_num)
        print(res)
        res = {"code": 200, "download_num": res}
    except Exception as e:
        print(traceback.print_exc())
        res = {"code": 400, "msg": f"接口服务异常:{e}"}
    return json.dumps(res, ensure_ascii=False)


# 数据分析模块
@app.route('/analy', methods=["GET", "POST"])
def file_info():
    try:
        tool.connect()
        request_data = request.get_json()
        file_name = request_data.get('file_name')
        flag = "download"
        if not file_name:
            res = {"code": 200, "info": "参数解析异常"}
            return json.dumps(res, ensure_ascii=False)
        if flag == "view":
            select_sql = f"SELECT file_name,sys_user.user_name,browse_timestamp as timestamp  FROM sys_user, yuntu_files, " \
                         f"file_browse_history WHERE " \
                         f"file_browse_history.user_id = sys_user.user_id AND file_name = '{file_name}'"
        else:
            # select_sql = f"SELECT file_name,sys_user.nick_name,download_timestamp as timestamp FROM sys_user, yuntu_files, " \
            #              f"file_download_history WHERE " \
            #              f"file_download_history.user_id = sys_user.user_id AND file_name = '{file_name}'"
            # select_sql = f"SELECT file_name,nick_name,download_timestamp as timestamp  FROM  yuntu_files, " \
            #              f"file_download_history, sys_user WHERE file_download_history.user_id = sys_user.user_id AND " \
            #              f"file_download_history.file_id = yuntu_files.file_id and file_name = '{file_name}' "
            select_sql = f"SELECT nick_name,count(*) as count FROM  yuntu_files, " \
                         f"file_download_history, sys_user WHERE file_download_history.user_id = sys_user.user_id AND " \
                         f"file_download_history.file_id = yuntu_files.file_id and file_name = '{file_name}'" \
                         f"group by nick_name "

        print(select_sql)
        info = pd.read_sql(select_sql, tool.conn)
        print(info)
        info = info.sort_values('count', ascending=False)
        res_info = []
        user_info = info['nick_name'].tolist()
        count_info = info['count'].tolist()
        for i in range(len(info)):
            temp = {"user_name": user_info[i], "count": str(count_info[i])}
            res_info.append(temp)
        res = {"code": 200, "info": res_info}
        print(res)
    except Exception as e:
        print(traceback.print_exc())
        res = {"code": 400, "msg": f"接口服务异常:{e}"}
    return json.dumps(res, ensure_ascii=False)


@app.route('/caozuo', methods=["GET", "POST"])
def caozuo_info():
    try:
        tool.connect()
        request_data = request.get_json()
        print(request_data)
        file_name = request_data.get('file_name')
        flag = request_data.get('flag')
        user_name = request_data.get('user_name')
        if not file_name or not flag or not user_name:
            res = {"code": 200, "info": "参数解析异常"}
            return json.dumps(res, ensure_ascii=False)
        file_select_sql = f"select file_id from yuntu_files where file_name = '{file_name}'"
        user_select_sql = f"select user_id from sys_user where user_name = '{user_name}'"
        temp_file_id = tool.select_data(file_select_sql)
        if temp_file_id:
            file_id = temp_file_id[0][0]
        else:
            res = {"code": 401, "info": "未找到该文件"}
            return json.dumps(res, ensure_ascii=False)
        tool.connect()
        temp_user_id = tool.select_data(user_select_sql)
        if temp_user_id:
            user_id = temp_user_id[0][0]
        else:
            res = {"code": 401, "info": "未找到该用户"}
            return json.dumps(res, ensure_ascii=False)
        now_time = datetime.now()
        timestamp = now_time.strftime('%Y-%m-%d %H:%M:%S')
        if flag == 'view':
            insert_sql = f"insert into file_browse_history(file_id,user_id,browse_timestamp)values({file_id},{user_id},'{timestamp}')"
        else:
            insert_sql = f"insert into file_download_history(file_id,user_id,download_timestamp)values({file_id},{user_id},'{timestamp}')"
        print(insert_sql)
        tool.connect()
        tool.insert_data(insert_sql)
        info = "数据库修改成功"
        res = {"code": 200, "info": info}
    except Exception as e:
        print(traceback.print_exc())
        res = {"code": 400, "msg": f"接口服务异常:{e}"}
    return json.dumps(res, ensure_ascii=False)


@app.route('/huaxiang', methods=["GET", "POST"])
# 用户画像接口
def huaxiang():
    try:
        tool.connect()
        request_data = request.get_json()
        # file_name = request_data.get('file_name')
        # flag = request_data.get('flag')
        user_name = request_data.get('user_name')
        if not user_name:
            res = {"code": 200, "info": "参数解析异常"}
            return json.dumps(res, ensure_ascii=False)
        print(user_name)
        # 查看用户浏览历史数据
        select_b_sql = f"select user_name, file_name from sys_user,yuntu_files,file_browse_history where " \
                       f"sys_user.user_id = file_browse_history.user_id and file_browse_history.file_id = " \
                       f"yuntu_files.file_id and user_name = '{user_name}' "
        print(select_b_sql)
        temp = tool.select_data(select_b_sql)
        print(temp)
        b_list = [i[1] for i in tool.select_data(select_b_sql)]
        # 查看用户下载历史数据
        select_d_sql = f"select user_name, file_name from sys_user,yuntu_files,file_download_history where " \
                       f"sys_user.user_id = file_download_history.user_id and file_download_history.file_id = " \
                       f"yuntu_files.file_id and user_name = '{user_name}'"
        d_list = [i[1] for i in tool.select_data(select_d_sql)]
        select_l_sql = f"select area from sys_user where  user_name = '{user_name}'"
        u_file_list = b_list + d_list

        r_label = tool.select_data(select_l_sql)
        if len(r_label) == 0:
            u_label_list = []
        else:
            tmp_l_list = r_label[0][0].split(',')
            print(tmp_l_list)
            s_num = 2 if len(tmp_l_list) >= 2 else len(tmp_l_list)
            u_label_list = random.sample(tmp_l_list, s_num)
            print(u_label_list)
        # def extract_keywords(text_list, topK=5):
        # 将列表中的所有字符串合并为一个长字符串
        # 使用jieba分词进行分词，并提取关键词
        keywords = []
        for f in u_file_list:
            keywords.extend(jieba.analyse.extract_tags(f, topK=1, withWeight=False))
        keywords = list(set(keywords))
        keywords = keywords if len(keywords) < 5 else random.sample(keywords, 5)
        u_huaxiang_list = u_label_list + list(set(keywords))
        res = {"code": 200, "info": u_huaxiang_list}
    except Exception as e:
        print(traceback.print_exc())
        res = {"code": 400, "msg": f"接口服务异常:{e}"}
    return json.dumps(res, ensure_ascii=False)


@app.route('/rec_kg', methods=["GET", "POST"])
# 推送可能感兴趣的知识
def rec_kg():
    try:
        tool.connect()
        request_data = request.get_json()
        user_name = request_data.get('user_name')
        if not user_name:
            res = {"code": 200, "info": "参数解析异常"}
            return json.dumps(res, ensure_ascii=False)
        data = {
            'user_name': user_name,
        }  # 根据API的要求，构造请求的参数

        # 发送POST请求
        headers = {'Content-Type': 'application/json'}
        response = requests.post("https://taction.com.cn:6013/huaxiang", data=json.dumps(data), headers=headers)
        u_label = json.loads(response.text)["info"]
        print(u_label)
        print(type(u_label))
        # 根据用户标签推荐课程数据

        labels = ["生产", "基建", "调度", "营销", "变电检修", "运检", "供电", "管理"]

        biaoqian = [i for i in u_label if i in labels]
        keywords = [i for i in u_label if i not in labels]
        cql = """
           MATCH (p)-[:成果专业]->(m:`成果专业（生产/基建/营销/调度/其他）`)
           WHERE (p:`管理创新成果名称` OR p:`质量管理（QC）小组成果名称`) AND (m.名称 = "{}" OR m.名称 = "{}")
           RETURN p.名称 limit 5
         """.format(biaoqian[0], biaoqian[1])
        f_sql = "SELECT file_name FROM yuntu_files WHERE "
        for i in range(len(keywords)):
            if i == len(keywords) - 1:
                f_sql += "file_name LIKE '%{}%'".format(keywords[i])
            else:
                f_sql += "file_name LIKE '%{}%' OR ".format(keywords[i])
        # # if len(keywords) == 0: #     pass f_sql = """ SELECT file_name FROM yuntu_files WHERE file_name LIKE '%{
        # }%' OR file_name LIKE '%{}%' OR file_name LIKE '%{}%'; """.format(keywords[0], keywords[1], keywords[2])

        cql_res = graph.run(cql).data()
        print(cql_res)
        c_file = [i['p.名称'] for i in cql_res]
        print(f_sql)
        sql_res = tool.select_data(f_sql)
        s_file = [i[0] for i in sql_res]
        print(s_file)
        rec_file_list = c_file + s_file
        res = {"code": 200, "file": rec_file_list[:12]}
        tool.disconnect()
    except Exception as e:
        print(traceback.print_exc())
        res = {"code": 400, "msg": f"接口服务异常:{e}"}
    return json.dumps(res, ensure_ascii=False)


@app.route('/get_labels', methods=["GET", "POST"])
# 用户注册时的选择标签接口
def get_label():
    try:
        # l_cql = 'match (n:`成果专业（生产/基建/营销/调度/其他）`) return n.名称 limit 10'
        # t_res = graph.run(l_cql).data()
        # print(t_res)
        # labels = [i['n.名称'] for i in t_res]
        labels = ["生产,基建,调度,营销,变电检修,运检,供电,管理"]
        info = ",".join(labels)
        res = {"code": 200, "info": info}
    except Exception as e:
        print(traceback.print_exc())
        res = {"code": 400, "msg": f"接口服务异常:{e}"}
    return json.dumps(res, ensure_ascii=False)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, port=6004)
    # app.run(host='0.0.0.0', debug=True, port=6013)
    app.run(host='0.0.0.0', debug=True, port=6013,
            ssl_context=('../key_data/www.taction.com.cn.pem', '../key_data/www.taction.com.cn.key'))
