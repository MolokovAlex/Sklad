# autor: MolokovAlex
# lisence: GPL
# coding: utf-8
# version 0.0.2 - создаю класс Component и генератор уникального номера
# version 0.0.3 - функции создания резрвного файла
# version 0.0.4 - функции импорта/экспорта в pickle файл
# version 0.0.5 - переброска части функций и классов в модули и функции импорта/экспорта файл XLSX
# version 0.1.0 - слияние графических примитиввных окон и backend-ом обработки файла БД
#
#  Редактирование компонента:
# - раюотают все кнопки на дереве компоынентов 
# - работают кнопки на дереве Групп : Удалить, Переименовать
# ОК - в кнопке Добавить подумать над указанием lvl03, lvl04  и т.п.
# OK - перейти на pd.concat вместо append
# ОК- сделать кнопку Переместить в дереве Групп
#  - сделать рефакторинг кода, добавить комментарии
# OK - сделать сохранение DatFrame в файл Pickle и при запуске программы загружать DataFrame из этого файла
# - добавить "умную процедуру импорта"

# надо: 
# ОК- делать копию того файла который открываем и открывать копию, при закрытии файла - обратная замена. Те.в папке будут два файла - исходный и измененный
# - считывать файл Иксель
# - сохранять и считывать в собственном фомате в файл
# ОК- генерировать уникальный номер компонента в зависимости от даты, времени до милисекунды
#  - сделать защиту от дурака при импорте файлов в БД
# - проверить при запуске программы существует ли файл БД? елси нет - оповесить пользователя что его нет и будет создан пустой
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # сделать защиту от дурака:
    # - появление в таблицах или БД одинаковых наименований и одинаковых кодов


import os.path as ospath

import sqlite3 as sql3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Menu
import tkinter.messagebox as mb
import modulAppGUI as mag
import skladConfig as scfg
import moduleDBClass as mdbc
import moduleImport as mi
import moduleExport as me
import moduleSQLite as msql
import pandas as pd
import numpy as np







# глобальные переменные
DBComponent = []
DBUnits =[]

flag_createDBbackup = False # флаг результата создания резервной БД
flag_CreateTableDB = False  # флаг создания/обновления таблицы в памяти
flag_copyTableInMemory = False      # флаг копирования таблицы из файла в память



sql_create_tableDBGroupComponent = """ CREATE TABLE IF NOT EXISTS DBGroupComponent (
        id_code_group INTEGER PRIMARY KEY,
        name_group TEXT);
        """
sql_create_tableDBComponent = """ CREATE TABLE IF NOT EXISTS DBComponent (
        id_code_component INTEGER PRIMARY KEY,
        name_component TEXT, 
        code_group0 INTEGER, 
        code_group1 INTEGER,
        code_group2 INTEGER,
        code_group3 INTEGER,
        code_group4 INTEGER,
        code_group5 INTEGER,
        amount INTEGER,
        min_rezerve INTEGER,
        code_units INTEGER, 
        articul TEXT
        );
        """
sql_create_tableDBUnits = """ CREATE TABLE IF NOT EXISTS DBUnits (
        id_code_units INTEGER PRIMARY KEY,
        name_units TEXT );
        """
    
sql_delete_data_in_tableDBGroupComponent = 'DELETE FROM DBGroupComponent WHERE code_group > 0;'


def main():
    # создаем графический оконный интерфейс
    app = mag.App()
    app.title("Программа ведения склада")

    # проверка наличия файла БД SQLite
    if msql.CheckExistDBFile (scfg.DBSqlite):
        # функция резервного создания файла БД
        flag_create_back_DBF = msql.createBackUpDBFile (scfg.DBSqlite_backup, scfg.DBSqlite)
        if flag_create_back_DBF:
            # загрузим DataFrame БД склада компоненов из файла
            if ospath.isfile(scfg.nameFile_DBC_pickle):
                mi.Load_DataFrameDBC_From_PickleFile() 
                print('Файл БД склада компоненов pickle найден')
            else:
                print('Файл БД склада компоненов pickle НЕнайден !!!!!!!!!!!!!!!!!!!!!!')
                # new_row = {'name':'Sklad', 'id_code_lvl': 'lvl00', 'id_code_item': '0', 'id_code_parent':'0', 'amount':0} #append row to the dataframe 
                # scfg.df1 = pd.DataFrame(new_row , index=[0])
                a=scfg.demo_DBС_1
                scfg.df_DBC = pd.DataFrame(data=scfg.demo_DBС_1)


            # загрузим DataFrame БД спецификаций из файла
            if ospath.isfile(scfg.nameFile_DBS_pickle):
                mi.Load_DataFrameDBS_From_PickleFile() 
                print('Файл БД спецификаций pickle найден')
            else:
                print('Файл БД спецификаций pickle НЕнайден !!!!!!!!!!!!!!!!!!!!!!')
                 # заполним демо-данными
                scfg.df_DBS = pd.DataFrame(data=scfg.demo_DBS_1)
                df22 = pd.DataFrame(data=scfg.demo_DBS_2)
                scfg.df_DBS = pd.concat([scfg.df_DBS, df22])
                #  переиндексируем DataFrame
                scfg.df_DBS = scfg.df_DBS.reset_index(drop=True)

            # загрузим DataFrame БД приходов из файла
            if ospath.isfile(scfg.nameFile_DBI_pickle):
                mi.Load_DataFrameDBI_From_PickleFile() 
                print('Файл БД приходов pickle найден')
            else:
                print('Файл БД приходов pickle НЕнайден !!!!!!!!!!!!!!!!!!!!!!')
                # заполним демо-данными
                scfg.df_DBI = pd.DataFrame(data=scfg.demo_DBI_1) 



            # загрузим DataFrame БД расходов из файла
            if ospath.isfile(scfg.nameFile_DBE_pickle):
                mi.Load_DataFrameDBE_From_PickleFile() 
                print('Файл БД расходов pickle найден')
            else:
                print('Файл БД расходов pickle НЕнайден !!!!!!!!!!!!!!!!!!!!!!')
                # заполним демо-данными
                scfg.df_DBE = pd.DataFrame(data=scfg.demo_DBE_1)   

            # загрузим DataFrame БД ед измерения из файла
            if ospath.isfile(scfg.nameFile_DBCU_pickle):
                mi.Load_DataFrameDBCU_From_PickleFile() 
                print('Файл БД ед измерения pickle найден')
            else:
                print('Файл БД ед измерения pickle НЕнайден !!!!!!!!!!!!!!!!!!!!!!')
                # заполним демо-данными
                scfg.df_DBCU = pd.DataFrame(data=scfg.demo_DBCU_1)  
            # a = scfg.df_DBCU 

            app.createMainMenu()            # теперь можно работать дальше - создаем главное меню

    app.mainloop()

    return None


if __name__ == "__main__":
    main()
    


