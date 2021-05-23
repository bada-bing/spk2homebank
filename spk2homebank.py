#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ml 2016
#
# convert mbs csv to homebank csv
#
# python mbs2homebank.py CSV
#
### mbs csv header
# 0 Auftragskonto
# 1 Buchungstag
# 2 Valutadatum
# 3 Buchungstext
# 4 Verwendungszweck
# 5 Beguenstigter/Zahlungspflichtiger
# 6 Kontonummer
# 7 BLZ
# 8 Betrag
# 9 Waehrung
# 10 Info
#
#
### homebank header
# date		format must be DD-MM-YY
# paymode	from 0=none to 10=FI fee
# info		a string
# payee		a payee name
# memo		a string
# amount	a number with a '.' or ',' as decimal separator, ex: -24.12 or 36,75
# category	a full category name (category, or category:subcategory)
# tags		tags separated by space, tag is mandatory since v4.5
#
#
### classification
# date		= Valutadatum
# paymode	= Buchungstext (as int)
# info		= Buchungstext (as string)
# payee		= Beguenstigter/Zahlungspflichtiger
# memo		= Verwendungszweck
# amount	= Betrag
# category	= empty
# tags		= empty
#

import logging;
from string import Template
from paymode import paymodes


### imports
import csv
import argparse
import os
import sys
import datetime

### parse
parser = argparse.ArgumentParser()
parser.add_argument("csv", help="csv from SPK")
args = parser.parse_args()
incsv = args.csv


### functions
def remove_quotes(string):
	if string.startswith('"') and string.endswith('"'):
		string = string[1:-1]
	return string

def convert_date(date):
	return datetime.datetime.strptime(date, '%d.%m.%y').strftime('%d/%m/%Y')


### read csv
try:
	with open(incsv, encoding="utf-8") as csvfile:
		reader = csv.reader(csvfile,delimiter=';', quoting=csv.QUOTE_NONE)
		counter = 1
		firstline = True
		
		for row in reader:
			if firstline:
				firstline = False
				continue

			try:
				date = convert_date(remove_quotes(row[1]))
				paymode = paymodes[remove_quotes(row[3].upper())]
				info = remove_quotes(row[3])
				payee = remove_quotes(row[5])
				memo = remove_quotes(row[4])[:10]
				balance = remove_quotes(row[8])
				
				t = Template('$name,$paymode,$info,$payee,$memo,$balance')
				s = t.substitute(name=date, paymode=paymode, info=info, payee=payee, memo=memo, balance=balance)
				print(s)
			except KeyError as e:
				print("There is an error" + unicode(e).encode("utf-8"))
			except AttributeError as e:
				print("error", e)
			# ;paymode;info;payee;memo;balance;--cat;--tag
			# print "%s;%s;%s;%s;%s;%s;;" % (
			# 	remove_quotes(row[3]),
			# 	remove_quotes(row[5]),
			# 	remove_quotes(row[4]),
			# 	remove_quotes(row[8]),
			# )
except IOError as e:
	print(e)
	print(incsv + " not found")

except:
	print("Unexpected error:", sys.exc_info()[0])
else:
	csvfile.close()
