from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from ai_response import ai_response
import os
import json


app = Flask(__name__)
CORS(app)
config_file_path = 'C:/01-下载/word.json'


@app.route('/')
def index():
    # 数据文件校验，检查文件情况
    if os.path.exists(config_file_path):
        return render_template('home.html')
    else:
        return f"文件不存在或路径错误！"


@app.route('/config', methods=['GET', 'POST'])
def config():
    # 前端获取数据
    if request.method == "GET":
        with open(config_file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
        # 给前端的错题本配置界面返回 单词库内容 和 当前学习单词的序号
        return render_template('editor.html', content="\n".join(json_content["word_list"]), serial_num=json_content["serial_num"])

    # 当前端post进行文件保存操作时，对文件进行保存
    else:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
        data = request.get_json()
        json_content["serial_num"] = int(data.get("serial_num"))
        json_content["word_list"] = data.get("content").split("\n")
        with open(config_file_path, 'w', encoding='utf-8') as file:
            json.dump(json_content, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "保存成功"})


@app.route('/error_word', methods=['GET', 'POST'])
def error_word():
    if request.method == "GET":
        with open(config_file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
        # 给前端的错题本配置界面返回 单词库内容 和 当前学习单词的序号
        return render_template('error_word.html', content="\n".join(json_content["error_word_list"]))
    # 当前端post进行文件保存操作时，对文件进行保存
    else:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
        data = request.get_json()
        json_content["error_word_list"] = data.get("content").split("\n")
        with open(config_file_path, 'w', encoding='utf-8') as file:
            json.dump(json_content, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "保存成功"})


@app.route('/query_vocabulary', methods=['POST'])
def query_vocabulary():
    # 使用json文件，根据序号查询单词库文件
    with open(config_file_path, 'r', encoding='utf-8') as file:
        json_content = json.load(file)
    serial_num = json_content["serial_num"]
    word_list = json_content["word_list"]
    word = word_list[serial_num]
    # 更新单词学习序号，到json文件
    json_content["serial_num"] = serial_num + 1

    with open(config_file_path, "w", encoding="utf-8") as file:
        json.dump(json_content, file, ensure_ascii=False, indent=4)

    return jsonify({'response': word})


@app.route('/collect_word', methods=['POST'])
def collect_word():
    # 对错误的单词进行收藏，存入json文件的error_word_list键中
    with open(config_file_path, 'r', encoding='utf-8') as file:
        json_content = json.load(file)
    serial_num = json_content["serial_num"]
    word_list = json_content["word_list"]
    word = word_list[serial_num - 1]

    error_word_list = json_content.get("error_word_list", [])
    # 添加不重复的单词
    if word not in error_word_list:
        error_word_list.append(word)
    json_content["error_word_list"] = error_word_list  # 更新 JSON 中的列表

    with open(config_file_path, "w", encoding="utf-8") as file:
        json.dump(json_content, file, ensure_ascii=False, indent=4)

    return jsonify({'response': f"{word} 收藏成功"})


@app.route('/ai_translate', methods=['POST'])
def ai_translate():
    input_text = request.json.get('inputText', '')
    print(input_text)
    ai_translate_response = ai_response(
        '',
        url='http://43.134.8.116:9090/v1/chat/completions',
        model="glm-4-flash",
        system_prompt='翻译输入的单词，不要说别的没用的',
        user_input=input_text
    )
    ai_translate_result = ai_translate_response.json()['choices'][0]['message']['content']

    return jsonify({'response': ai_translate_result})


if __name__ == '__main__':
    app.run(debug=True, port=2324, host="0.0.0.0")
