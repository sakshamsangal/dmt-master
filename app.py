from flask import Flask, request, jsonify
from service import tag_service as ts
from service import xml_service as xs

app = Flask(__name__)


@app.route('/tag/all')
def tag_all():
    return ts.select_tb_main()


@app.route('/tag/unique')
def tag_unique():
    ln, x = ts.tag_service()
    return jsonify({'total_tag': ln, 'tags': x})


@app.route('/tag/rem')
def tag_rem():
    return ts.tag_service_rem()


@app.route('/file')
def file():
    return ts.file_service()

@app.route('/file/tag/<string:xml_file>')
def select_one(xml_file):
    return ts.select_one(xml_file)

@app.route('/file/rem')
def file_rem():
    return ts.file_service_rem()


@app.route('/clear')
def clear():
    ts.clear_tb()
    return {'clear': 1}


@app.route('/file/<string:xml_file>/<string:status>', methods=["GET"])
def change_tag_status(xml_file, status):
    ts.change_tag_status(xml_file, status)
    return {'file_name': xml_file, 'status': status}


@app.route("/xml/process", methods=["POST"])
def xml_process():
    if request.method == "POST":
        xml_path = request.form['path']
        xs.process_xml(xml_path)
        return jsonify({'xml_processed': 1})


if __name__ == '__main__':
    app.run()
