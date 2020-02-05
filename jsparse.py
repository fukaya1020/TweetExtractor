# -*- coding: utf-8 -*-
import re
import sys
import os
import codecs
import json
import pytz
import traceback
import tzlocal
from datetime import datetime, date
from datetime import timedelta as td
from dateutil.parser import parse
import timeutils

INPUT_FILE = 'tweet.js'
OUTPUT_FILE = 'tw_output.txt'

tz_jst = pytz.timezone('Asia/Tokyo')

# ツイート情報に関するオブジェクト
class tweetinfo:
	timestamp = None
	tweet = None
	timestr = None

	def __init__(self, timestamp, tweet):
		self.timestamp = timestamp
		self.tweet = tweet

	def __lt__(self, other):
		# self < other
		return self.timestamp < other.timestamp

	def __repr__(self):
		return repr((self.timestamp, self.tweet))


def main():
	i = 0
	out_num = 0
	tmpline = ""
	tweet_list = []

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
		print("Usage: python jsparse.py yyyymmdd yyyymmdd")
		print(traceback.format_exc())
		sys.exit(1)

	if begindate > enddate:
		print("Begindate & Enddate are opposite.")
		sys.exit(1)

	jsonstr = ""
	with open(INPUT_FILE) as f:
		s = f.read()
		jsonstr = jsonstr + str(s)

	json_start_pos = 0
	jsonstr_len = len(jsonstr)
	for i1 in range(jsonstr_len):
		if jsonstr[i1] == '[':
			json_start_pos = i1
			break
	jsonstr = jsonstr[json_start_pos:]
	json_dict = json.loads(jsonstr)
	json_count = len(json_dict)

	for i1 in range(json_count):
		try:
			dt_val = timeutils.jsstr_to_datetime(str(json_dict[i1]["tweet"]["created_at"]))
			tweet_s = str(json_dict[i1]["tweet"]["full_text"])
			if tweet_s is not None:
				tweet_s = tweet_s.replace("\"\"", "\"").replace("\'\'", "\'").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")

			if dt_val >= begindate and dt_val < enddate:
				tinfo = tweetinfo(dt_val, tweet_s)
				tinfo.timestr = "=====" + dt_val.strftime("%Y-%m-%d %H:%M:%S") + "====="
				tweet_list.append(tinfo)
		except:
			print(traceback.format_exc())
			break

	sorted_tweets = sorted(tweet_list)

	OUTPUT_FILE = 'tw_output-%s-%s.txt' % (sys.argv[1], sys.argv[2])

	foutput = codecs.open(OUTPUT_FILE, 'w', 'utf-8')
	for stw in sorted_tweets:
		if stw.tweet is not None:
			foutput.write(stw.timestr + '\r\n' + stw.tweet + '\r\n')
			out_num = out_num + 1
	foutput.close()

	print("OUTPUT TWEETS: " + str(out_num))
	print("ALL TWEETS: " + str(json_count))

###############################################
# Module to call main function
###############################################
if __name__ == '__main__':
	main()
