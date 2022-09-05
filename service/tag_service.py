from dao import tag_dao as td


def tag_service():
    x = td.select_tag_master()
    return x

def tag_service_rem():
    x = td.select_tag_master_rem()
    return x


def file_service():
    x = td.select_file_master()
    return x


def file_service_rem():
    x = td.select_file_master_rem()
    return x


def clear_tb():
    td.clear_tb()


def set_file(xml_file):
    td.set_file(xml_file)


def select_tb_main():
    return td.select_tb_main()
