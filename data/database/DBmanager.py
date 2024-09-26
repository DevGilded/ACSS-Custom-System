import sqlite3 as sql
import time

import pandas as pd


class DataBase:
    def __init__(self, path) -> None:
        self.__database = path
        self.__tables = {}
        self.__tables_ID = {}
        self.get_table()
        self.get_IDs()

    def create_table(self, name: str, **columns) -> None:
        """
        Create Table

        Column Ex.
        Name = 'TEXT'
        Age = 'INTEGER'
        """
        connect = sql.connect(self.__database)
        cursor = connect.cursor()

        query = f'CREATE TABLE IF NOT EXISTS {name} ({', '.join(f'{col} {type_}' for col, type_ in columns.items())})'
        # print(query)

        try:
            cursor.execute(query)
            connect.commit()
            self.__tables[name] = columns
            self.__tables_ID[name] = []
            # print(self.__tables)
            print(f'Table {name} Created')
        except sql.Error as e:
            print(f"SQLite error: {e}")
        finally:
            connect.close()

    def delete_table(self, name: str) -> None:
        """
        Delete Table
        """
        connect = sql.connect(self.__database)
        cursor = connect.cursor()

        try:
            cursor.execute(f'DROP TABLE IF EXISTS {name}')
            connect.commit()
            self.__tables.pop(name)
            print(f'Table {name} Deleted')
        except sql.Error as e:
            print(f"SQLite error: {e}")
        finally:
            connect.close()

    def get_columns(self, table: str) -> dict[str, str]:
        """
        Get All Columns in the Table
        """
        if self.__tables[table]:
            return self.__tables[table]

        connect = sql.connect(self.__database)
        cursor = connect.cursor()

        try:
            cursor.execute(f"PRAGMA table_info({table})")
            self.__tables[table] = {}
            for column in cursor.fetchall():
                _, name, data_type, _, _, _ = column
                self.__tables[table][name] = data_type
        except sql.Error as e:
            print(f"SQLite error: {e}")
        finally:
            connect.close()

    def get_column(self, table: str, column: str) -> dict:
        """
        Get All Columns in the Table
        """
        if column == '*':
            rows = {}
            for i in range(len(self.__tables_ID[table])):
                rows[i+1] = {}
                for column_name in self.__tables[table]:
                    column_ = self.get_column(table, column_name)[i+1]
                    if column_[column_name] is not None:
                        rows[i+1].update(column_)
            return rows

        connect = sql.connect(self.__database)
        cursor = connect.cursor()

        query = f"SELECT {column} FROM {table}"

        try:
            cursor.execute(query)
            rows = {}
            index = 1
            for val in cursor.fetchall():
                rows[index] = {column: val[0]}
                index += 1
            return rows
        except sql.Error as e:
            print(f"SQLite error: {e}")
        finally:
            connect.close()

    def get_table(self, table: str = None) -> list | dict[str, dict]:
        """
        Get All Table in the Database
        """
        if table:
            return self.__tables[table]
        if self.__tables:
            return self.__tables

        connect = sql.connect(self.__database)
        cursor = connect.cursor()

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            for table in cursor.fetchall():
                if table[0] == 'sqlite_sequence':
                    continue
                cursor.execute(f'PRAGMA table_info({table[0]});')
                self.__tables[table[0]] = {}
                self.__tables_ID[table[0]] = []
                self.get_columns(table[0])
            return self.__tables
        except sql.Error as e:
            print(f"SQLite error: {e}")
        finally:
            connect.close()

    def get_IDs(self, table: str = None) -> list | dict[str, dict]:
        if table:
            return self.__tables_ID[table]

        for table, _ in self.__tables_ID.items():
            ID_NAME = list(self.__tables[table])[0]
            self.__tables_ID[table] = self.get_column(table, ID_NAME)
        return self.__tables_ID

    def import_excel(self, path: str, **tables) -> None:
        """
        Import excel file into the database

        tables ex.
        TABLE NAME = dict{db column name: excel column name}
        """
        df = pd.read_excel(path)
        for row in range(len(df.values)):
            ID = None
            for table, columns in tables.items():
                print()
                print(table, ']====================')
                column = {}
                for db_column, xlsx_column in columns.items():
                    # print(xlsx_column, str(df.get(xlsx_column)[row]))
                    if str(df.get(xlsx_column)[row]) == 'nan':
                        continue
                    if isinstance(xlsx_column, list):
                        column[db_column] = ', '.join(' '.join(str(df.get(y)[row]) for y in x) if isinstance(x, list) else str(df.get(x)[row]) for x in xlsx_column)
                    else:
                        if isinstance(df.get(xlsx_column)[row], pd.Timestamp):
                            column[db_column] = str(df.get(xlsx_column)[row]).split(' ')[0]
                        else:
                            column[db_column] = str(df.get(xlsx_column)[row])
                if ID:
                    self.add_row_by(table, ID, **column)
                else:
                    ID = self.add_row(table, **column)
            print(f'row {row + 1} is added')
        # raise NotImplemented

    def update_column(self, table: str, id_: str, column: str, value:str) -> None:
        """
        Update a column in a row
        """
        connect = sql.connect(self.__database)
        cursor = connect.cursor()

        ID_NAME = list(self.__tables[table])[0]
        query = f'UPDATE {table} SET {column} = ? WHERE {ID_NAME} = ?'
        # print(query, (value, ID))

        try:
            cursor.execute(query, (value, id_))
            connect.commit()
        except sql.Error as e:
            print(f"SQLite error: {e}")
        finally:
            connect.close()

    def add_row_by(self, table: str, id_: str, **param) -> str:
        """
        Add a row in {table}
        """
        connect = sql.connect(self.__database)
        cursor = connect.cursor()

        columns = ', '.join(column for column in param)

        custom_id = create_ID(self.__tables_ID[table])

        ID_NAME = list(self.__tables[table])[0]
        RELATION_ID_NAME = list(self.__tables[table])[1]
        if columns:
            query = f'INSERT INTO {table} ({ID_NAME}, {RELATION_ID_NAME}, {columns}) VALUES (?, ?, {', '.join('?' * len(param))})'
        else:
            query = f'INSERT INTO {table} ({ID_NAME}, {RELATION_ID_NAME}) VALUES (?, ?)'

        try:
            if columns:
                cursor.execute(query, (custom_id, id_) + tuple(value for _, value in param.items()))
            else:
                cursor.execute(query, (custom_id, id_))
            self.__tables_ID[table].append(custom_id)
            connect.commit()
            print('ADDED TO THE TABLE SUCCESSFULLY')
            return custom_id
        except sql.Error as e:
            print(f"SQLite error: {e}")
        finally:
            connect.close()

    def add_row(self, table: str, **param) -> str:
        """
        Add a row in {table}
        """
        connect = sql.connect(self.__database)
        cursor = connect.cursor()

        columns = ', '.join(column for column in param)

        custom_id = create_ID(self.__tables_ID[table])

        ID_NAME = list(self.__tables[table])[0]
        query = f'INSERT INTO {table} ({ID_NAME}, {columns}) VALUES (?, {', '.join('?' * len(param))})'

        try:
            cursor.execute(query, (custom_id,) + tuple(value for _, value in param.items()))
            self.__tables_ID[table].append(custom_id)
            connect.commit()
            print('ADDED TO THE TABLE SUCCESSFULLY')
            return custom_id
        except sql.Error as e:
            print(f"SQLite error: {e}")
        finally:
            connect.close()

def create_ID(ids: list = None) -> str:
    ID_num = str(time.time()).split('.')
    ID = f'{ID_num[0][-2::]}-{ID_num[1][0:5]}-ACSS'

    if ids:
        return f'{ID_num[0][-2::]}-{ID_num[1][0:5]}-ACSS'

    while ID in ids:
        ID = f'{str(time.time()).split('.')[0][-2::]}-{str(time.time()).split('.')[1][0:5]}-ACSS'

    return ID

def create_table(database: str, tblname: str, *args):
    '''
    
    param: database
    '''
    
    connection = sql.connect(database)
    cursor = connection.cursor()

    columns = ', '.join(f'{name} {type_}' for name, type_ in args)

    sql_command = f'CREATE TABLE IF NOT EXISTS {tblname} ({columns})'
    # print(sql_command)
    # print()

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

def update_value(database: str, tblname: str, ID: str, ID_NAME: str = 'ID', **kwargs):
    connection = sql.connect(database)
    cursor = connection.cursor()

    # Generate SQL command
    columns = ', '.join(f'{name} = ?' for name in kwargs)
    sql_command = f'UPDATE {tblname} SET {columns} WHERE {ID_NAME} = ?'

    # Debugging output
    # print("SQL Command:", sql_command)
    # print("Parameters:", tuple(kwargs.values()) + (ID,))

    try:
        cursor.execute(sql_command, tuple(kwargs.values()) + (ID,))
        connection.commit()
        print('UPDATED TABLE SUCCESSFULLY')
    except sql.Error as e:
        print(f"SQLite error: {e}")
    finally:
        connection.close()

def add_value(database: str, tblname: str, **kwargs):
    connection = sql.connect(database)
    cursor = connection.cursor()

    # Prepare SQL command
    columns = ', '.join(f'{name}' for name in kwargs)
    values_placeholder = ', '.join('?' for _ in kwargs)
    sql_command = f'INSERT INTO {tblname} ({columns}) VALUES ({values_placeholder})'

    try:
        cursor.execute(sql_command, tuple(kwargs.values()))
        connection.commit()
        print('ADDED TO THE TABLE SUCCESSFULLY')
    except sql.IntegrityError as e:
        print('Error: Duplicate value detected. Attempting to update.')
        print('IntegrityError occurred:', e)
        if 'UNIQUE constraint failed' in str(e):
            # Extract table and column information from the error message
            parts = str(e).split('UNIQUE constraint failed: ')
            if len(parts) > 1:
                constraint_info = parts[1]
                # print(f'Constraint failed for: {constraint_info}')

                # Extract table and column names
                table_name, column_name = constraint_info.split('.')
                # print(f'Table: {table_name}, Column: {column_name}')

                # Retrieve the duplicate value that caused the error
                value = kwargs[column_name]  # assuming 'data' is a tuple and the value being inserted is the first element
                # Retrieve the ID of the existing record
                cursor.execute(f"SELECT id FROM {table_name} WHERE {column_name} = ?", (value,))
                row = cursor.fetchone()
                if row:
                    connection.close()
                    # print('Existing row with duplicate value:', row)
                    update_value(database, tblname, row[0], **kwargs)
                else:
                    connection.close()
                    # print('no existing row')
        else:
            connection.close()
            print('Error message:', e)

def get_value(database: str, tblname: str, ID: str, ID_NAMING: str = 'ID'):
    connection = sql.connect(database)
    cursor = connection.cursor()

    query = f'SELECT * FROM {tblname} WHERE {ID_NAMING} = ?'
    columns = f'PRAGMA table_info({tblname});'

    try:
        cursor.execute(columns)
        columns = [col[1] for col in cursor.fetchall()]
        cursor.execute(query, (ID,))
        value = cursor.fetchone()
        result = {}
        for i in range(len(columns)):
            # print(columns[i], value[i])
            result[columns[i]] = value[i]

        return result
    except sql.Error as e:
        print(f"SQLite error: {e}")
        return 0
    finally:
        connection.close()

def get_table(database: str, tblname: str, ):
    connection = sql.connect(database)
    cursor = connection.cursor()

    values = f'SELECT * FROM {tblname}'
    columns = f'PRAGMA table_info({tblname});'

    try:
        cursor.execute(values)
        values = cursor.fetchall()
        cursor.execute(columns)
        columns = [col[1] for col in cursor.fetchall()]

        result = {}
        for i in range(len(values)):
            result[values[i][0]] = {}
            for j in range(len(values[i])):
                if values[i][j]:
                    result[values[i][0]][columns[j]] = values[i][j]

        return result
    except sql.Error as e:
        print(f"SQLite error: {e}")
        return 0
    finally:
        connection.close()

def filter_by(database: str, tblname: str, filter_value):
    connection = sql.connect(database)
    cursor = connection.cursor()

    # Query to select all rows from the table
    values_query = f'SELECT * FROM {tblname}'

    # Query to get column information
    columns_query = f'PRAGMA table_info({tblname});'

    try:
        # Step 1: Get all values (rows) from the table
        cursor.execute(values_query)
        values = cursor.fetchall()

        # Step 2: Get the column names from the table
        cursor.execute(columns_query)
        columns = [col[1] for col in cursor.fetchall()]

        # Step 3: Filter across all columns for the filter_value
        result = {}
        for i in range(len(values)):
            row_id = values[i][0]  # Assuming the first column is a unique identifier
            result[row_id] = {}

            # Check each column value in the row for the filter_value
            for j in range(len(values[i])):
                if not values[i][j]:
                    continue
                if filter_value.lower() == 'all':
                    result[row_id][columns[j]] = values[i][j]
                elif (filter_value.lower() in str(values[i][j]).lower() or
                      columns[j].lower() == filter_value.lower()):
                    result[row_id][columns[j]] = values[i][j]

            # Remove the row from the result if no columns match the filter
            if not result[row_id]:
                result.pop(row_id)

        return result
    except sql.Error as e:
        print(f"SQLite error: {e}")
        return 0
    finally:
        connection.close()

def filter_by_column(database: str, tblname: str, column: str, select: str):
    connection = sql.connect(database)
    cursor = connection.cursor()

    if select.lower() == 'all':
        query = f'SELECT * FROM {tblname} WHERE {column} = ?'
    else:
        query = f'SELECT * FROM {tblname} WHERE {column} LIKE ?'

    try:
        if select.lower() == 'all':
            cursor.execute(query, (f'%{select}',))
        else:
            cursor.execute(query)
        values = cursor.fetchall()

        result = {}
        cursor.execute(f'PRAGMA table_info({tblname});')
        columns = [col[1] for col in cursor.fetchall()]
        for i in range(len(values)):
            result[i+1] = {}
            for j in range(len(columns)):
                if values[i][j]:
                    result[i+1][columns[j]] = values[i][j]

        return result
    except sql.Error as e:
        print(f"SQLite error: {e}")
        return 0
    except Exception as e:
        print(f'Some other error: {e}')
    finally:
        connection.close()

def get_ID(database: str, tblname: str, **conditions):
    connection = sql.connect(database)
    cursor = connection.cursor()

    columns = ' AND '.join(f'{col} = ?' for col in conditions)
    query = f'SELECT id FROM {tblname} WHERE {columns}'

    try:
        cursor.execute(query, tuple(conditions.values()))
        # print(query)
        # print(tuple(conditions.values()))
        result = cursor.fetchone()
        return result[0] if result else None
    except sql.Error as e:
        print(f"SQLite error: {e}")
        return None
    finally:
        connection.close()

def get_rows(database: str, tblname: str):
    connection = sql.connect(database)
    cursor = connection.cursor()

    value = f'SELECT id FROM {tblname}'

    try:
        cursor.execute(value)
        result = cursor.fetchall()
        return result
    except sql.Error as e:
        print(f"SQLite error: {e}")
        return 0
    finally:
        connection.close()

def print_table(database: str, tblname: str):

    connection = sql.connect(database)
    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM {tblname}')

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()

if __name__ == '__main__':

    # update_value('member.db', 'PERSONAL_INFORMATION', '1', 'ID', Last_Name = 'k')
    # add_value('member.db', 'PERSONAL_INFORMATION', Last_Name = 'D')

    del_table('member.db', 'PERSONAL_INFORMATION')
    del_table('member.db', 'QUESTIONS')
    del_table('member.db', 'SPECIALIZATION')
    create_table('member.db', 'PERSONAL_INFORMATION',
                 ('ID', 'INTEGER PRIMARY KEY AUTOINCREMENT'), ('Last_Name', 'TEXT NOT NULL'),
                 ('Middle_Name', 'TEXT'), ('First_Name', 'TEXT NOT NULL'), ('Facebook_Account', 'TEXT'),
                 ('Birth_Date', 'TEXT NOT NULL'), ('Age', 'INTEGER NOT NULL'), ('Sex', 'TEXT'), ('Phone_Number', 'TEXT NOT NULL'),
                 ('ID_Number', 'TEXT UNIQUE'), ('Admission_Score', 'INTEGER'), ('Email_Address', 'TEXT'), ('Standing', 'TEXT'))
    create_table('member.db', 'QUESTIONS',
                 ('ID', 'INTEGER PRIMARY KEY AUTOINCREMENT'), ('PI_ID', 'INTEGER NOT NULL UNIQUE'), ('Q1', 'TEXT'), ('A1', 'TEXT'), ('Q2', 'TEXT'),
                 ('A2', 'TEXT'), ('Q3', 'TEXT'), ('A3', 'INTEGER'), ('Q4', 'TEXT'), ('A4', 'TEXT'), ('Q5', 'TEXT'), ('A5', 'TEXT'))
    create_table('member.db', 'SPECIALIZATION',
                 ('ID', 'INTEGER PRIMARY KEY AUTOINCREMENT'), ('PI_ID', 'INTEGER NOT NULL UNIQUE'), ('DANCE', 'TEXT'),
                 ('SPORT', 'TEXT'), ('MULTIMEDIA', 'TEXT'), ('LITERARY', 'TEXT'), ('ATHLETICS', 'TEXT'),
                 ('MUSIC', 'TEXT'), ('VISUAL_ARTS', 'TEXT'), ('PROGRAMMING_LANGUAGE', 'TEXT'), ('OTHERS', 'TEXT'))
