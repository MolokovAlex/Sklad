# autor: MolokovAlex
# lisence: GPL
# coding: utf-8
# version 0.0.2 - создаю класс Component и генератор уникального номера
# version 0.0.3 - функции создания резрвного файла
# version 0.0.4 - функции импорта/экспорта в pickle файл
# version 0.0.5 - переброска части функций и классов в модули и функции импорта/экспорта файл XLSX

# надо: 
# ОК- делать копию того файла который открываем и открывать копию, при закрытии файла - обратная замена. Те.в папке будут два файла - исходный и измененный
# - считывать файл Иксель
# - сохранять и считывать в собственном фомате в файл
# ОК- генерировать уникальный номер компонента в зависимости от даты, времени до милисекунды

# from re import X
import win32com.client
import string
import shutil
import pickle
import sys
import os
import DBClassModule


def SeparationFileName (nameFile:str) -> list:
    """
    функция разделяет строковую переменную имени файла на имя файла и расширение
    Выход:
    list_name = [name: str, ext: str]
    
    """
    list_name = []
    name = ''
    ext = ''
    for x in range (len(nameFile)-1,0,-1):      #  поиск расширения
        if nameFile[x] != ".":
            ext = nameFile[x] + ext
        else:
            x_stop = x
            break
    for y in range (0,x_stop,1):                # поиск имени
        name = name + nameFile[y]
    list_name.append(name)
    list_name.append(ext)
    return list_name

def ArchFileCopy(nameFileOrigin:str)-> str:
    """
    функция делает копию исходного файла, добавляя к имени в конце "V1"
    вход:
    nameFileOrigin:str - например, "test.xlsx"
    выход:
    создание копии и 
    nameArchFile - имя созданного файла, например "testV1.xlsx"
    """
    nameOrigin = []
    nameOrigin = SeparationFileName(nameFileOrigin)
    nameArchFile = nameOrigin[0] + 'V1' + '.' + nameOrigin[1]
    shutil.copy2(nameFileOrigin, nameArchFile)
    return nameArchFile

def FillingDBComponent():
    """
     функция наполнения базы данных класса Component
    """


    return None

def SaveDBComponentInFileXLS():
    """
    функция экспорта базы  DBComponent в файл xls
    """
    global DBComponent

    # создадим COM объект
    Excel = win32com.client.Dispatch("Excel.Application")

    # Теперь мы можем работать с помощью объекта Excel мы можем получить доступ ко всем возможностям VBA. Давайте, для начала, откроем любую книгу и выберем активный лист. Это можно сделать так:
    # G:\NO_Work\Python\Sklad\
    wb = Excel.Workbooks.Open(u'G:\\NO_Work\\Python\\Sklad\\ex1.xlsx')
    sheet = wb.ActiveSheet

    #получаем значение первой ячейки
    #val = sheet.Cells(1,1).value
    #print (val)

    #получаем значения цепочки A1:A2
    #vals = [r[0].value for r in sheet.Range("A1:A2")]
    #print(vals)

    #записываем значение в определенную ячейку
    #sheet.Cells(1,2).value = val

    #записываем последовательность
    # переменная i, которая инициализируется не 0, как принято python, а 1. Это связано с тем, что мы работаем с индексами ячеек как из VBA, а там нумерация начинается не с 0, а с 1.
    #i = 1
    #for rec in vals:
    #    sheet.Cells(i,3).value = rec
    #    i = i + 1
    for i in range (1, len (DBComponent)-1, 1):
        # у Cells( строка, столбец)
        sheet.Cells(i, 1).value = DBComponent[i].code
        sheet.Cells(i, 1).Font.Color = 0xFF0000
        sheet.Cells(i, 2).value = DBComponent[i].name
        sheet.Cells(i, 2).Font.Color = 0x00FF00

    #сохраняем рабочую книгу
    wb.Save()
    #закрываем ее
    wb.Close()
    #закрываем COM объект
    Excel.Quit()



    # with open(fileName) as dbfile:
    #     dbfile = open(fileName, "wb")
    #     pickle.dump(DBComponent, dbfile, 4)
    # dbfile.close()
    print ("OK file save XLS")

    return None

def AnalizPustoInStr(instring: str) -> bool:
    Pusto = True
    #Instring.replace(" ", "")
    #instring.translate({ord(c): None for c in string.whitespace})
    if (instring == '' ) | (instring == '\n') | (instring == " ") | (instring == None):
        Pusto = True
    else:
        Pusto = False

    return Pusto

def LoadDBComponentFromFileXLS():
    """
    функция импорта базы  DBComponent из файла xls
    """
    global DBComponent

    # создадим COM объект
    Excel = win32com.client.Dispatch("Excel.Application")

    # Теперь мы можем работать с помощью объекта Excel мы можем получить доступ ко всем возможностям VBA. Давайте, для начала, откроем любую книгу и выберем активный лист. Это можно сделать так:
    # G:\NO_Work\Python\Sklad\
    wb = Excel.Workbooks.Open(u'G:\\NO_Work\\Python\\Sklad\\ex2.xlsx')
    sheet = wb.ActiveSheet
    
    for indexInFile in range (1, 80, 1):
        # у Cells( строка, столбец)
        #print (sheet.Cells(indexInFile, 1).value)
        if AnalizPustoInStr(sheet.Cells(indexInFile, 1).value) == False:
            nam = sheet.Cells(indexInFile, 1).value
            dbc = DBClassModule.Component(nam, DBClassModule.getCode())
            DBComponent.append(dbc)

        

    #сохраняем рабочую книгу
    #wb.Save()
    #закрываем ее
    wb.Close()
    #закрываем COM объект
    Excel.Quit()
    print ("OK file load XLS in DBComponent")

    return None



def SaveDBComponentInFilePickle(fileName: str):
    """
    функция экспорта базы  DBComponent в файл упаковкой pickle
    """
    global DBComponent
    with open(fileName) as dbfile:
        dbfile = open(fileName, "wb")
        pickle.dump(DBComponent, dbfile, 4)
    dbfile.close()
    print ("OK file save")
    return None

def LoadDBComponentFromFilePickle(fileName: str):
    """
    функция импорта базы  DBComponent из файла упаковкой pickle
    """
    global DBComponent
    with open(fileName) as dbfile:
        dbfile = open(fileName, "rb")
        DBComponent = pickle.load(dbfile)
    dbfile.close()
    print ("OK file load")
    return None



# nameFile = "ex1.xlsx"
# fileNamePickle = 'DBComponents.db'
DBComponent = []                # БД по наименованию компонентов


# тестовое наполнение DBComponent
# baseNameComponent = 'транзистор'
# for x in range (0, 10, 1):
#     nameComponent = baseNameComponent + str(x)
#     obj = DBClassModule.Component(nameComponent, DBClassModule.getCode())
#     DBComponent.append(obj)
# for x in range (0, 10, 1):
#     print (DBComponent[x].code + '  ' + DBComponent[x].name)


#SaveDBComponentInFilePickle(fileNamePickle)
#DBComponent = []
LoadDBComponentFromFileXLS()
# for x in range (1, 10, 1):
#     print (str(DBComponent[x].code) + '  ' + str(DBComponent[x].name))

SaveDBComponentInFileXLS()

#DBComponent = []

#LoadDBComponentInFilePickle(fileNamePickle)

# for x in range (0, 10, 1):
#     print (DBComponent[x].code + '  ' + DBComponent[x].name)
