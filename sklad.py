# autor: MolokovAlex
# lisence: GPL
# coding: utf-8
# version 0.0.2 - создаю класс Component и генератор уникального номера
# version 0.0.3 - функции создания резрвного файла
# version 0.0.4 - функции импорта/экспорта в pickle файл

# надо: 
# ОК- делать копию того файла который открываем и открывать копию, при закрытии файла - обратная замена. Те.в папке будут два файла - исходный и измененный
# - считывать файл Иксель
# - сохранять и считывать в собственном фомате в файл
# ОК- генерировать уникальный номер компонента в зависимости от даты, времени до милисекунды

from re import X
import win32com.client
import time
import shutil
import pickle
import sys
import os

class Component:
    def __init__(self, name, code, 
                group='', sub_group_level1='', sub_group_level2='', sub_group_level3='', sub_group_level4='', sub_group_level5='', 
                amount=0, dimencion='шт', articul=''):
        """ Конструктор класса Component

        Args:
        name - наимнование компонента, например "транзистор", "винт М2x20 DIN912 A2"
        code - уникальный номер компонента, его цифровой отпечаток
        group - группа верхнего уровня, например "Метизы/крепеж"
        sub_group_level1 - подгруппа нижнего уровня, например "Винты"
        sub_group_level2 - подгруппа нижнего уровня, например "М2"
        sub_group_level3 - подгруппа нижнего уровня, например "DIN"
        sub_group_level4 - подгруппа нижнего уровня, например "тип стали"
        sub_group_level5 - подгруппа нижнего уровня, например "" ???? на всякий случай
        amount - количество на складе в единицах измерения
        dimencion - единица измерения, например "шт", "комлект", "л"
        articul -  артикул компонента
        """
        self.name = name        
        self.code = code
        self.group = group
        self.sub_group_level1 = sub_group_level1 
        self.sub_group_level2 = sub_group_level2 
        self.sub_group_level3 = sub_group_level3 
        self.sub_group_level4 = sub_group_level4 
        self.sub_group_level5 = sub_group_level5 
        self.dimencion = dimencion
        self.amount = amount
        self.articul = articul

    def move(self):
        """
        пока не знаю что здесь будет 
        FIXED
        """
        return None

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

def LoadDBComponentInFilePickle(fileName: str):
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


nameFile = "ex1.xlsx"
fileNamePickle = 'DBComponents.db'
DBComponent = []                # БД по наименованию компонентов

print (ArchFileCopy(nameFile))

# тестовое наполнение DBComponent
baseNameComponent = 'транзистор'
for x in range (0, 10, 1):
    nameComponent = baseNameComponent + str(x)
    obj = Component(nameComponent, getCode())
    DBComponent.append(obj)
for x in range (0, 10, 1):
    print (DBComponent[x].code + '  ' + DBComponent[x].name)

#os.chdir(r'G:\NO_Work\Python\Sklad')       # change dir
#print(os.getcwd())          # print current directory

SaveDBComponentInFilePickle(fileNamePickle)


DBComponent = []

LoadDBComponentInFilePickle(fileNamePickle)

for x in range (0, 10, 1):
    print (DBComponent[x].code + '  ' + DBComponent[x].name)
