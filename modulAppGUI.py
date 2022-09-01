# module
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8
# from sys import getsizeof
import os
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, N, NSEW, Menu
import tkinter.messagebox as mb
import sqlite3 as sqlite
import pandas as pd
import numpy as np
import sqlite3 as sql3

import moduleDBClass as mdbc
import moduleImport as mi
import skladConfig as scfg
import moduleSQLite as msql

import modulеIncomeExpenditureGUI as mieGUI
import modulеEditGUI as meGUI
import moduleExport as me
# import moduleSpecification as ms


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)
        self.widthscreen = self.winfo_screenwidth()#-30    # размеры экрана
        self.heigthscreen = 640 #window.winfo_screenheight()-30
        self.geometry('{}x{}+5+5'.format(self.widthscreen, self.heigthscreen))

        self.frame_Logger = tk.LabelFrame(master=self, text="Log", relief=tk.SUNKEN, borderwidth=3, height=20)
        self.frame_Logger.pack(fill=tk.X, side=tk.TOP, ipadx=5, ipady=5, padx=10, pady=5)
        self.scroll_logger_x = tk.Scrollbar(self.frame_Logger, orient=tk.HORIZONTAL)
        self.scroll_logger_y = tk.Scrollbar(self.frame_Logger, orient=tk.VERTICAL)
        self.text_box = tk.Text(master=self.frame_Logger, xscrollcommand=self.scroll_logger_x.set, yscrollcommand=self.scroll_logger_y.set, height= 20)
        self.scroll_logger_x.config(command=self.text_box.xview)
        self.scroll_logger_y.config(command=self.text_box.yview)
        self.text_box.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.scroll_logger_x.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.scroll_logger_y.grid(row=0, column=1) #, sticky=tk.N + tk.S)
        self.frame_Logger.columnconfigure(0, weight=1)
        self.frame_Logger.rowconfigure(0, weight=0)

    def confirm_delete(self):
    #     message = "Вы уверены, что хотите закрыть это окно?"
    #     if mb.askyesno(message=message, parent=self):
        # сохраняем изменненный DataFame в файл перед закрытием основного окна
        # me.Save_DataFrame_in_PickleFile(df=scfg.df1, namefile=scfg.nameFile_DBC_pickle)
        # me.Save_DataFrame_in_ExcelFile(df=scfg.df1, namefile=scfg.nameFile_DBC_excel)
        me.Save_DataFrame_in_PickleFile()
        self.destroy()
        return None        

    def createMainMenu(self):
        self.mainmenu = Menu(self)
        self.config(menu=self.mainmenu)

        self.db_import_menu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label='Импорт из xls', menu=self.db_import_menu)

        self.db_import_menu.add_command(label='Импорт Components', command=lambda modeWind='import', viewWind = 'DBC': self.open_Window_Import_Component(modeWindow = modeWind, viewWindow = viewWind))
        self.db_import_menu.add_command(label='Импорт спецификаций', command=lambda modeWind='import', viewWind = 'DBS': self.open_Window_Import_Component(modeWindow = modeWind, viewWindow = viewWind))

        self.db_export_menu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label='Экспорт в xls', menu=self.db_export_menu)
        self.db_export_menu.add_command(label='Экспорт Components', command=self.open_Window_Export) 
        self.db_export_menu.add_command(label='Экспорт спецификаций', command=self.open_Window_Export)
        
        self.editmenu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label='Правка БД', menu=self.editmenu)
        self.editmenu.add_command(label='Редактирование Components', command=self.open_Window_Edit_Component) 
        self.editmenu.add_command(label='Редактирование спецификаций', command=self.open_Window_Edit_Specification)

        self.arrivalmenu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label='Приход на склад', menu= self.arrivalmenu)
        self.arrivalmenu.add_command(label='Приход', command=self.open_Window_income_Component) 
        self.arrivalmenu.add_command(label='История приходов', command=self.clicked) 

        self.expensemenu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label='Расход из склада', menu= self.expensemenu)
        self.expensemenu.add_command(label='Расход', command=self.open_Window_expenditure_Component) 
        self.expensemenu.add_command(label='История расходов', command=self.clicked)

        self.specmenu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label='Спецификации', menu=self.specmenu)
        self.specmenu.add_command(label='Новая', command=self.clicked) 
        self.specmenu.add_command(label='Редактирование', command=self.clicked)
        self.specmenu.add_command(label='Удаление', command=self.clicked)
        self.specmenu.add_command(label='Проводка спецификации', command=self.clicked)

        self.helpmenu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="Справка", menu=self.helpmenu)
        self.helpmenu.add_command(label="Помощь")
        self.helpmenu.add_command(label="О программе")


        return None

    def open_Window_Export(self):
        """
        открытие окна экспорта        
        """
        we = me.WindowExport(self)
        we.grab_set()                      #  чтобы окно получало все события
        return None


    def open_Window_expenditure_Component(self):
        """
        открытие окна для операции расхода компонента на различные цели        
        """
        # viewDB - отображение в окне БД:
        # 'DBC' = DataBaseComponents
        # 'DBS' = DataBaseSpecification 
        # 'DBE' - DataBaseExpenditure - БД расхода компонентов (expenditure)  
        # modeWindow - внешний вид и расположени кнопок окна в режимах:
        # modeWindow = 'edit'
        # modeWindow = 'comp_in_spec'
        # modeWindow = 'expenditure'  - режим окна Расход компонента
        # modeWindow = 'income'  - режим окна Приход компонента
        we = mieGUI.WindowExpenditure(self, viewDB = 'DBE', modeWindow = 'expenditure')
        we.grab_set()                      #  чтобы окно получало все события
        # self.text_box.insert(tk.END, "open_WindowExpenditure"+"\n")

        return None

    def open_Window_income_Component(self):
        """
        открытие окна для операции расхода компонента на различные цели        
        """
        # viewDB - отображение в окне БД:
        # 'DBC' = DataBaseComponents
        # 'DBS' = DataBaseSpecification 
        # 'DBE' - DataBaseExpenditure - БД расхода компонентов (expenditure)  
        # modeWindow - внешний вид и расположени кнопок окна в режимах:
        # modeWindow = 'edit'
        # modeWindow = 'comp_in_spec'
        # modeWindow = 'expenditure'  - режим окна Расход компонента
        # modeWindow = 'income'  - режим окна Приход компонента
        we = mieGUI.WindowExpenditure(self, viewDB = 'DBI', modeWindow = 'income')
        we.grab_set()                      #  чтобы окно получало все события
        # self.text_box.insert(tk.END, "open_WindowExpenditure"+"\n")

        return None    
    

    def open_Window_Edit_Specification(self):
        # viewWindow = 'DBC' = DataBaseComponents
        # 'DBS' = DataBaseSpecification   
        # modeWindow = 'edit'
        # modeWindow = 'comp_in_spec'
        wec = meGUI.WindowEditComponent(self, modeWindow = 'edit', viewWindow='DBS')
        wec.grab_set()                      #  чтобы окно получало все события
        self.text_box.insert(tk.END, "open_WindowEdit_Specification"+"\n")
        return None

    def open_Window_Edit_Component(self):
        # viewWindow = 'DBC' = DataBaseComponents
        # 'DBS' = DataBaseSpecification   
        # modeWindow = 'edit'
        # modeWindow = 'comp_in_spec'
        wec = meGUI.WindowEditComponent(self, modeWindow = 'edit', viewDB='DBC')
        wec.grab_set()                      #  чтобы окно получало все события
        self.text_box.insert(tk.END, "open_WindowEdit_Component"+"\n")
        return None  

    def open_Window_Import_Component(self, modeWindow, viewWindow):
        """
        сюда приходим из меню 'Импорт Components'
        Функция открытия универсального окна Импрта или Перемещния
        Вход:
        # визуальное отображение окна для БД компонентов или БД спецификаций :
        # viewWindow = DBC = DataBaseComponents
        # viewWindow = DBS = DataBaseSpecification
        # режим работы окна - или "перемещнние " или "импорт"
        # modeWindow = 'remove'
        # modeWindow == 'import
        
        """
        mW = modeWindow
        vW = viewWindow
        wior = mi.Window_Import_OR_Remove(self, modeWindow = mW, viewWindow = vW)
        # wig.grab_set()                      #  чтобы окно получало все события
        self.text_box.insert(tk.END, "open_Window_Import_Group"+"\n")
        return None 
        
    def clicked(self):
        return None


class WindowTree(tk.Toplevel):
    def __init__(self, parent, modeWindow, viewDB):    
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

        if  (viewDB == 'DBS') and (modeWindow == 'expenditure'):
            self.label_to = tk.Label(self, text="В какую спецфикацию переместить ? ")    
        self.label_to.grid(row=0, column=0, **opts)

        self.frame_tableTreeGroup = tk.LabelFrame(master=self, text="Группы", relief=tk.SUNKEN, borderwidth=3)   #, height=50)
        self.frame_tableTreeGroup.grid(row=1, column=0,columnspan=2, **opts)

        if  (viewDB == 'DBS') and (modeWindow == 'expenditure'):
            self.btn_Remove = tk.Button(master=self, height=3, text="Сюда", command=self.fn_removComponent)
        self.btn_Remove.grid(row=2, column=0, **opts)
        self.btn_Cansel = tk.Button(master=self, height=3, text="Отмена", command=self.destroy)
        self.btn_Cansel.grid(row=2, column=1, **opts)

        self.treeGroup = ttk.Treeview(self.frame_tableTreeGroup, show="tree headings", height= 15)#, columns=col) #self.columns)
        self.treeGroup.grid(row=0, column=1, rowspan=4, **opts)

        Setting_TreeView(self.treeGroup, form = 'short')

        self.ysb = ttk.Scrollbar(self.frame_tableTreeGroup, orient=tk.VERTICAL, command=self.treeGroup.yview)
        self.treeGroup.configure(yscroll=self.ysb.set)
        self.ysb.grid(row=0, column=2, rowspan=4, **opts)

        self.treeGroup.bind('<<TreeviewSelect>>', self.on_select)

        self.new_parent = 0
        self.sel = 0
        
        # DBC = DataBaseComponents
        # DBS = DataBaseSpecification
        if viewDB == 'DBC':   
            dataFrame_in = scfg.df_DBC
            if not(dataFrame_in.empty):
                viewTreeGroup(self.treeGroup, dataFrame_in)       # отобразим данные из памяти DataFrame в TreeGroup с родителями

        elif viewDB == 'DBS': 
            dataFrame_in = scfg.df_DBS
            if not(dataFrame_in.empty):
                viewTreeGroupSpec(self.treeGroup, dataFrame_in)       # отобразим данные из памяти DataFrame в TreeGroup с родителями
        return None

    def open(self):
        self.grab_set()
        self.wait_window()
        usr = self.new_parent
        return usr
    
    def fn_removComponent(self):
        self.new_parent = self.sel[0]
        self.destroy()
        return None

    def on_select(self, event):
        self.sel = self.treeGroup.selection()


def Unpack_String_DataFrame(DataFrameTree: pd.DataFrame, index: str):
    """
    Универсальная Распаковка строки таблцицы DataFrama на поля(столбцы), т.е. SerialFrame
    список полей- какие найдутся в DataFrame
    плюс поля:
    'UnitsName' - наименование ед изм - возмем по коду 'id_code_item' из DBCU
    'index'
    # 'PathDistanation' - путь списания компонента в спецификацию - возмем по коду 'id_code_parent' из DBS

    Выход:
    словарь типа {'название поля/столбца': содержимое} 
    
    """
    # будущий результат работы функции - словать типа {'название поля/столбца': содержимое}
    upsdf = {}
    # список названий всех полей/столбцов в DataFrame
    # в pandas
    nameColunms = DataFrameTree.columns.values.tolist()
   

    
    #  для каждого наименования столбца извлекаем содержимое  value и помещаем в выходной словарь
    for itemNameColunm in nameColunms:
        value = DataFrameTree.loc[index, itemNameColunm]
        upsdf[itemNameColunm] = value

        if (itemNameColunm == 'id_code_item') | (itemNameColunm == 'amount'):
            if isinstance(value, str) :
                if (value == ''):    
                    upsdf[itemNameColunm] = '0'
            else:
                if value.empty:
                    upsdf[itemNameColunm] = '0'
    # поле индекса тоже должно быть                
    upsdf['index'] = DataFrameTree.index

    # извлекем наименование ед изм - возмем по коду 'id_code_item' из DBCU
    a = scfg.df_DBCU
    unitsCodeSF = scfg.df_DBCU[scfg.df_DBCU['id_code_item'] == upsdf['id_code_item']]['code_units']
    # если такой компонент ('id_code_item') отсутствет в БД ед изм - проверим это
    if unitsCodeSF.empty: unitsCode = '1699' 
    else : unitsCode = unitsCodeSF.item()
    upsdf['UnitsName'] = scfg.UnitsCodeName[unitsCode]

    # # извлекем путь списания компонента в спецификацию - возмем по коду 'id_code_parent' из DBS
    # if (upsdf['id_code_parent'] !=''):
    #     # self.idCodeDistanation = id_item_group
    #     nameGroup = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_e']==upsdf['id_code_parent']]['name']
    #     ValuePathDistanation= nameGroup.item()
    #     id_code_parent = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_e']==upsdf['id_code_parent']]['id_code_parent']
    #     while (id_code_parent.item() != '10000'):
    #         id_item = id_code_parent.item()
    #         nextNameGroup = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_e']==id_item]['name']
    #         a= nextNameGroup.item()
    #         ValuePathDistanation = a + '/' + ValuePathDistanation
    #         #  перейдем к слудущему родителю
    #         id_code_parent = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_e']==id_item]['id_code_parent']
    # upsdf['PathDistanation'] = ValuePathDistanation


    return upsdf


def viewTreeComponents(treeF:ttk.Treeview, DataFrameTree: pd.DataFrame, parent):
    """
    отображение ветки в дереве Компонентов
    Вход:
    treeF:ttk.Treeview - объект дерева из формы
    DataFrameTree: pd.DataFrame - БД которую надо отобразить
    parent - id_code_item группы(ветки) дерева
    """
    stringDF = {}
    # выдать всех у кого в родителях код parent
    df2 = DataFrameTree[DataFrameTree['id_code_parent'] == parent]   

    # очистим все дерево компонентов            
    for i in treeF.get_children(): treeF.delete(i)      
    # заполним дерево
    if not(df2.empty):
            for indx in df2.index:
                stringDF = Unpack_String_DataFrame(DataFrameTree, indx)
                # if (stringDF['id_code_lvl'] != 'lvl01' ):
                if stringDF['id_code_lvl'] in scfg.listOfLevel:
                    ...
                else:
                    id_code_item = int(stringDF['id_code_item'])
                    # # извлекем наименование ед изм - возмем по коду 'id_code_item' из DBCU
                    UnitsName = stringDF['UnitsName']
                    # treeF.insert('', 'end',  id_code_item, text=name, values=[id_code_item, amount, code_units, min_rezerve, articul_1C, code_1C, name_1C, id_code_parent, id_code_lvl])
                    treeF.insert('', 'end',  id_code_item, text=stringDF['name'], values=[stringDF['id_code_item'], stringDF['amount'], UnitsName, stringDF['min_rezerve'], stringDF['articul_1C'], stringDF['code_1C'], stringDF['name_1C'], stringDF['id_code_parent'], stringDF['id_code_lvl']])

    return None

def viewTreeGroupSpec(treeF:ttk.Treeview, DataFrameTree: pd.DataFrame): 

    a=0
    stringDF = {}
    # очищаем дерево
    for i in treeF.get_children(): treeF.delete(i)
    for lvl in scfg.listOfLevel:
        # выдать всех у кого в родителях код lvl
        df2 = DataFrameTree[DataFrameTree['id_code_lvl'] == lvl]     
        if not(df2.empty):
            for indx in df2.index:
                stringDF = Unpack_String_DataFrame(DataFrameTree, indx)  
                if lvl == 'lvl01':
                    id_code_parent = ''
                else: 
                    id_code_parent = DataFrameTree.loc[indx, 'id_code_parent'] 
                index_code_parent = id_code_parent
                id_code_e = int(stringDF['id_code_e'])
                # treeF.insert(index_code_parent, 'end',  id_code_item, text=name, values=[id_code_item, amount, code_units, min_rezerve, articul_1C, code_1C, name_1C, id_code_parent, id_code_lvl])
                treeF.insert(index_code_parent, 'end',  id_code_e, text=stringDF['name'], values=[stringDF['id_code_item'], stringDF['amount'],  stringDF['id_code_parent'], stringDF['id_code_lvl']])
        

def viewTreeGroup(treeF:ttk.Treeview, DataFrameTree: pd.DataFrame): 

    a=0
    stringDF = {}
    # очищаем дерево
    for i in treeF.get_children(): treeF.delete(i)
    


    # заполним дерево TreeGroup названиями групп
    
    connectionDBFile = sql3.connect(scfg.DBSqlite)
    cursorDB = connectionDBFile.cursor()
    with connectionDBFile: 
        # вычисли максимальное значение id родителя в таблице DBG
        cursorDB.execute("""SELECT MAX(id_parent) FROM DBG;""")
        maxxx = cursorDB.fetchone()
        maxx = maxxx[0]

        cursorDB.execute('PRAGMA table_info("DBG")')
        column_names = [i[1] for i in cursorDB.fetchall()]
        print(column_names)
        # ['id', 'name', 'id_parent']
        for item_id_parent in range (0, maxx+1, 1):
            # получим из DBG названия у которых id_parent =0
            # item_id_parent = 0
            cursorDB.execute("""SELECT * FROM DBG WHERE id_parent=?;""", (item_id_parent,))
            row_from_DBG = cursorDB.fetchall()
            print(row_from_DBG)
            # [(1, 'Склад', 0)]
            if row_from_DBG:
                # сделаем словарь и заполняем дерево
                for item_tupple in row_from_DBG:
                    stringDF = {}
                    stringDF[column_names[0]] = item_tupple[0]
                    stringDF[column_names[1]] = item_tupple[1]
                    stringDF[column_names[2]] = item_tupple[2]
                    print(stringDF)
                    # {'id': 1, 'name': 'Склад'}
                    if stringDF['id_parent'] ==0: 
                        index_code_parent=''
                    else:
                        index_code_parent = str(stringDF['id_parent'])
                    # treeF.insert(index_code_parent, 'end',  id_code_item, text=stringDF['name'], values=[stringDF['id_code_item'], stringDF['amount'], UnitsName, stringDF['min_rezerve'], stringDF['articul_1C'], stringDF['code_1C'], stringDF['name_1C'], stringDF['id_code_parent'], stringDF['id_code_lvl']])
                    treeF.insert(index_code_parent, 'end',  stringDF['id'], text=stringDF['name'], values=[stringDF['id'], 0, '', 0, '', '', '', stringDF['id_parent'], 0])

        # item_id_parent = 1
        # cursorDB.execute("""SELECT * FROM DBG WHERE id_parent=?;""", (item_id_parent,))
        # row_from_DBG = cursorDB.fetchall()
        # print(row_from_DBG)
        # # [(1, 'Склад', 0)]
        # # сделаем словарь и заполняем дерево
        # for item_tupple in row_from_DBG:
        #     stringDF = {}
        #     stringDF[column_names[0]] = item_tupple[0]
        #     stringDF[column_names[1]] = item_tupple[1]
        #     stringDF[column_names[2]] = item_tupple[2]
        #     print(stringDF)
        #     # {'id': 1, 'name': 'Склад'}
        #     if stringDF['id_parent'] ==0: 
        #         index_code_parent=''
        #     else:
        #         index_code_parent = str(stringDF['id_parent'])
        #     # treeF.insert(index_code_parent, 'end',  id_code_item, text=stringDF['name'], values=[stringDF['id_code_item'], stringDF['amount'], UnitsName, stringDF['min_rezerve'], stringDF['articul_1C'], stringDF['code_1C'], stringDF['name_1C'], stringDF['id_code_parent'], stringDF['id_code_lvl']])
        #     treeF.insert(index_code_parent, 'end',  stringDF['id'], text=stringDF['name'], values=[stringDF['id'], 0, '', 0, '', '', '', stringDF['id_parent'], 0])

    if(connectionDBFile):
            connectionDBFile.close()


    #
    # for lvl in scfg.listOfLevel:
    #     # список названий всех полей/столбцов в
    #     # в sqlite
    #     # connectionDBFile = sql3.connect(scfg.DBSqlite)
    #     # cursorDB = connectionDBFile.cursor()
    #     # with connectionDBFile: 
    #     #     # for item in data_list:
    #     #     cursorDB.execute('PRAGMA table_info("DBC")')
    #     #     column_names = [i[1] for i in cursorDB.fetchall()]
    #     #     print(column_names)
    #     #     # извлекаем строку по индксу
    #     #     cursorDB.execute("""SELECT * FROM DBC WHERE id=?;""", (index+1,))
    #     #     a = cursorDB.fetchone()
    #     # выдать всех у кого в родителях код lvl
    #     df2 = DataFrameTree[DataFrameTree['id_code_lvl'] == lvl]     
    #     if not(df2.empty):
    #         for indx in df2.index:
    #             stringDF = Unpack_String_DataFrame(DataFrameTree, indx)  
    #             if lvl == 'lvl01':
    #                 id_code_parent = ''
    #             else: 
    #                 id_code_parent = DataFrameTree.loc[indx, 'id_code_parent'] 
    #             index_code_parent = id_code_parent
    #             id_code_item = int(stringDF['id_code_item'])

    #             # # извлекем наименование ед изм - возмем по коду 'id_code_item' из DBCU
    #             UnitsName = stringDF['UnitsName']

    #             # treeF.insert(index_code_parent, 'end',  id_code_item, text=name, values=[id_code_item, amount, code_units, min_rezerve, articul_1C, code_1C, name_1C, id_code_parent, id_code_lvl])
    #             treeF.insert(index_code_parent, 'end',  id_code_item, text=stringDF['name'], values=[stringDF['id_code_item'], stringDF['amount'], UnitsName, stringDF['min_rezerve'], stringDF['articul_1C'], stringDF['code_1C'], stringDF['name_1C'], stringDF['id_code_parent'], stringDF['id_code_lvl']])


def Setting_TreeView(treeF:ttk.Treeview, form):
    """
    Установка и настройка столбцов компонента TreeView
    Визуальная настройка

    """
    
    col = scfg.columns_DB_components.copy()
    col.remove('name')
    treeF["columns"]=col

    # treeF.heading('#0', text='NameID')
    # treeF.heading('#1', text='id_code_item')
    # treeF.heading('#2', text='amount')
    # treeF.heading('#3', text='code_units')
    # treeF.heading('#4', text='min_rezerve')
    # treeF.heading('#5', text='articul_1C')
    # treeF.heading('#6', text='code_1C')
    # treeF.heading('#7', text='name_1C')
    # treeF.heading('#8', text='id_code_parent')
    # treeF.heading('#9', text='id_code_lvl')
            # Specify attributes of the columns 
    # treeF.column('#0', width=200,stretch=tk.YES)
    # treeF.column('#1', width=60,stretch=tk.YES)
    # treeF.column('#2', width=60,stretch=tk.YES)
    # treeF.column('#3', width=60,stretch=tk.YES)
    # treeF.column('#4', width=60, stretch=tk.YES)
    # treeF.column('#5', width=60, stretch=tk.YES)
    # treeF.column('#6', width=60, stretch=tk.YES)
    # treeF.column('#7', width=60, stretch=tk.YES)
    # treeF.column('#8', width=60, stretch=tk.YES)
    # treeF.column('#9', width=60, stretch=tk.YES)

    # treeF["columns"]=scfg.columns_DB_components.copy()
    # a = scfg.columns_DB_components.copy()

    for i in col:
            treeF.heading(i, text=i)
            treeF.column(i, width=scfg.widthColunmsTreeWindowEditComponent[i], stretch=True)
    treeF.heading('#0', text='NameID')
    # treeF.column('#0', width=300,stretch=tk.YES)

    if form == 'short':
        # отобразим визуально только те столбцы, которые заложены в конфигуоационный модуль
        treeF["displaycolumns"]=scfg.displayColumnsShort
        treeF.column('#0', width=200,stretch=tk.YES)
    elif form == 'full':
        treeF["displaycolumns"]=scfg.displayColumnsFull
        treeF.column('#0', width=400,stretch=tk.YES)
    else :
        treeF["displaycolumns"]=scfg.displayColumnsE
    return None



    # mask = (scfg.df1['id_code_lvl'] != 'lvl01') & (scfg.df1['id_code_lvl'] != 'lvl02') & (scfg.df1['id_code_lvl'] != 'lvl03') & (scfg.df1['id_code_lvl'] != 'lvl04') & (scfg.df1['id_code_lvl'] != 'lvl05') & (scfg.df1['id_code_lvl'] != 'lvl06')
    # df2 = scfg.df1.loc[mask]     # выдать всех у кого в родителях 
    # if not(df2.empty):
    #         for indx in df2.index:
    #             id_group =  int(scfg.df1.loc[indx, 'id_code_item'])    
    #             name_group = scfg.df1.loc[indx, 'name'] 
    #             id_code_parent = scfg.df1.loc[indx, 'id_code_parent'] 
    #             id_code_lvl = scfg.df1.loc[indx, 'id_code_lvl'] 
    #             amount = scfg.df1.loc[indx, 'amount']
    #             treeF.insert(id_code_parent, 'end',  id_group, text=name_group, values=[id_group, id_code_parent, id_code_lvl, amount])
    
        # self.tree.insert('', 'end', 10, text='Разъемы', values=0)
        # self.tree.insert('', 'end', 11, text='Наконечники НКИ', values=0)
        # self.tree.insert(10, 'end', 1001, text='DIN', values=0)
        # self.tree.insert(10, 'end', 1002, text='DВ', values=0)
        # self.tree.insert(11, 'end', 1101, text='НКИ', values=0)
        # self.tree.insert(11, 'end', 1102, text='НВИ', values=0)


    return None



    # def fn_add_groupComponents(self):
    #     sql_insert_data_in_tableDBGroupComponent = 'INSERT INTO DBGroupComponent (code_group, name_group) values(?, ?)' 
    #     if self.flagSelection:
    #         name_group=self.ent_NameComponent.get()
    #         data = []
    #         connectionDBFile = sqlite.connect(scfg.nameFile_DB)
    #         cursorDB = connectionDBFile.cursor()
    #         with connectionDBFile:
    #             sel = self.tree.selection()
    #             id_item=int(sel[0])
    #             code_group, flag_oversize_number_child = self.next_code_in_parent(id_item)
    #             if not(flag_oversize_number_child):
    #                 data.append(code_group)
    #                 data.append(name_group)
    #                 cursorDB.execute(sql_insert_data_in_tableDBGroupComponent, data)
    #                 connectionDBFile.commit()
    #             else:
    #                 msg = "Число подгрупп в родительской группе не должно быть больше 15"
    #                 mb.showerror("Ошибка", msg)
    #     return None

    # def next_code_in_parent(self, id_itemf):
    #     """
    #     генерация нового кода для элемета в родительской группе
    #     """
    #     #Считаем таблицы из файла БД и положим их в памятть
    #     # DBGroupF, flag_copyTableInMemory = dbcm.copy_FileDBGroupComponent_In_ListDBGroup(scfg.nameFile_DB)
    #     # for j in range (0, len(DBGroupF), 1):
    #     #         if DBGroupF[j].code_group ==
    #     flag_oversize_number_child_f = False
    #     next_id_item = id_itemf
    #     while next_id_item != '':
    #         id_itemf = next_id_item
    #         next_id_item = self.tree.next(id_itemf)
    #         print (id_itemf, ' - ', next_id_item)

    #     cg = []
    #     cg = mdbc.Unpack_codegroup(int(id_itemf))
    #     if cg[0]>=0x10 and cg[1]==0 and cg[2]==0 and cg[3]==0 and cg[4]==0: # если это группа верхнего уровня        
    #         increment_item_in_parent = 0x010000
    #     elif cg[1]!=0 and cg[2]==0 and cg[3]==0 and cg[4]==0: # если это группа второго уровня    
    #         increment_item_in_parent = 0x001000
    #     elif cg[2]!=0 and cg[3]==0 and cg[4]==0: # если это группа третьего уровня       
    #         increment_item_in_parent = 0x000100
    #     elif cg[3]!=0 and cg[4]==0: # если это группа четвертого уровня       
    #         increment_item_in_parent = 0x000010
    #     elif cg[4]!=0: # если это группа пятого уровня       
    #         increment_item_in_parent = 0x000001
    #     new_code = int(id_itemf)+increment_item_in_parent
    #     flag_oversize_number_child_f = False
    #     # число детей в родительской группе не должно быть больше 15 (номер 0 - родитель)
    #     if (increment_item_in_parent == 0x010000) and (new_code >= 0xFA0000):               
    #         new_code = id_itemf
    #         flag_oversize_number_child_f = True
    #     # elif (increment_item_in_parent == 0x001000) and (new_code >= 0x00E000)               
    #     #     new_code = id_itemf
    #     #     flag_oversize_number_child_f = True
    #     return new_code, flag_oversize_number_child_f

    # def fn_edit_groupComponent(self):
    #     sql_update_query_in_tableDBGroupComponent = 'UPDATE DBGroupComponent SET name_group = ? WHERE code_group = ?'
    #     if self.flagSelection:
    #         var=self.ent_NameComponent.get()
    #         connectionDBFile = sqlite.connect(scfg.nameFile_DB)
    #         cursorDB = connectionDBFile.cursor()
    #         with connectionDBFile:
    #             sel = self.tree.selection()
    #             data = []
    #             #dic = self.tree.item(sel[0])
    #             name_group=var          #dic['text']
    #             code_group=int(sel[0])
    #             data.append(name_group)
    #             data.append(code_group)
    #             cursorDB.execute(sql_update_query_in_tableDBGroupComponent, data)
    #             connectionDBFile.commit()
    #         self.ent_NameComponent.delete(0, END)
    #         for i in self.tree.get_children(): self.tree.delete(i)      # очистим все дерево
    #         viewTreeGroup(self.tree)       # отобразим данные из памяти DBGroup в Tree
    #     else:
    #         mb.showinfo('Ошибка', 'Вы ничего не выделили!!!') 
    #     self.flagSelection = False
    #     return None

    # def fn_delete_groupComponents(self):
    #     sql_delete_single_data_in_tableDBGroupComponent = 'DELETE FROM DBGroupComponent WHERE code_group = ?;'
    #     if self.flagSelection:
    #         connectionDBFile = sqlite.connect(scfg.nameFile_DB)
    #         cursorDB = connectionDBFile.cursor()
    #         with connectionDBFile:
    #             sel = self.tree.selection()
    #             data = int(sel[0])
    #             print(data)
    #             print(type(data))
    #             cursorDB.execute(sql_delete_single_data_in_tableDBGroupComponent, (data,))
    #             connectionDBFile.commit()
    #         for i in self.tree.get_children(): self.tree.delete(i)      # очистим все дерево
    #         viewTreeGroup(self.tree)       # отобразим данные из памяти DBGroup в Tree
    #     else:
    #         mb.showinfo('Ошибка', 'Вы ничего не выделили!!!') 
    #     self.flagSelection = False
    #     self.ent_NameComponent.delete(0, END)
    #     return None

    # def on_select(self, event):
    #     #print(event)
    #     sel = self.tree.selection()
    #     print(sel)
    #     print(sel[0])
    #     # self.tree.see(sel[0])                 # не работает- не понято !!!!!!!!!
    #     dic = self.tree.item(sel[0])
    #     print(dic['text'])    
    #     self.ent_NameComponent.delete(0, END)
    #     self.ent_NameComponent.insert(0, dic['text'])
    #     self.flagSelection = True

    #     return None

   
    # def confirm_delete(self):
    #     message = "Вы уверены, что хотите закрыть это окно?"
    #     if mb.askyesno(message=message, parent=self):
    #         self.destroy()


# class WindowImportComponent(tk.Toplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         #self.protocol("WM_DELETE_WINDOW", self.confirm_delete)
#         self.frame_wig = tk.LabelFrame (master=self, text="Импорт групп", relief=tk.SUNKEN, borderwidth=3, height=50)
#         self.frame_wig.pack(fill=tk.X, side=tk.TOP, ipadx=5, ipady=5, padx=10, pady=10)
#         self.btn_wig = tk.Button(master=self.frame_wig, text="Импорт групп", command=self.press_Button_ImportGroup)
#         self.btn_wig.pack(fill=tk.X, expand=0, side=tk.TOP, ipadx=5, ipady=5)


#         self.frame_tableTree = tk.Frame(master=self, relief=tk.SUNKEN, borderwidth=3, height=50)
#         self.frame_tableTree.pack(fill=tk.X, side=tk.TOP, ipadx=5, ipady=5, padx=10, pady=5)
#         # Set the treeview
#         self.columns = ('NameID', 'id_code_item',  'id_code_parent',   'id_code_lvl', 'amount')
        
#         self.tree = ttk.Treeview(self.frame_tableTree, show="tree headings", columns=self.columns)
#             # Set the heading (Attribute Names)
#         self.tree.heading('#0', text='NameID')
#         self.tree.heading('#1', text='id_code_item')
#         self.tree.heading('#2', text='id_code_parent')
#         self.tree.heading('#3', text='id_code_group')
#         self.tree.heading('#4', text='amount')

#         self.ysb = ttk.Scrollbar(self.frame_tableTree, orient=tk.VERTICAL, command=self.tree.yview)
#         self.tree.configure(yscroll=self.ysb.set)
#             # Specify attributes of the columns (We want to stretch it!)
#         self.tree.column('#0', stretch=tk.YES)
#         self.tree.column('#1', stretch=tk.YES)
#         self.tree.column('#2', stretch=tk.YES)
#         self.tree.column('#3', stretch=tk.YES)
#         self.tree.column('#4', stretch=tk.YES)

#         self.tree.grid(row=0, column=0, sticky=tk.W + tk.E)
#         self.ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
        
#         self.frame_tableTree.columnconfigure(0, weight=1)
#         self.tree.bind('<<TreeviewSelect>>', self.on_select)

#         if not(scfg.df1.empty):
#             viewTreeGroup(self.tree, scfg.df1)        # отобразим данные из памяти DataFrame в Tree
        
#     def on_select(self, event):
#         print(event)
#         print(self.tree.selection())
#         return None

#     def press_Button_ImportGroup(self):
#         mi.Load_DBGroup_From_XLS_pandas(scfg.nameFile_pu)
#         viewTreeGroup(self.tree, scfg.df1)       # отобразим данные из памяти DBGroup в Tree
#         return None

    # def confirm_delete(self):
    #     message = "Вы уверены, что хотите закрыть это окно?"
    #     if mb.askyesno(message=message, parent=self):
    #         self.destroy()

    # def fn_addGroup_Components(self):
    #     # запомним 'id_code_item' элемента из treeGroup
    #     id_code_item = self.treeGroup.selection()
    #     # получим от родителя  строку 'id_code_parent'
    #     df2 = scfg.df1[scfg.df1['id_code_item'] == id_code_item[0]]['id_code_parent']
    #     id_code_parent = df2.item()
    #     # получаем новое наименование из self.ent_NameComponent
    #     newNameComponent = self.ent_NameComponent.get()
    #     # сгенерим для него уникальный код
    #     codeItem = mdbc.getCode()
    #     # получим от родителя  строку 'id_code_lvl'
    #     df2 = scfg.df1[scfg.df1['id_code_item'] == id_code_item[0]]['id_code_lvl']
    #     id_lvl = df2.item()
        
    #     # сформируем строку для DataFrame
    #     new_row = {'name':newNameComponent, 'id_code_lvl': id_lvl, 'id_code_item': codeItem, 'id_code_parent':id_code_parent, 'amount':0} #append row to the dataframe 
    #     # scfg.df1 = scfg.df1.append(new_row, ignore_index=True)
    #     # пересоздадим добавление строки в DataFrame  как рекомендует Pandas 1.4.0. 22jan2022
    #     df_new_row = pd.DataFrame(new_row , index=[0])
    #     scfg.df1 = pd.concat([scfg.df1, df_new_row])
    #     #  переиндексируем DataFrame
    #     scfg.df1 = scfg.df1.reset_index(drop=True)
    #     # очищаем дерево
    #     for i in self.tree2.get_children(): self.tree2.delete(i)
    #     # и выводим его заново
    #     viewTreeGroup(self.treeGroup, scfg.df1)
    #     # сохраняем изменненный DataFame в файл
    #     mi.Save_DataFrame_in_PickleFile()
    #     mi.Save_DataFrame_in_ExcelFile()

    #     return None


# def fn_renameGroup_Component(self):
    #     # запомним 'id_code_item' элемента из treeGroup
    #     id_code_item = self.treeGroup.selection()[0]
    #     # получаем выделенный элемент
    #     # sel = self.tree2.selection()
    #     # получаем индекс и 'id_code_item' выделенного элемента
    #     df2 = scfg.df1[scfg.df1['id_code_item'] == id_code_item]   
    #     indx = df2.index
    #     # получаем измененное наименование из self.ent_NameComponent
    #     newNameComponent = self.ent_NameComponent.get()
    #     # изменяем наименоевание в DataFrame по индексу
    #     scfg.df1.loc[indx, 'name'] = newNameComponent
    #     # и выводим его заново
    #     viewTreeGroup(self.treeGroup, scfg.df1)
    #     self.treeGroup.see(id_code_item)
    #     self.treeGroup.selection_set(id_code_item)
    #     viewTreeComponents(self.tree2, scfg.df1, id_code_item)
    #     # сохраняем изменненный DataFame в файл
    #     mi.Save_DataFrame_in_PickleFile()
    #     mi.Save_DataFrame_in_ExcelFile()
    #     return None

# def fn_deleteGroup_Components(self):
    #     # запомним id_code_item выделенной строки в treeGroup
    #     id_code_item = self.treeGroup.selection()
    #     # постмотрим, есть ли у выделенного родителя потомки
    #     df2 = scfg.df1[scfg.df1['id_code_parent'] == id_code_item[0]]
    #     # пустая ли таблица df2?
    #     if df2.empty:
    #         df2 = scfg.df1[scfg.df1['id_code_item'] == id_code_item[0]]
    #         indx = df2.index
    #         # удаляем его из DataFrame по индексу
    #         scfg.df1 = scfg.df1.drop(index=indx)
    #         #  переиндексируем DataFrame
    #         scfg.df1 = scfg.df1.reset_index(drop=True)
    #         # очищаем дерево
    #         for i in self.tree2.get_children(): self.tree2.delete(i)
    #         # for i in self.treeGroup.get_children(): self.treeGroup.delete(i)
    #         # и выводим его заново
    #         viewTreeGroup(self.treeGroup, scfg.df1)
    #         # сохраняем изменненный DataFame в файл
    #         mi.Save_DataFrame_in_PickleFile()
    #         mi.Save_DataFrame_in_ExcelFile()
    #     else:
    #         message = "Группа компонентов не пуста!"
    #         mb.askyesno(message=message, parent=self)
    #         self.destroy()
    #     return None

# def fn_removeGroup_Components(self):
    #     # запомним 'id_code_item' элемента из treeGroup
    #     id_code_item = self.treeGroup.selection()
    #     # получаем индекс по 'id_code_item' выделенного элемента
    #     df2 = scfg.df1[scfg.df1['id_code_item'] == id_code_item[0]]   
    #     indx = df2.index
    #     # выводим окно в котором спрашваем куда в дереве переместить
    #     # в ответ получаем  'id_code_parent' нового родителя
    #     new_id_code_parent = self.open_Window_Remove_Component()
    #     # проверим - если этот код родителя тот же самый selTreeGroup - ничего не делаем
    #     if (new_id_code_parent != id_code_item[0]) and (new_id_code_parent != 0):
    #         # изменяем код родителя компонента в DataFrame по индексу
    #         scfg.df1.loc[indx, 'id_code_parent'] = new_id_code_parent
    #         # очищаем дерево
    #         for i in self.tree2.get_children(): self.tree2.delete(i)
    #         # for i in self.treeGroup.get_children(): self.treeGroup.delete(i)
    #         # и выводим его заново
    #         viewTreeGroup(self.treeGroup, scfg.df1)
    #         # сохраняем изменненный DataFame в файл
    #         mi.Save_DataFrame_in_PickleFile()
    #         mi.Save_DataFrame_in_ExcelFile()
    #     return None