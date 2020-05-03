#!/usr/bin/env python
# encoding:utf-8

import os
# import time
# import base64
import uuid
# from strUtil import Pic_str
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
# from flask import abort
from flask import make_response
from flask import send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload')
def upload_test():
    return render_template('up.html')


# 上传文件
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        #new_filename = Pic_str().create_uuid() + '.' + ext
        name = 'test_name'
        # namespace = 'test_namespace'
        # namespace = uuid.NAMESPACE_URL
        print(uuid.uuid1())
        new_filename = str(uuid.uuid1()) + '.' + ext
        f.save(os.path.join(file_dir, new_filename))

        return jsonify({"success": 0, "msg": "上传成功"})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})


# download photo: http://192.168.2.10:5000/download/7b8da8e8-8c8d-11ea-97d8-e8b1fce9a683.png
@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('uploads', filename)):
            return send_from_directory('uploads', filename, as_attachment=True)
        pass


# show photo: http://192.168.2.10:5000/show/7b8da8e8-8c8d-11ea-97d8-e8b1fce9a683.png
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename),
                              "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
