from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from add_data import add_data
from ai_translate import baidu_translate
import pandas as pd
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('05.html')


@app.route('/config')
def config():
    file_path = 'C:/01-下载/11.csv'  # 替换为你的txt文件路径
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # 读取文件内容
    else:
        content = "文件不存在或路径错误！"
    return render_template('06.html', content=content, serial_num="22")


@app.route('/query_vocabulary', methods=['POST'])
def query_vocabulary():
    file_path = "C:/01-下载/word.xlsx"

    df = pd.read_excel(file_path)
    # 查找状态列中为空的数据
    empty_rows = df[df['状态'].isna()]
    # 获取最小的空行号
    min_row = empty_rows.index.min()
    row_data = df.loc[empty_rows.index.min()]
    word = row_data['单词']
    # 更新状态列的值为 1
    df.loc[min_row, '状态'] = 1
    df.to_excel(file_path, index=False)

    return jsonify({'response': word})


@app.route('/error_word', methods=['POST'])
def error_word():
    file_path = "C:/01-下载/word.xlsx"
    tenant_access_token = "t-g104c8ehNDCSO3SJO5KMAQAX6ZHLXNE6P5CUIB7P"
    app_token = "BLQFb58SKaEJSPsyoo9cfFcmn4d"
    table_id = "tblQbbTKnGL0asov"

    df = pd.read_excel(file_path)
    # 查找状态列中为空的数据
    empty_rows = df[df['状态'].isna()]
    # 获取最小的空行号的数据
    row_data = df.loc[empty_rows.index.min() - 1]
    word = row_data['单词']
    print(word)
    payload = {
        "fields": {
            "文本": f"{word}"
        }
    }
    response = add_data(tenant_access_token, app_token, table_id, payload)

    return jsonify({'response': response.status_code})


@app.route('/ai_translate', methods=['POST'])
def ai_translate():
    input_text = request.json.get('inputText', '')
    print(input_text)
    translate_response = baidu_translate("tp2cmCmEwvYEmbuifKBui1HL", "jhr5ZG0Y6KumAtq2Xo3VTWVANOvXgrS3", input_text)
    translate_result = translate_response.json()['result']['trans_result'][0]['dst']

    return jsonify({'response': translate_result})


if __name__ == '__main__':
    app.run(debug=True, port=2324)
