# -*- coding: utf-8 -*-
import sys
import os
import json

current_path = sys.path[0]

search_engine_path = os.path.join(current_path, "..", "SearchEngine", "script")

sys.path.append(search_engine_path)

import SearchEngine

searchEngine = SearchEngine.SearchEngine()

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app_root = app.root_path
app.config['DEBUG'] = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query/<query>')
def search(query):
    query = query.encode("utf-8")
    res = searchEngine.query(query)
    diction = {}
    diction["basic_info"] = res[0]
    diction["links"] = res[1]
    diction["pics"] = res[2]
    res = json.dumps(diction)
    return res


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1339)