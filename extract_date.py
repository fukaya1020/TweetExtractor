# -*- coding: utf-8 -*-
import re
import sys
import os
import codecs
import traceback
import pytz
import tzlocal
from datetime import datetime, date
from datetime import timedelta as td
from dateutil.parser import parse
import timeutils

INPUT_FILE = 'tweets.csv'

tz_jst = pytz.timezone('Asia/Tokyo')

def main():
	i = 0
	tmpline = ""
	outtweets = []

	# 引数解析
	try:
		begindate = timeutils.str_to_datetime('19800101', '')
		enddate = timeutils.str_to_datetime('21000101', '')

		if len(sys.argv) != 3:
			raise Exception			

		begindate = timeutils.str_to_datetime(sys.argv[1], '')
		enddate = timeutils.str_to_datetime(sys.argv[2], '')
		enddate = enddate + td(days=1)

	except Exception:
		print("Usage: python date_split.py yyyymmdd yyyymmdd")
		print(traceback.format_exc())
		sys.exit(1)

	if begindate > enddate:
		print("Begindate & Enddate are opposite.")
		sys.exit(1)

	finput = codecs.open(INPUT_FILE, 'r', 'utf-8')

	for i1, line in enumerate(finput):
		i = i + 1
		if tmpline != "":
			line = tmpline + line
		else:
			line = line[1:]

		# Read a line of input file
		#item_list = line[:-1].replace('\"', '').replace('\n', '\t').split(',')
		item_list = line.replace("\"\n", "\t").split("\",\"")

		if len(item_list) < 10:
			tmpline = line
			continue
		elif i == 1:
			continue
		else:
			tmpline = ""

		tstamp = item_list[3]
		tdtime = parse(tstamp).astimezone(tz_jst)

		if tdtime < begindate or tdtime >= enddate:
			continue

		timestr = tdtime.strftime("%Y-%m-%d %H:%M:%S")
		print(str(tdtime) + " : " + str(timestr) + "  : " + tstamp)

#		foutput.write(timestr + ":," + item_list[5] + '\n')
		outtweets.append("=====" + timestr + "=====\r\n" + item_list[5].replace("\"\"", "\"").replace("\'\'", "\'"))

	OUTPUT_FILE = 'tw_output-%s-%s.txt' % (sys.argv[1], sys.argv[2])
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
