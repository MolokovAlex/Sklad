# autor: MolokovAlex
# lisence: GPL
# version 0.0.1

import win32com.client

# создадим COM объект
Excel = win32com.client.Dispatch("Excel.Application")

# Теперь мы можем работать с помощью объекта Excel мы можем получить доступ ко всем возможностям VBA. Давайте, для начала, откроем любую книгу и выберем активный лист. Это можно сделать так:
# G:\NO_Work\Python\Sklad\
wb = Excel.Workbooks.Open(u'G:\\NO_Work\\Python\\Sklad\\ex1.xlsx')
sheet = wb.ActiveSheet

#получаем значение первой ячейки
val = sheet.Cells(1,1).value
print (val)

#получаем значения цепочки A1:A2
vals = [r[0].value for r in sheet.Range("A1:A2")]
print(vals)

#записываем значение в определенную ячейку
sheet.Cells(1,2).value = val

#записываем последовательность
# переменная i, которая инициализируется не 0, как принято python, а 1. Это связано с тем, что мы работаем с индексами ячеек как из VBA, а там нумерация начинается не с 0, а с 1.
i = 1
for rec in vals:
    sheet.Cells(i,3).value = rec
    i = i + 1

#сохраняем рабочую книгу
wb.Save()

#закрываем ее
wb.Close()

#закрываем COM объект
Excel.Quit()
