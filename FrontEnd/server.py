# -*- coding: utf-8 -*-
import sys
import os

current_path = sys.path[0]

search_engine_path = os.path.join(current_path, "..", "SearchEngine", "script")

sys.path.append(search_engine_path)

import SearchEngine

searchEngine = SearchEngine.SearchEngine()

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app_root = app.root_path
app.config['DEBUG'] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query/<query>')
def search(query):
    query = query.encode("utf-8")
    print(query)
    res = searchEngine.query(query)
    print(res)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1339)