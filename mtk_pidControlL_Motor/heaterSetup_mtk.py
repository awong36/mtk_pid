#!/usr/bin/env python
#heater setup version 1.0
#updates: setup heater parameters
#Program designed by Adrian Wong
import sys, minimalmodbus, serial, time
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu


def setup():  #communication setup
    #Configure Hardware
    com_port = 'COM45'  #For windows
    #com_port = '/dev/ttyO4' #For UART4
    #com_port = '/dev/ttyO2' #For UI using UART2
    #com_port = '/dev/ttyUSB0' #For BB USB port
    baud = 115200
    byte = 8
    par = serial.PARITY_EVEN
    stop = 1
    timeout = 1

    #configure communication settings in serConfig
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=com_port, baudrate=baud, bytesize=byte, parity=par, stopbits=stop, xonxoff=0))
    master.set_timeout(timeout)
    master.set_verbose(True)

    return master


class HeaterConfig(object):
    #variables within class
    SendDelay = 5

    #SIB registers
    TempLimitReg = [52, 53, 54, 55, 56]
    TempReg = [84, 85, 86, 87, 88]
    TempSpReg = [92, 93, 94, 95, 96]
    TcOffsetReg = [247, 248, 249, 250, 251]
    TcColdJuncReg = [256, 257]
    TcFilterReg = 258
    pwmReg = [278,279,280,281,282]
    RpidReg = 124
    MpidReg = 142
    FpidReg = 160
    UpGratepidReg = 133
    LoGratepidReg = 151

    #settings
    TempLimit = [2211,2211,2211,2211,2211]
    TemperatureSP = [1406, 1489, 1406, 1489, 1406]
    TcOffset = [-35, -50, -35, -50, -35]
    TcColdJunc = [1, 2]
    TcFilter = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  #0 to 15 mult/div, total of 16 reg

    Rpid = [5, 1, 1, 10, 1000, 1, 32767, -10, -22222]  #0 to 8, total of 9 reg
    Mpid = [5, 1, 1, 10, 1000, 1, 32767, -10, -22222]
    Fpid = [5, 1, 1, 10, 100, 1, 32767, -50, -22222]
    UpGratepid = [5, 1, 1, 10, 100, 1, 32767, -50, -22222]
    LoGratepid = [5, 1, 1, 10, 100, 1, 32767, -50, -22222]

    KeyControl = 's'

    #functions within class
    def __init__(self):
        SendDelay = self.SendDelay
        TempLimitReg = self.TempLimitReg
        TempLimit = self.TempLimit
        TempReg = self.TempReg
        TemperatureSP = self.TemperatureSP
        TempSpReg = self.TempSpReg
        TcOffsetReg = self.TcOffsetReg
        TcOffset = self.TcOffset
        TcColdJuncReg = self.TcColdJuncReg
        TcColdJunc = self.TcColdJunc
        TcFilterReg = self.TcFilterReg
        TcFilter = self.TcFilter
        pwmReg = self.pwmReg
        RpidReg = self.RpidReg
        Rpid = self.Rpid
        MpidReg = self.MpidReg
        Mpid = self.Mpid
        FpidReg = self.FpidReg
        Fpid = self.Fpid
        UpGratepidReg = self.UpGratepidReg
        LoGratepidReg = self.LoGratepidReg
        UpGratepid = self.UpGratepid
        LoGratepid = self.LoGratepid
        KeyControl = self.KeyControl

    def setTempLimit(self,master):
        for x in range(5):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.TempLimitReg[x], output_value=self.TempLimit[x])
            time.sleep(0.02)
        print "Temp Limit Setup...Completed"

    def setTcOffset(self,master):
        for x in range(5):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.TcOffsetReg[x], output_value=self.TcOffset[x])
            time.sleep(0.02)
        print "TcOffset setup...Completed"

    def setTemp(self,master):
        for x in range(5):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.TempSpReg[x], output_value=self.TemperatureSP[x])
            time.sleep(0.02)

    def setColdJunction(self,master):
        master.execute(1, cst.WRITE_SINGLE_REGISTER, self.TcColdJuncReg[0], output_value=self.TcColdJunc[0])
        time.sleep(0.02)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, self.TcColdJuncReg[1], output_value=self.TcColdJunc[1])
        time.sleep(0.02)
        print "CJ Filter Setup...Completed"

    def setTcFilter(self,master):
        for x in range(16):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.TcFilterReg + x, output_value=self.TcFilter[x])
            time.sleep(0.02)
        print "Tc Filter setup...Completed"
    def setPid(self,master, initReg, plusReg, pid):
        for x in range(0, plusReg):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, initReg + x, output_value=pid[x])
            time.sleep(0.02)
        print "Heater PID setup...Completed"

    def readPWM(self,master):
        pwm = list()
        for x in range(0,5):
            temp = master.execute(1,cst.READ_HOLDING_REGISTERS,self.pwmReg[x],1)
            pwm.append(temp[0])
        return pwm

def main():
    global instruments
    master = setup()
    Heater = HeaterConfig()  #initizalize class instance

    Heater.setTempLimit(master)
    Heater.setTcOffset(master)
    Heater.setColdJunction(master)
    Heater.setTcFilter(master)
    Heater.setPid(master,Heater.RpidReg, 9, Heater.Rpid) #rear pid
    Heater.setPid(master,Heater.MpidReg, 9, Heater.Mpid) #mid pid
    Heater.setPid(master,Heater.FpidReg, 9, Heater.Fpid) #front pid
    Heater.setPid(master,Heater.UpGratepidReg, 9, Heater.UpGratepid)
    Heater.setPid(master,Heater.LoGratepidReg, 9, Heater.LoGratepid)
    print "Heater Setup Completed..."


if __name__ == "__main__":
    main()
