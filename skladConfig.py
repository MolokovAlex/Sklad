# skladConfig
# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

# модуль держатель конфигурацонных переменных
# файл хранения глобальных переменных и настроечных параметров


import os

# nameFile_DBgroup_import = 'sklad_group.xlsx'
# nameFile_DBcomponent_import =  'sklad_component.xlsx'
# nameFile_DBunits_import =  'sklad_units.xlsx'
# nameFile_DBbackUp = 'DBbackup.db'
nameFile_DB = 'DBsklad.db'


# nameFile_pu = 'sklad_pu.xlsx'
# nameFile_out = 'sklad_pu_out.xlsx'

# demo-данные
# (name, id_parent) 
data_list_demo_DBGS = [
        ('Спецификации',            0),     #id=1
        ('Проекты',                 1),     #id=2
        ('СБЕ Шкаф',                1),     #id=3
        ('СБЕ Крейт',               1),     #id=4
        ('СБЕ Корпус',              1),     #id=5
        ('СБЕ Передняя панель',     1),     #id=6
        ('СБЕ Плата',               1),     #id=7
        ('СБЕ Тара',                1),     #id=8
        ('СБЕ блок',                1),     #id=9
        ('СБЕ модуль',              1),     #id=10
        ('СБЕ разное',              1),     #id=11
        ('Проект ЭКЗ_2022',             2),     #id=12
        ('Проект Импульс_2022',         2),     #id=13
        ('Проект Е6-42_2022',           2),     #id=14
        ('СБЕ Крейт RX модиф ЭКЗ',      4),     #id=15
        ('СБЕ Крейт RS модиф ЭКЗ',      4),     #id=16
        ('СБЕ Крейт RX модиф Имп',      4),     #id=17
        ('СБЕ шкаф модиф ЭКЗ',          3),     #id=18
        ('СБЕ СТПЛ',                    5),     #id=19
        ('СБЕ корпус СТПЛ',             5),     #id=20
        ('СБЕ передняя панель СТПЛ',    6),     #id=21
        ('СБЕ Корпус Е642',             5),     #id=22
        ('СБЕ Плата индикации Е642',    7),    #id=23
        ('СБЕ Плата основная Е642',     7),    #id=24
        ('СБЕ Плата питания Е642',      7),     #id=25
        ('СБЕ тара Е642',               8),     #id=26
        ('СБЕ тара Импульс',            8),     #id=27
        ('СБЕ тара ЭКЗ',                8),    #id=28
        ('СБЕ блок силовой электрики шкафа',     9),    #id=29
        ('СБЕ Плата М192А01',           7)     #id=30

        ]

# demo-данные
# (name, id_parent_dbgs) 
data_list_demo_DBLS = [
        ('Список Спецификаций',         0),     #id=1
        ('Проект ЭКЗ_2022',             2),     #id=2
        ('Проект Импульс_2022',         2),     #id=3
        ('Проект Е6-42_2022',           2),     #id=4
        ('СБЕ Крейт RX модиф ЭКЗ',      4),     #id=5
        ('СБЕ Крейт RS модиф ЭКЗ',      4),     #id=6
        ('СБЕ Крейт RX модиф Имп',      4),     #id=7
        ('СБЕ шкаф модиф ЭКЗ',          3),     #id=8
        ('СБЕ СТПЛ',                    5),     #id=9
        ('СБЕ корпус СТПЛ',             5),     #id=10
        ('СБЕ передняя панель СТПЛ',    6),     #id=11
        ('СБЕ Корпус Е642',             5),     #id=12
        ('СБЕ Плата индикации Е642',    7),    #id=13
        ('СБЕ Плата основная Е642',     7),    #id=14
        ('СБЕ Плата питания Е642',      7),     #id=15
        ('СБЕ тара Е642',               8),     #id=16
        ('СБЕ тара Импульс',            8),     #id=17
        ('СБЕ тара ЭКЗ',                8),    #id=18
        ('СБЕ блок силовой электрики шкафа',     9),    #id=19
        ('СБЕ Плата М192А01',           7)     #id=20
        ]

# (name, id_parent) 
data_list_demo_DBG = [
        ('Склад',       0),     #id=1
        ('Разъемы',     1),     #id=2
        ('DIN',         2),     #id=3
        ('СП Каскад',   2),     #id=4
        ('6Р100-6Р150', 2),     #id=5
        ('СНП407-100',  4),     #id=6
        ('СНП407-150',  4),     #id=7
        ('6Р100',       5),     #id=8
        ('6Р150',       5),     #id=9
        ('DIN 32 конт', 3),     #id=10
        ('DIN 64 конт', 3),     #id=11
        ('Микросхемы',  1),     #id=12
        ('Аналоговые',  12),    #id=13
        ('Цифровые',    12),    #id=14
        ('прочие',      12)     #id=15
        ]

# (name, amount, id_unit, min_rezerve, articul_1C, code_1C, name_1C, id_parent, id_lvl)        
data_list_demo_DBC = [
        ('К155ЛА3', 15,     1,  10, 'К155ЛА3',  '00101217551',  'nК155ЛА3', 14,  0),            #id=1
        ('К155ЛА4', 5,      1,  10, 'К155ЛА4',  '00101217552',  'nК155ЛА4', 14,  0),            #id=2
        ('К155ЛА8', 6,      1,  1,  'К155ЛА8',  '00101217553',  'nК155ЛА8', 14,  0),            #id=3
        ('6Р100 вилка кабельная', 6,      1,  1,  'К155ЛА8',  '00101217553',  'nК155ЛА8', 8,  0),            #id=4
        ('6Р150 розетка блочная', 6,      1,  1,  'К155ЛА8',  '00101217553',  'nК155ЛА8', 9,  0)            #id=5
    ]

# (date, id_component, amount, comments)
data_list_demo_DBI = [
        ('1999-12-01 22:01:15', 1,  1,  'из ЧипиДипа счет 2345 от 1999-11-01'),        #id=1
        ('1999-12-02 08:07:15', 2,  2,  'из ЧипиДипа счет 2345 от 1999-11-01'),        #id=2
        ('1999-12-03 09:04:15', 3,  1,  'из ЧипиДипа счет 2345 от 1999-11-01'),        #id=3
    ]

# (date, id_component, amount, comments)
data_list_default_DBE = [
        ('2001-11-01 23:01:15', 1,  1,  'уехало в офис через ДЛ'),                  #id=1
        ('2001-11-02 04:07:15', 2,  2,  'взято инженером в коммандировку'),         #id=2
        ('2001-11-03 05:04:15', 3,  1,  'проект Автора'),                           #id=3
    ]

# (name)
data_list_demo_DBU = [
        ('шт',),                #id=1             
        ('мл',),                #id=2 
        ('л',),                 #id=3 
        ('мм',),                #id=4 
        ('см',),                #id=5 
        ('м',),                 #id=6 
        ('км',),                #id=7 
        ('г',),                 #id=8 
        ('кг',),                #id=9 
        ('т',),                 #id=10 
        ('компл',)              #id=11 
    ]
id_default_DBU = 1




# ------------------------------------------------------------------
# --------------- константы всей программы --------------------------
# ------------------------------------------------------------------

# файл всех БД в экспортте
nameFile_DB_export_excel = 'DB_export_Sklad.xlsx'

# расположение картинок на кнопках
icon_button_delete = os.path.abspath('icon\delete1.png')
icon_button_remove = os.path.abspath('icon\iemove1.png')
icon_button_rename = os.path.abspath('icon\edit1.png')
icon_button_edit = os.path.abspath('icon\edit3.png')

# -------------------------------------------------------------------------------------------------------------------------------------
# --------------- БД SQLite программы --------------------------
# -------------------------------------------------------------------------------------------------------------------------------------

DBSqlite = os.path.abspath('DB\DB_sql_sklad.db')
DBSqlite_backup =  os.path.abspath('DB\DB_sql_sklad_backup.db')


# -------------------------------------------------------------------------------------------------------------------------------------
# --------------- БД склада компонентов --------------------------
# -------------------------------------------------------------------------------------------------------------------------------------

# файл БД склада компоненов в формате Pickle для загрузки в DataFrame Pandas
nameFile_DBC_pickle = os.path.abspath('DB\DBCsklad.pkl')
# файл БД склада компоненов в формате XLXS для визуального контроля
nameFile_DBC_excel = os.path.abspath('DB\DBCsklad.xlsx')
# файл импорта DBC
nameFile_importDBC_excel = os.path.abspath('import\DBC_import_Sklad.xlsx')
# файлы экспорта DBC
nameFile_exportDBC_pickle = os.path.abspath('export\DBC_export_Sklad.pkl')
nameFile_exportDBC_excel = os.path.abspath('export\DBC_export_Sklad.xlsx')

# максимальное количество уровней групп в БД склада компонентов
MAX_LEVEL_GROUP = 10

# объект типа DataFrame содержащий БД склада компоненов
df_DBC = []

# наименования полей (столбцов) БД компонентов
columns_DB_components = [
    'id_code_item',                 # уникальный номер компонента, его цифровой отпечаток
    'name',                         # наимнование компонента, например "транзистор", "винт М2x20 DIN912 A2"
    'amount',                       # количество на складе в единицах измерения
    'code_units',                   # код единицы измерения, например: "шт",  "комлект", "л" и т.д.
    'min_rezerve',                  # минимальный остаток на складе в единицах измерения
    'articul_1C',                   # артикул компонента по базе 1С
    'code_1C',                      # код по базе 1С
    'name_1C',                      # наименование по базе 1С
    'id_code_parent',               # служебное поле - id_code_item родителя(группы) компонента
    'id_code_lvl'                   # служебное поле - буквенный код уровня вложенности родителя(группы) (поле только для группы)
    ]

# Какие столбцы должны отображаться в дереве таблицы в окне "Импорт" и "редактировании групп"
# displayColumnsInWindowsImport=['id_code_item', 'amount', 'code_units', 'min_rezerve', 'articul_1C', 'code_1C', 'name_1C',  'id_code_parent',   'id_code_lvl']
# displayColumnsShort=['id_code_item',   'id_code_parent',   'id_code_lvl']
displayColumnsShort=['id_code_item',   'id_code_parent']#,   'id_code_lvl']

# Какие столбцы должны отображаться в дереве таблицы в окне "редактирование компонентов"
# displayColumnsInWindowsImport=['id_code_item', 'amount', 'code_units', 'min_rezerve', 'articul_1C', 'code_1C', 'name_1C',  'id_code_parent',   'id_code_lvl']
displayColumnsFull=['id_code_item', 'amount', 'code_units', 'min_rezerve', 'articul_1C', 'code_1C', 'name_1C']#,  'id_code_parent',   'id_code_lvl']

# настройка ширины столбцов в окне/таблице "Редактирование БД" - размер в пикселях
widthColunmsTreeWindowEditComponent = {
            'id_code_item':     [60],  
            'name':             [400], 
            'amount':           [50],  
            'code_units':       [50],
            'min_rezerve':      [50],  
            'articul_1C':       [100],
            'code_1C':          [50],
            'name_1C':          [100],
            'id_code_parent':   [60],
            'id_code_lvl':      [30]                       
            }


# наимеования столбцов ячеек в XLSX файле для импорта в поля БД компонентов
import_columns_in_XLSX_file = [
    '',
    'A',
    'C',
    '',
    '',
    '',
    '',
    '',
    '',
    'B'
]

# номер строки в XLSX файле содержащей названия заголовков (None - нет заголовков)
number_row_of_name_columns = 0

#  наименование листа в импортируемом файле, содержащем БД компонентов
namesheet_DB_components = "База_осн"

# список буквенных кодов уровня вложенности родителя(группы)
listOfLevel = ['lvl01', 'lvl02', 'lvl03', 'lvl04', 'lvl05', 'lvl06']


# demo-данные
demo_DBС_1 = {
            'id_code_item':  ['1001',           '1002',                   '1003',         '1004'           ,    '1005'           ,    '1006'       ],        
            'name':          ['ЭРЭ',            'Микросхемы',             'Цифровые',     'К155ЛА3'        ,    'К155ЛА4'        ,    'К155ЛА8'    ], 
            'amount':        ['',               '',                       '',             '15'             ,    '5'              ,    '6'          ],
            'code_units':    ['1699',           '1699',                   '1699',         '1700'           ,    '1700'           ,    '1700'       ], 
            'min_rezerve':   ['',               '',                       '',             '10'             ,    '10'             ,    '1'          ],
            'articul_1C':    ['ЭРЭ_1C',         'Микросхемы_1C',          'Цифровые_1C',  'К155ЛА3'        ,    'К155ЛА4'        ,    'К155ЛА8'    ],
            'code_1C':       ['00101217548',    '00101217549',            '00101217550',  '00101217551'    ,    '00101217552'    ,    '00101217553'],
            'name_1C':       ['nЭРЭ_1C',        'nМикросхемы_1C',         'nЦифровые_1C', 'nК155ЛА3'       ,    'nК155ЛА4'       ,    'nК155ЛА8'   ],
            'id_code_parent':['10000',          '1001',                   '1002',         '1003'           ,    '1003'           ,    '1003'       ],
            'id_code_lvl':   ['lvl01',          'lvl02',                  'lvl03',        ''               ,    ''               ,    ''           ]         
            }

            
# demo_DBС_2 = {
#             'id_code_item':  ['1005',           '1006',                   '1007',         '1008'],
#             'name':          ['ЭРЭ',            'Микросхемы',             'Цифровые',     'К155ЛА3'], 
#             'amount':        ['',               '',                       '',             '15'],
#             'code_units':    ['1699',           '1699',                   '1699'          '1700'] , 
#             'min_rezerve':   ['',               '',                       '',             '10'],
#             'articul_1C':    ['ЭРЭ_1C',         'Микросхемы_1C',          'Цифровые_1C',  'К155ЛА3'],
#             'code_1C':       ['00101217548',    '00101217549',            '00101217550',  '00101217551'],
#             'name_1C':       ['nЭРЭ_1C',        'nМикросхемы_1C',         'nЦифровые_1C', 'nК155ЛА3'],
#             'id_code_parent':['10000',          '1001',                   '1002',         '1003'],
#             'id_code_lvl':   ['lvl01',          'lvl02',                  'lvl03',        '']         
#             }


# -------------------------------------------------------------------------------------------------------------------------------------
# --------------- БД прихода компонентов (income) -------------
# -------------------------------------------------------------------------------------------------------------------------------------

# файл БД расхода  компоненов в формате Pickle для загрузки в DataFrame Pandas
nameFile_DBI_pickle = os.path.abspath('DB\DBIsklad.pkl')
# файл БД расхода  компоненов в формате XLXS для визуального контроля
nameFile_DBI_excel = os.path.abspath('DB\DBIsklad.xlsx')

# файл импорта DBE
nameFile_importDBI_excel = os.path.abspath('import\DBI_import_Sklad.xlsx')
# файлы экспорта DBE
nameFile_exportDBI_pickle = os.path.abspath('export\DBI_export_Sklad.pkl')
nameFile_exportDBI_excel = os.path.abspath('export\DBI_export_Sklad.xlsx')


df_DBI = []

# наименования полей (столбцов) БД прихода
columns_DBI = [
    'id_code_e',                    # уникальный номер строки прихода, его цифровой отпечаток
    'date',                         # дата прихода
    'id_code_item',                 # уникальный номер компонента в приходе
    # 'name',                         # наимнование компонента  - возмем по коду 'id_code_item' из DBC
    'amount',                       # количество на приход в единицах измерения
    # 'code_units',                   # код единицы измерения - возмем по коду 'id_code_item' из DBC
    # 'dist',                         # символьный "путь" в дерево (БД) спецификаций куда нужно приход компонент - возмем по коду 'id_code_parent' из DBS
    'id_code_parent',               # служебное поле - id_code_item родителя(группы) в БД компонентов куда приход компонент
    'comments'                      # комментарии к строке прихода
    ]

# КАКИЕ и в каком ПОРЯДКЕ столбцы должны отображаться в дереве таблицы в окне "приход компонентов"
displayColumnsI=['id_code_e','date', 'name', 'amount', 'code_units', 'dist', 'comments']#, 'id_code_item', 'id_code_parent']
# displayColumnsI=['id_e','date', 'name', 'amount', 'units', 'dist', 'comments']#, 'id_code_item', 'id_code_parent']

# настройка ширины столбцов в окне/таблице "приход компонентов" - размер в пикселях
widthColunmsTreeWindowIncome = {
            'id_code_e': [60], 
            'date':[100], 
            'id_code_item': [60],                 
            'name': [400],                        
            'amount':[50],  
            'code_units':[50],
            'dist': [400],    
            # 'id_code_parent':[60],
            'comments':[400]                       
            }


demo_DBI_1 = {
            'id_code_e':     ['7001',         '7002',          '7003'], 
            'date':          ['1999-12-01',   '1999-12-02',    '1999-12-03'], 
            'id_code_item':  ['1004',         '1006',          '1006'],     
            'name':          ['К155ЛА3',      'К155ЛА8',       'К155ЛА8'],  
            'amount':        ['110',          '212',         '330'], 
            'code_units':    ['1700'     ,    '1700'      ,    '1700' ],
            # 'dist':        ['',             '',              ''],                                    
            'id_code_parent':['1003',         '1003',          '1003'],
            'comments':      ['из ЧипиДипа счет 2345 от 1999-11-01', 'из ЧипиДипа счет 2345 от 1999-11-01', 'из ЧипиДипа счет 2345 от 1999-11-01']
            }



# -------------------------------------------------------------------------------------------------------------------------------------
# --------------- БД расхода компонентов (expenditure) -------------
# -------------------------------------------------------------------------------------------------------------------------------------

# файл БД расхода  компоненов в формате Pickle для загрузки в DataFrame Pandas
nameFile_DBE_pickle = os.path.abspath('DB\DBEsklad.pkl')
# файл БД расхода  компоненов в формате XLXS для визуального контроля
nameFile_DBE_excel = os.path.abspath('DB\DBEsklad.xlsx')

# файл импорта DBE
nameFile_importDBE_excel = os.path.abspath('import\DBE_import_Sklad.xlsx')
# файлы экспорта DBE
nameFile_exportDBE_pickle = os.path.abspath('export\DBE_export_Sklad.pkl')
nameFile_exportDBE_excel = os.path.abspath('export\DBE_export_Sklad.xlsx')


df_DBE = []

# наименования полей (столбцов) БД расходов
columns_DBE = [
    'id_code_e',                    # уникальный номер строки расхода, его цифровой отпечаток
    'date',                         # дата расхода
    'id_code_item',                 # уникальный номер компонента в расходе
    # 'name',                         # наимнование компонента  - возмем по коду 'id_code_item' из DBC
    'amount',                       # количество на списание в единицах измерения
    # 'code_units',                   # код единицы измерения - возмем по коду 'id_code_item' из DBC
    # 'dist',                         # символьный "путь" в дерево (БД) спецификаций куда нужно списать компонент - возмем по коду 'id_code_parent' из DBS
    'id_code_parent',               # служебное поле - id_code_item родителя(группы) в БД спецификации куда списан компонент
    'comments'                      # комментарии к строке расхода
    ]

# КАКИЕ и в каком ПОРЯДКЕ столбцы должны отображаться в дереве таблицы в окне "списание компонентов"
displayColumnsE=['id_code_e','date', 'name', 'amount', 'code_units', 'dist', 'comments']#, 'id_code_item', 'id_code_parent']

# настройка ширины столбцов в окне/таблице "расход компонентов" - размер в пикселях
widthColunmsTreeWindowExpenditure = {
            'id_code_e': [60], 
            'date':[100], 
            'id_code_item': [60],                 
            'name': [400],                        
            'amount':[50],  
            'code_units':[50],
            'dist': [400],    
            # 'id_code_parent':[60],
            'comments':[400]                       
            }
# demo-данные
# demo_DBE_1 = {
#             'id_code_e':     ['4001',         '4002',          '4003'], 
#             'date':          ['2000-01-01',   '2000-01-02',    '2000-01-03'], 
#             'id_code_item':  ['1004',         '1006',          '1006'],     
#             'name':          ['К155ЛА3',      'К155ЛА8',       'К155ЛА8'],  
#             'amount':        ['1',            '12',            '3'], 
#             'code_units':    ['1700'     ,    '1700'      ,    '1700' ],
#             # 'dist':          ['',             '',              ''],                                    
#             'id_code_parent':['00001',        '00001',         '00001'],
#             'comments':      ['post in CDEK', 'отправлено ДЛ', 'уехало с инженером Ивановым в московский оффисс']              
#             }
demo_DBE_1 = {
            'id_code_e':     ['4001',         '4002',          '4003'], 
            'date':          ['2000-01-01',   '2000-01-02',    '2000-01-03'], 
            'id_code_item':  ['1004',         '1006',          '1006'],     
            'name':          ['К155ЛА3',      'К155ЛА8',       'К155ЛА8'],  
            'amount':        ['1',            '12',            '3'], 
            'code_units':    ['1700'     ,    '1700'      ,    '1700' ],
            # 'dist':        ['',             '',              ''],                                    
            'id_code_parent':['3011',         '3011',          '3011'],
            'comments':      ['в спец 2 плата Плата ЛДПА_М128', 'в спец 2 плата Плата ЛДПА_М128', 'в спец 2 плата Плата ЛДПА_М128']
            }




# -------------------------------------------------------------------------------------------------------------------------------------
# --------------- БД единиц измерения 'code_units' ------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------
# файл БД расхода  компоненов в формате Pickle для загрузки в DataFrame Pandas
nameFile_DBCU_pickle = os.path.abspath('DB\DBCUsklad.pkl')
# файл БД расхода  компоненов в формате XLXS для визуального контроля
nameFile_DBCU_excel = os.path.abspath('DB\DBCUsklad.xlsx')

# файл импорта DBE
nameFile_importDBCU_excel = os.path.abspath('import\DBCU_import_Sklad.xlsx')
# файлы экспорта DBE
nameFile_exportDBCU_pickle = os.path.abspath('export\DBCU_export_Sklad.pkl')
nameFile_exportDBCU_excel = os.path.abspath('export\DBCU_export_Sklad.xlsx')

#'code_units'
df_DBCU = []
# наименования полей (столбцов) БД единиц измерения
columns_DBCU = [
    'id_code_item',                 # уникальный номер компонента, его цифровой отпечаток
    'code_units'                   # код единицы измерения, например: "шт",  "комлект", "л" и т.д.
    ]
# список всех возможных вариантов поля 'code_units'
UnitsCodeName = {
            '1699':'',    
            '1700':'шт',
            '1701':'л',
            '1702':'мл',
            '1703':'м',
            '1704':'кг',
            '1705':'г',
            '1706':'компл'
}

# demo-данные
demo_DBCU_1  = {
            'id_code_item': ['1001',           '1002',                   '1003',         '1004',         '1005',         '1006'],                 
            'code_units':   ['1699',           '1699',                   '1699',         '1700',         '1700',         '1700']           
            }
# demo_DBCU_1  = {
#             'id_code_item': ['1001',           '1002',                   '1003',         '1004',         '1005'],                 
#             'code_units':   ['1699',           '1699',                   '1699',         '1700',         '1700']           
#             }


# -------------------------------------------------------------------------------------------------------------------------------------
# --------------- БД спецификаций ----------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------

# файл БД спецификаций в формате Pickle для загрузки в DataFrame Pandas
nameFile_DBS_pickle = os.path.abspath('DB\DBSpec.pkl')
# файл БД спецификаций в формате XLXS для визуального контроля
nameFile_DBS_excel = os.path.abspath('DB\DBSpec.xlsx')
# файл импорта спецификаций для загрузки в DataFrame Pandas
# nameFile_importDBS_excel = 'importDBSpec.xlsx'

# файл импорта DBE
nameFile_importDBS_excel = os.path.abspath('import\DBS_import_Sklad.xlsx')
# файлы экспорта DBE
nameFile_exportDBS_pickle = os.path.abspath('export\DBS_export_Sklad.pkl')
nameFile_exportDBS_excel = os.path.abspath('export\DBS_export_Sklad.xlsx')

# объект типа DataFrame содержащий БД спецификаций
df_DBS = []

# наименования полей (столбцов) БД спецификаций
columns_DBS = [
    'id_code_e',                    # уникальный номер строки спецификации, его цифровой отпечаток
    'id_code_item',                 # уникальный номер компонента в спецификации
    'name',                         # наимнование компонента, например "транзистор", "винт М2x20 DIN912 A2" (может быть не нужно?????????  можно определить через id_code_item)
    'amount',                        # количество компонента в единицах измерения
    'id_code_parent',               # служебное поле - id_code_item родителя(группы) в БД спецификации
    'id_code_lvl',                   # служебное поле - буквенный код уровня вложенности родителя(группы) (поле только для группы)
    'comments'                      # комментарии к строке спецификации
    ]

# demo-данные
demo_DBS_1 = {
            'id_code_e':     ['3000',            '3001',                   '3002',     '3004'              ,'3005'            ,'3006'            ],
            'id_code_item':  ['',                '',                       '',         ''                  ,''                ,''                ],
            'name':          ['Спецификация 1',  'Персональный компьютер', 'Модуль А', 'Плата ЛДПА_кросс'  ,'Плата ЛДПА_М192' ,'Плата ЛДПА_LVOC' ], 
            'amount':        ['1',               '1',                      '1',        '1'                 ,'15'              ,'1'               ],
            'id_code_lvl':   ['lvl01',           'lvl02',                  'lvl02',    ''                  ,''                ,''                ],              
            'id_code_parent':['10000',           '3000',                   '3001',     '3002'              ,'3002'            ,'3002'            ],
            'comments':      ['шаблон 1',        '',                       '',         ''                  ,'вер5'            ,'после ремонта'   ]         
            }
demo_DBS_2 = {
            'id_code_e':     ['3010',           '3011',                   '3012',      '3013'     ,  '3014'            ],
            'id_code_item':  ['',               '',                       '1004',      '1006'     ,  '1006'            ],
            'name':          ['Спецификация 2', 'Плата ЛДПА_М128',        'К155ЛА3',   'К155ЛА8'  ,  'К155ЛА8'         ], 
            'amount':        ['1',              '1',                      '1',         '12'       ,  '3'               ],
            'id_code_lvl':   ['lvl01',          'lvl02',                  '',          ''         ,  ''                ],              
            'id_code_parent':['10000',          '3010',                   '3011',      '3011'     ,  '3011'            ],
            'comments':      ['шаблон 2',       '',                       '',          ''         ,  ''                ]         
            }

# КАКИЕ и в каком ПОРЯДКЕ столбцы должны отображаться в дереве таблицы в окне "редактирование спецификации"
displayColumnsEditSpec=['id','path_DBGS', 'name', 'cbe', 'amount', 'units',  'comments']#, 'dist', 'comments']#, 'id_code_item', 'id_code_parent']
        # id INTEGER PRIMARY KEY AUTOINCREMENT,
        # id_dbls INTEGER,
        # id_component INTEGER ,
        # id_specification INTEGER,
        # flag_case_DB TEXT NOT NULL CHECK(flag_case_DB !=''),
        # amount INTEGER NOT NULL DEFAULT 0 CHECK(amount >= 0), 
        # id_unit INTEGER,
        # id_parent INTEGER,
        # id_lvl INTEGER,

# настройка ширины столбцов в окне/таблице "приход компонентов" - размер в пикселях
widthColunmsTreeWindowEditSpecification = {
            'id': [30], 
            'path_DBGS':[100], 
            'name': [400],  
            'cbe': [5],                      
            'amount':[50],  
            'units':[50],
            'comments':[100]                      
            }

displayColumnsEditSpecification=['id','path_DBGS', 'name', 'cbe', 'amount', 'units',  'comments']
