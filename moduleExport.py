# moduleExport
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# модуль держатель элементов GUI для функций экспорта

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, N, NSEW, Menu
import tkinter.messagebox as mb
import sqlite3 as sqlite
import pandas as pd
import numpy as np


import modulAppGUI as mag
import skladConfig as scfg
import moduleDBClass as mdbc
import moduleSQLite as msql



class WindowExport(tk.Toplevel):
    def __init__(self, parent):    
        # визуальное отображение универсального окна дерева групп для БД компонентов или БД спецификаций :
        # viewDB = DBC = DataBaseComponents
        # viewDB = DBS = DataBaseSpecification
        # режим работы окна - или "перемещнние " или "импорт"
        # modeWindow = 'remove'
        # modeWindow == 'import
        # modeWindow = 'expenditure'  - режим окна Расход компонента
                                                                        
        super().__init__(parent)
        # self.geometry("1024x600")
        opts = { 'ipadx': 3, 'ipady': 3 , 'sticky': 'nswe' }

        self.label_to = tk.Label(self, text="Выберите объект/объекты для экспорта ")    
        self.label_to.grid(row=0, column=0, **opts)

        self.frame_CB = tk.LabelFrame(master=self, text="Группы", relief=tk.SUNKEN, borderwidth=3)   #, height=50)
        self.frame_CB.grid(row=1, column=0, columnspan=2, **opts)
        self.ExpDBC = tk.BooleanVar()
        self.ExpDBS = tk.BooleanVar()
        self.ExpDBE = tk.BooleanVar()
        self.ExpDBCU = tk.BooleanVar()
        self.cbExpDBC = tk.Checkbutton(master=self.frame_CB, text="БД компонентов", onvalue= True, offvalue=False, variable=self.ExpDBC)#, command=self.exportDB)
        self.cbExpDBS = tk.Checkbutton(master=self.frame_CB, text="БД спецификаций", onvalue= True, offvalue=False, variable=self.ExpDBS)#, command=self.exportDB)
        self.cbExpDBE = tk.Checkbutton(master=self.frame_CB, text="БД расхода", onvalue= True, offvalue=False, variable=self.ExpDBE)#, command=self.exportDB)
        self.cbExpDBCU = tk.Checkbutton(master=self.frame_CB, text="БД ед изм", onvalue= True, offvalue=False, variable=self.ExpDBCU)#, command=self.exportDB)
        self.cbExpDBC.grid(row=0, column=0, columnspan=2, **opts)
        self.cbExpDBS.grid(row=1, column=0, columnspan=2, **opts)
        self.cbExpDBE.grid(row=2, column=0, columnspan=2, **opts)
        self.cbExpDBCU.grid(row=3, column=0, columnspan=2, **opts)

        self.btn_Remove = tk.Button(master=self, height=3, text="Пуск ракет на Америку", command=self.exportDB)
        self.btn_Remove.grid(row=2, column=0, **opts)
        self.btn_Cansel = tk.Button(master=self, height=3, text="Отмена", command=self.destroy)
        self.btn_Cansel.grid(row=2, column=1, **opts)

        return None

    # def open(self):
    #     self.grab_set()
    #     self.wait_window()
    #     usr = self.new_parent
    #     return usr
    
    # def fn_removComponent(self):
    #     self.new_parent = self.sel[0]
    #     self.destroy()
    #     return None

    # def on_select(self, event):
    #     self.sel = self.treeGroup.selection()

def exportDB():

        # if self.ExpDBC:
        #     Save_DataFrame_in_PickleFile(df=scfg.df1, namefile=scfg.nameFile_exportDBC_pickle)
        #     Save_DataFrame_in_ExcelFile(df=scfg.df1, namefile=scfg.nameFile_exportDBC_excel)
        # if self.ExpDBS:
        #     Save_DataFrame_in_PickleFile(df=scfg.df_DB_Specification, namefile=scfg.nameFile_exportDBS_pickle)
        #     Save_DataFrame_in_ExcelFile(df=scfg.df_DB_Specification, namefile=scfg.nameFile_exportDBS_excel)
        # if self.ExpDBE:
        #     Save_DataFrame_in_PickleFile(df=scfg.df_DBE, namefile=scfg.nameFile_exportDBE_pickle)
        #     Save_DataFrame_in_ExcelFile(df=scfg.df_DBE, namefile=scfg.nameFile_exportDBE_excel)
        # if self.ExpDBCU:
        #     Save_DataFrame_in_PickleFile(df=scfg.df_DBCU, namefile=scfg.nameFile_exportDBCU_pickle)
        #     Save_DataFrame_in_ExcelFile(df=scfg.df_DBCU, namefile=scfg.nameFile_exportDBCU_excel)
        pd.to_pickle(scfg.df_DBC, scfg.nameFile_exportDBC_pickle)
        # scfg.df1.to_excel(scfg.nameFile_DB_export_excel, sheet_name='DBC')

        pd.to_pickle(scfg.df_DBS, scfg.nameFile_exportDBS_pickle)
        # scfg.df_DB_Specification.to_excel(scfg.nameFile_DB_export_excel, sheet_name='DBS')

        pd.to_pickle(scfg.df_DBI, scfg.nameFile_exportDBI_pickle)
        # scfg.df_DBI.to_excel(scfg.nameFile_DB_export_excel, sheet_name='DBI')

        pd.to_pickle(scfg.df_DBE, scfg.nameFile_exportDBE_pickle)
        # scfg.df_DBE.to_excel(scfg.nameFile_DB_export_excel, sheet_name='DBE')

        pd.to_pickle(scfg.df_DBCU, scfg.nameFile_exportDBCU_pickle)
        # scfg.df_DBCU.to_excel(scfg.nameFile_DB_export_excel, sheet_name='DBCU')

        with pd.ExcelWriter(scfg.nameFile_DB_export_excel) as writer:  
            scfg.df_DBC.to_excel(writer, sheet_name='DBC')
            scfg.df_DBS.to_excel(writer, sheet_name='DBS')
            scfg.df_DBI.to_excel(writer, sheet_name='DBI')
            scfg.df_DBE.to_excel(writer, sheet_name='DBE')
            scfg.df_DBCU.to_excel(writer, sheet_name='DBCU')

        # установка в эскпортом файле ширины столбцов примерно равным длины текста в ячейках
        wb = openpyxl.load_workbook(scfg.nameFile_DB_export_excel)
        ws = wb['DBC']
        width_col(wb['DBC'])
        width_col(wb['DBS'])
        width_col(wb['DBI'])
        width_col(wb['DBE'])
        width_col(wb['DBCU'])
        # пишем электронную таблицу в 
        # файл
        wb.save(scfg.nameFile_DB_export_excel)


        # self.destroy()
        return None

def width_col(worksheet):
# установка в файле ширины столбцов примерно равным длины текста в ячейках
    
    # размер шрифта документа
    font_size = 11
    # словарь с размерами столбцов
    cols_dict = {}

    # проходимся по всем строкам документа
    for row in worksheet.rows:
        # теперь по ячейкам каждой строки
        for cell in row:
            # получаем букву текущего столбца
            letter = cell.column_letter
            # если в ячейке записаны данные
            if cell.value:
                # устанавливаем в ячейке размер шрифта 
                cell.font = Font(name='Calibri', size=font_size)
                # вычисляем количество символов, записанных в ячейку
                len_cell = len(str(cell.value))
                # длинна колонки по умолчанию, если буква 
                # текущего столбца отсутствует в словаре `cols_dict`
                len_cell_dict = 0
                # смотрим в словарь c длинами столбцов
                if letter in cols_dict:
                    # если в словаре есть буква текущего столбца 
                    # то извлекаем соответствующую длину
                    len_cell_dict = cols_dict[letter]

                # если текущая длина данных в ячейке 
                #  больше чем длинна из словаря
                if len_cell > len_cell_dict:
                    # записываем новое значение ширины этого столбца
                    cols_dict[letter] = len_cell
                    ###!!! ПРОБЛЕМА АВТОМАТИЧЕСКОЙ ПОДГОНКИ !!!###
                    ###!!! расчет новой ширины колонки (здесь надо подгонять) !!!###
                    new_width_col = len_cell * font_size**(font_size*0.015)
                    # применение новой ширины столбца
                    worksheet.column_dimensions[cell.column_letter].width = new_width_col

    



    return None


# def Save_DataFrame_in_PickleFile(df: pd.DataFrame, namefile):
def Save_DataFrame_in_PickleFile():
    """
    функция записи в файл Pickle базы DataFrame
    Вход:
    None
    Выход:
    None
    """
    # pd.to_pickle(df, namefile)
    scfg.df_DBC.to_pickle(scfg.nameFile_DBC_pickle)
    scfg.df_DBS.to_pickle(scfg.nameFile_DBS_pickle)
    scfg.df_DBI.to_pickle(scfg.nameFile_DBI_pickle)
    scfg.df_DBE.to_pickle(scfg.nameFile_DBE_pickle)
    scfg.df_DBCU.to_pickle(scfg.nameFile_DBCU_pickle)

    return None

def Save_DataFrame_in_ExcelFile(df: pd.DataFrame, namefile):
    """
    функция записи в файл Excel базы DataFrame
    Вход:
    None
    Выход:
    None
    """
    # сохраняем изменненный DataFame в Иксель
    df.to_excel(namefile)
    return None