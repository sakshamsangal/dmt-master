import glob
import os

from lxml import etree
from dao import tag_dao as td

g_tag_set = set()
tag_set = set()
prod_name = ''
file_name = ''


def xml_traverse(root):
    tag_name = etree.QName(root).localname
    g_tag_set.add(tag_name)
    tag_set.add(tag_name)
    for child in root:
        if not (type(child) == etree._ProcessingInstruction):
            xml_traverse(child)


def process_xml(path):
    res = []
    global prod_name, file_name, tag_set
    for prod_path in glob.glob(f"{path}/*"):
        print(prod_path)
        prod = prod_path.rsplit('\\', 1)[1]
        prod_name = prod
        x = []
        z = []
        for xml_file in glob.glob(f"{prod_path}/*.xml"):
            tag_set = set()
            file_name = os.path.basename(xml_file)
            print(file_name)
            tree = etree.parse(xml_file)
            root = tree.getroot()
            xml_traverse(root)
            file_size = round(os.stat(xml_file).st_size / 1024,2)
            print(file_size)
            for y in tag_set:
                x.append((f'{file_name}@{y}', file_name, y, prod_name, file_size, 'new'))
            res.append((prod_name,file_name))

        for y in g_tag_set:
            z.append((y, '', '', 'new'))

        td.create_tb_main()
        td.create_tb_tag_master()

        td.create_tb_temp()
        td.create_tb_temp_tag_master()

        td.insert(x)
        td.insert_tag_master(z)

        td.merge('tb_main', 'tb_temp', 'id')
        td.merge('tb_tag_master', 'tb_temp_tag_master', 'tag')

        td.drop_tb('tb_temp')
        td.drop_tb('tb_temp_tag_master')

    return res
