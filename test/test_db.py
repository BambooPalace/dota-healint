from src.db import create_table, insert_values, query_db

def test_create():
    create_table('test_table', ['id', 'value'])
    
def test_insert():
    table = 'test_table'
    insert_values(table, [(1, 10)])
    query = f'''select * from {table}
    limit 1
    '''
    res = query_db(query)
    assert len(res) == 1

    



if __name__ == '__main__':
    test_insert()
    