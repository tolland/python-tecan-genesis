#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import sys
import tecan_funcs as t

if len(sys.argv)>1:
  action = sys.argv[1]
else:
  action = ""

#@todo check init

zval="1800"
zvals=[zval,zval,zval,zval,zval,zval,zval,zval]
t.do_cmd("PAZ"+",".join(zvals),"A1")
t.do_cmd("PAY2000","A1")
t.do_cmd("PAX5500","A1")

t.do_cmd("SHZ2080,2080,2080,2080,2080,2080,2080,2080","A1")

t.do_cmd("PAY2040","A1")
t.do_cmd("PAX10160","A1")

zval="1400"
zvals=[zval,zval,zval,zval,zval,zval,zval,zval]
t.do_cmd("PAZ"+",".join(zvals),"A1")

for foo in range(1,9):
  t.do_cmd("V3600c900D217M0R","D"+str(foo))

zval="1800"
zvals=[zval,zval,zval,zval,zval,zval,zval,zval]
t.do_cmd("PAZ"+",".join(zvals),"A1")

t.close()


