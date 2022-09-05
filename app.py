from flask import Flask, render_template, redirect, request
from service import tag_service as ts
from service import xml_service as xs

app = Flask(__name__)


@app.route('/tag')
def tag():
    return ts.tag_service()


@app.route('/main')
def tb_main():
    return ts.select_tb_main()


@app.route('/tag-rem')
def tag_rem():
    return ts.tag_service_rem()


@app.route('/file')
def file():
    return ts.file_service()


@app.route('/file-rem')
def file_rem():
    return ts.file_service_rem()


@app.route('/clear')
def clear():
    ts.clear_tb()
    return {'clear': 1}


@app.route('/sf/<string:xml_file>', methods=["GET"])
def set_file(xml_file):
    ts.set_file(xml_file)
    return {'sf': xml_file}




@app.route("/px", methods=["GET"])
def px():
    if request.method == "GET":
        xs.process_xml()
        return {'xml_processed': 1}


if __name__ == '__main__':
    app.run()
