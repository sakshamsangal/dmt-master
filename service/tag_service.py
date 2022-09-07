from dao import tag_dao as td


def file_service_rem_with_tag():
    x = td.file_service_rem_with_tag()
    return x


def file_service_rem():
    x = td.select_file_master_rem()
    return x


def clear_tb():
    td.clear_tb()


def change_tag_status(xml_file):
    td.change_tag_status(xml_file)


def ca():
    td.ca()


def export_tb_tag_master(loc, prod, tb_name):
    td.export_tb_tag_master(loc,prod, tb_name)


def tag_in_file(tag_name):
    return td.tag_in_file(tag_name)
