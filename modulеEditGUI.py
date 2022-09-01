# modulеEditGUI
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# модуль держатель элементов GUI для редактирования компонентов склада


import os
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, N, NSEW, Menu
import tkinter.messagebox as mb
import pandas as pd
# importing re for regular expressions
import re
import numpy as np

import skladConfig as scfg
import moduleSQLite as msql
import moduleDBClass as mdbc
import moduleImport as mi
import moduleExport as me
import modulAppGUI as mag


class WindowEditComponent(tk.Toplevel):
    def __init__(self, parent, modeWindow, viewDB):  
        # viewDB - отображение в окне БД:
        # viewDB = 'DBC' = DataBaseComponents
        # viewDB = 'DBS' = DataBaseSpecification   
        # modeWindow - внешний вид и расположени кнопок окна в режимах:
        # modeWindow = 'edit'
        # modeWindow = 'comp_in_spec'
        # modeWindow = 'expenditure'  - режим окна Расход компонента

        super().__init__(parent)
        # self.geometry("1100x700")
        self.widthscreen = self.winfo_screenwidth()-30    # размеры экрана
        self.heigthscreen = self.winfo_screenheight()-100
        self.geometry('{}x{}+5+5'.format(self.widthscreen, self.heigthscreen))

        self.ImageDelete = tk.PhotoImage(file = scfg.icon_button_delete)
        self.ImageRemove = tk.PhotoImage(file = scfg.icon_button_remove)
        self.ImageRename = tk.PhotoImage(file = scfg.icon_button_rename)
        self.ImageEdit =   tk.PhotoImage(file = scfg.icon_button_edit )

        #self.protocol("WM_DELETE_WINDOW", self.confirm_delete)
        opts = { 'ipadx': 3, 'ipady': 3 , 'sticky': 'nswe' }

        self.frame_search = tk.LabelFrame (master=self, text="Поиск", relief=tk.SUNKEN, borderwidth=3, height=10)
        self.frame_search.grid(row=0, column=0, columnspan=4, **opts)

        self.frame_NameComponent = tk.LabelFrame(master=self, text="Наименование", relief=tk.SUNKEN, borderwidth=3, height=10)
        self.frame_NameComponent.grid(row=1, column=0, columnspan=4, **opts)

        self.frame_Dimension = tk.LabelFrame(master=self, text="Единица измерения", relief=tk.SUNKEN, borderwidth=3, height=10, width= 80)
        self.frame_Dimension.grid(row=2, column=0, **opts)

        self.frame_1C = tk.LabelFrame(master=self, text="1C", relief=tk.SUNKEN, borderwidth=3, height=10, width= 150)
        self.frame_1C.grid(row=2, column=1, **opts)

        self.frame_Image = tk.LabelFrame(master=self, text="Изображение", relief=tk.SUNKEN, borderwidth=3, height=10, width= 150)
        self.frame_Image.grid(row=2, column=2, **opts)

        self.frame_TreeGroup = tk.LabelFrame(master=self, text="Группы", relief=tk.SUNKEN, borderwidth=3)  
        self.frame_TreeGroup.grid(row=3, column=0, **opts)

        self.frame_TreeComponents = tk.LabelFrame(master=self, text="Компоненты", relief=tk.SUNKEN, borderwidth=3)  
        self.frame_TreeComponents.grid(row=3, column=1, columnspan=2,  **opts)

        self.btn_RenameGroup = tk.Button(master=self.frame_TreeGroup, text="Изм\n груп", command=lambda m='group', vDB = viewDB: self.fn_rename_Component(mode = m, viewDB = vDB))
        self.btn_EditGroup = tk.Button(master=self.frame_TreeGroup, text="Доб\n  груп", command=lambda m='group', vDB = viewDB: self.fn_add_Components(mode = m, viewDB = vDB))
        self.btn_DeleteGroup = tk.Button(master=self.frame_TreeGroup, text="Уд\n  груп", command=lambda m='group', vDB = viewDB: self.fn_delete_Components(mode = m, viewDB = vDB))
        self.btn_RemoveGroup = tk.Button(master=self.frame_TreeGroup, text="Пере\n  груп", command=lambda m='group', vDB = viewDB: self.fn_remove_Components(mode = m, viewDB = vDB))
        
        self.btn_RenameGroup.grid(row=0, column=0, **opts)
        self.btn_EditGroup.grid(row=1, column=0, **opts)
        self.btn_DeleteGroup.grid(row=2, column=0, **opts)
        self.btn_RemoveGroup.grid(row=3, column=0, **opts)
        if (viewDB == 'DBC') and (modeWindow == 'expenditure'):
            self.btn_RenameGroup.grid_remove()
            self.btn_RemoveGroup.grid_remove()
            self.btn_DeleteGroup.grid_remove()
            self.btn_EditGroup.grid_remove()

        # self.btn_RenameGroup.config(image=self.ImageRename,width="25",height="25")
        # self.btn_EditGroup.config(image=self.ImageEdit,width="25",height="25")
        # self.btn_DeleteGroup.config(image=self.ImageDelete,width="25",height="25")
        # self.btn_RemoveGroup.config(image=self.ImageRemove,width="25",height="25")
        
        # self.btn_DeleteComp = tk.Button(master=self.frame_TreeComponents, command=lambda m='comp', vDB = viewDB: self.fn_delete_Components(mode = m, viewWind = vDB))
        # DBC = DataBaseComponents
        # DBS = DataBaseSpecification
        if (viewDB == 'DBC') and (modeWindow == 'edit'):
            self.btn_EditComp = tk.Button(master=self.frame_TreeComponents, height=1, text="Доб.",command=lambda mW='comp', vDB = viewDB: self.fn_add_Components(mode = mW, viewDB = vDB))
            self.btn_RenameComp = tk.Button(master=self.frame_TreeComponents, height=1, text="Изм.", command=lambda mW='comp', vDB = viewDB: self.fn_rename_Component(mode = mW, viewDB = vDB))
            self.btn_DeleteComp = tk.Button(master=self.frame_TreeComponents, text="Удал", command=lambda mW='comp', vDB = viewDB: self.fn_delete_Components(mode = mW, viewDB = vDB))
            self.btn_RemoveComp = tk.Button(master=self.frame_TreeComponents, height=1, text="Пере", command=lambda mW='comp', vDB = viewDB: self.fn_remove_Components(mode = mW, viewDB = vDB))
        elif (viewDB == 'DBC') and (modeWindow == 'expenditure'):
            self.btn_EditComp = tk.Button(master=self.frame_TreeComponents, height=1)#, command=self.fn_choice_comp_in_expenditure)
            self.btn_RenameComp = tk.Button(master=self.frame_TreeComponents, height=1,  command=self.clicked)
            self.btn_RemoveComp = tk.Button(master=self.frame_TreeComponents, height=1,  command=self.clicked)
        elif (viewDB == 'DBS') and (modeWindow == 'edit'): 
            self.btn_EditComp = tk.Button(master=self.frame_TreeComponents, height=1, text="Доб\n  в сп",command=lambda mW='comp_in_spec', vDB = viewDB: self.open_Window_Comp_in_Spec(modeWindow = mW, viewDB = vDB))
        elif (viewDB == 'DBS') and (modeWindow == 'comp_in_spec'): 
            self.btn_EditComp = tk.Button(master=self.frame_TreeComponents, height=1, text="Выбр",command=lambda mW='comp_in_spec', vDB = viewDB: self.fn_choice_comp_in_spec(modeWindow = mW, viewDB = vDB))
            self.btn_RenameComp = tk.Button(master=self.frame_TreeComponents, height=1, text="----", command=self.clicked)
            self.btn_RemoveComp = tk.Button(master=self.frame_TreeComponents, height=1, text="----", command=self.clicked)

        self.btn_RenameComp.grid(row=0, column=0, **opts)
        self.btn_EditComp.grid(row=1, column=0, **opts)
        self.btn_DeleteComp.grid(row=2, column=0, **opts)
        self.btn_RemoveComp.grid(row=3, column=0, **opts)
        if (viewDB == 'DBC') and (modeWindow == 'expenditure'):
            self.btn_RenameComp.grid_remove()
            self.btn_RemoveComp.grid_remove()
            self.btn_DeleteComp.grid_remove()
            self.btn_EditComp.config(image=self.ImageEdit,width="25",height="25", text="Выбр", command=self.fn_choice_comp_in_expenditure)
        # self.btn_RenameComp.config(image=self.ImageRename,width="25",height="25")
        # self.btn_EditComp.config(image=self.ImageEdit,width="25",height="25")
        # self.btn_DeleteComp.config(image=self.ImageDelete,width="25",height="25")
        # self.btn_RemoveComp.config(image=self.ImageRemove,width="25",height="25")

        self.rowconfigure(0, weight=0, minsize=5)
        self.rowconfigure(1, weight=0, minsize=5)
        self.rowconfigure(2, weight=0, minsize=5)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)


        self.ent_search = tk.Entry(master=self.frame_search )
        self.btn_search = tk.Button(master=self.frame_search, text="Искать", command=lambda mW='comp', vDB = viewDB: self.fn_search(modeWindow = mW, viewDB = vDB))
        # elf.btn_EditComp = tk.Button(master=self.frame_TreeComponents, height=1, text="Выбр",command=lambda mW='comp_in_spec', vDB = viewDB: self.fn_choice_comp_in_spec(modeWindow = mW, viewDB = vDB))
        # self.ent_search.pack(fill=tk.X, expand=1, side=tk.LEFT, ipadx=5, ipady=5)
        # self.btn_search.pack(fill=tk.X, expand=0, side=tk.LEFT, ipadx=5, ipady=5)
        self.ent_search.config(width="100")
        self.btn_search.config(width="100")
        self.ent_search.grid(row=0, column=0, **opts)
        self.btn_search.grid(row=0, column=1, **opts)
        

        self.ent_NameComponent = tk.Entry(master=self.frame_NameComponent)
        self.ent_NameComponent.pack(fill=tk.X, expand=1, side=tk.LEFT, ipadx=5, ipady=5)

        self.name_unit = tk.StringVar()
        # self.name_unit.set(scfg.UnitsCodeName['1699'])   # default value

        # a = msql.query_name_from_DBU_where_id()#, query = scfg.id_default_DBU)
        self.name_unit.set(msql.query_name_from_DBU_where_id())

        self.lbl_name_units = tk.Label(master=self.frame_Dimension, text="Ед измерения:") 
        # self.CB_name_units = ttk.Combobox(self.frame_Dimension, values=list(scfg.UnitsCodeName.values()), textvariable = self.name_unit, width=5)
        # b = msql.query_all_name_from_DBU()
        self.CB_name_units = ttk.Combobox(self.frame_Dimension, values=msql.query_all_name_from_DBU(), textvariable = self.name_unit, width=5)        

        self.lbl_amount = tk.Label(master=self.frame_Dimension, text="Количество на складе ПУ:") 
        self.lbl_Namount = tk.Label(master=self.frame_Dimension, text="_______") 

        self.lbl_min_rezerve = tk.Label(master=self.frame_Dimension, text="Мин. количество на складе:") 
        self.ent_min_rezerve = tk.Entry(master=self.frame_Dimension )

        self.lbl_code_1C = tk.Label(master=self.frame_1C, text="Код по базе 1С")
        self.ent_code_1C = tk.Entry(master=self.frame_1C )

        self.lbl_name_1C = tk.Label(master=self.frame_1C, text="Наименование по базе 1С")
        self.ent_name_1C = tk.Entry(master=self.frame_1C )

        self.lbl_articul_1C = tk.Label(master=self.frame_1C, text="Артикул компонента по базе 1С по базе 1С")
        self.ent_articul_1C = tk.Entry(master=self.frame_1C )

        self.lbl_name_units.grid(row=0, column=0, **opts)
        self.CB_name_units.grid(row=0, column=1, **opts)
        self.lbl_amount.grid(row=1, column=0, **opts)
        self.lbl_Namount.grid(row=1, column=1, **opts)
        self.lbl_min_rezerve.grid(row=2, column=0, **opts)
        self.ent_min_rezerve.grid(row=2, column=1, **opts)
        self.lbl_code_1C.grid(row=0, column=0, **opts)
        self.ent_code_1C.grid(row=0, column=1, **opts)
        self.lbl_name_1C.grid(row=1, column=0, **opts)
        self.ent_name_1C.grid(row=1, column=1, **opts)
        self.lbl_articul_1C.grid(row=2, column=0, **opts)
        self.ent_articul_1C.grid(row=2, column=1, **opts)

        self.treeGroup = ttk.Treeview(self.frame_TreeGroup, show="tree headings")
        self.treeGroup.grid(row=0, column=1, rowspan=4, **opts)
        mag.Setting_TreeView(self.treeGroup, form = 'short')
        self.ysb = ttk.Scrollbar(self.frame_TreeGroup, orient=tk.VERTICAL, command=self.treeGroup.yview)
        self.treeGroup.configure(yscroll=self.ysb.set, height= 33)
        self.ysb.grid(row=0, column=2, rowspan=4, **opts)
        self.treeGroup.bind('<<TreeviewSelect>>', lambda e, mW=modeWindow, vW=viewDB: self.on_select_TreeGroup(e, modeWindow = mW, viewDB = vW))

        self.tree2 = ttk.Treeview(self.frame_TreeComponents, show="tree headings") #, columns=self.columns2)
        self.tree2.grid(row=0, column=1, rowspan=4, **opts)
        mag.Setting_TreeView(self.tree2, form = 'full')
        self.ysb2 = ttk.Scrollbar(self.frame_TreeComponents, orient=tk.VERTICAL, command=self.tree2.yview)
        self.ysb2.grid(row=0, column=2, rowspan=4, **opts)
        self.tree2.configure(yscroll=self.ysb2.set, height= 33)
        self.tree2.bind('<<TreeviewSelect>>', lambda e, mW=modeWindow, vW=viewDB: self.on_select_TreeComponents(e, modeWindow = mW, viewDB = vW))
    
        self.id_code_itemElement = 0
        # здесь храним содержимое 'id_code_item' выделенного элемнта в любой Tree  
        self.selection_item = 0
        self.selection_item_Group = 0
        # DBC = DataBaseComponents   
        # DBS = DataBaseSpecification   
        if viewDB == 'DBC':   dataFrame_in = scfg.df_DBC
        elif (viewDB == 'DBS') and (modeWindow == 'edit'): dataFrame_in = scfg.df_DBS   
        elif (viewDB == 'DBS') and (modeWindow == 'comp_in_spec'): dataFrame_in = scfg.df_DBC   
        mag.viewTreeGroup(self.treeGroup, dataFrame_in)       # отобразим данные из памяти DataFrame в TreeGroup с родителями

            
        return None   

    def clicked(self):
        return None

    def open_Window_Remove_Component(self, modeWindow, viewDB): 
        new_id_prnt = 0
        vW = viewDB
        mW = modeWindow
        mW = 'remove'
        wior = mi.Window_Import_OR_Remove(self, modeWindow = mW, viewDB = vW)
        new_id_prnt = wior.open()
        # wrc.grab_set()                      #  чтобы окно получало все события
        # self.text_box.insert(tk.END, "open_WindowRemoveComponent"+"\n")

        # new_id_prnt = wrc.new_parent
        return new_id_prnt

    def on_select_TreeGroup(self, event,  modeWindow, viewDB):
        if viewDB == 'DBC':   dataFrame_in = scfg.df_DBC
        elif (viewDB == 'DBS') and (modeWindow == 'edit'): dataFrame_in = scfg.df_DBS
        elif (viewDB == 'DBS') and (modeWindow == 'comp_in_spec'): dataFrame_in = scfg.df_DBC
        self.selection_item_Group = self.treeGroup.selection()[0]
        dic = self.treeGroup.item(self.selection_item_Group)
        self.ent_NameComponent.delete(0, END)
        self.ent_NameComponent.insert(0, dic['text'])
        mag.viewTreeComponents(self.tree2, dataFrame_in, self.selection_item_Group)
        self.treeGroup.see(self.selection_item_Group)

        # при выделении группы отключим лишние элементы на форме
        self.lbl_Namount.config(text='')
        self.ent_min_rezerve.delete(0, END)
        self.ent_min_rezerve.config(state='disabled')
        self.name_unit.set(scfg.UnitsCodeName['1699'])
        self.CB_name_units.config(state='disable')
        self.ent_code_1C.delete(0, END)
        self.ent_code_1C.config(state='disabled')
        self.ent_name_1C.delete(0, END)
        self.ent_name_1C.config(state='disabled')
        self.ent_articul_1C.delete(0, END)
        self.ent_articul_1C.config(state='disabled')

        return None

    def on_select_TreeComponents(self, event,  modeWindow, viewDB):
        """
        При выделении компонента в дереве Компонетнов
         - поймем с каким DataFramом работаем
         - получим поле id_code_item выделенного этемента
         - зная id_code_item получим поле 'name' из DataFrame и отобразим его на форме
         - зная id_code_item получим поля 'amount', 'code_units', 'min_rezerve', 'articul_1C', 'code_1C', 'name_1C' из DataFrame и отобразим их на форме
        """
        # при выделении компонентов включим отключенные элементы на форме
        self.ent_min_rezerve.config(state='normal')
        self.CB_name_units.config(state='normal')
        self.ent_code_1C.config(state='normal')
        self.ent_name_1C.config(state='normal')
        self.ent_articul_1C.config(state='normal')

        stringDF = {}
        if viewDB == 'DBC':   dataFrame_in = scfg.df_DBC
        elif (viewDB == 'DBS') and (modeWindow == 'edit'): dataFrame_in = scfg.df_DBS
        elif (viewDB == 'DBS') and (modeWindow == 'comp_in_spec'): dataFrame_in = scfg.df_DBC
        id_code_item = self.tree2.selection()[0]
        self.selection_item = self.tree2.selection()[0]
        indx = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item].index[0]   
        # indx = df2.index[0]
        stringDF = mag.Unpack_String_DataFrame(dataFrame_in, indx)
        self.ent_NameComponent.delete(0, END)
        self.ent_NameComponent.insert(0, stringDF['name'])
        self.lbl_Namount.config(text=stringDF['amount'])
        self.ent_min_rezerve.delete(0, END)
        self.name_unit.set(stringDF['UnitsName'])

        self.ent_min_rezerve.insert(0, stringDF['min_rezerve'])
        self.ent_articul_1C.delete(0, END)
        self.ent_articul_1C.insert(0, stringDF['articul_1C'])
        self.ent_code_1C.delete(0, END)
        self.ent_code_1C.insert(0, stringDF['code_1C'])
        self.ent_name_1C.delete(0, END)
        self.ent_name_1C.insert(0, stringDF['name_1C'])
        # self.ent_NameComponent.insert(0, stringDF['name'].item())
        # self.lbl_Namount.config(text=stringDF['amount'].item())
        # self.ent_min_rezerve.delete(0, END)
        # self.ent_min_rezerve.insert(0, stringDF['min_rezerve'].item())
        # self.ent_articul_1C.delete(0, END)
        # self.ent_articul_1C.insert(0, stringDF['articul_1C'].item())
        # self.ent_code_1C.delete(0, END)
        # self.ent_code_1C.insert(0, stringDF['code_1C'].item())
        # self.ent_name_1C.delete(0, END)
        # self.ent_name_1C.insert(0, stringDF['name_1C'].item())

        # для поиска нужно при выделении в TreeComponents - обновлялось TreeGroup
        mag.viewTreeGroup(self.treeGroup, dataFrame_in)# возьмем его родителя
        id_code_parent = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item]['id_code_parent'].item()
        # распахнуть TreeGroup на родителе выделенного элемента в TreeComponents
        self.treeGroup.see(id_code_parent)
        # self.treeGroup.focus(id_code_parent)
        self.treeGroup.selection_set(id_code_parent)
        return None

    def open_WindowTree(self, modeWindow, viewDB):
        """
        открытие окна с целевым деревом - "куда" нужно поместить/переместить/списать компонент
        """
        vW = viewDB
        mW = modeWindow
        wt = mag.WindowTree(self, modeWindow = mW, viewDB = 'DBS')


        return None

    def fn_choice_comp_in_expenditure(self):
        self.new_parent = self.tree2.selection()[0]
        self.destroy()
        return None

    def fn_choice_comp_in_spec(self, modeWindow, viewDB):
        self.id_code_itemElement = self.tree2.selection()[0]
        # self.new_parent = self.sel[0]
        self.destroy()
        return None

    def open_Window_Comp_in_Spec(self, modeWindow, viewDB):
        id_code_item_group = self.treeGroup.selection()[0]
        # получим от родителя  строку 'id_code_lvl'
        df2 = scfg.df_DBS[scfg.df_DBS['id_code_item'] == id_code_item_group]['id_code_lvl']
        id_lvl_group = df2.item()
        id_code_elem = 0
        vW = viewDB
        mW = modeWindow
        # mW = 'remove'
        wec = WindowEditComponent(self, modeWindow = mW, viewDB = vW)
        id_code_elem = wec.open()
        # получаем индекс по 'id_code_item' выделенного элемента
        df3 = scfg.df_DBC[scfg.df_DBC['id_code_item'] == id_code_elem]   
        indx_elem = df3.index
        # изменяем код родителя компонента в DataFrame по индексу
        df3.loc[indx_elem, 'id_code_parent'] = id_code_item_group
        # df3.loc[indx_elem, 'id_code_lvl'] = id_lvl_group
        # добавить в группу Спецификации этот компоннт
        df_new_row = pd.DataFrame(df3, index=[0])
        # scfg.df_DB_Specification = pd.concat([scfg.df_DB_Specification, df_new_row])
        scfg.df_DBS = pd.concat([scfg.df_DBS, df3])
        #  переиндексируем DataFrame
        scfg.df_DBS = scfg.df_DBS.reset_index(drop=True)
        
        if (viewDB == 'DBS') and (modeWindow == 'comp_in_spec'): dataFrame_in = scfg.df_DBS
        mag.viewTreeGroup(self.treeGroup, dataFrame_in)
        self.treeGroup.see(id_code_item_group)
        self.treeGroup.selection_set(id_code_item_group)
        mag.viewTreeComponents(self.tree2, dataFrame_in, id_code_item_group)
        return id_code_elem

    def open(self):
        self.grab_set()
        self.wait_window()
        # usr = self.id_code_itemElement
        usr  = self.new_parent 
        return usr
    
    def fn_search(self, modeWindow, viewDB):
        if viewDB == 'DBC':   dataFrame_in = scfg.df_DBC
        elif viewDB == 'DBS': dataFrame_in = scfg.df_DBS
        search_str = self.ent_search.get()
        # df2 = dataFrame_in.isin(search_str)

        stringDF = {}
        # выдать всех у кого в родителях код parent
        # df2 = dataFrame_in[dataFrame_in['id_code_parent'] == parent]   

        # очистим все дерево компонентов            
        for i in self.tree2.get_children(): self.tree2.delete(i)      
        # заполним дерево
        if not(dataFrame_in.empty):
                for indx in dataFrame_in.index:
                    sf2 = dataFrame_in.loc[indx]
                    sf3 = sf2.str.contains(search_str,flags=re.IGNORECASE, regex=True).to_list()
                    for i in sf3:
                        if i:

                            stringDF = mag.Unpack_String_DataFrame(dataFrame_in, indx)
                            if stringDF['id_code_lvl'] in scfg.listOfLevel:
                                ...
                            else:
                                id_code_item = int(stringDF['id_code_item'])
                                # # извлекем наименование ед изм - возмем по коду 'id_code_item' из DBCU
                                UnitsName = stringDF['UnitsName']
                                # treeF.insert('', 'end',  id_code_item, text=name, values=[id_code_item, amount, code_units, min_rezerve, articul_1C, code_1C, name_1C, id_code_parent, id_code_lvl])
                                self.tree2.insert('', 'end',  id_code_item, text=stringDF['name'], values=[stringDF['id_code_item'], stringDF['amount'], UnitsName, stringDF['min_rezerve'], stringDF['articul_1C'], stringDF['code_1C'], stringDF['name_1C'], stringDF['id_code_parent'], stringDF['id_code_lvl']])
                                break


        return None

    def fn_remove_Components(self, mode, viewDB):
        if viewDB == 'DBC':   dataFrame_in = scfg.df_DBC
        elif viewDB == 'DBS': dataFrame_in = scfg.df_DBS
        # запомним 'id_code_item' элемента из treeGroup
        # получаем индекс и 'id_code_item' выделенного элемента
        if mode == 'comp':
            id_code_item = self.selection_item
        elif mode == 'group':
            id_code_item = self.selection_item_Group
        # получаем индекс по 'id_code_item' выделенного элемента
        indx = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item].index       
        # выводим окно в котором спрашваем куда в дереве переместить
        # в ответ получаем  'id_code_parent' нового родителя
        new_id_code_parent = self.open_Window_Remove_Component(modeWindow = mode, viewDB = viewDB)
        # проверим - если этот код родителя тот же самый selTreeGroup - ничего не делаем
        if (new_id_code_parent != id_code_item) and (new_id_code_parent != 0):
            # изменяем код родителя компонента в DataFrame по индексу
            dataFrame_in.loc[indx, 'id_code_parent'] = new_id_code_parent
            # и выводим его заново имитируя выбор TreeView родителя            
            mag.viewTreeGroup(self.treeGroup, dataFrame_in)
            self.treeGroup.see(new_id_code_parent)
            self.treeGroup.selection_set(new_id_code_parent)
            mag.viewTreeComponents(self.tree2, dataFrame_in, new_id_code_parent)
            # сохраняем изменненный DataFame в файл
            me.Save_DataFrame_in_PickleFile()
            if viewDB == 'DBC':   scfg.df_DBC = dataFrame_in
            elif viewDB == 'DBS': scfg.df_DBS = dataFrame_in
        
        return None

    def fn_rename_Component(self, mode, viewDB):
        """
        функция Измениия Компонента|Группы в DBC|DBS
        """
        if viewDB == 'DBC':   dataFrame_in = scfg.df_DBC
        elif viewDB == 'DBS': dataFrame_in = scfg.df_DBS
        # запомним родителя из treeGroup - не всегда срабатывает, т.к. теряется фокус!!!!!!!!!!!
        # id_code_item = self.treeGroup.selection()
        # сделаем по другому - в дереыекомпонетнов всегда кто-то выделен
        # получаем индекс и 'id_code_item' выделенного элемента
        if mode == 'comp':
            id_code_item = self.selection_item
        elif mode == 'group':
            id_code_item = self.selection_item_Group
        indx = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item].index   
        # возьмем его родителя
        id_code_parent = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item]['id_code_parent'].item()
        # получаем измененное наименование из self.ent_NameComponent
        # найдем по значению name_unit значение code_unit
        new_name_unit = self.name_unit.get()
        for code_units in scfg.UnitsCodeName:
            if new_name_unit == scfg.UnitsCodeName[code_units]: break

        # И наконец - изменяем поля выбраного компонента в соответвии с данными формы :
        dataFrame_in.loc[indx, 'name'          ] = self.ent_NameComponent.get()
        dataFrame_in.loc[indx, 'code_units'    ] = code_units
        dataFrame_in.loc[indx, 'min_rezerve'   ] = self.ent_min_rezerve.get()
        dataFrame_in.loc[indx, 'articul_1C'    ] = self.ent_articul_1C.get()
        dataFrame_in.loc[indx, 'code_1C'       ] = self.ent_code_1C.get()
        dataFrame_in.loc[indx, 'name_1C'       ] = self.ent_name_1C.get()

        # добавим|изменим запись в DBCU
        # проверим есть ли такой столбец в df_DBCU
        # если есть - изменяем
        # если нет (странно) - добавляем и печатаем в консоль код ошибки
        # сформируем строку
        # и запищем ее в DBCU
        df2 = scfg.df_DBCU[scfg.df_DBCU['id_code_item'] == id_code_item]
        if not df2.empty:
            scfg.df_DBCU.loc[df2.index, 'code_units'] = code_units
        else:
            new_row_in_DBCU = {'id_code_item': id_code_item, 'code_units' : code_units} 
            df_new_row = pd.DataFrame(new_row_in_DBCU, index=[0])
            scfg.df_DBCU = pd.concat([scfg.df_DBCU, df_new_row])
            scfg.df_DBCU = scfg.df_DBCU.reset_index(drop=True)
            print ('Error 435 !!!')

        # и выводим его заново имитируя выбор TreeView родителя
        if mode == 'comp': viewID =  id_code_parent
        elif mode == 'group': viewID =  id_code_item
        mag.viewTreeGroup(self.treeGroup, dataFrame_in)
        self.treeGroup.see(viewID)
        self.treeGroup.selection_set(viewID)
        mag.viewTreeComponents(self.tree2, dataFrame_in, viewID)

        # сохраняем изменненный DataFame в файл
        me.Save_DataFrame_in_PickleFile()
        if viewDB == 'DBC':   scfg.df_DBC = dataFrame_in
        elif viewDB == 'DBS': scfg.df_DBS = dataFrame_in
        return None

    def fn_add_Components(self, mode, viewDB):
        """
    
        при добавлении группы - выделеный объект становиться родителем

        при добавлении комопнента или группы - происходит запись в DBCU
        """        
        if viewDB == 'DBC':   dataFrame_in = scfg.df_DBC
        elif viewDB == 'DBS': dataFrame_in = scfg.df_DBS
        # запомним родителя из treeGroup - не всегда срабатывает, т.к. теряется фокус!!!!!!!!!!!
        # id_code_item = self.treeGroup.selection()
        # сделаем по другому - в дереыекомпонетнов всегда кто-то выделен
        if mode == 'comp':
            if self.selection_item != 0:
                id_code_item = self.selection_item
                # id_lvl = np.NaN
                
                # возьмем его родителя
                id_code_parent = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item]['id_code_parent'].item()
            else:
                id_code_parent = self.selection_item_Group
                # id_code_parent = dataFrame_in[dataFrame_in['id_code_item'] == self.selection_item_Group]['id_code_parent'].item()
            id_lvl = ''
            # code_units = self.name_unit.get()
            # получаем измененное наименование из self.ent_NameComponent
            # найдем по значению name_unit значение code_unit
            new_name_unit = self.name_unit.get()
            for code_units in scfg.UnitsCodeName:
                if new_name_unit == scfg.UnitsCodeName[code_units]: break
        elif mode == 'group':
            id_code_item = self.selection_item_Group
            # получим от родителя  строку 'id_code_lvl'
            id_lvl = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item]['id_code_lvl'].item()
            # id_lvl = df2.item()
            # он сам становиться родителем для новой группы
            id_code_parent = id_code_item
            # определим какой позиции соответвует текущий lvl в списке listOfLevel
            # и увеличим уровень lvl на более глубокий
            for i in range (0, len(scfg.listOfLevel), 1):
                if scfg.listOfLevel[i] == id_lvl: break
            id_lvl = scfg.listOfLevel[i+1]
            code_units = '1699'
        
        # получаем новое наименование из self.ent_NameComponent
        # newNameComponent = self.ent_NameComponent.get()
        # сгенерим для него уникальный код
        codeItem = mdbc.getCode()
        # сформируем строку для DataFrame
        new_row_in_DBC = {
            'id_code_item':     codeItem, 
            'name':             self.ent_NameComponent.get(), 
            'amount':           '0', 
            'code_units' :      code_units, 
            'min_rezerve':      self.ent_min_rezerve.get(), 
            'articul_1C':       self.ent_articul_1C.get(), 
            'code_1C':          self.ent_code_1C.get(), 
            'name_1C':          self.ent_name_1C.get(), 
            'id_code_parent':   id_code_parent, 
            'id_code_lvl':      id_lvl
            } 
        # scfg.df1 = scfg.df1.append(new_row, ignore_index=True)
        # пересоздадим добавление строки в DataFrame  как рекомендует Pandas 1.4.0. 22jan2022
        df_new_row = pd.DataFrame(new_row_in_DBC, index=[0])
        dataFrame_in = pd.concat([dataFrame_in, df_new_row])
        #  переиндексируем DataFrame
        dataFrame_in = dataFrame_in.reset_index(drop=True)
        # добавим запись в DBCU
        # сформируем строку
        # и запищем ее в DBCU
        new_row_in_DBCU = {'id_code_item': codeItem, 'code_units' : code_units} 
        df_new_row = pd.DataFrame(new_row_in_DBCU, index=[0])
        scfg.df_DBCU = pd.concat([scfg.df_DBCU, df_new_row])
        scfg.df_DBCU = scfg.df_DBCU.reset_index(drop=True)
        # и выводим его заново имитируя выбор TreeView родителя
        if mode == 'comp': viewID =  id_code_parent
        elif mode == 'group': viewID =  codeItem
        mag.viewTreeGroup(self.treeGroup, dataFrame_in)
        self.treeGroup.see(viewID)
        self.treeGroup.selection_set(viewID)
        mag.viewTreeComponents(self.tree2, dataFrame_in, viewID)
        # сохраняем изменненный DataFame в файл
        me.Save_DataFrame_in_PickleFile()
        if viewDB == 'DBC':   scfg.df_DBC = dataFrame_in
        elif viewDB == 'DBS': scfg.df_DBS = dataFrame_in
        return None

    def fn_delete_Components(self, mode, viewDB):
        if viewDB == 'DBC':   dataFrame_in = scfg.df_DBC
        elif viewDB == 'DBS': dataFrame_in = scfg.df_DBS
        # запомним родителя из treeGroup - не всегда срабатывает, т.к. теряется фокус!!!!!!!!!!!
        # id_code_item = self.treeGroup.selection()
        # сделаем по другому - в дереыекомпонетнов всегда кто-то выделен

        # если удаляем комонент
        if mode == 'comp':
            id_code_item = self.selection_item
            # возьмем его родителя
            id_code_parent = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item]['id_code_parent'].item()
            # получаем индекс и 'id_code_item' выделенного элемента
            # удаляем его из DataFrame по индексу
            #  переиндексируем DataFrame
            indx = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item].index   
            dataFrame_in = dataFrame_in.drop(index=indx)
            dataFrame_in = dataFrame_in.reset_index(drop=True)
            # и выводим его заново имитируя выбор TreeView родителя
            # mag.viewTreeGroup(self.treeGroup, dataFrame_in)
            # self.treeGroup.see(id_code_parent)
            # mag.viewTreeComponents(self.tree2, dataFrame_in, id_code_parent)
            # сохраняем изменненный DataFame в файл
            # me.Save_DataFrame_in_PickleFile()
        #  если удаляем группу
        elif mode == 'group':
            id_code_item = self.selection_item_Group
            #
            # возьмем его родителя
            id_code_parent = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item]['id_code_parent'].item()

            # постмотрим, есть ли у выделенного родителя потомки
            df2 = dataFrame_in[dataFrame_in['id_code_parent'] == id_code_item]
            # пустая ли таблица df2?-  да, пуста -нет потомков - удаляем группу
            if df2.empty:
                indx = dataFrame_in[dataFrame_in['id_code_item'] == id_code_item].index
                # удаляем его из DataFrame по индексу
                #  переиндексируем DataFrame
                dataFrame_in = dataFrame_in.drop(index=indx)
                dataFrame_in = dataFrame_in.reset_index(drop=True)
                # очищаем дерево
                for i in self.tree2.get_children(): self.tree2.delete(i)
                # и выводим его заново
                
            else:
                message = "Группа компонентов не пуста!"
                mb.askyesno(message=message, parent=self)
                # self.destroy()
        
        mag.viewTreeGroup(self.treeGroup, dataFrame_in)
        self.treeGroup.see(id_code_parent)
        self.treeGroup.selection_set(id_code_parent)
        mag.viewTreeComponents(self.tree2, dataFrame_in, id_code_parent)
        # сохраняем изменненный DataFame в файл
        me.Save_DataFrame_in_PickleFile()        
        if viewDB == 'DBC':   scfg.df_DBC = dataFrame_in
        elif viewDB == 'DBS': scfg.df_DBS = dataFrame_in

        return None

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy() 

