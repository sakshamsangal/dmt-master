import glob
import os
import re

from dao import tag_dao as td
from lxml import etree
import pandas as pd

tag_dic = {}
file_name = ''
prod_name = ''


def xml_traverse(root):
    tag_name = etree.QName(root).localname
    if tag_name not in tag_dic:
        tag_dic[tag_name] = {
            'tag': tag_name,
            'map_tag': '',
            'rendered': '',
            'file_name': file_name,
            'prod_name': prod_name
        }
    for child in root:
        if type(child) == etree._Element:
            xml_traverse(child)


def create_tag_master_all_dir(loc, content_type):
    global prod_name, file_name, tag_dic
    for prod_path in glob.glob(f"{loc}/{content_type}/xml/chunk_xml_{content_type}/*"):
        prod = prod_path.rsplit('\\', 1)[1]
        prod_name = prod
        for xml_file in glob.glob(f"{prod_path}/*.xml"):
            print(xml_file)
            file_name = os.path.basename(xml_file)
            parser = etree.XMLParser(recover=True)
            tree = etree.parse(xml_file, parser)
            root = tree.getroot()
            xml_traverse(root)
        df = pd.DataFrame(tag_dic.values())
        df.to_excel(f'{loc}/{content_type}/excel/tag_master_{content_type}.xlsx', index=False)


def create_tag_master(loc, content_type, prods):
    global file_name,prod_name, tag_dic
    for x in prods:
        prod_name = x
        for xml_file in glob.glob(f"{loc}/{content_type}/xml/chunk_xml_{content_type}/{prod_name}/*.xml"):
            print(xml_file)
            file_name = os.path.basename(xml_file)
            parser = etree.XMLParser(recover=True)
            tree = etree.parse(xml_file, parser)
            root = tree.getroot()
            xml_traverse(root)
        df = pd.DataFrame(tag_dic.values())
        df.to_excel(f'{loc}/{content_type}/excel/tag_master_{content_type}.xlsx', index=False)


if __name__ == '__main__':
    td.create_tb_t3('tm2')
    td.create_tb_t3('tb_temp_tm2')
    create_tag_master('D:\\Pictures\\sak', 'akshu', ['temp2', 'temp'])
    z = []
    for y in tag_dic.values():
        z.append(tuple(y.values()))

    td.insert_tb_temp_tm2(z)
    td.merge('tm2', 'tb_temp_tm2', 'tag')
    td.drop_tb('tb_temp_tm2')
    tag_dic = {}


