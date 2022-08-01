
#   файл для испытаний и проверки гипотез

#import DBClassModule as dbcm
import time
import pandas as pd
import numpy as np

def getCode():
    """генерировать уникальный номер компонента в зависимости от даты, времени до милисекунды
    генерация на основе числа секунд, которые прошли с начала Unix-эпохи, то есть с 00:00:00 UTC 1.01.1979
    Выход
    Ccode -  тип str,  число увелививающееся на 1 каждые 100 мс
    """
    CCode = ''
    time.sleep(0.2)         # задержка генерации кода в 0.2 сек
    Utime = time.time()
    #  ограничим число, чтобы оно не было таким большим
    Utime = int(round((Utime-1640000000),1)*10)
    CCode = str(Utime)
    return CCode


# for i in range (1, 10, 1):
#     print(getCode() + '\n')


DBGroupFFX = []

with pd.ExcelFile("01.xlsx") as xls:
        df1 = pd.read_excel(xls, "База_осн")
df1.to_excel("2_out.xlsx")


# columns = ['name', 'id_code_parent', 'amount']
columns = ['name', 'id_code_lvl', 'amount']
with pd.ExcelFile("2_out.xlsx") as xls:
        df1 = pd.read_excel(xls, "Sheet1", names= columns)      #  скопируем данные из xlsx в DataFrame с заданием названия столбцов 
# df1['id_code_item'] = ''                                 
df1.insert(0, "id_code_item", '')               # добавляем еще один столбец в позицию 0, т.е. в начало
df1.insert(1, "id_code_parent", '')      
df1['name'].replace('', np.nan, inplace=True)       # заменим пустые строки на NAN
df1.dropna(subset=['name'], inplace=True)           # удалим строки с NAN
print('1')

df1.reset_index(drop=True, inplace=True)        # удалим пропущенные индексы
for indx in df1.index:                              # присвоим каждому элементу - и ЭРЭ и группе ЭРЭ уникальные номера
    df1.loc[indx, 'id_code_item'] = getCode()
print('2')
listOfIndexComponent = []
listOfIndexL4 = []
listOfIndexL3 = []
listOfIndexL2 = []
listOfIndexL1 = []
# for indx in df1.index:                              # пройдем по всем индексам таблицы
#     if df1.loc[indx, 'id_code_lvl'] == 'lvl01':      # если мы встетили элемент lvl01 - это родитель первого уровня
#         id_group =  df1.loc[indx, 'id_code_item']       # считаем его id код
#         for k in listOfIndexL1 :                            # 
#             df1.loc[k, 'id_code_parent'] = id_group
#             listOfIndexL1 = []
#     else:        
#         if df1.loc[indx, 'id_code_lvl'] == 'lvl02':          # если мы встетили в родителях lvl02 - это родитель второго уровня
#             id_group_parent = df1.loc[indx, 'id_code_item']     # считаем его id код
#             listOfIndexL1.append(indx)                          # и добавим его индекс в список индексов первого уровня
#             for i in listOfIndexL2:
#                 df1.loc[i, 'id_code_parent'] = id_group_parent
#             listOfIndexL2 = []
#         else:                                                       # если не lvl01 и не lvl02 - это элемент третьего уровня
#             listOfIndexL2.append(indx)

#  такой странный порядок из-за того что Excel  делает группировку ВВЕРХ, т.е. название группы идет после всех элементов, входящих в группу
for indx in df1.index:                              # пройдем по всем индексам таблицы
    if df1.loc[indx, 'id_code_lvl'] == 'lvl01':      # если мы встетили элемент lvl01 - это родитель первого уровня
        id_group =  df1.loc[indx, 'id_code_item']       # считаем его id код
        listOfIndexL1.append(indx)                          # и добавим его индекс в список индексов родителей первого уровня - не зачем - удальть строку
        for k in listOfIndexL2 :                            # если список родителей второго уровня существует
            df1.loc[k, 'id_code_parent'] = id_group         # пробегая по всем родителям второго уровня даем им этот код родителя
        listOfIndexL2 = []                                  # после пробега - очистить список

    elif df1.loc[indx, 'id_code_lvl'] == 'lvl02':          # если мы встетили элемент lvl02 - это родитель второго уровня
            id_group_parent = df1.loc[indx, 'id_code_item']     # считаем его id код
            listOfIndexL2.append(indx)                          # и добавим его индекс в список индексов родителей второго уровня
            for i in listOfIndexL3:                                 # если список родителей третьего уровня  существует
                df1.loc[i, 'id_code_parent'] = id_group_parent      # пробегая по всем родителям третьего уровня даем им этот код родителя
            listOfIndexL3 = []                               # после пробега - очистить список

    elif df1.loc[indx, 'id_code_lvl'] == 'lvl03':          # если мы встетили элемент lvl03 - это родитель третьего уровня
            id_group_parent = df1.loc[indx, 'id_code_item']     # считаем его id код
            listOfIndexL3.append(indx)                          # и добавим его индекс в список индексов родителей третьего уровня
            for i in listOfIndexL4:                                 # если список компонентов существует
                df1.loc[i, 'id_code_parent'] = id_group_parent      # пробегая по всем компонентам даем им этот код родителя
            listOfIndexL4 = []                               # после пробега - очистить список

    elif df1.loc[indx, 'id_code_lvl'] == 'lvl04':          # если мы встетили элемент lvl02 - это родитель второго уровня
            id_group_parent = df1.loc[indx, 'id_code_item']     # считаем его id код
            listOfIndexL4.append(indx)                          # и добавим его индекс в список индексов родителей второго уровня
            for i in listOfIndexComponent:                                 # если список родителей третьего уровня  существует
                df1.loc[i, 'id_code_parent'] = id_group_parent      # пробегая по всем родителям третьего уровня даем им этот код родителя
            listOfIndexComponent = []                               # после пробега - очистить список

    else:                                                       # если не lvl01 и не lvl02 и не... - это не название группы - это просто компонент
        listOfIndexComponent.append(indx)                             # добавляем его в список индексов третьго уровня


df2 = df1[df1['id_code_lvl'] == 'lvl01']     # выдать всех у кого в родителях код lvl01 ,т.е. это родители первого уровня
print (df2)
print ('\n')
for indx in df2.index:
    a = df1.loc[indx, 'id_code_item']                   # взять последоватььно id код родителя первого уровня
    df3 = df1.loc[df1['id_code_parent'] == a]      # найти кто в родителях имеет родителя первого уровня
    print (df3)

print ('Save in file')
df1.to_excel("2_out.xlsx")
print ('ALL END')