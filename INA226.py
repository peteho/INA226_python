#!/usr/bin/env python

import smbus
import sys
import time
import os

class INA226(object):
  def __init__(self):
    self.INA226_ADDR = 0x40
    self.INA226_CONFIG = 0x2741
    self.INA226_CALIBRATION = 0x0002
    self.INA226_REG_CONFIG = 0x00
    self.INA226_REG_SHUNTVOLTAGE = 0x01
    self.INA226_REG_BUSVOLTAGE = 0x02
    self.INA226_REG_POWER = 0x03
    self.INA226_REG_CURRENT = 0x04
    self.INA226_REG_CALIBRATION = 0x05
    self.currentLSB = 0.0001
    self.powerLSB = 0.0025
    
    self.ina226 = smbus.SMBus(1)

  def get_status(self):
    self.status = False
    try:
      self.ina226.read_byte(self.INA226_ADDR)
      #print("INA226 detected")
      #ina226 = True
      #self.ina226.write_word_data(INA226_ADDR, INA226_REG_CONFIG, self.ina226.read_word_data(INA226_ADDR, INA226_REG_CONFIG) | 0x0080)
      self.ina226.write_word_data(self.INA226_ADDR, self.INA226_REG_CONFIG, self.INA226_CONFIG)
      self.ina226.write_word_data(self.INA226_ADDR, self.INA226_REG_CALIBRATION, self.INA226_CALIBRATION)
      #print("%04x" % self.ina226.read_word_data(INA226_ADDR, INA226_REG_CONFIG))
      #print("%04x" % self.ina226.read_word_data(INA226_ADDR, INA226_REG_CALIBRATION))
      self.status = True
    except IOError:
      print("INA226 not detected")
      #ina226 = False
    return self.status
	
  def busVoltage(self):
    if self.get_status():
      val = self.ina226.read_word_data(self.INA226_ADDR, self.INA226_REG_BUSVOLTAGE)
    else:
      val = 0
    valh = (val & 0xff00) >> 8
    vall = (val & 0x00ff)
    val = (vall << 8) | valh
    return val * 0.00125

  def shuntVoltage(self):
    if self.get_status():
      val = self.ina226.read_word_data(self.INA226_ADDR, self.INA226_REG_SHUNTVOLTAGE)
    else:
      val = 0
    valh = (val & 0xff00) >> 8
    vall = (val & 0x00ff)
    val = (vall << 8) | valh
    return val * 0.0000025

  def shuntCurrent(self):
    if self.get_status():
      val = self.ina226.read_word_data(self.INA226_ADDR, self.INA226_REG_CURRENT)
    else:
      val = 0
    valh = (val & 0xff00) >> 8
    vall = (val & 0x00ff)
    val = (vall << 8) | valh
    return val * self.currentLSB
	

def main():
  ina226 = INA226()
  print("INA226 detected: %s" % ina226.get_status())
  print("Voltage:  %6.3f V" % ina226.busVoltage())
  print("Current:  %6.3f A" % ina226.shuntCurrent())
  print("sVoltage: %6.3f V" % ina226.shuntVoltage())

  
if __name__ == '__main__':
  main()
