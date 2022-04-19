# module
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# модуль держатель классов Баз Данных

import time

class Component:
    def __init__(self, name, code=0, 
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
