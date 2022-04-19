# autor: MolokovAlex
# lisence: GPL
# coding: utf-8
# version 0.0.2 - создаю класс Component и генератор уникального номера
# version 0.0.3 - функции создания резрвного файла

# надо: 
# ОК- делать копию того файла который открываем и открывать копию, при закрытии файла - обратная замена. Те.в папке будут два файла - исходный и измененный
# - считывать файл Иксель
# - сохранять и считывать в собственном фомате в файл
# ОК- генерировать уникальный номер компонента в зависимости от даты, времени до милисекунды

import win32com.client
import time
import shutil


class Component:
    def __init__(self, name, code, 
                group, sub_group_level1, sub_group_level2, sub_group_level3, sub_group_level4, sub_group_level5, 
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
    for x in range (len(nameFile)-1,0,-1):
        if nameFile[x] != ".":
            ext = nameFile[x] + ext
        else:
            x_stop = x
            break
    for y in range (0,x_stop,1):
        name = name + nameFile[y]
    list_name.append(name)
    list_name.append(ext)
    return list_name

def ArchFileCopy(nameFileOrigin:str):
    """
    функция делает копию исходного файла, добавляя к имени в конце "V1"
    """
    nameOrigin = []
    nameOrigin = SeparationFileName(nameFileOrigin)
    archFile = nameOrigin[0] + 'V1' + '.' + nameOrigin[1]
    shutil.copy2(nameFileOrigin, archFile)
    return archFile

nameFile = "ex1.xlsx"
print (getCode())
print (SeparationFileName(nameFile))
print (ArchFileCopy(nameFile))

