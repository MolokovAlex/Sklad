
# test file
# relativ path file

import os

path = '\image\test_5.py'
# path = 'test_5.py'
# path = '/Users/krunal/Desktop/code/python/database/app.py'
p1 = os.path.dirname(path)
print (p1)
print(os.getcwd())
p = os.path.abspath('image\delete1.png')
print(p) 
