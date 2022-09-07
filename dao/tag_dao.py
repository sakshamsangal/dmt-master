import sqlite3

import pandas as pd

# conn = sqlite3.connect('db/dmt_master.db', check_same_thread=False)
conn = sqlite3.connect('../db/dmt_master.db', check_same_thread=False)
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
        tag_count int default 0,
        file_size real default 0,
        cost real default 0,
        status text default 'new'
    )""")


def create_tb_t3(tb_name):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tb_name} (
        tag text,
        map_tag text,
        rendered text,
        file_name text,
        prod_name text
    )""")


def insert(data):
    insert_query = 'INSERT INTO tb_temp VALUES(?,?,?,?,?)'
    cursor.executemany(insert_query, data)
    conn.commit()


def insert_tag_master(data):
    insert_query = 'INSERT INTO tb_temp_tag_master VALUES(?,?,?,?,?,?,?)'
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


def rem_tag(xml_file):
    q = f'''SELECT tag from tb_rem_tag where file_name="{xml_file}"'''
    c = conn.cursor()
    c.execute(q)
    result = c.fetchall()
    return get_list_of_dic(result)


def select_file_master_rem():
    q = '''
        SELECT  file_name,COUNT(tag) as tag_count, file_size,ROUND(file_size / COUNT(file_name),3) as cost 
        FROM tb_rem_tag
        GROUP BY file_name 
        ORDER BY COUNT(tag) DESC, cost ASC;
        '''
    cursor.execute(q)
    result = cursor.fetchall()
    x = get_list_of_dic(result)
    return x


def file_service_rem_with_tag():
    q = '''
        SELECT  file_name,COUNT(tag) as tag_count, file_size,ROUND(file_size / COUNT(file_name),3) as cost 
        FROM tb_rem_tag
        GROUP BY file_name 
        ORDER BY COUNT(tag) DESC, cost ASC;
        '''
    cursor.execute(q)
    result = cursor.fetchall()
    x = get_list_of_dic(result)

    for item in x:
        file_name = item['file_name']
        tags = rem_tag(file_name)
        item['tags'] = tags
    return x


def clear_tb():
    q = '''Delete FROM tb_main'''
    cursor.execute(q)

    q = '''Delete FROM tb_rem_tag'''
    cursor.execute(q)

    conn.commit()


def change_tag_status(xml_file):
    q = f'''
            SELECT prod_name, COUNT(file_name) as tag_count, file_size, ROUND(file_size / COUNT(file_name),3) as cost 
            FROM tb_rem_tag
            GROUP BY file_name having file_name="{xml_file}";
        '''
    cursor.execute(q)
    result2 = dict(cursor.fetchone())

    q = f'''SELECT tag, prod_name from tb_rem_tag where file_name="{xml_file}"'''
    cursor.execute(q)
    result = cursor.fetchall()

    tag_ls = []
    tag_ls_for_delete = []
    for item in result:
        tag_ls.append(
            (xml_file, result2['prod_name'], result2['tag_count'], result2['file_size'], result2['cost'], 'active',
             item['tag']))
        tag_ls_for_delete.append((item['tag'],))

    q = "update tb_tag_master set file_name=?, prod_name=? ,tag_count=?, file_size=?,cost=?, status=? where tag=?"
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
    q = "update tb_tag_master set file_name='', prod_name='', tag_count=0, file_size=0, cost=0 , status='new'"
    cursor.execute(q)
    conn.commit()


def export_tb_tag_master(loc, prod, tb_name):
    # q = '''SELECT distinct file_name, prod_name, tag_count, cost from tb_tag_master order by cost'''
    q = f'''SELECT * from {tb_name} order by cost'''
    c = conn.cursor()
    c.execute(q)
    result = c.fetchall()
    df = pd.DataFrame(result)
    df.to_excel(f'{loc}/{prod}/excel/export_{tb_name}.xlsx', index=False)


def tag_in_file(tag_name):
    q = f'''select DISTINCT file_name, file_size from tb_rem_tag where tag="{tag_name}" ORDER by file_size asc;'''
    c = conn.cursor()
    c.execute(q)
    result = c.fetchall()
    return get_list_of_dic(result)


def insert_tb_temp_tm2(data):
    insert_query = 'INSERT INTO tb_temp_tm2 VALUES(?,?,?,?,?)'
    cursor.executemany(insert_query, data)
    conn.commit()

# if __name__ == '__main__':
    # create_tb_t3('tm2')
