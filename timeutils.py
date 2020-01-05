# -*- coding: UTF-8 -*-
import sys
import string
import re
import traceback
import pytz
import tzlocal
from datetime import datetime as dt
from datetime import timedelta as tdelta

tz_local = tzlocal.get_localzone()
tz_jst = pytz.timezone('Asia/Tokyo')

#regex_js_datetime_format = r'([A-z]{3}) ([A-z]{3}) ([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}) \+([0-9]{4}) (20[0-9]{2})'
regex_js_datetime_format = r'([A-z]{3}) ([A-z]{3}) ([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}) \+([0-9]{4}) (20[0-9]{2})'

list_month = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def get_index_month(x):
	if x in list_month:
		return list_month.index(x)
	else:
		return -1

######## 日付⇔文字列 ########
def str_to_datetime(yyyymmdd, separator):
	yyyymmdd_format = '%Y' + separator + '%m' + separator + '%d'
	try:
		tdate = dt.strptime(yyyymmdd, yyyymmdd_format)
		tdate = tdate.replace(tzinfo=tz_jst)
		return tdate
	except:
		return None

def datetime_to_str(date_dt, separator):
	yyyymmdd_format = '%Y' + separator + '%m' + separator + '%d'
	try:
		tstr = date_dt.strftime(yyyymmdd_format)
		return tstr
	except:
		return None

def jsstr_to_datetime(js_dt_str):
	#Sat Apr 27 13:07:43 +0000 2019"
	regex_rslt = re.match(regex_js_datetime_format, js_dt_str)
	if regex_rslt:
		month = get_index_month(regex_rslt.group(2))
		day = int(regex_rslt.group(3))
		hour = int(regex_rslt.group(4))
		minute = int(regex_rslt.group(5))
		second = int(regex_rslt.group(6))
		year = int(regex_rslt.group(8))

		retdt = dt(year, month, day, hour, minute, second).replace(tzinfo=tz_jst)
		retdt = retdt + tdelta(hours=9)
		return retdt
	else:
		return None
