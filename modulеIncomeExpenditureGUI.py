# modulеIncomeExpenditureGUI
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# модуль держатель элементов GUI для расхода-прихода склада

import os
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, N, NSEW, Entry, Menu
import pandas as pd
import numpy as np
import sqlite3 as sql3

import skladConfig as scfg
import moduleDBClass as mdbc
import modulAppGUI as mag
import modulеEditGUI as meGUI

# класс окна по списанию компоентов
        # viewDB - отображение в окне БД:
        # 'DBC' = DataBaseComponents
        # 'DBS' = DataBaseSpecification 
        # 'DBE' - DataBaseExpenditure - БД расхода компонентов (expenditure)  
        # modeWindow - внешний вид и расположени кнопок окна в режимах:
        # modeWindow = 'edit'
        # modeWindow = 'comp_in_spec'
        # modeWindow = 'expenditure'  - режим окна Расход компонента
        # modeWindow = 'income'  - режим окна Приход компонента
class WindowExpenditure(tk.Toplevel):
    def __init__(self, parent, viewDB, modeWindow): 
        super().__init__(parent)
        # self.geometry("1024x600")
        if modeWindow == 'expenditure': self.title('Расход компонентов')
        if modeWindow == 'income': self.title('Приход компонентов')
        opts = { 'ipadx': 3, 'ipady': 3 , 'sticky': 'nswe' }

        self.frame_tableTreeGroup = tk.LabelFrame(master=self, text="Группы", relief=tk.SUNKEN, borderwidth=3) 
        self.frame_tableTreeGroup.grid(row=0, column=0, columnspan=2, **opts)

        self.treeF = ttk.Treeview(self.frame_tableTreeGroup, show="headings", height=20)#, columns=col) #self.columns)
        self.treeF.grid(row=0, column=0, rowspan=4, columnspan=6, **opts)

        # Setting_TreeView(self.treeGroup, form = 'short')
    #     """
    # Установка и настройка столбцов компонента TreeView
    # Визуальная настройка

    # """
    
        # col = scfg.columns_DBE.copy()
        # col.remove('name')
        # self.treeF["columns"]=scfg.columns_DBE.copy()
        if modeWindow == 'expenditure': 
            self.treeF["columns"]=scfg.displayColumnsE.copy()
            a = scfg.displayColumnsE.copy()
        if modeWindow == 'income': 
            self.treeF["columns"]=scfg.displayColumnsI.copy()
            a = scfg.displayColumnsE.copy()
        # self.treeF["columns"]=scfg.displayColumnsE.copy()
        
        # for i in scfg.displayColumnsE:
        for i in a:
            self.treeF.heading(i, text=i)
            if modeWindow == 'expenditure': 
                self.treeF.column(i, width=scfg.widthColunmsTreeWindowExpenditure[i], stretch=True)
            if modeWindow == 'income': 
                self.treeF.column(i, width=scfg.widthColunmsTreeWindowIncome[i], stretch=True)
            
            

        # self.treeF.heading('#0', text='NameID')
        # self.treeF.heading('#1', text='id_code_e')
        # self.treeF.heading('#2', text='id_code_item')
        # self.treeF.heading('#3', text='name')
        # self.treeF.heading('#4', text='amount')
        # self.treeF.heading('#5', text='date')
        # self.treeF.heading('#6', text='id_code_parent')
        # self.treeF.heading('#7', text='comments')
        # self.treeF.column('#0', width=100,stretch=tk.YES)
        # self.treeF.column('#1', width=60,stretch=tk.YES)
        # self.treeF.column('#2', width=60,stretch=tk.YES)
        # self.treeF.column('#3', width=60,stretch=tk.YES)
        # self.treeF.column('#4', width=60, stretch=tk.YES)
        # self.treeF.column('#5', width=60, stretch=tk.YES)
        # self.treeF.column('#6', width=60, stretch=tk.YES)
        # self.treeF.column('#7', width=100, stretch=tk.YES)

        form = 0
        if form == 'short':
            # отобразим визуально только те столбцы, которые заложены в конфигуоационный модуль skladConfig.py
            self.treeF["displaycolumns"]=scfg.displayColumnsShort
        elif form == 'full':
            self.treeF["displaycolumns"]=scfg.displayColumnsFull
        else :
            if modeWindow == 'expenditure': 
                self.treeF["displaycolumns"]=scfg.displayColumnsE
            if modeWindow == 'income': 
                self.treeF["displaycolumns"]=scfg.displayColumnsI
            

        self.ysb = ttk.Scrollbar(self.frame_tableTreeGroup, orient=tk.VERTICAL, command=self.treeF.yview)
        self.treeF.configure(yscroll=self.ysb.set)
        self.ysb.grid(row=0, column=6, rowspan=4, **opts)

        if modeWindow == 'expenditure': 
                self.viewTreeEI(self.treeF, scfg.df_DBE)
        if modeWindow == 'income': 
                self.viewTreeI(self.treeF)#, scfg.df_DBI)
        

        self.id_code_e_DBEI = tk.StringVar()
        self.dateStringDBEI = tk.StringVar()
        self.id_code_item_DBEI = ''
        self.name_DBEI = tk.StringVar()
        self.amount_DBEI = tk.StringVar()
        self.UnitName = tk.StringVar()
        self.PathDistanation = tk.StringVar()
        # self.id_code_parent_DBE = tk.StringVar()
        self.commentsStringDBEI = tk.StringVar()
        # self.commentsStringDBE.trace("w", lambda: self.ent_commentsStringDBEself.commentsStringDBE.get())
        # self.parent_DBE = tk.StringVar()

        self.frame_Input = tk.LabelFrame(master=self, text="Ввод", relief=tk.SUNKEN, borderwidth=3) 
        self.frame_Input.grid(row=1, column=0, columnspan=2, **opts)
        # поле для даты         width= В ЧИСЛЕ СИМВОЛОВ!!!!
        self.ent_date = tk.Entry(master=self.frame_Input, textvariable=self.dateStringDBEI, width=10)
        self.ent_date.grid(row=0, column=0, **opts)
        # автоматически дадим текущую дату
        self.dateStringDBEI.set(datetime.now().date())
        #  поле ввода имени комопнента
        self.ent_name_DBEI = tk.Entry(master=self.frame_Input, textvariable=self.name_DBEI, width=80, state="readonly")
        self.ent_name_DBEI.grid(row=0, column=1, **opts)
        self.ent_name_DBEI.insert(0, 'Нажать для ввода компонента')
        # если кликнуть по полю ввода компонента - попадаем на форму WindowEditComponent
        self.ent_name_DBEI.bind('<Button-1>', lambda e, mW = modeWindow, vdb = viewDB: self.click_Ent_name_DBE(e, modeWindow=mW, viewDB=vdb))
        # поле ввода количества
        self.ent_amount_DBEI = tk.Entry(master=self.frame_Input, textvariable=self.amount_DBEI, width=6)
        self.ent_amount_DBEI.grid(row=0, column=2, **opts)
        # поле ввода ед изм
        # self.CB_code_units_DBCU = ttk.Combobox(self.frame_Input, values=list(scfg.UnitsCodeName.values()), width=5)
        self.CB_code_units_DBCU = tk.Entry(self.frame_Input, textvariable=self.UnitName, state="readonly")
        # self.ent_amount_DBE = tk.Entry(master=self.frame_Input, textvariable=self.amount_DBE)
        self.CB_code_units_DBCU.grid(row=0, column=3, **opts)
        # поле ввода КУДА приход\списать компонент
        if modeWindow == 'expenditure': 
                self.ent_PathDistanation = tk.Entry(master=self.frame_Input, textvariable=self.PathDistanation, width=60)
                self.ent_PathDistanation.insert(0, 'Нажать КУДА СПИСАТЬ')
                # если кликнуть по полю ввода компонента - попадаем на форму WindowEditComponent
                self.ent_PathDistanation.bind('<Button-1>', self.click_Ent_PathDistanation)
        if modeWindow == 'income': 
                self.ent_PathDistanation = tk.Entry(master=self.frame_Input, textvariable=self.PathDistanation, width=60, state="readonly")
        self.ent_PathDistanation.grid(row=0, column=4, **opts)
        
        
        # поле ввода комментария
        self.ent_commentsStringDBE = tk.Entry(master=self.frame_Input, width=80)
        self.ent_commentsStringDBE.grid(row=0, column=5, **opts)
        

        if modeWindow == 'expenditure': 
            self.btn_In = tk.Button(master=self, height=3, text="Запись РАСХОДА", command=self.saveExpenditure)
        if modeWindow == 'income': 
            self.btn_In = tk.Button(master=self, height=3, text="Запись ПРИХОДА", command=self.saveIncome)
        self.btn_In.grid(row=3, column=0, **opts)
        
        self.btn_Cansel = tk.Button(master=self, height=3, text="Отмена", command=self.destroy)
        self.btn_Cansel.grid(row=3, column=1, **opts)

        # self.treeGroup.bind('<<TreeviewSelect>>', self.on_select)

        self.new_parent = 0
        self.sel = 0
        self.idCodeDistanation =''
        # self.PathDistanation=''

        return None

    # def viewTreeI(self, treeF:ttk.Treeview, DataFrameTree: pd.DataFrame)-> None:
    def viewTreeI(self, treeF:ttk.Treeview)-> None:    
        """ Отобаржение дерева прихода"""

        # очистим все дерево компонентов            
        for i in treeF.get_children(): treeF.delete(i)  

        connectionDBFile = sql3.connect(scfg.DBSqlite)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile:
            cursorDB.execute("""SELECT DBI.*, DBC.name FROM DBI JOIN DBC ON DBC.id = DBI.id_component;""")
            rows_from_DBI = cursorDB.fetchall()    
            for item_row in rows_from_DBI:
                id_DBI, date, id_component, amount, comments, name_component = item_row 
                # вытащим строку - получим из DBC у которых DBC.name=stringDF['name_component'] и приклеим название ед измерения
                cursorDB.execute("""SELECT DBC.id_parent, DBU.name FROM DBC JOIN DBU ON DBU.id = DBC.id_unit WHERE DBC.name=? ;""", (name_component,))
                id_parent_DBC, name_unit = cursorDB.fetchone()
                # вытащим строку - получим из DBG название группы:  у которых DBG.id=stringDF['id_parent']
                cursorDB.execute("""SELECT id,name,id_parent FROM DBG WHERE id=? ;""", (id_parent_DBC,))
                id_DBG, name_DBG, id_parent_DBG = cursorDB.fetchone()
                # построим полную строку пути по иерархии групп
                string_path = name_DBG
                id_next_DBG = id_parent_DBG
                while id_DBG !=1:
                    # вытащим строку - получим из DBG название родителя:  у которых DBG.id=row_from_DBG[2]
                    cursorDB.execute("""SELECT * FROM DBG WHERE DBG.id=? ;""", (id_next_DBG,))
                    id_DBG, name_parent, id_next_DBG = cursorDB.fetchone()
                    string_path = name_parent + '/' + string_path
                
                treeF.insert('', 'end',  id_DBI, text=name_component, values=[id_DBI, date, name_component, amount, name_unit, string_path, comments])

        if(connectionDBFile):
            connectionDBFile.close()

        
        return None


    def viewTreeEI(self, treeF:ttk.Treeview, DataFrameTree: pd.DataFrame):

        # очистим все дерево компонентов            
        for i in treeF.get_children(): treeF.delete(i)      
        # заполним дерево
        if not(DataFrameTree.empty):
                for indx in DataFrameTree.index:
                    stringDF = mag.Unpack_String_DataFrame(DataFrameTree, indx)
                    # извлекем имя компонента - возмем по коду 'id_code_item' из DBC 
                    ComponentName = scfg.df_DBC[scfg.df_DBC['id_code_item'] == stringDF['id_code_item']]['name'].item()

                    # # извлекем наименование ед изм - возмем по коду 'id_code_item' из DBCU
                    UnitsName = stringDF['UnitsName']
                    
                    # извлекем путь списания компонента в спецификацию - возмем по коду 'id_code_parent' из DBS
                    if stringDF['id_code_parent'] !='':
                        # self.idCodeDistanation = id_item_group
                        nameGroup = scfg.df_DBS[scfg.df_DBS['id_code_e']==stringDF['id_code_parent']]['name']
                        ValuePathDistanation= nameGroup.item()
                        id_code_parent = scfg.df_DBS[scfg.df_DBS['id_code_e']==stringDF['id_code_parent']]['id_code_parent']
                        while (id_code_parent.item() != '10000'):
                            id_item = id_code_parent.item()
                            nextNameGroup = scfg.df_DBS[scfg.df_DBS['id_code_e']==id_item]['name']
                            a= nextNameGroup.item()
                            ValuePathDistanation = a + '/' + ValuePathDistanation
                            #  перейдем к слудущему родителю
                            id_code_parent = scfg.df_DBS[scfg.df_DBS['id_code_e']==id_item]['id_code_parent']
                    # ValuePathDistanation = stringDF['PathDistanation']


                    id_code_e = int(stringDF['id_code_e'])
                    # self.treeF.insert('', 'end',  id_code_e, text=stringDF['name'], values=[stringDF['id_code_e'],stringDF['date'], stringDF['id_code_item'], stringDF['name'], stringDF['amount'],  stringDF['dist'], stringDF['id_code_parent'], stringDF['comments']])
                    # self.treeF.insert('', 'end',  id_code_e, text=nameComp.item(), values=[stringDF['id_code_e'],stringDF['date'], stringDF['id_code_item'], nameComp.item(), stringDF['amount'], code_units, stringDF['dist'], stringDF['id_code_parent'], stringDF['comments']])
                    treeF.insert('', 'end',  id_code_e, text=ComponentName, values=[stringDF['id_code_e'],stringDF['date'], ComponentName, stringDF['amount'], UnitsName, ValuePathDistanation, stringDF['comments']])
           

        return None

    def click_Ent_name_DBE(self, event, modeWindow, viewDB):
        # если кликнуть по полю ввода компонента - попадаем на форму WindowEditComponent
        # от формы должны получить компонент - код компонента id_item_comp
        # по коду получаем ИМЯ комопнента и вносим его в форму
        # автоматчески заполняем ед изм
        wec = meGUI.WindowEditComponent(self, modeWindow='expenditure', viewDB='DBC')
        id_item_comp = wec.open()
        if (id_item_comp !=0) | (id_item_comp !=''):
            connectionDBFile = sql3.connect(scfg.DBSqlite)
            cursorDB = connectionDBFile.cursor()
            with connectionDBFile:
                cursorDB.execute("""SELECT DBC.name, DBC.id_parent, DBU.name FROM DBC JOIN DBU ON DBU.id = DBC.id_unit WHERE DBC.id=?;""", (int(id_item_comp),))
                row_from_DBC = cursorDB.fetchall()[0]
                self.name_DBEI.set(row_from_DBC[0])
                self.UnitName.set(row_from_DBC[2])

                # вытащим строку - получим из DBG название группы:  у которых DBG.id=stringDF['id_parent']
                cursorDB.execute("""SELECT * FROM DBG WHERE DBG.id=? ;""", (row_from_DBC[1],))
                row_from_DBG = cursorDB.fetchone()
                ValuePathDistanation = row_from_DBG[1]
                # print (stringDF)

                # построим полную строку пути по иерархии групп
                while row_from_DBG[0] != 1:
                    # вытащим строку - получим из DBG название родителя:  у которых DBG.id=row_from_DBG[2]
                    cursorDB.execute("""SELECT * FROM DBG WHERE DBG.id=? ;""", (row_from_DBG[2],))
                    row_from_DBG = cursorDB.fetchone()
                    ValuePathDistanation = row_from_DBG[1] + '/' + ValuePathDistanation
                self.PathDistanation.set(ValuePathDistanation)
            if(connectionDBFile):
                connectionDBFile.close()
            # nameComp = scfg.df_DBC[scfg.df_DBC['id_code_item']==id_item_comp]['name']
            # # t= nameComp.item()
            # self.name_DBEI.set(nameComp.item())
            # self.id_code_item_DBEI =  id_item_comp
            # UnitsCode = scfg.df_DBC[scfg.df_DBC['id_code_item']==id_item_comp]['code_units'].item()
            # self.UnitName.set(scfg.UnitsCodeName[UnitsCode])

            # # в режиме "прихода" в поле "путь" будем автоматически показывать путь нахождения компонента в группах БД компоненты
            # if modeWindow == 'income':
            #     id_item_group = scfg.df_DBC[scfg.df_DBC['id_code_item']==id_item_comp]['id_code_parent'].item()
            #     self.idCodeDistanation = id_item_group
            #     if id_item_group !=0:
            #         # найдем имя родителя и код дедушки родителя
            #         nameGroup = scfg.df_DBC[scfg.df_DBC['id_code_item']==id_item_group]['name']
            #         id_code_parent_parent = scfg.df_DBC[scfg.df_DBC['id_code_item']==id_item_group]['id_code_parent']
            #         ValuePathDistanation= nameGroup.item()
            #         # id_code_parent = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_item']==id_item_group]['id_code_parent']
            #         # id_code_parent = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_e']==id_item_group]['id_code_parent']
            #         while (id_code_parent_parent.item() != '10000'):
            #             id_item = id_code_parent_parent.item()
            #             nextNameGroup = scfg.df_DBC[scfg.df_DBC['id_code_item']==id_item]['name']
            #             a= nextNameGroup.item()
            #             ValuePathDistanation = a + '/' + ValuePathDistanation
            #             #  перейдем к слудущему родителю
            #             id_code_parent_parent = scfg.df_DBC[scfg.df_DBC['id_code_item']==id_item]['id_code_parent']

            #     self.PathDistanation.set(ValuePathDistanation)
        return None

    def click_Ent_PathDistanation(self, event):
        """
        Обработка клика мыши по полю "Куда списать компонент"
        Выход:
         - в Entry -  "путь" по дереву спецификаций до названия группы
         - в self.idCodeDistanation - код для поля 'id_code_parent' DBE
        """
        # если кликнуть по полю ввода компонента - попадаем на форму WindowTree и передаем ей базу DBS
        # выбираем в дереве группу куда списываем компонент - получаем код группы id_item_group
        # по нему находим строку, а в ней ИМЯ и КОД РОДИТЕЛЯ этой группы - получаем SerialFrame 2 шт
        # зная код родителя - находим дедушку родителя и его имя
        # имена последовательно склеиваем - получаем "путь"
        # контролируем - если у родителя или у дедушки код родителя = "1000" - то это высший родитель, глубже смотреть не надо
        # и наконец - выводим имя группы в форму в Entry через переменую parent_DBE
         
        wt = mag.WindowTree(self, viewDB='DBS', modeWindow='expenditure')
        id_item_group = wt.open()
        if id_item_group !=0:
            self.idCodeDistanation = id_item_group
            # nameGroup = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_item']==id_item_group]['name']
            nameGroup = scfg.df_DBS[scfg.df_DBS['id_code_e']==id_item_group]['name']
            ValuePathDistanation= nameGroup.item()
            # id_code_parent = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_item']==id_item_group]['id_code_parent']
            id_code_parent = scfg.df_DBS[scfg.df_DBS['id_code_e']==id_item_group]['id_code_parent']

            # t = ''
            while (id_code_parent.item() != '10000'):
                id_item = id_code_parent.item()
                # nextNameGroup = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_item']==id_item]['name']
                nextNameGroup = scfg.df_DBS[scfg.df_DBS['id_code_e']==id_item]['name']
                a= nextNameGroup.item()
                ValuePathDistanation = a + '/' + ValuePathDistanation
                #  перейдем к слудущему родителю
                # id_code_parent = scfg.df_DB_Specification[scfg.df_DB_Specification['id_code_item']==id_item]['id_code_parent']
                id_code_parent = scfg.df_DBS[scfg.df_DBS['id_code_e']==id_item]['id_code_parent']


            self.PathDistanation.set(ValuePathDistanation)
            # self.parent_DBE.set(t)
            # print(self.PathDistanation.get())
        return None

    def saveIncome (self):
        """
        запись данных окна/формы в БД прихода
        и в БД компонентов
        """
        amount = int(self.amount_DBEI.get())
        if amount >= 0 :
            connectionDB = sql3.connect(scfg.DBSqlite)
            cursorDB = connectionDB.cursor()
            with connectionDB:

                # создадим строку для БД прихода
                # вспомним id_component по полю name формы
                cursorDB.execute("""SELECT DBC.id, DBC.amount FROM DBC WHERE DBC.name=? ;""", (self.name_DBEI.get(),))
                row_from_DBC = cursorDB.fetchone()
                if row_from_DBC[0] >0:
                    # (date, id_component, amount, comments)
                    data_list_in_DBI = (
                        # self.dateStringDBEI.get(),         
                        row_from_DBC[0],
                        amount,  
                        self.ent_commentsStringDBE.get()
                    )
                    cursorDB.execute("""INSERT INTO DBI (date, id_component, amount, comments) VALUES (datetime('now'),?,?,?);""", data_list_in_DBI)
                    connectionDB.commit()
                    cursorDB.execute("""UPDATE DBC SET amount = ? WHERE id = ?;""", (row_from_DBC[1]+ int(self.amount_DBEI.get()), row_from_DBC[0] ))
            if (connectionDB):
                connectionDB.close()
            self.viewTreeI(treeF=self.treeF)
        
        # # и сольем ее с БД прихода
        # new_row_DBI = {
        #     'id_code_e': mdbc.getCode(),                    
        #     'id_code_item': self.id_code_item_DBEI,                 
        #     'name': self.name_DBEI.get(),                        
        #     'amount':self.amount_DBEI.get(), 
        #     'date':self.dateStringDBEI.get(),                        
        #     'id_code_parent':self.idCodeDistanation,
        #     # 'dist':self.PathDistanation.get(),
        #     'comments':self.ent_commentsStringDBE.get()             
        #     }
        # # пересоздадим добавление строки в DataFrame  как рекомендует Pandas 1.4.0. 22jan2022
        # df_new_row_DBI = pd.DataFrame(new_row_DBI, index=[0])
        # scfg.df_DBI = pd.concat([scfg.df_DBI, df_new_row_DBI])
        # #  переиндексируем DataFrame
        # scfg.df_DBI = scfg.df_DBI.reset_index(drop=True)
        # self.viewTreeI(treeF=self.treeF)#, DataFrameTree=scfg.df_DBI)

        # # изменим строку БД компонентов - количество , т.к. идет приход
        # # больше ничего менять в этой форме нельзя
        # df2 = scfg.df_DBC[scfg.df_DBC['id_code_item'] == self.id_code_item_DBEI]['amount']
        # amount_income = int(df2.item())
        # indx = df2.index[0]
        # amount_income += int(self.amount_DBEI.get())
        # df3 = scfg.df_DBC
        # scfg.df_DBC['amount'][indx]  = str(amount_income)
   
        return None

    def saveExpenditure (self):
        """
        запись данных окна/формы в БД расхода
        и в БД спецификаций
        """
        # создадим строку для БД расхода
        # и сольем ее с БД расхода
        new_row_DBE = {
            'id_code_e': mdbc.getCode(),                    
            'id_code_item': self.id_code_item_DBEI,                 
            'name': self.name_DBEI.get(),                        
            'amount':self.amount_DBEI.get(), 
            'date':self.dateStringDBEI.get(),                        
            'id_code_parent':self.idCodeDistanation,
            # 'dist':self.PathDistanation.get(),
            'comments':self.ent_commentsStringDBE.get()             
            }
        # пересоздадим добавление строки в DataFrame  как рекомендует Pandas 1.4.0. 22jan2022
        df_new_row_DBE = pd.DataFrame(new_row_DBE, index=[0])
        scfg.df_DBE = pd.concat([scfg.df_DBE, df_new_row_DBE])
        #  переиндексируем DataFrame
        scfg.df_DBE = scfg.df_DBE.reset_index(drop=True)
        self.viewTreeEI(treeF=self.treeF, DataFrameTree=scfg.df_DBE)

        # создадим строку для БД спецификаций
        # и сольем ее с БД спецификаций
        new_row_DBS = {
            'id_code_e':     mdbc.getCode(),
            'id_code_item':   self.id_code_item_DBEI,
            'name':          self.name_DBEI.get(), 
            'amount':        self.amount_DBEI.get(),
            'id_code_lvl':   '',              
            'id_code_parent':self.idCodeDistanation,
            'comments': self.ent_commentsStringDBE.get()               
            }
        # пересоздадим добавление строки в DataFrame  как рекомендует Pandas 1.4.0. 22jan2022
        df_new_row_DBS = pd.DataFrame(new_row_DBS, index=[0])
        scfg.df_DBS = pd.concat([scfg.df_DBS, df_new_row_DBS])
        #  переиндексируем DataFrame
        scfg.df_DBS = scfg.df_DBS.reset_index(drop=True)

        # изменим строку БД компонентов - количество , т.к. идет расход
        # больше ничего менять в этой форме нельзя
        df2 = scfg.df_DBC[scfg.df_DBC['id_code_item'] == self.id_code_item_DBEI]['amount']
        amount_income = int(df2.item())
        indx = df2.index[0]
        amount_income -= int(self.amount_DBEI.get())
        df3 = scfg.df_DBC
        scfg.df_DBC['amount'][indx]  = str(amount_income)
        # print (df3)

        return None







def Unpack_String_DataFrameDBE(DataFrameTree: pd.DataFrame, index: str):
    """
    Распаковка строки таблцицы DataFrama БД расходов на поля(столбцы)

    Выход:
    словарь с полями 'id_code_e', 'id_code_item', 'name', 'amount', 'date', 'id_code_parent', 'comments'
    
    """
    upsdf = {}
    upsdf['id_code_e'] = DataFrameTree.loc[index, 'id_code_e']
    upsdf['id_code_item'] = DataFrameTree.loc[index, 'id_code_item'] 
    upsdf['name'] = DataFrameTree.loc[index, 'name'] 
    upsdf['id_code_parent'] = DataFrameTree.loc[index, 'id_code_parent']
    upsdf['amount'] = DataFrameTree.loc[index, 'amount']
    upsdf['date'] = DataFrameTree.loc[index, 'date']
    upsdf['comments'] = DataFrameTree.loc[index, 'comments'] 
    return upsdf