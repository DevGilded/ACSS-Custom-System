import sqlite3 as sql

def create_table(database: str, tblname: str, *args):
    '''
    
    param: database
    '''
    
    connection = sql.connect(database)
    cursor = connection.cursor()

    columns = ', '.join(f'{name} {type_}' for name, type_ in args)

    sql_command = f'CREATE TABLE IF NOT EXISTS {tblname} ({columns})'
    print(sql_command)
    print()

    cursor.execute(sql_command)

    connection.commit()
    connection.close()

    print('TABLE CREATED SUCCESFULLY')

def del_table(database: str, tblname: str):
    connection = sql.connect(database)
    cursor = connection.cursor()

    cursor.execute(f'''
    DROP TABLE IF EXISTS {tblname}
    ''')

    connection.commit()
    connection.close()

    print('TABLE DELETED SUCCESFULLY')




def add_value(database: str, tblname: str, **kwargs):
    
    connection = sql.connect(database)
    cursor = connection.cursor()

    columns = ', '.join(f'{name}' for name in kwargs)
    value = ', '.join('?' for _ in kwargs)

    sql_command = f'INSERT INTO {tblname} ({columns}) VALUES ({value})'
    print(sql_command)
    print()

    cursor.execute(sql_command, (tuple(value for _, value, in kwargs.items())))

    connection.commit()
    connection.close()

    print('ADDED TO THE TABLE SUCCESFULLY')

    
def get_value(database: str, tblname: str, column: str):

    connection = sql.connect(database)
    cursor = connection.cursor()

    cursor.execute(f'SELECT {column} FROM {tblname}')

    value = cursor.fetchall()

    connection.close()

    return value


def print_table(database: str, tblname: str):
    
    connection = sql.connect(database)
    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM {tblname}')

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()


# create_table('data\database\member.db', 'PERSONAL_INFORMATIONS', ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), ('first_name', 'TEXT'), ('middle_name', 'TEXT'), ('last_name', 'TEXT'), ('facebook_account', 'TEXT'), ('sex', 'TEXT'), ('age', 'INTEGER'), ('birth_day', 'DATE'), ('phone_num', 'TEXT'), ('school_id', 'TEXT'))
# create_table('data\database\member.db', 'SPECIALIZATIONS', ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), ('pers_info_id', 'TEXT'), ('dance', 'TEXT'), ('sport', 'TEXT'), ('multimedia', 'TEXT') , ('literary', 'TEXT'), ('athletics', 'TEXT'), ('music', 'TEXT'), ('visual arts', 'TEXT'), ('others', 'TEXT'))

del_table(r'data\database\member.db', 'sqlite_sequence')
# del_table(r'data\database\member.db', 'SPECIALIZATIONS')
