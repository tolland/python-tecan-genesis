
import time
import serial

def parse_stream(buff=""):
  pass

# portmon dump
# 74	0.00000810	RSPDRV.exe	IOCTL_SERIAL_SET_BAUD_RATE	Serial0	SUCCESS	Rate: 9600	
# 77	0.00000363	RSPDRV.exe	IOCTL_SERIAL_SET_LINE_CONTROL	Serial0	SUCCESS	StopBits: 1 Parity: NONE WordLength: 8	


ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1, writeTimeout=5, interCharTimeout=10 )

#if ser.isOpen():
#  print "port is open"

# portmon dump. seems like it asserts DTR and RTS always on
# 75	0.00000559	RSPDRV.exe	IOCTL_SERIAL_SET_RTS	Serial0	SUCCESS		
#ser.setRTS(False)

# 76	0.00000419	RSPDRV.exe	IOCTL_SERIAL_SET_DTR	Serial0	SUCCESS		
#ser.setDTR(False)

# 17	0.00000223	RSPDRV.exe	IOCTL_SERIAL_SET_CHAR	Serial0	SUCCESS	EOF:0 ERR:0 BRK:0 EVT:0 XON:11 XOFF:13	
#18	0.00000419	RSPDRV.exe	IOCTL_SERIAL_SET_HANDFLOW	Serial0	SUCCESS	Shake:1 Replace:40 XonLimit:2048 XoffLimit:512	

# I haven't yet seen any XON/XOFF chars in the dump, so am disabling for the moment
#ser.setXonXoff(False)

# the bit mask for Shake and Replace are
# SERIAL_DTR_CONTROL 0x01
# SERIAL_NULL_STRIPPING  0x8
# SERIAL_RTS_CONTROL 0x20

romaaxis = ("x", "y", "z", "r", "g")
lihiaxis = ("x", "y", "ys", "z1", "z2", "z3", "z4", "z5", "z6", "z7", "z8")

seq = ("A","B","C","D","E","F","G")
seqnum = 0

def nextseq():
  global seqnum, seq
  
  if seqnum >= len(seq):
    seqnum=0

  nextseq=seq[seqnum]
  seqnum+=1
  
  return nextseq

def do_flush():
  
  pass

class Cmd_delayed:
  'Common base class for all cmds stacks'
  cmdCount = 0

  def __init__(self):
    self.runningStack = []
    self.cmdStack = []
   
  def add_cmd(self, cmd="RFV",dev="M1"):
   self.cmdStack.append((cmd,dev))
   Cmd_delayed.cmdCount += 1


  def start(self, cmd="RFV",dev="M1"):

    do_cmd("GFC","M1")

    for (cmd,dev) in self.cmdStack:
     do_cmd_delayed(cmd,dev)
     self.runningStack.append(dev)

    print self.runningStack
     
    do_cmd("GSC","M1")
    
    for dev in self.runningStack:
      res2 = read(ser,dev)
  
      print "Second Ack/Data: "+res2
      
      #strMes  = "@"+dev

      print "Reply Ack: @"+dev

      strMes  = [ord(x) for x in "@"+dev]
      strMes.insert(0, 2)
      strMes.append(3)

      oldch=0x0
      xored=0x0

      for ch in strMes:
        xored = oldch ^ ch
        oldch = xored
        
      #print "check bit"+str(xored)
      strMes.append(xored)
      #print repr(strMes)
      strMes = "".join([chr(foo) for foo in strMes])
      #print "writing %s " % strMes
      
      ser.write(strMes+'\n')      # write a string


def do_cmd_delayed(cmd="RFV",dev="M1"):
  ch=nextseq()
  ser.flushInput()
  print "calling command "+ch+dev+cmd
  strMes  = [ord(x) for x in ch+dev+cmd]
  strMes.insert(0, 2)
  strMes.append(3)

  oldch=0x0
  xored=0x0

  for ch in strMes:
    xored = oldch ^ ch
    oldch = xored
    
  #print "check bit"+str(xored)
  strMes.append(xored)
  #print repr(strMes)
  strMes = "".join([chr(foo) for foo in strMes])
  #print(strMes+'\n')
  #for foo in strMes:
  #  print hex(ord(foo))
  #return
  ser.write(strMes+'\n')      # write a string
  
  time.sleep(0.1) 
  
  res1 = read(ser,dev)
  
  print "First Ack: "+res1
  
  time.sleep(0.1) 
  

  
  
def do_cmd(cmd="RFV",dev="M1"):
  ch=nextseq()
  ser.flushInput()
  print "calling command "+ch+dev+cmd
  strMes  = [ord(x) for x in ch+dev+cmd]
  strMes.insert(0, 2)
  strMes.append(3)

  oldch=0x0
  xored=0x0

  for ch in strMes:
    xored = oldch ^ ch
    oldch = xored
    
  strMes.append(xored)
  strMes = "".join([chr(foo) for foo in strMes])
  ser.write(strMes+'\n')
  
  time.sleep(0.1) 
  
  res1 = read(ser,dev)
  
  print "First Ack: "+res1
  
  time.sleep(0.1) 
  
  res2 = read(ser,dev)
  
  print "Second Ack/Data: "+res2
  
  #strMes  = "@"+dev

  print "Reply Ack: "+res1

  strMes  = [ord(x) for x in res1]
  strMes.insert(0, 2)
  strMes.append(3)

  oldch=0x0
  xored=0x0

  for ch in strMes:
    xored = oldch ^ ch
    oldch = xored
    
  #print "check bit"+str(xored)
  strMes.append(xored)
  #print repr(strMes)
  strMes = "".join([chr(foo) for foo in strMes])
  #print "writing %s " % strMes
  
  ser.write(strMes+'\n')      # write a string

def close():

  ser.close()             # close port

def showBytes(str):
  for foo in str:
    print repr(foo),
  print

def read(conn,devstr):
  
  time.sleep(0.2) 

  #print "There are "+str(conn.inWaiting())+" characters waiting"

  chars = conn.inWaiting()
  
  buff=""
  msgs=[]
  inword=False
  etx=False #set this at etx to collect next byte for xor check

  looking = True

  #print "Initially %d chars" % chars
  line = ""

  while looking:
    if chars > 0:
      
      line += conn.read(1)
      
      if (line.find('\x02') > -1) and (line.find('\x03') > -1):
        
        #print "reading %d chars from input" % chars
        
        for foo in line:
          if ord(foo) == 0:
            continue #NUL 
          elif ord(foo) == 2:
            #print "stx"
            inword=True
            buff=""
          elif ord(foo) == 3 and inword==True:
            #print "etx"
            inword=False
            etx=True
            msgs.append(buff)
            
          elif inword==True:
            buff=buff+foo
            
          if etx==True: # next char after is xor byte
            etx=False
            xor=foo
      #end if
      
      for msg in msgs:
#        print "'"+msg+"'=="+"@"+devstr
        #showBytes(msg)
#        showBytes("@"+devstr)
        if msg=="@"+devstr:
          #print "found it breaking on: "+msg
          looking = False
          return msg
          #break
        elif msg=="@"+devstr:
          pass
        else:
          #print "other message is "+msg
          return msg
      #end for
      
      #print line
      
    #end if
    time.sleep(0.1) 
    chars = conn.inWaiting()
    #print chars,
    #print "Now %d chars" % chars
  #end while

def do_action(action="RFV",args=[]):
  


  if action == "firmware":

    do_cmd("RFV0","M1")


  elif action == "roma":

    for axis in ("X","Y","Z"):
      for i in range(0,8):
        do_cmd("RP"+axis+str(i),"R1")


  elif action == "romapos":

    for axis in ("X","Y","Z"):
      
        do_cmd("RP"+axis+"0","R1")


  elif action == "roma_home":
    
    
    
    do_cmd("PAZ2480","R1")
    do_cmd("PAR0","R1")
    do_cmd("PAY0","R1")
    do_cmd("PAX0","R1")

  elif action == "roma_x":
    
    xpos=args[0]
    
    do_cmd("PAX"+str(xpos),"R1")


  elif action == "roma_rx":
    
    xpos=args[0]
    
    do_cmd("PRX"+str(xpos),"R1")

  elif action == "roma_r":
    
    xpos=args[0]
    
    do_cmd("PAR"+str(xpos),"R1")
    
    
  elif action == "roma_y":
    
    xpos=args[0]
    
    do_cmd("PAY"+str(xpos),"R1")  
    
    
    
  elif action == "roma_ry":
    
    xpos=args[0]
    
    do_cmd("PRY"+str(xpos),"R1")  
    
    
  elif action == "roma_g":
    
    xpos=args[0]
    
    do_cmd("PAG"+str(xpos),"R1")  
      
  elif action == "roma_rg":
    
    xpos=args[0]
    
    do_cmd("PRG"+str(xpos),"R1")  
    
  elif action == "grippos":
    
    do_cmd("RPG0","R1")
    
  # zero the ROMA to the current position     
  elif action == "roma_zero":

    do_cmd("PIF","R1")
    
      
    
  elif action == "roma_z":
    
    xpos=args[0]
    
    do_cmd("PAZ"+str(xpos),"R1")
    
        
    
  elif action == "roma_rz":
    
    xpos=args[0]
    
    do_cmd("PRZ"+str(xpos),"R1")
    
    

  elif action == "liha":

    for axis in ("X","Y","Z"):
      for i in range(0,8):
        do_cmd("RP"+axis+str(i),"A1")


  elif action == "lihapos":

    for axis in ("X","Y","Z"):
      
        do_cmd("RP"+axis+"0","A1")


  elif action == "init_l":
    do_cmd("PIA","A1")
    
    print "init liha complete"

  elif action == "init_r":
    do_cmd("PIA","R1")
    
    print "init Roma complete"
    
  elif action == "init":
    do_cmd("PIS","M1")
    
    do_cmd("PIA","R1")
    print "init both complete"

  elif action == "read":
    print "reading buffer"


    '''
    PAA - POSITION ABSOLUTE FOR ALL AXIS:
  X, Y, Ys, Z1, Z2, Z3, Z4, Z5, Z6, Z7, Z8
  POSITION ABSOLUTE FOR ALL AXIS:
  The PAA command moves the X/Y/Z-axis to the entered coordinates in the absolute field. After using this command, the Z-travel heights, set with the SHZ command is in effect. If no Z-travels are set by SHZ command the Z-drives move to init position while traveling. The number of Z parameter depends on the number of installed tips.
  X:	distance in 0.1 mm  [(-InitOffset + 10)...X-Range set by SRA cmd] 
  Y:	distance in 0.1 mm  [(-InitOffset + 10)...Y-Range set by SRA cmd]  of tip 1.
  Ys:	space distance in 0.1 mm [90...380]  min. distance 9 mm,  max. distance 38 mm.
  Zi:	distance in 0.1 mm [(-InitOffset + 10)...Z-Range set by SRA cmd] of tip i [1..8]
  EXAMPLE: #A1PAA1000,200,100,500,500,500,500,500,500,500,500
  Moves all axis to the specified coordinates. The tips moves up to Z-travel position while moving.
  RESPONSE: none
  GENERATED ERRORS:  (3) invalid operand, (7) device not init, (10) drive no load, (13) Arm collision avoided with PosId, (17) Arm collision avoided with ROMA.
    '''

  elif action == "go_waste":
    #do_cmd("PAA5510,2027,90,1480,1480,1480,1480,1480,1480,1480,1480")
    
    do_cmd("PAA5295,1031,90,1200,1200,1200,1200,1200,1200,1200,1200","A1")
    
    
      
  elif action == "errors":
    print "reading system errors"
    for addr in ("M", "A", "P", "R"):
      do_cmd("REE",addr+"1")
      
      
  elif True:
    print t.nextseq()
    print t.nextseq()
    print t.nextseq()





