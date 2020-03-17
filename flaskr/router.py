#coding:utf-8
#api
from flask import Blueprint, request, jsonify
from extend import execjs
import requests
import json
import time

api = Blueprint('api',__name__)

@api.route('/translate', methods=['POST'])
def do():
    searchtext = request.form.get('text', '')
    if searchtext == '':
        return_body = {
            'code': 400,
            'msg' : '文本不能为空'
        }
        return jsonify(return_body)
    js = execjs.Py4Js()
    str_contents = searchtext.split('\n')
    translated_text = ''
    for paragraph in str_contents:
        paragraph_split = paragraph.split('.')
        statement_list = []
        for statement in paragraph_split:
            statement = statement.strip()
            if statement == '':
                statement_list.append('\n')
                continue
            res = translate(statement.strip(),js)
            statement_list.append(res)
            time.sleep(3)
        if len(statement_list) == 1:
            statement_list.append('\n')
        translated_text += ''.join(statement_list)
    return_body = {
        'code': 200,
        'msg': 'translated success',
        'content' : translated_text
    }
    return jsonify(return_body)


def buildUrl(text, tk):
    baseUrl = 'https://translate.google.cn/translate_a/single'
    baseUrl += '?client=webapp&'
    baseUrl += 'sl=auto&'
    baseUrl += 'tl=zh-CN&'
    baseUrl += 'hl=zh-CN&'
    baseUrl += 'dt=at&'
    baseUrl += 'dt=bd&'
    baseUrl += 'dt=ex&'
    baseUrl += 'dt=ld&'
    baseUrl += 'dt=md&'
    baseUrl += 'dt=qca&'
    baseUrl += 'dt=rw&'
    baseUrl += 'dt=rm&'
    baseUrl += 'dt=ss&'
    baseUrl += 'dt=t&'
    baseUrl += 'ie=UTF-8&'
    baseUrl += 'oe=UTF-8&'
    baseUrl += 'otf=1&'
    baseUrl += 'pc=1&'
    baseUrl += 'ssel=0&'
    baseUrl += 'tsel=0&'
    baseUrl += 'kc=2&'
    baseUrl += 'tk=' + str(tk) + '&'
    baseUrl += 'q=' + text
    return baseUrl


def translate(text, js=None):
    header = {
        'authority': 'translate.google.cn',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'x-client-data': 'CIi2yQEIo7bJAQjEtskBCKmdygEIt6rKAQjLrsoBCNCvygEIvLDKAQiGtcoBCJe1ygEI7bXKAQiOusoB'
    }
    url = buildUrl(text, js.getTk(text))
    res = ''
    try:
        r = requests.get(url)
        result = json.loads(r.text)
        if result[7] is not None:
            # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
            try:
                correctText = result[7][0].replace('<b><i>', ' ').replace('</i></b>', '')
                correctUrl = buildUrl(correctText, js.getTk(correctText))
                correctR = requests.get(correctUrl)
                newResult = json.loads(correctR.text)
                res = newResult[0][0][0]
            except Exception as e:
                # print(e)
                res = result[0][0][0]

        else:
            res = result[0][0][0]
    except Exception as e:
        res = ''
        print(url)
        print("翻译" + text + "失败")
        print("错误信息:")
        print(e)
    finally:
        return res