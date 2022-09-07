import glob
import os

from lxml import etree


def xml_split(prod, loc, tag_selected):
    path = rf'{loc}\\{prod}\\xml\\orig_xml_{prod}'
    fout = open('xml_split_log. txt', 'w')
    for xml_file_path in glob.glob(rf'{path}\*\*.xml'):
        context = etree.iterparse(xml_file_path, events=('end',), recover=True)
        prod_name = os.path.splitext(os.path.basename(xml_file_path))[0]
        fout.write(prod_name + '\n')
        directory = f'{loc}/{prod}/xml/chunk_xml_{prod}/{prod_name}'
        os.makedirs(directory, exist_ok=True)
        my_dict = tag_selected.copy()
        for event, elem in context:
            tn = etree.QName(elem).localname
            if tn in my_dict.keys():
                fn = f'{directory}/{prod_name}_{tn}_{my_dict[tn]}.xml'
                my_dict[tn] += 1
                print(fn)
                fout.write(fn + '\n')
                with open(fn, 'wb') as f:
                    f.write(bytearray('<?xml version="1.0" encoding="utf-8" ?>\n', 'utf-8'))
                    f.write(etree.tostring(elem))
        fout.write('=====\n')
    fout.close()


# if __name__ == '__main__':
#     prod = 'book'
#     tag_selected = {
#         'book': 1
#     }
#     loc = 'C:\\Users\\saksangal\\Pictures\\saksham'
#     xml_split(prod, loc, tag_selected)
