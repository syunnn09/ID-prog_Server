# -*- coding: utf-8 -*-

year = int(input())

if year % 4 != 0:
	print('No')
elif year % 400 == 0:
	print('Yes')
elif year % 100 == 0:
	print('No')
else:
	print('Yes')