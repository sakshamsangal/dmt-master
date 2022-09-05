from dao import tag_dao as td


def tag_service():
    ln, x = td.select_tag_master()
    return ln, x

def tag_service_rem():
    x = td.select_tag_master_rem()
    return x


def file_service():
    x = td.select_file_master()
    return x


def select_one(xml_file):
    x = td.select_one(xml_file)
    return x


def file_service_rem():
    x = td.select_file_master_rem()
    return x


def clear_tb():
    td.clear_tb()


def change_tag_status(xml_file,status):
    td.change_tag_status(xml_file,status)



def select_tb_main():
    return td.select_tb_main()
