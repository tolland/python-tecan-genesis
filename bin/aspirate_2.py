#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import sys
import tecan_funcs as t

if len(sys.argv)>1:
  action = sys.argv[1]
else:
  action = ""

t.do_cmd("PAZ1429,1429,1429,1429,1429,1429,1429,1429","A1")
t.do_cmd("PAY5510","A1")
t.do_cmd("PAX5500","A1")

t.do_cmd("SHZ1480,1480,1480,1480,1480,1480,1480,1480","A1")
t.do_cmd("SDM3,1","A1")

t.do_cmd("SSL600,600,600,600,600,600,600,600","A1")
t.do_cmd("STL1429,1429,1429,1429,1429,1429,1429,1429","A1")
t.do_cmd("SML527,527,527,527,527,527,527,527","A1")
t.do_cmd("SBL20,20,20,20,20,20,20,20","A1")

t.do_cmd("MDT255,,,,1,1,1,1,1,1,1,1","A1")

for foo in range(1,9):
  t.do_cmd("V900P187M200R","D"+str(foo))

t.close()



