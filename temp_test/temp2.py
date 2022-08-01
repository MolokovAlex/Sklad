
#   файл для испытаний и проверки гипотез

#import DBClassModule as dbcm
import time
import pandas as pd
import numpy as np


# mi.Load_DBGroup_From_XLS_pandas(scfg.nameFile_pu)

newNameComponent = 'qwer1'
id_lvl = 'lvl01'
codeItem = '10001'
selTreeGroup = '10000'
row1 = {'name':newNameComponent, 'id_code_lvl': id_lvl, 'id_code_item': codeItem, 'id_code_parent':selTreeGroup, 'amount':0}
df11 = pd.DataFrame(row1 , index=[0])
# df1 = pd.concat([df1, df_new_row])

newNameComponent = 'qwer2'
id_lvl = 'lvl02'
codeItem = '10002'
selTreeGroup = '10000'
row2 = {'name':newNameComponent, 'id_code_lvl': id_lvl, 'id_code_item': codeItem, 'id_code_parent':selTreeGroup, 'amount':0}
df2 = pd.DataFrame(row2 , index=[0])
df11 = pd.concat([df11, df2])


newNameComponent = 'qwer3'
id_lvl = 'lvl03'
codeItem = '10003'
selTreeGroup = '10000'
row3 = {'name':newNameComponent, 'id_code_lvl': id_lvl, 'id_code_item': codeItem, 'id_code_parent':selTreeGroup, 'amount':0}
df2 = pd.DataFrame(row3 , index=[0])
df11 = pd.concat([df11, df2])

#  переиндексируем DataFrame
df11 = df11.reset_index(drop=True)

# df2 = df11[df11['id_code_item'] == '10002']
df2 = df11.loc[df11['id_code_item'] == '10002', 'id_code_lvl']
print (df2)
print (type(df2))
id_lvl = df2.item()
#self.treeGroup.item(sel[0])
# print(dic['text'])    
# ent_NameComponent.insert(0, dic['text'])

# indx = df2.index
# lvl = df2.at[indx, 'id_code_lvl']
# id_code_lvl = df2.loc[indx,'id_code_lvl']
# print (id_code_lvl[indx])
# # print (str(id_code_lvl[indx]))
# print (type(id_code_lvl[indx]))
# id_code_lvl1 = df2['id_code_lvl']
# print(id_code_lvl1)
# print (type(id_code_lvl1))
# id_lvl = id_code_lvl[indx]


# df = pd.DataFrame([[1, 2], [4, 5], [7, 8]], index=['cobra', 'viper', 'sidewinder'], columns=['max_speed', 'shield'])

# f1 = df.loc[df['shield'] > 6, ['max_speed']]
# print (f1)
# print(type(f1))




newNameComponent = 'qwer10'
# id_lvl = 'lvl10'
codeItem = '10010'
selTreeGroup = '10000'
row4 = {'name':newNameComponent, 'id_code_lvl': id_lvl, 'id_code_item': codeItem, 'id_code_parent':selTreeGroup, 'amount':0}
df2 = pd.DataFrame(row4 , index=[0])
df11 = pd.concat([df11, df2])

print ('Save in file')
# df1.to_excel("2_out.xlsx")
print ('ALL END')