# moduleSQLite
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# модуль держатель функций работы с SQLite

from sys import getsizeof
import sqlite3 as sqlite
import moduleDBClass as mdbc




def progress(status, remaining, total):
    print(f'Скопировано {total-remaining} из {total}...')
    return None

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
        connectionDBFile = sqlite.connect(nameFile_DBf)
        backup_connection = sqlite.connect(nameBackUpDBFile)
        with backup_connection, connectionDBFile:
            connectionDBFile.backup(backup_connection, pages=3, progress=progress)
            Flag_createBackDBF = True
        print("Резервное копирование выполнено успешно")
    except sqlite.Error as error:
        print("Ошибка при резервном копировании: ", error)
        Flag_createBackDBF = False
    finally:
        if(backup_connection):
            backup_connection.close()
            connectionDBFile.close()
    return Flag_createBackDBF

def createTableDBFile(nameFile_DBf, sql_request_create_tableDBGroup, 
                        sql_request_create_tableDBComponent, 
                        sql_request_create_tableDBUnits):
    """
    создадим таблицы компонентов, групп, едИзмерений
    """
    FlagCreateTableDBf = False
    try:
        connectionDBFile = sqlite.connect(nameFile_DBf)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile:
            cursorDB.execute(sql_request_create_tableDBGroup)
            connectionDBFile.commit()
            cursorDB.execute(sql_request_create_tableDBComponent)
            connectionDBFile.commit()
            cursorDB.execute(sql_request_create_tableDBUnits)
            connectionDBFile.commit()
            FlagCreateTableDBf = True
    except sqlite.Error as error:
        print("Ошибка при создании таблиц в БД: ", error)
        FlagCreateTableDBf = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
    return FlagCreateTableDBf


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
        connectionDBFile = sqlite.connect(nameFile_DBf)
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
        
    except sqlite.Error as error:
        print("Ошибка копировании таблиц в список БД: ", error)
        flag_copyTable = False
    finally:
        if(connectionDBFile):
                connectionDBFile.close()
    print (f'в функции copy_File_SQLDBGroupComponent_In_ListDBGroup размер DBGroupf = {getsizeof( DBGroupf)} бит')
    return DBGroupf, flag_copyTable, flag_empty_Table
