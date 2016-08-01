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
    res = searchEngine.query(query)
    print(res)
    py_dict = {}
    basic_info_list = res[0]
    links_list = res[1]
    pics_list = res[2]

    py_dict["basic_info"] = basic_info_list[0]
    py_dict["pics"] = pics_list
    links_rows = []
    for i in range(4):
        link_row = [links_list[i], basic_info_list[i]["title"]]
        links_rows.append(link_row)
    py_dict["links"] = links_rows
    res = json.dumps(py_dict)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1330)
