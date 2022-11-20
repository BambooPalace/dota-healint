import sqlite3
import pandas as pd



def connect_db(db='dota.db'):
    return sqlite3.connect(db)
    

def create_table(table, columns):
    cur = connect_db().cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table}({", ".join(columns)})')
    res = cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
    if res.fetchone() is not None:        
        print('table created or already exits')
    else:
        raise Exception('table not created, please check error')



def insert_values(table, values):
    con = connect_db()
    cur = con.cursor()
    cur.execute(f'''INSERT INTO {table} VALUES
    {str(values)[1:-1]}
    ''')
    con.commit()
    print(f'successfully insert {len(values)} entries to {table}.')
    

def query_db(query, return_df=True):
    cur = connect_db().cursor()
    res = cur.execute(query)
    temp = res.fetchall()

    if temp is None:
        return
    
    if return_df:
        cols = [d[0] for d in cur.description]
        df = pd.DataFrame(temp, columns=cols)
        return df
    else:
        return temp
    



    

