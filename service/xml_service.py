import glob
import os

from lxml import etree
from dao import tag_dao as td

tag_set = set()
prod_name = ''
file_name = ''


def xml_traverse(root):
    tag_set.add(etree.QName(root).localname)
    for child in root:
        if not (type(child) == etree._ProcessingInstruction):
            xml_traverse(child)


def process_xml():
    res = []
    global prod_name, file_name, tag_set
    for prod_path in glob.glob("static/xml/*"):
        prod = prod_path.rsplit('\\', 1)[1]
        prod_name = prod
        x = []
        for xml_file in glob.glob(f"{prod_path}/*.xml"):
            tag_set = set()
            file_name = os.path.basename(xml_file)
            print(file_name)
            tree = etree.parse(xml_file)
            root = tree.getroot()
            xml_traverse(root)
            for y in tag_set:
                x.append((f'{file_name}@{y}', file_name, y, prod_name, 0, 'new'))
            res.append((prod_name,file_name))
        td.create_tb_main()
        td.create_tb_temp()
        td.insert(x)
        td.merge()
        td.drop_tb('temp')
    return res
