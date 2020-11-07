from flask import Flask
from flask import render_template, redirect, request, url_for, jsonify
import requests
from requests_oauthlib import OAuth1Session

import os
import sys
import json
import re

from database import insert_user, update_user, is_exist, delete_user, update_query, fetch_all_users
from tweets import parser

CK = os.environ.get('CK')
CS = os.environ.get('CS')

app = Flask(__name__)
user = None

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    global user
    user = OAuth1Session(CK, CS)
    params = {
        'oauth_callback': 'http://127.0.0.1:5000/oauth'
    }
    res = user.post('https://api.twitter.com/oauth/request_token', params)
    params = parser(res.text)

    user = OAuth1Session(CK, CS, params['oauth_token'], params['oauth_token_secret'])
    redirect_url = 'https://api.twitter.com/oauth/authorize?oauth_token={}'.format(params['oauth_token'])

    return redirect(redirect_url)

@app.route('/oauth')
def oauth():
    global user
    url = request.url
    text = re.sub('.*\?', '', url)
    params = parser(text)
    user = OAuth1Session(CK, CS, params['oauth_token'], params['oauth_verifier'])
    res = user.post('https://api.twitter.com/oauth/access_token', params)
    params = parser(res.text)
    AK, AS = params['oauth_token'], params['oauth_token_secret']
    id_ = params['user_id']

    user = OAuth1Session(CK, CS, AK, AS)

    if is_exist(id_):
        update_user(id_, AK, AS)
    else:
        insert_user(id_, AK, AS)

    return redirect(url_for('application'))

@app.route('/get_id')
def get_id():
    global user
    params = {
        'count': 1,
    }
    res = user.get('https://api.twitter.com/1.1/statuses/user_timeline.json', params=params)
    user_data = json.loads(res.text)
    id_ = user_data[0]['user']['id_str']

    obj = {
        'id': id_,
    }
    obj = json.dumps(obj)

    return jsonify(obj)


@app.route('/application')
def application():
    return render_template('app.html')

@app.route('/update', methods=['POST'])
def update():
    id_ = request.json['id']
    query = request.json['query']

    update_query(id_, query)
    obj = {
        'msg': '{}でクエリを登録しました。'.format(query)
    }

    obj = json.dumps(obj)

    return jsonify(obj)

@app.route('/delete', methods=['POST'])
def delete_user():
    id_ = request.json['id']

    delete(id_)
    empty = json.dumps({'msg': 'ユーザーを削除しました。'})

    return jsonify(empty)
    

if __name__ == "__main__":
    app = app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))