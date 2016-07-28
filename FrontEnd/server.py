# -*- coding: utf-8 -*-

import os
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

    pass


if __name__ == '__main__':
    app.run(port=1339)