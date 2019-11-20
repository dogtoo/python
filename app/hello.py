#!/usr/bin/python
print("哈囉 派森");
print(" test", end="")
_int = 1
_bool = True
_float = 1.1
_complex = 1 + 2j
_str = "sss"
print(type(_int))
print(type(_bool))
print(type(_float))
print(type(_complex))
print(type(_str))
print(_complex)
if True:
    print ("True")
else:
    print ("False")
    
_str='Runoob'
print('------------------------------')
print(_str)                 # 输出字符串
print(_str[0:-1])           # 输出第一个到倒数第二个的所有字符
print(_str[0])              # 输出字符串第一个字符
print(_str[-1])
print(_str[2:5])            # 输出从第三个开始到第五个的字符
print(_str[2:])             # 输出从第三个开始的后的所有字符
print(_str * 2)             # 输出字符串两次
print(_str + '你好')        # 连接字符串
 
print('------------------------------')
 
print('hello\nrunoob')      # 使用反斜杠(\)+n转义特殊字符
print(r'hello\nrunoob')     # 在字符串前面添加一个 r，表示原始字符串，不会发生转义

print(input("\n按下 enter 键后退出。"))

if _int == 2 :
    print("is 2")
else :
    print("is 1")

import sys
print('================Python import mode==========================');
print ('命令行参数为:')
for i in sys.argv:
    print (i)
print ('\n python 路径为',sys.path)    

print(isinstance(_str, str))

list = [ 'abcd', 786 , 2.23, 'runoob', 70.2 ]
tinylist = [123, 'runoob']

print ("all = ", end = "")
print (list)            # 输出完整列表
print ("first = ", end = "")
print (list[0])         # 输出列表第一个元素
print ("2 to 3 =", end="")
print (list[1:3])       # 从第二个开始输出到第三个元素
print ("after 3 = ", end="")
print (list[2:])        # 输出从第三个元素开始的所有元素
print (tinylist * 2)    # 输出两次列表
print (list + tinylist) # 连接列表

a = [1, 2, 3, 4, 5, 6]

dict = {'Name': 'Runoob', 'Age': 7}
 
print ("Value : %s" %  dict.items())

dict = {'Name': 'Runoob', 'Age': 7}
for i,j in dict.items():
    print(i, ":\t", j)
    
    
dict = {'Name': 'Runoob', 'Age': 7}
for i in dict.keys():
    print("key = " + i)
    
students = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
print(sorted(students, key=lambda a: a[2]))

basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
basket2 = {'apple',  'apple', 'banana'}
print(basket - basket2)