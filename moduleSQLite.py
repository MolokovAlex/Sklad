# moduleSQLite
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# модуль держатель функций работы с SQLite


from sys import getsizeof
import sqlite3 as sql3
import traceback
import sys
import moduleDBClass as mdbc
import skladConfig as scfg

# --------------- БД склада DBGroupComponent --------------------------
# сделать список смежности
sql_create_table_DBG = """ CREATE TABLE IF NOT EXISTS DBG (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL CHECK(name !=''),
        id_parent INTEGER
        );
        """

# --------------- БД склада компонентов --------------------------
sql_create_table_DBC = """ CREATE TABLE IF NOT EXISTS DBC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL CHECK(name !=''), 
        amount INTEGER NOT NULL DEFAULT 0 CHECK(amount >= 0), 
        id_unit INTEGER,
        min_rezerve INTEGER NOT NULL DEFAULT 0 CHECK(amount >= 0),
        articul_1C TEXT,
        code_1C TEXT,
        name_1C TEXT,
        id_parent INTEGER,
        id_lvl INTEGER,
        FOREIGN KEY (id_unit)  REFERENCES DBU (id) ON DELETE RESTRICT
        );
        """



sql_create_table_DBU = """ CREATE TABLE IF NOT EXISTS DBU (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL CHECK(name !='')
        );
        """

# --------------- БД прихода компонентов (income) -------------
sql_create_table_DBI = """ CREATE TABLE IF NOT EXISTS DBI (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL CHECK(date !=''),
        id_component INTEGER NOT NULL, 
        amount INTEGER NOT NULL CHECK(amount > 0), 
        comments TEXT,
        FOREIGN KEY (id_component)  REFERENCES DBC (id) ON DELETE RESTRICT
        );
        """
# --------------- БД расхода компонентов (expenditure) -------------
sql_create_table_DBE = """ CREATE TABLE IF NOT EXISTS DBE (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL CHECK(date !=''),
        id_component INTEGER NOT NULL, 
        amount INTEGER NOT NULL CHECK(amount > 0), 
        comments TEXT,
        FOREIGN KEY (id_component)  REFERENCES DBC (id) ON DELETE RESTRICT
        );
        """

sql_create_table_DBS = """ CREATE TABLE IF NOT EXISTS DBS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_component INTEGER NOT NULL, 
        amount INTEGER NOT NULL DEFAULT 0 CHECK(amount > 0), 
        id_parent INTEGER,
        id_lvl INTEGER,
        comments TEXT,
        FOREIGN KEY (id_component)  REFERENCES DBC (id) ON DELETE RESTRICT
        );
        """


sql_delete_data_in_tableDBGroupComponent = 'DELETE FROM DBGroupComponent WHERE code_group > 0;'



def progress(status, remaining, total):
    print(f'Скопировано {total-remaining} из {total}...')
    return None

def viewCodeError (sql_error):
    print("Ошибка при работе с sqlite", sql_error)
    print("Класс исключения: ", sql_error.__class__)
    print("Исключение", sql_error.args)
    print("Печать подробноcтей исключения SQLite: ")
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))


def CheckExistDBFile ():
    """ функция проверки файла БД
        Вход:
        nameFile_DBf - наименование файла резерной БД
        Выход:
        - Flag_checkDBF - флаг результата проверки БД
    """ 
    nameFile_DBf = scfg.DBSqlite
    Flag_checkDBF = False
    try:
        sqlite_connection = sql3.connect(nameFile_DBf)
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")
        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)
        cursor.close()
        Flag_checkDBF = True

    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        Flag_checkDBF = False

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return Flag_checkDBF


def createBackUpDBFile (nameBackUpDBFile: str, nameFile_DBf: str):
    """ функция резервного создания файла БД
        Вход:
        nameBackUpDBFile - наименование файла резерной БД
        Выход:
        - созданный файл резервной БД
        - Flag_createBackDBF - флаг результата создания резервной БД
    """    
    Flag_createBackDBF = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        backup_connection = sql3.connect(nameBackUpDBFile)
        with backup_connection, connectionDBFile:
            connectionDBFile.backup(backup_connection, pages=3, progress=progress)
            Flag_createBackDBF = True
        print("Резервное копирование выполнено успешно")
    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        Flag_createBackDBF = False
    finally:
        if(backup_connection):
            backup_connection.close()
            connectionDBFile.close()
    return Flag_createBackDBF



def createTableDBFile():
    """
    создадим таблицы компонентов, групп, едИзмерений
    """
    nameFile_DBf = scfg.DBSqlite
    FlagCreateTableDBf = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile:
            cursorDB.execute(sql_create_table_DBG)
            connectionDBFile.commit()
            cursorDB.execute(sql_create_table_DBC)
            connectionDBFile.commit()
            cursorDB.execute(sql_create_table_DBU)
            connectionDBFile.commit()
            cursorDB.execute(sql_create_table_DBI)
            connectionDBFile.commit()
            cursorDB.execute(sql_create_table_DBE)
            connectionDBFile.commit()
            cursorDB.execute(sql_create_table_DBS)
            connectionDBFile.commit()
            FlagCreateTableDBf = True
    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        FlagCreateTableDBf = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
    # if FlagCreateTableDBf : 
    #     fill_TableDBG_defaul_value()
    #     fill_TableDBU_defaul_value()
    #     fill_TableDBC_defaul_value()
    #     fill_TableDBI_defaul_value()
    #     fill_TableDBE_defaul_value()
    return FlagCreateTableDBf



def fill_TableDBG_defaul_value():
    """
    заполнение таблицы DBG значениями по умолчанию
    """
    nameFile_DBf = scfg.DBSqlite
    insert_data_query = """INSERT INTO DBG 
                            (name, id_parent) 
                        VALUES 
                            (?,?);"""
    
    Flag_fill_TableDBG_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            cursorDB.executemany(insert_data_query, scfg.data_list_default_DBG)
            connectionDBFile.commit()
            Flag_fill_TableDBG_defaul_value = True

    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        Flag_fill_TableDBG_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
    return Flag_fill_TableDBG_defaul_value


def fill_TableDBU_defaul_value():
    """
    заполнение таблицы DBU значениями по умолчанию
    """
    nameFile_DBf = scfg.DBSqlite
    insert_data_query = """INSERT INTO DBU (name) VALUES (?);"""
    
    Flag_fill_TableDBU_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            # for item in data_list:
            #     cursorDB.execute(insert_data_query, item)
            #     connectionDBFile.commit()
            cursorDB.executemany(insert_data_query, scfg.data_list_default_DBU)
            connectionDBFile.commit()
            Flag_fill_TableDBU_defaul_value = True

    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        Flag_fill_TableDBU_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
    return Flag_fill_TableDBU_defaul_value


def fill_TableDBC_defaul_value():
    """
    заполнение таблицы DBC значениями по умолчанию
    """
    nameFile_DBf = scfg.DBSqlite
    insert_data_query = """INSERT INTO DBC (name, amount, id_unit, min_rezerve, articul_1C, code_1C, name_1C, id_parent, id_lvl) VALUES (?,?,?, ?,?,?, ?,?,?);"""

    
    Flag_fill_TableDBC_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            cursorDB.executemany(insert_data_query, scfg.data_list_default_DBC)
            connectionDBFile.commit()
            Flag_fill_TableDBC_defaul_value = True

    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        Flag_fill_TableDBC_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
    return Flag_fill_TableDBC_defaul_value


def fill_TableDBI_defaul_value():
    """
    заполнение таблицы DBI значениями по умолчанию
    """
    nameFile_DBf = scfg.DBSqlite
    insert_data_query = """INSERT INTO DBI (date, id_component, amount, comments) VALUES (?,?,?,?);"""
    
    Flag_fill_TableDBI_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            cursorDB.executemany(insert_data_query, scfg.data_list_default_DBI)
            connectionDBFile.commit()
            Flag_fill_TableDBI_defaul_value = True

    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        Flag_fill_TableDBI_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
    return Flag_fill_TableDBI_defaul_value

def fill_TableDBE_defaul_value():
    """
    заполнение таблицы DBI значениями по умолчанию
    """
    nameFile_DBf = scfg.DBSqlite
    insert_data_query = """INSERT INTO DBE (date, id_component, amount, comments) VALUES (?,?,?,?);"""

    Flag_fill_TableDBE_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            cursorDB.executemany(insert_data_query, scfg.data_list_default_DBE)
            connectionDBFile.commit()
            Flag_fill_TableDBE_defaul_value = True

    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        Flag_fill_TableDBI_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
    return Flag_fill_TableDBE_defaul_value

def query_name_from_DBU_where_id():
    # if database == 'DBC':   dataFrame_in = scfg.df_DBCU
    nameFile_DBf = scfg.DBSqlite
    query_data = """SELECT name FROM DBU WHERE id=?;"""
    # Flag_fill_TableDBU_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            # for item in data_list:
            cursorDB.execute(query_data, (scfg.id_default_DBU,))
            one_result = cursorDB.fetchone()
            print(one_result)
            # connectionDBFile.commit()
            # Flag_fill_TableDBU_defaul_value = True

    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        # Flag_fill_TableDBU_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()

    return one_result

def query_all_name_from_DBU():
    # if database == 'DBC':   dataFrame_in = scfg.df_DBCU
    nameFile_DBf = scfg.DBSqlite
    query_data = """SELECT name FROM DBU;"""
    # Flag_fill_TableDBU_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            # for item in data_list:
            cursorDB.execute(query_data)
            one_result = cursorDB.fetchall()
            print(one_result)
            # connectionDBFile.commit()
            # Flag_fill_TableDBU_defaul_value = True

    except sql3.Error as error_sql:
        viewCodeError (error_sql)
        # Flag_fill_TableDBU_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()

    return one_result

def copy_File_SQLDBGroupComponent_In_memory(nameFile_DBf):
    """
    считаем строки из таблицы БД_SQL DBGroupComponent (файл) и положим их в список DBGroup (память)
    Вход:
    nameFile_DBf - наименование файла SQL содержащего DBGroupComponent
    ВЫход:
    DBGroupf - список на базе  GRoup 
    flag_copyTable - флаг успешного/неуспешного копирования в память
    flag_empty_Table - флаг обнаружения пустой таблицы
    """
    DBGroupf = []
    # codegroup = []
    # namegroup = []
    # name_item = ''
    flag_copyTable = False
    flag_empty_Table = False
    try:
        connectionDBFile = sql3.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile:
            #  Надо ппроверить есть ли в таблице данные вообще, иначе будет оибка при SQL запросе на пустую таблицу!!!!!!
            p = cursorDB.execute("SELECT * FROM DBGroupComponent")  # WHERE code_group0 = 01")                                    # Empty 
            if p.fetchone() != None:
                p = cursorDB.execute("SELECT * FROM DBGroupComponent")  # WHERE code_group0 = 01")
                for row in p:
                    # codegroup_item = []
                    # namegroup = []
                    # codegroup_item.append(list(row)[0])           # id_code_group INTEGER PRIMARY KEY  
                    # codegroup_item.append(list(row)[1])     
                    # codegroup_item.append(list(row)[2])
                    # codegroup_item.append(list(row)[3])
                    # codegroup_item.append(list(row)[4])
                    # codegroup_item.append(list(row)[5])     # codegroup[4]
                    # codegroup_item.append(list(row)[6])     # codegroup[5]
                    # namegroup.append(list(row)[1])          # name_group TEXT
                    item_dbgoup = mdbc.Group(list(row)[0], list(row)[1])
                    DBGroupf.append(item_dbgoup)   
                    #print(codegroup, namegroup)
                    flag_copyTable = True
            else:
                print ("Ошибка - БД SQL  пуста")
                flag_copyTable = False
                flag_empty_Table = True
        
    except sql3.Error as error:
        print("Ошибка копировании таблиц в список БД: ", error)
        flag_copyTable = False
    finally:
        if(connectionDBFile):
                connectionDBFile.close()
    print (f'в функции copy_File_SQLDBGroupComponent_In_ListDBGroup размер DBGroupf = {getsizeof( DBGroupf)} бит')
    return DBGroupf, flag_copyTable, flag_empty_Table
