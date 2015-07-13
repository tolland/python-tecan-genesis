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

t.do_cmd("PAY2000","A1")
t.do_cmd("PAX5500","A1")

t.do_cmd("RPX0","R1")

t.do_cmd("RPX0","R9")

t.do_cmd("SHZ2080,2080,2080,2080,2080,2080,2080,2080","A1")

t.do_cmd("RPX0","A1")

t.do_cmd("RPY0","A1")
t.do_cmd("RPY0","A1")




#t.do_cmd("GFC","M1")

for foo in range(1,9):
  t.do_cmd("OV120P60M0R","D"+str(foo))

#t.do_cmd("GSC","M1")

t.do_cmd("MDT255,20,1480,1100","A1")

#Length 12: .BA1SDM3,1.G
t.do_cmd("SDM3,1","A1")
t.do_cmd("SBL20,20,20,20,20,20,20,20","A1")
t.do_cmd("SSL600,600,600,600,600,600,600,600","A1")

t.do_cmd("SDR40,40,40,40,40,40,40,40","A1")
t.do_cmd("SML527,527,527,527,527,527,527,527","A1")
t.do_cmd("STL1429,1429,1429,1429,1429,1429,1429,1429","A1")

t.do_cmd("SSS10,10,10,10,10,10,10,10,","A1")



t.do_cmd("MDT255,,,,1,1,1,1,1,1,1,1","A1")

for foo in range(1,9):
  t.do_cmd("V900P60M200R","D"+str(foo))


#Length 32: .DA1SDR40,40,40,40,40,40,40,40.\	
#Length 48: .EA1STL1429,1429,1429,1429,1429,1429,1429,1429.S	
#Length 40: .FA1SML527,527,527,527,527,527,527,527.I	
#Length 32: .GA1SBL20,20,20,20,20,20,20,20.G	
#Length 31: .AA1MDT255,,,,1,1,1,1,1,1,1,1.s	
#Length 10: .BA1RPZ0.[	
##Length 30: ,977,981,977,984,980,980,986.@	
#Length 32: .CA1SSS10,10,10,10,10,10,10,10.M	

t.do_cmd("SSS200,200,200,200,200,200,200,200","A1")

t.do_cmd("PAZ2000","A1")

for foo in range(1,9):
  t.do_cmd("V3600c900D92M0R","D"+str(foo))



t.close()


