#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import sys
import tecan_funcs as t

if len(sys.argv)>1:
  action = sys.argv[1]
else:
  action = ""

t.do_cmd("PAZ1829,1829,1829,1829,1829,1829,1829,1829","A1")
t.do_cmd("PAY2000","A1")
t.do_cmd("PAX5500","A1")

t.do_cmd("SHZ1829,1829,1829,1829,1829,1829,1829,1829","A1")
t.do_cmd("SDM3,1","A1")

t.do_cmd("SSL600,600,600,600,600,600,600,600","A1")
t.do_cmd("STL1429,1429,1429,1429,1429,1429,1429,1429","A1")
t.do_cmd("SML527,527,527,527,527,527,527,527","A1")
t.do_cmd("SBL20,20,20,20,20,20,20,20","A1")

t.do_cmd("MDT255,,,,4,4,4,4,4,4,4,4","A1")

t.do_cmd("SSS10,10,10,10,10,10,10,10","A1")


t.do_cmd("MRZ-4,-4,-4,-4,-4,-4,-4,-4","A1")

for foo in range(1,9):
  #t.do_cmd("V3600c900D217M0R","D"+str(foo))
  t.do_cmd("V900P187M200R","D"+str(foo))

t.do_cmd("SSS200,200,200,200,200,200,200,200","A1")

t.do_cmd("MRZ50,50,50,50,50,50,50,50","A1")

delayed = t.Cmd_delayed()
for foo in range(1,9):
  delayed.add_cmd("OV420P30M0R","D"+str(foo))


delayed.start()

t.do_cmd("PAZ1829,1829,1829,1829,1829,1829,1829,1829","A1")

t.close()



