# -*- coding: utf-8 -*-
import sys
import os

current_path = sys.path[0]

search_engine_path = os.path.join(current_path, "..", "SearchEngine", "script")
lac_path = os.path.join(current_path, "..", "LAC")

sys.path.append(lac_path)
sys.path.append(search_engine_path)

import thulac
import SearchEngine

thu = thulac.thulac("-seg_only")

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
    print thu.cut(query)
    return '{"result":true,"count":1}'


if __name__ == '__main__':
    app.run(port=1339)