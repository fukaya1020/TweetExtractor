# -*- coding: UTF-8 -*-
import sys
import string
import traceback
import pytz
import tzlocal
from datetime import datetime as dt
from datetime import timedelta as tdelta

tz_local = tzlocal.get_localzone()
tz_jst = pytz.timezone('Asia/Tokyo')

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