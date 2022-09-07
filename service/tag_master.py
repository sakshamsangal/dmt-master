import glob
import os
import re

from lxml import etree
import pandas as pd

tag_dic = {}
parent_dic = {}

ins = (etree._ProcessingInstruction, etree._Entity, etree._Comment)


def xml_traverse(parent, root):
    tag_name = etree.QName(root).localname
    if tag_name not in tag_dic:
        tag_dic[tag_name] = {
            'tag': tag_name,
            'map_tag': '',
            'text': 'no',
            'rendered': '',
            'child': set(),
            'att': {}
        }
    if tag_name in parent_dic:
        tag_dic[tag_name]['all_parent'] = parent_dic[tag_name]

    tag_dic[tag_name]['parent'] = parent
    # print(len(root.text))
    pattern = '(\n|\s)*'
    if root.text is not None and not re.fullmatch(pattern, root.text):
        tag_dic[tag_name]['text'] = 'yes'

    if root.tail is not None and not re.fullmatch(pattern, root.tail):
        tag_dic[tag_dic[tag_name]['parent']]['text'] = 'yes'

    for k, v in root.attrib.items():
        if k not in tag_dic[tag_name]['att']:
            tag_dic[tag_name]['att'][k] = set()
            tag_dic[tag_name]['att'][k].add(v)
        else:
            if len(tag_dic[tag_name]['att'][k]) < 10:
                tag_dic[tag_name]['att'][k].add(v)

    for child in root:
        if type(child) == etree._Element:
            x = etree.QName(child).localname
            tag_dic[tag_name]['child'].add(x)

            if x not in parent_dic:
                parent_dic[x] = set()

            parent_dic[x].add(tag_name)
            xml_traverse(tag_name, child)


def create_tag_master(loc, my_prod):
    for prod in my_prod:
        for xml_file in glob.glob(f"{loc}/{prod}/xml/orig_xml_{prod}/*/*.xml"):
            print(xml_file)
            tree = etree.parse(xml_file)
            root = tree.getroot()
            xml_traverse(None, root)
        df = pd.DataFrame(tag_dic.values())
        df.drop('parent', axis=1, inplace=True)
        df.to_excel(f'{loc}/{prod}/excel/tag_master_{prod}.xlsx', index=False)
