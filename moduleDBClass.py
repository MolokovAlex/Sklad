# moduleDBClass
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# модуль держатель классов Баз Данных


import time
import sqlite3 as sqlite
import openpyxl
import shutil
import tkinter.messagebox as mb
import modulAppGUI as mag
import moduleImport as mi
import skladConfig as scfg
import moduleSQLite as msql




class Component:
    def __init__(self, 
                code_component, 
                name_component, 
                code_group_list, 
                amount=0, 
                min_rezerve = 10,
                code_units=0, 
                articul=''):
        """ Конструктор класса Component
        Args:
        name - наимнование компонента, например "транзистор", "винт М2x20 DIN912 A2"
        code - уникальный номер компонента, его цифровой отпечаток
        code_group - уникальный номер группы/подгруппы
        amount - количество на складе в единицах измерения
        min_rezerve - минимальный остаток на складе
        code_units - код единицы измерения, например "шт", "комлект", "л"

        articul -  артикул компонента
        """
        self.name_component = name_component        
        self.code_component = code_component
        #self.code_group = code_group
        self.code_group = []
        for item in code_group_list:
            self.code_group.append(item)
        self.min_rezerve = min_rezerve
        self.code_units = code_units
        self.amount = amount
        self.articul = articul

        return None

class Units:
    def __init__(self, code_units=0, name_units = ''):
        """ Конструктор класса Units
        Args:
        name_units - наимнование единицы измерения
        code_units -  уникальный номер
        """
        self.name_units = name_units        
        self.code_units = code_units


class Group:
    def __init__(self, id_code_group_item: str, name_groupGroup: str) -> None:
        """ Конструктор класса Group
        Args:
        id_code_group_item - уникальный номер группы/подгруппы
        name_group - наимнование группы/подгруппы, например "разъемы", "термоусадочная трубка"
        """
        self.id_code_group_item = id_code_group_item
        self.name_group = name_groupGroup  
        #self.id_code_group_parent = id_code_group_parent

class GenesisTree:
    def __init__(self, id_code_group_item: str, id_code_parent_Level: list) -> None:
        """ Конструктор класса GenesisTree - родителского дерева для каждого номера группы/подгруппы
        Args:
        id_code_group_item - уникальный номер группы/подгруппы
        id_code_parent_Level - список уникальных номеров всех родителей до 1 уровня в формате
                (номер родителя уровня 1, номер родителя уровня 2, ... номер родителя уровня MAX_LEVEL_GROUP)
        """
        self.id_code_group_item = id_code_group_item
        self.id_code_parent_Level = []
        for item in id_code_parent_Level:
            self.id_code_parent_Level.append(id_code_parent_Level[item]) 

def parsing_tree_parent(id_code_group_itemPTP: int) -> str:
    """
    Разбор кода id_code_group на номера уровней и индивидуальные коды элемента и родителя
    Вход:
    id_code_group_itemPTP
                LWWXYY,
                где 
                LWW - номер родительской группы/подгруппы, состоит из полей:
                    L - номер уровня родителя, от 00(верхний уровень) до 9(реально примерно 06)
                    WW - порядкоывый номер группы/подгруппы у родителя родителя ( у дедушки...)
                XYY - уникальный номер группы/подгруппы, состоит из полей:
                    ХХ - номер уровня, от 0(верхний уровень) до 9(реально примерно 06)
                    YY - порядкоывый номер группы/подгруппы у родителя 
    Выход:
    code_group_item - (YY)
    level_item - (X)
    code_group_parent - (WW)
    level_parent - (L)
    
    """
    # code_group_item_YY = (id_code_group_itemPTP- int(id_code_group_itemPTP/100))*100
    # a = id_code_group_itemPTP - code_group_item_YY
    # level_item_XX =  (a- int(a/10000))*100
    # b = id_code_group_itemPTP - (level_item_XX*100+code_group_item_YY)      
    # code_group_parent_WW = (b- int(b/1000000))*100
    # level_parent_LL = int(id_code_group_itemPTP/1000000)


    id_code_group_itemPTP_str = str(id_code_group_itemPTP)
    print(id_code_group_itemPTP_str, '  ', id_code_group_itemPTP)
    code_group_item_YY = id_code_group_itemPTP_str[4] + id_code_group_itemPTP_str[5]
    level_item_XX =  id_code_group_itemPTP_str[3]
    code_group_parent_WW = id_code_group_itemPTP_str[1:3]
    level_parent_LL = id_code_group_itemPTP_str[0]
    print(code_group_item_YY, '  ',level_item_XX, '  ', code_group_parent_WW, '  ', level_parent_LL)


    return code_group_item_YY, level_item_XX, code_group_parent_WW, level_parent_LL


# def parsing_tree_parent(id_code_group_itemPTP, id_code_group_parentPTP):
#     """
#     Разбор кодов id_code_group и id_code_group_parent на номера уровней и индивидуальные коды
#     Вход:
#     id_code_group_itemPTP - уникальный номер группы/подгруппы, состоит из полей:
#                 XXYY,
#                 где ХХ - номер уровня, от 00(верхний уровень) до 99(реально примерно 06)
#                 YY - порядкоывый номер группы/подгруппы у родителя 
#     id_code_group_parentPTP - номер родительской группы/подгруппы, состоит из полей:
#                 LLWW,
#                 где LL - номер уровня родителя, от 00(верхний уровень) до 99(реально примерно 06)
#                 WW - порядкоывый номер группы/подгруппы у родителя родителя ( у дедушки...)
#     Выход:
#     code_group_item - (YY)
#     level_item - (XX)
#     code_group_parent - (WW)
#     level_parent - (LL)
    
#     """
#     code_group_item = (id_code_group_itemPTP- int(id_code_group_itemPTP/100))*100
#     level_item = int(id_code_group_itemPTP/100)         
#     code_group_parent = (id_code_group_parentPTP- int(id_code_group_parentPTP/100))*100
#     level_parent = int(id_code_group_parentPTP/100)

#     return code_group_item, level_item, code_group_parent, level_parent

def Unpack_codegroup(codegroupf):
    """
    Распаковка переменной codegroup  из упакованного формата типа 0xFFFFFF на список из 5-ти значений групп/подгрупп
    Args:
    codegroupf

    Выход:
    список u_codegroup = [значение группы верхнего уровня, 
                        значение подгруппы второго уровня,
                        значение подгруппы третьего уровня,
                        значение подгруппы четвертого уровня,
                        значение подгруппы пятого уровня
                        ]
    
    """
    u_codegroup = []
    u_codegroup.append(int(codegroupf) >> 16)
    u_codegroup.append((int(codegroupf) >> 12) & 0x0F)
    u_codegroup.append((int(codegroupf) >> 8) & 0x0F)
    u_codegroup.append((int(codegroupf) >> 4) & 0x0F)
    u_codegroup.append(int(codegroupf) & 0x0F)

    return u_codegroup

def getCode():
    """генерировать уникальный номер компонента в зависимости от даты, времени до милисекунды
    генерация на основе числа секунд, которые прошли с начала Unix-эпохи, то есть с 00:00:00 UTC 1.01.1979
    Выход
    Ccode -  тип int,  число увелививающееся на 1 каждые 100 мс
    """
    CCode = ''
    time.sleep(0.2)         # задержка генерации кода в 0.2 сек
    Utime = time.time()
    #  ограничим число, чтобы оно не было таким большим
    Utime = int(round((Utime-1640000000),1)*10)
    CCode = str(Utime)
    return CCode





