# -*- coding: utf-8 -*-
import re
import sys
import os
import codecs
import pytz
import tzlocal
from datetime import datetime, date, timedelta
from dateutil.parser import parse

INPUT_FILE = 'tweets.csv'
OUTPUT_FILE = 'tw_output.txt'

tz_jst = pytz.timezone('Asia/Tokyo')

def main():
	i = 0
	tmpline = ""
	outtweets = []
	finput = codecs.open(INPUT_FILE, 'r', 'utf-8')

	for line in finput:
		i = i + 1
		if tmpline != "":
			line = tmpline + line

		# Read a line of input file
		item_list = line[:-1].replace('\"', '').replace('\n', '\t').split(',')

		if len(item_list) < 10:
			tmpline = line
			continue
		elif i == 1:
			continue
		else:
			tmpline = ""

		tstamp = item_list[3]
		tdtime = parse(tstamp).astimezone(tz_jst)
		timestr = tdtime.strftime("%Y-%m-%d %H:%M:%S")

#		foutput.write(timestr + ":," + item_list[5] + '\n')
		outtweets.append("=====" + timestr + "=====\r\n" + item_list[5])

	outtweets.reverse()
	foutput = codecs.open(OUTPUT_FILE, 'w', 'utf-8')
	for l in outtweets:
		foutput.write(l.replace('\t', '\r\n') + '\r\n')
	foutput.close()

	
###############################################
# Module to call main function
###############################################
if __name__ == '__main__':
	main()
