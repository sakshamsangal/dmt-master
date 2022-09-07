from flask import Flask, request, jsonify, json
from service import tag_service as ts
from service import xml_service as xs

app = Flask(__name__)

from werkzeug.exceptions import HTTPException


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/tag/rem')
def tag_rem():
    return jsonify(ts.tag_service_rem())


@app.route('/file')
def file():
    return jsonify(ts.file_service())


@app.route('/file/tag/<string:xml_file>')
def select_one(xml_file):
    return jsonify(ts.select_one(xml_file))


@app.route('/file/rem')
def file_rem():
    return jsonify(ts.file_service_rem())


@app.route('/file/rem/sim')
def file_rem_sim():
    return jsonify(ts.file_service_rem_sim())


@app.route('/clear')
def clear():
    ts.clear_tb()
    return {'clear': 1}


@app.route('/active', methods=["POST"])
def active():
    if request.method == "POST":
        ls = request.json['file_name']
        for xml_file in ls:
            ts.change_tag_status(xml_file)
        return {'file_name': ls, 'status': 'active'}


@app.route('/rem-tag/<string:xml_file>', methods=["GET"])
def rem_tag(xml_file):
    return jsonify(ts.rem_tag(xml_file))


@app.route("/xml/process", methods=["POST"])
def xml_process():
    if request.method == "POST":
        xml_path = request.form['path']
        xs.process_xml(xml_path)
        ts.copy_tb()
        return jsonify({'xml_processed': 1})


@app.route('/ca')
def ca():
    ts.ca()
    return jsonify({'msg': 'success'})


@app.route('/file-to-consider')
def file_to_consider():
    return jsonify(ts.file_to_consider())


@app.route('/tag-in-file/<string:tag_name>')
def tag_in_file(tag_name):
    return jsonify(ts.tag_in_file(tag_name))


if __name__ == '__main__':
    app.run()
