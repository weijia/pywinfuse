from ctypes import *

def setDwordByPoint(valueAddress, value):
  '''
  valueAddress[0] = value && 0xff
  valueAddress[1] = (value >> 8) && 0xff 
  '''
  i = 0
  while i < 4:
    memset(valueAddress+i, value&0xff, 1)
    i += 1
    value >>= 8


def setLongLongByPoint(valueAddress, value):
  setDwordByPoint(valueAddress, value & 0xffffffff)
  setDwordByPoint(valueAddress+4, (value>>32) & 0xffffffff)


def setStringByPoint(valueAddress, value, length):
  cnt = 0
  for i in value:
    #print i
    cnt += 2
    if cnt+2 > length:
      break
    #0061: u'a' -> 0x00000000: 61, 0x00000001: 00
    memset(valueAddress, ord(i)&0xff, 1)
    valueAddress += 1
    memset(valueAddress, (ord(i)>>8)&0xff, 1)
    valueAddress += 1
    #print valueAddress
  memset(valueAddress, 0, 1)
  valueAddress += 1
  memset(valueAddress, 0, 1)
