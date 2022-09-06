import sqlite3

conn = sqlite3.connect('db/dmt_master.db', check_same_thread=False)
# conn = sqlite3.connect('../db/dmt_master.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()



def create_tb_t1(tb_name):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tb_name} (
        id text,
        file_name text,
        tag text,
        prod_name text,
        file_size real default 0
    )""")


def create_tb_t2(tb_name):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tb_name} (
        tag text,
        file_name text,
        prod_name text,
        status text default 'new'
    )""")


def insert(data):
    insert_query = 'INSERT INTO tb_temp VALUES(?,?,?,?,?)'
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



def get_list_of_dic(result):
    ls = []
    for item in result:
        ls.append({k: item[k] for k in item.keys()})
    return ls



def select_one(xml_file):
    q = f'''SELECT * from tb_main where file_name="{xml_file}"'''
    c = conn.cursor()
    c.execute(q)
    result = c.fetchall()
    return get_list_of_dic(result)


def rem_tag(xml_file):
    q = f'''SELECT tag from tb_rem_tag where file_name="{xml_file}"'''
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
    SELECT  file_name,COUNT(tag) as tag_count, file_size
    FROM tb_main
    GROUP BY file_name 
    ORDER BY COUNT(tag) DESC;
    '''
    cursor.execute(q)
    result = cursor.fetchall()
    return get_list_of_dic(result)


def select_file_master_rem():
    q = '''
        SELECT  file_name,COUNT(tag) as tag_count, file_size
        FROM tb_rem_tag
        GROUP BY file_name 
        ORDER BY COUNT(tag) DESC;
        '''
    cursor.execute(q)
    result = cursor.fetchall()
    x = get_list_of_dic(result)

    for item in x:
        file_name = item['file_name']
        tags = rem_tag(file_name)
        item['tags'] = tags
    return x


def select_file_master_rem_sim():
    q = '''
        SELECT  file_name,COUNT(tag) as tag_count, file_size
        FROM tb_rem_tag
        GROUP BY file_name 
        ORDER BY COUNT(tag) DESC;
        '''
    cursor.execute(q)
    result = cursor.fetchall()
    x = get_list_of_dic(result)
    return x



def clear_tb():
    q = '''Delete FROM tb_main'''
    cursor.execute(q)


def change_tag_status(xml_file):
    q = f'''SELECT tag,prod_name from tb_rem_tag where file_name="{xml_file}"'''
    cursor.execute(q)
    result = cursor.fetchall()
    tag_ls = []
    tag_ls_for_delete = []
    for item in result:
        tag_ls.append((xml_file, item['prod_name'], 'active', item['tag']))
        tag_ls_for_delete.append((item['tag'],))

    q = "update tb_tag_master set file_name=?, prod_name=? , status=? where tag=?"
    cursor.executemany(q, tag_ls)

    q = "DELETE FROM tb_rem_tag WHERE tag=?"
    cursor.executemany(q, tag_ls_for_delete)

    conn.commit()


def copy_tb():
    q = "delete from tb_rem_tag"
    cursor.execute(q)
    cursor.execute("INSERT INTO tb_rem_tag SELECT * FROM tb_main;")
    conn.commit()


def ca():
    copy_tb()
    q = "update tb_tag_master set file_name='', prod_name='' , status='new'"
    cursor.execute(q)
    conn.commit()


# if __name__ == '__main__':
#     change_tag_status('book2.xml', '')
    # create_tb_rem_tag()


def file_to_consider():
    q = '''SELECT distinct file_name, prod_name from tb_tag_master'''
    c = conn.cursor()
    c.execute(q)
    result = c.fetchall()
    return get_list_of_dic(result)