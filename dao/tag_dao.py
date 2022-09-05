import sqlite3


conn = sqlite3.connect('db/dmt_master.db', check_same_thread=False)
# conn = sqlite3.connect('../db/dmt_master.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def create_tb_temp():
    cursor.execute(f"""CREATE TABLE if not exists tb_temp(
        id text,
        file_name text,
        tag text,
        prod_name text,
        file_size real default 0,
        status text default 'new'
    )""")


def create_tb_temp_tag_master():
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS tb_temp_tag_master(
           tag text,
           file_name text,
           prod_name text,
           status text default 'new'
       )""")


def create_tb_main():
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS tb_main(
        id text,
        file_name text,
        tag text,
        prod_name text,
        file_size int default 0,
        status text default 'new'
    )""")


def create_tb_tag_master():
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS tb_tag_master(
        tag text,
        file_name text,
        prod_name text,
        status text default 'new'
    )""")


def insert(data):
    insert_query = 'INSERT INTO tb_temp VALUES(?,?,?,?,?,?)'
    cursor.executemany(insert_query, data)
    conn.commit()


def insert_tag_master(data):
    insert_query = 'INSERT INTO tb_temp_tag_master VALUES(?,?,?,?)'
    cursor.executemany(insert_query, data)
    conn.commit()


def merge(t1, t2, col_to_comp):
    q = f"""
    INSERT INTO {t1} 
    SELECT * FROM {t2} A 
    WHERE NOT EXISTS (SELECT 1 FROM {t1} X WHERE A.{col_to_comp} = X.{col_to_comp})
    """
    cursor.execute(q)
    conn.commit()


def drop_tb(tb_name):
    qry = f"DROP table {tb_name}"
    try:
        cur = conn.cursor()
        cur.execute(qry)
        conn.commit()
        print("tb drop successfully")
    except:
        print("error in operation")
        conn.rollback()


def select_tag_master():
    q = '''SELECT tag, file_name, prod_name from tb_main group by tag'''
    cursor.execute(q)
    result = cursor.fetchall()
    return len(result), get_list_of_dic(result)

    # return result


def get_list_of_dic(result):
    ls = []
    for item in result:
        ls.append({k: item[k] for k in item.keys()})
    return ls


def select_tb_main():
    q = '''SELECT * from tb_main'''
    c = conn.cursor()
    c.execute(q)
    result = c.fetchall()
    return get_list_of_dic(result)


def select_one(xml_file):
    q = f'''SELECT * from tb_main where file_name="{xml_file}"'''
    c = conn.cursor()
    c.execute(q)
    result = c.fetchall()
    return get_list_of_dic(result)


def select_tag_master_rem():
    q = '''SELECT tag FROM tb_tag_master where status="new"'''
    cursor.execute(q)
    result = cursor.fetchall()
    return get_list_of_dic(result)
    # return result


def select_file_master():
    q = '''
    SELECT  file_name,COUNT(tag), file_size
    FROM tb_main
    GROUP BY file_name 
    ORDER BY COUNT(tag) DESC;
    '''
    cursor.execute(q)
    result = cursor.fetchall()
    return get_list_of_dic(result)


def select_file_master_rem():
    q = f'''
        SELECT file_name, COUNT(tag), file_size
        FROM tb_main where tag in (SELECT tag from tb_tag_master where status="new")
        GROUP BY file_name 
        ORDER BY COUNT(tag) DESC;
    '''
    cursor.execute(q)
    result = cursor.fetchall()
    return get_list_of_dic(result)
    # return result


def clear_tb():
    q = '''Delete FROM tb_main'''
    cursor.execute(q)


def change_tag_status(xml_file, status):
    q = f'''SELECT tag,prod_name from tb_main where file_name="{xml_file}"'''
    cursor.execute(q)
    result = cursor.fetchall()
    ls = []
    if status == 'new':
        for item in result:
            ls.append(('', '', status, item['tag']))
    else:
        for item in result:
            ls.append((xml_file, item['prod_name'], status, item['tag']))

    q = f"update tb_tag_master set file_name=?, prod_name=? , status=? where tag=?"
    cursor.executemany(q, ls)
    conn.commit()





# if __name__ == '__main__':
#     set_file('book2.xml')
