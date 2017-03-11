#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# Copyright 2015-2016 liantian
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>


import os
import StringIO
from flask import Flask
from flask import send_file, request,render_template
from PIL import Image

import qrcode
from qrcode.exceptions import DataOverflowError

ecl_map = {
    'L': qrcode.constants.ERROR_CORRECT_L,
    'M': qrcode.constants.ERROR_CORRECT_H,
    'Q': qrcode.constants.ERROR_CORRECT_Q,
    'H': qrcode.constants.ERROR_CORRECT_H,
}

app = Flask(__name__)
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    app.config['DEBUG'] = True


@app.errorhandler(404)
def page_not_found(e):
    return "Error : 404 - Page Not Found", 404


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api', methods=['GET', 'POST'])
def api():
    data = request.values.get('data', "parameter 'data' is empty\n")

    try:
        size = int(request.values.get('size'))
        if size < 1 or size > 100:
            size = 4
    except:
        size = 4

    ecl = request.values.get('ecl', "L")

    if ecl not in ['L', 'M', 'Q', 'H']:
        ecl = 'M'
    qr = qrcode.QRCode(error_correction=ecl_map[ecl],box_size=size, border=1)
    qr.add_data(data)
    try:
        qr.make()
    except DataOverflowError:
        return "Error, Data Too Long",400

    img = qr.make_image()


    #
    strIO = StringIO.StringIO()
    img.save(strIO)
    strIO.seek(0)

    return send_file(strIO , mimetype='image/png')
