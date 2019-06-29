#!/usr/bin/python
import twstock
data = twstock.t86.get('01', '20190620', 'json')
print(data)