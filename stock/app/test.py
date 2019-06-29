#!/usr/bin/python
import twstock
data = twstock.t86.get('0', '20190628', 'json')
print(data)