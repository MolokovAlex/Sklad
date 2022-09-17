# module
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, N, NSEW, Menu
import tkinter.messagebox as mb
import sqlite3 as sql3

import modulAppGUI as mag
import skladConfig as scfg


class Window_Choice_Specification(tk.Toplevel):
    def __init__(self, parent): 
           
        # визуальное отображение окна выбора спецификации :
        # viewWindow = DBC = DataBaseComponents
        # viewWindow = DBS = DataBaseSpecification
        # режим работы окна - или "перемещнние " или "импорт"
        # modeWindow = 'remove'
        # modeWindow == 'import
                                                                        
        super().__init__(parent)
        # self.geometry("1024x600")
        opts = { 'ipadx': 3, 'ipady': 3 , 'sticky': 'nswe' }

        self.label_to = tk.Label(self, text="Выберите спецификацию...")    
        self.label_to.grid(row=0, column=0, **opts)

        self.frame_tableTreeGroup = tk.LabelFrame(master=self, text="Группы", relief=tk.SUNKEN, borderwidth=3)   #, height=50)
        self.frame_tableTreeGroup.grid(row=1, column=0,columnspan=2, **opts)

        
        self.btn_Remove = tk.Button(master=self, height=3, text="Вот эту!", command=self.fn_choice_Specification)
        self.btn_Remove.grid(row=2, column=0, **opts)
        self.btn_Cansel = tk.Button(master=self, height=3, text="Отмена", command=self.destroy)
        self.btn_Cansel.grid(row=2, column=1, **opts)

        self.treeGroup = ttk.Treeview(self.frame_tableTreeGroup, show="tree headings")#, columns=col) #self.columns)
        self.treeGroup.grid(row=0, column=1, rowspan=4, **opts)

        mag.Setting_TreeView(self.treeGroup, form = 'choice_specification')

        self.ysb = ttk.Scrollbar(self.frame_tableTreeGroup, orient=tk.VERTICAL, command=self.treeGroup.yview)
        self.treeGroup.configure(yscroll=self.ysb.set)
        self.ysb.grid(row=0, column=2, rowspan=4, **opts)

        self.treeGroup.bind('<<TreeviewSelect>>', self.on_select)

        self.new_parent = 0
        self.sel = 0
        
        mag.viewTreeGroupDBGS(self.treeGroup)       # отобразим данные из памяти DataFrame в TreeGroup с родителями
        return None

    def open(self):
        self.grab_set()
        self.wait_window()
        usr = self.new_parent
        return usr
    
    def fn_choice_Specification(self):
        self.new_parent = self.sel[0]
        self.destroy()
        return None

    def on_select(self, event):
        self.sel = self.treeGroup.selection()
        return None


class Window_Edit_Specification(tk.Toplevel):
    def __init__(self, parent, id_select): 
        super().__init__(parent)
        # self.geometry("1024x600")

        opts = { 'ipadx': 3, 'ipady': 3 , 'sticky': 'nswe' }
        self.create_frame_tableTreeGroup(opts = opts)
        self.create_frame_Input(opts = opts)

        self.btn_In = tk.Button(master=self, height=3, text="Запись строки спецификации", command=self.save_Row_in_Specification)
        self.btn_In.grid(row=3, column=0, **opts)
        self.btn_Cansel = tk.Button(master=self, height=3, text="Отмена", command=self.destroy)
        self.btn_Cansel.grid(row=3, column=1, **opts)

        # self.treeGroup.bind('<<TreeviewSelect>>', self.on_select)

        self.viewTreeEditSpecification(self.treeF)#, scfg.df_DBI)
        self.new_parent = 0
        self.sel = 0
        self.idCodeDistanation =''
        # self.PathDistanation=''

        return None

    def create_frame_tableTreeGroup(self, opts) -> None:
        self.frame_tableTreeGroup = tk.LabelFrame(master=self, text="Группы", relief=tk.SUNKEN, borderwidth=3) 
        self.frame_tableTreeGroup.grid(row=0, column=0, columnspan=2, **opts)
        self.treeF = ttk.Treeview(self.frame_tableTreeGroup, show="headings", height=20)#, columns=col) #self.columns)
        self.treeF.grid(row=0, column=0, rowspan=4, columnspan=6, **opts)
        # Установка и настройка столбцов компонента TreeView
        # Визуальная настройка
        self.treeF["columns"]=scfg.displayColumnsEditSpec.copy()
        a = scfg.displayColumnsE.copy()
        # for i in scfg.displayColumnsE:
        for i in a:
            self.treeF.heading(i, text=i)
            self.treeF.column(i, width=scfg.widthColunmsTreeWindowEditSpecification[i], stretch=True)
            # отобразим визуально только те столбцы, которые заложены в конфигуоационный модуль skladConfig.py
        self.treeF["displaycolumns"]=scfg.displayColumnsEditSpecification
        self.ysb = ttk.Scrollbar(self.frame_tableTreeGroup, orient=tk.VERTICAL, command=self.treeF.yview)
        self.treeF.configure(yscroll=self.ysb.set)
        self.ysb.grid(row=0, column=6, rowspan=4, **opts)
        
        return None

    def create_frame_Input(self, opts) -> None:
        self.id_code = tk.StringVar()
        # self.dateStringDBEI = tk.StringVar()
        # self.id_code_item_DBEI = ''
        self.name = tk.StringVar()
        # self.amount_DBEI = tk.StringVar()
        # self.UnitName = tk.StringVar()
        self.PathDistanation = tk.StringVar()
        # # self.id_code_parent_DBE = tk.StringVar()
        # self.commentsStringDBEI = tk.StringVar()
        # self.commentsStringDBE.trace("w", lambda: self.ent_commentsStringDBEself.commentsStringDBE.get())
        # self.parent_DBE = tk.StringVar()

            # 'id': [60], 
            # 'path_DBGS':[100], 
            # 'name': [400],  
            # 'cbe': [5],                      
            # 'amount':[50],  
            # 'units':[50],
            # 'comments':[100]


        self.frame_Input = tk.LabelFrame(master=self, text="Ввод строки спецификации", relief=tk.SUNKEN, borderwidth=3) 
        self.frame_Input.grid(row=1, column=0, columnspan=2, **opts)
        # поле для даты         width= В ЧИСЛЕ СИМВОЛОВ!!!!
        # self.ent_date = tk.Entry(master=self.frame_Input, textvariable=self.dateStringDBEI, width=10)
        self.ent_id = tk.Entry(master=self.frame_Input, textvariable=self.id_code, width=20, state="readonly")
        self.ent_id.grid(row=0, column=0, **opts)
        self.ent_PathDistanation = tk.Entry(master=self.frame_Input, textvariable=self.PathDistanation, width=60, state="readonly")
        self.ent_PathDistanation.grid(row=0, column=1, **opts)
        #  поле ввода имени комопнента
        self.ent_name = tk.Entry(master=self.frame_Input, textvariable=self.name, width=80, state="readonly")
        self.ent_name.grid(row=0, column=2, **opts)
        self.ent_name.insert(0, 'Нажать для ввода компонента')
        # если кликнуть по полю ввода компонента - попадаем на форму WindowEditComponent
        self.ent_name.bind('<Button-1>', lambda e: self.click_Ent_name_DBS(e))
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

        return None

    def viewTreeEditSpecification(self, treeF:ttk.Treeview)-> None:    
        """ Отображение таблицы спецификации"""

        # очистим все дерево компонентов            
        for i in treeF.get_children(): treeF.delete(i) 

         

        connectionDBFile = sql3.connect(scfg.DBSqlite)
        cursorDB = connectionDBFile.cursor()
        # with connectionDBFile:
        #     cursorDB.execute("""SELECT DBI.*, DBC.name FROM DBI JOIN DBC ON DBC.id = DBI.id_component;""")
        #     rows_from_DBI = cursorDB.fetchall()    
        #     for item_row in rows_from_DBI:
        #         id_DBI, date, id_component, amount, comments, name_component = item_row 
        #         # вытащим строку - получим из DBC у которых DBC.name=stringDF['name_component'] и приклеим название ед измерения
        #         cursorDB.execute("""SELECT DBC.id_parent, DBU.name FROM DBC JOIN DBU ON DBU.id = DBC.id_unit WHERE DBC.name=? ;""", (name_component,))
        #         id_parent_DBC, name_unit = cursorDB.fetchone()
        #         # вытащим строку - получим из DBG название группы:  у которых DBG.id=stringDF['id_parent']
        #         cursorDB.execute("""SELECT id,name,id_parent FROM DBG WHERE id=? ;""", (id_parent_DBC,))
        #         id_DBG, name_DBG, id_parent_DBG = cursorDB.fetchone()
        #         # построим полную строку пути по иерархии групп
        #         string_path = name_DBG
        #         id_next_DBG = id_parent_DBG
        #         while id_DBG !=1:
        #             # вытащим строку - получим из DBG название родителя:  у которых DBG.id=row_from_DBG[2]
        #             cursorDB.execute("""SELECT * FROM DBG WHERE DBG.id=? ;""", (id_next_DBG,))
        #             id_DBG, name_parent, id_next_DBG = cursorDB.fetchone()
        #             string_path = name_parent + '/' + string_path
                
        #         treeF.insert('', 'end',  id_DBI, text=name_component, values=[id_DBI, date, name_component, amount, name_unit, string_path, comments])

        if(connectionDBFile):
            connectionDBFile.close()

        
        return None

    def click_Ent_name_DBS(e)-> None:

        return None

    def save_Row_in_Specification() -> None:

        return None