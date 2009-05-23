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
