import sqlite3

from flask import jsonify
conn = sqlite3.connect('db/dmt_master.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def create_tb_temp():
    cursor.execute(f"""CREATE TABLE if not exists tb_temp(
        id text,
        file_name text,
        tag text,
        prod_name text,
        file_size int default 0,
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

def insert(data):
    insert_query = 'INSERT INTO tb_temp VALUES(?,?,?,?,?,?)'
    cursor.executemany(insert_query, data)
    conn.commit()


def merge():
    q = """
    INSERT INTO tb_main 
    SELECT * FROM tb_temp A 
    WHERE NOT EXISTS (SELECT 1 FROM tb_main X WHERE A.id = X.id)
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
    return get_list_of_dic(result)

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



def select_tag_master_rem():
    q = '''SELECT tag, file_name, prod_name from [rem_tag] group by tag'''
    cursor.execute(q)
    result = cursor.fetchall()
    return get_list_of_dic(result)
    # return result

def select_file_master():
    q = '''
    SELECT  file_name,COUNT(tag)
    FROM tb_main
    GROUP BY file_name 
    ORDER BY COUNT(tag) DESC;
    '''
    cursor.execute(q)
    result = cursor.fetchall()
    return get_list_of_dic(result)

    # return result


def select_file_master_rem():
    q = '''
    SELECT file_name,COUNT(tag)
    FROM [rem_tag]
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

    q = '''DROP view IF EXISTS  [rem_tag]'''
    cursor.execute(q)


def set_file(xml_file):
    q = f"update tb_main set status='active' where file_name='{xml_file}'"
    cursor.execute(q)

    q = '''CREATE VIEW rem_tag AS 
    SELECT * FROM tb_main t1 LEFT JOIN tb_main t2 ON t2.tag = t1.tag and t2.status != t1.status
    WHERE t2.tag IS NULL and t1.status is 'new';'''
    cursor.execute(q)





