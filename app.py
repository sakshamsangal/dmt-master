import os

from flask import Flask, request, jsonify, json
from service import tag_service as ts
from service import xml_service as xs
from service import xml_split as chunk
from service import tag_master as tm

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


@app.route('/clear')
def clear():
    ts.clear_tb()
    return {'clear': 1}


@app.route('/ca')
def ca():
    ts.ca()
    return jsonify({'msg': 'success'})


@app.route('/export', methods=["POST"])
def export_tb_tag_master():
    if request.method == "POST":
        loc = request.json['loc']
        prod = request.json['prod']
        tb_name = request.json['tb_name']
        ts.export_tb_tag_master(loc, prod, tb_name)
        return jsonify({'status': f'{tb_name} exported as excel', 'loc': f'{loc}/excel'})


@app.route('/tag-in-file/<string:tag_name>')
def tag_in_file(tag_name):
    return jsonify(ts.tag_in_file(tag_name))


@app.route('/dir-maker', methods=["POST"])
def dir_maker():
    if request.method == "POST":
        ls = request.json['folder_name']
        loc = request.json['loc']
        for x in ls:
            for item in ['xml', 'excel', 'word', 'pdf', 'res']:
                os.makedirs(f'{loc}/{x}/{item}', exist_ok=True)
            os.makedirs(f'{loc}/{x}/xml/orig_xml_{x}', exist_ok=True)
            os.makedirs(f'{loc}/{x}/xml/chunk_xml_{x}', exist_ok=True)
            os.makedirs(f'{loc}/{x}/xml/zip_xml_{x}', exist_ok=True)
        return {'folder_name': ls, 'loc': loc, 'status': 'created'}


@app.route('/tag-master-excel', methods=["POST"])
def tag_master_excel():
    if request.method == "POST":
        prod = request.json['prod']
        loc = request.json['loc']
        tm.create_tag_master(loc, prod)
        return {'prod': prod, 'loc': loc, 'status': 'tag master created'}


@app.route('/xml-chunk', methods=["POST"])
def xml_chunk():
    if request.method == "POST":
        prod = request.json['prod']
        loc = request.json['loc']
        tag_selected = request.json['tag_selected']
        chunk.xml_split(prod, loc, tag_selected)
        return {'prod': prod, 'loc': loc, 'status': 'xml chunk created', 'tag_selected': tag_selected}


@app.route("/xml/process", methods=["POST"])
def xml_process():
    if request.method == "POST":
        prod = request.json['prod']
        loc = request.json['loc']
        # xml_path = request.form['path']
        xs.process_xml(loc, prod)
        return jsonify({'status': 'db updated'})


@app.route('/active', methods=["POST"])
def active():
    if request.method == "POST":
        ls = request.json['file_name']
        for xml_file in ls:
            ts.change_tag_status(xml_file)
        return {'file_name': ls, 'status': 'active'}


@app.route('/file/rem')
def file_rem():
    return jsonify(ts.file_service_rem())


@app.route('/file/rem-with-tag')
def file_rem_with_tag():
    return jsonify(ts.file_service_rem_with_tag())


if __name__ == '__main__':
    app.run()
