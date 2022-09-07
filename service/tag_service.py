from dao import tag_dao as td


def tag_service_rem():
    x = td.select_tag_master_rem()
    return x


def file_service():
    x = td.select_file_master()
    return x


def select_one(xml_file):
    x = td.select_one(xml_file)
    return x


def rem_tag(xml_file):
    return td.rem_tag(xml_file)


def file_service_rem():
    x = td.select_file_master_rem()
    return x


def file_service_rem_sim():
    x = td.select_file_master_rem_sim()
    return x


def clear_tb():
    td.clear_tb()


def change_tag_status(xml_file):
    td.change_tag_status(xml_file)


def copy_tb():
    td.copy_tb()


def ca():
    td.ca()


def file_to_consider():
    return td.file_to_consider()


def tag_in_file(tag_name):
    return td.tag_in_file(tag_name)



