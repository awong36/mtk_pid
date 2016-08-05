#!/usr/bin/env python
# heater PID Control
# updates: egg cooking PID control, derivative parameter change control during cooking, platen control
# Program designed by Adrian Wong
import sys, serial, time, msvcrt, winsound
import heaterSetup_mtk, motorSetup_mtk, homing_mtk, setpoint_wp
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
from CommonFunction import timeCal, signedInt, keyScan
from derivativeMod import dMod, dModGrate
from time import gmtime, strftime


def setup():  #communication setup
    #Configure Hardware
    com_port = 'COM12'  #For windows
    #com_port = '/dev/ttyO4' #For UART4
    #com_port = '/dev/ttyO2' #For UI using UART2
    #com_port = '/dev/ttyUSB0' #For BB USB port
    baud = 115200
    byte = 8
    par = serial.PARITY_EVEN
    stop = 1
    timeout = 1

    #configure communication settings in serConfig
    #instruments = serConfig.serialSetup(com_port, baud, byte, par, stop, timeout)
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=com_port, baudrate=baud, bytesize=byte, parity=par, stopbits=stop, xonxoff=0))
    master.set_timeout(timeout)
    master.set_verbose(True)


    #return instruments, master
    return master

class CookProfile:
    cookTime = 156
    gapTime = 10
    stage1 = 3500
    stage2 = stage1 + 50
    hoodHeight = -5300
    KeyControl = 'r'
    file_name = "log\Right_%Y%b%d_%H.%M.%S.txt"


def readTemp():
    #rear = instruments[1].read_register(Heater.TempReg[0], 0, 3, signed=True)
    rear = master.execute(1,cst.READ_HOLDING_REGISTERS,Heater.TempReg[0],1)
    rear = signedInt(rear[0])
    #mid = instruments[1].read_register(Heater.TempReg[2], 0, 3, signed=True)
    mid = master.execute(1,cst.READ_HOLDING_REGISTERS,Heater.TempReg[2],1)
    mid = signedInt(mid[0])
    #front = instruments[1].read_register(Heater.TempReg[4], 0, 3, signed=True)
    front = master.execute(1,cst.READ_HOLDING_REGISTERS,Heater.TempReg[4],1)
    front = signedInt(front[0])
    #UpGrate = instruments[1].read_register(Heater.TempReg[1], 0, 3, signed=True)
    UpGrate = master.execute(1,cst.READ_HOLDING_REGISTERS,Heater.TempReg[1],1)
    UpGrate = signedInt(UpGrate[0])
    #LoGrate = instruments[1].read_register(Heater.TempReg[3], 0, 3, signed=True)
    LoGrate = master.execute(1,cst.READ_HOLDING_REGISTERS,Heater.TempReg[3],1)
    LoGrate = signedInt(LoGrate[0])
    return rear, mid, front, UpGrate, LoGrate


# def dMod(rearPreTemp, midPreTemp):
#     RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV = readTemp()
#     rear = RearPV - rearPreTemp
#     mid = MiddlePV - midPreTemp
#
#     if rear < -5:  #going down
#         #instruments[1].write_register(132, 22222, 0, 6, signed=True)
#         master.execute(1, cst.WRITE_SINGLE_REGISTER, 132, output_value=22222)
#         time.sleep(0.02)
#     elif rear > 5:  #going up
#         #instruments[1].write_register(132, -22222, 0, 6, signed=True)
#         master.execute(1, cst.WRITE_SINGLE_REGISTER, 132, output_value=-22222)
#         time.sleep(0.02)
#     if mid < -5:
#         #instruments[1].write_register(150, 22222, 0, 6, signed=True)
#         master.execute(1, cst.WRITE_SINGLE_REGISTER, 150, output_value=22222)
#         time.sleep(0.02)
#     elif mid > 5:
#         #instruments[1].write_register(150, -22222, 0, 6, signed=True)
#         master.execute(1, cst.WRITE_SINGLE_REGISTER, 150, output_value=-22222)
#         time.sleep(0.02)
#
#     if copysign(rear, 1) > 5 and copysign(mid, 1) > 5:
#         return RearPV, MiddlePV
#     elif copysign(rear, 1) > 5 and copysign(mid, 1) < 5:
#         return RearPV, midPreTemp
#     elif copysign(rear, 1) < 5 and copysign(mid, 1) > 5:
#         return rearPreTemp, MiddlePV
#     else:
#         return rearPreTemp, midPreTemp
#
#
# def dModGrate(UpGratePreTemp, LoGratePreTemp):
#     RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV = readTemp()
#     UpGrate = UpGratePV - UpGratePreTemp
#     LoGrate = LoGratePV - LoGratePreTemp
#     if UpGrate < -5:
#         #instruments[1].write_register(141, 22222, 0, 6, signed=True)
#         master.execute(1, cst.WRITE_SINGLE_REGISTER, 141, output_value=22222)
#         time.sleep(0.02)
#     elif UpGrate > 5:
#         #instruments[1].write_register(141, -22222, 0, 6, signed=True)
#         master.execute(1, cst.WRITE_SINGLE_REGISTER, 141, output_value=-22222)
#         time.sleep(0.02)
#     if LoGrate < -5:
#         #instruments[1].write_register(159, 22222, 0, 6, signed=True)
#         master.execute(1, cst.WRITE_SINGLE_REGISTER, 159, output_value=22222)
#         time.sleep(0.02)
#     elif LoGrate > 5:
#         #instruments[1].write_register(159, -22222, 0, 6, signed=True)
#         master.execute(1, cst.WRITE_SINGLE_REGISTER, 159, output_value=-22222)
#         time.sleep(0.02)
#
#     if copysign(UpGrate, 1) > 5 and copysign(LoGrate, 1) > 5:
#         return UpGratePV, LoGratePV
#     elif copysign(UpGrate, 1) > 5 and copysign(LoGrate, 1) < 5:
#         return UpGratePV, LoGratePreTemp
#     elif copysign(UpGrate, 1) < 5 and copysign(LoGrate, 1) > 5:
#         return UpGratePreTemp, LoGratePV
#     else:
#         return UpGratePreTemp, LoGratePreTemp


def main():
    #global instruments
    global master
    global Heater
    master = setup()
    motor = motorSetup_mtk.motorConfig()
    motor.setPIDhalfSpeed(master)
    #motor.setPIDfullSpeed(instruments)
    #motor.setPIDincfullSpeed(instruments)


    Heater = heaterSetup_mtk.HeaterConfig()  #initizalize class instance
    Heater.setTempLimit(master)
    Heater.setTcOffset(master)
    Heater.setColdJunction(master)
    Heater.setTcFilter(master)
    Heater.setPid(master, Heater.RpidReg, 9, Heater.Rpid)
    Heater.setPid(master, Heater.MpidReg, 9, Heater.Mpid)
    Heater.setPid(master, Heater.FpidReg, 9, Heater.Fpid)
    Heater.setPid(master, Heater.UpGratepidReg, 9, Heater.UpGratepid)
    Heater.setPid(master, Heater.LoGratepidReg, 9, Heater.LoGratepid)

    homing_mtk.goHome(master, 1)
    motor.setPIDfullSpeed(master)
    setpoint_wp.movePlaten(master, CookProfile.hoodHeight)


    currentTime = 0
    rearTemp, midTemp, frontTemp, UpGrateTemp, LoGrateTemp = readTemp()
    button = 1
    while True:
        print "\n "
        print "Press %r to start new cycle cook time: %rs RearSP:%r dC MidSP:%r dC" % (
            CookProfile.KeyControl, CookProfile.cookTime, Heater.TemperatureSP[0], Heater.TemperatureSP[2])
        done = False

        while not done:
            Heater.setTemp(master)
            RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV = readTemp()
            rearTemp, midTemp = dMod(master, rearTemp, midTemp, RearPV, MiddlePV, FrontPV)
            UpGrateTemp, LoGrateTemp = dModGrate(master, UpGrateTemp, LoGrateTemp, UpGratePV, LoGratePV)
            button = master.execute(1,cst.READ_COILS,2,1) #(id, cst.WRITE_SINGLE_COIL, 35, output_value=state) #(slave,function,address,output)
            button = button[0]
            done = keyScan(1,button,1,1)
            if msvcrt.kbhit():
                Key = msvcrt.getch()
                done = keyScan(2,1,Key,CookProfile.KeyControl)


        #moving platen to setpoint
        setpoint_wp.movePlaten(master, CookProfile.stage1)

        filename = strftime(CookProfile.file_name, time.localtime())
        f = open(filename, "w")
        f.write("\n")
        f.write("\n")
        f.write(strftime("Time:%a, %Y%b%d %H:%M:%S\n", time.localtime()))
        f.write("\n")
        f.write("---------------------Cooking Profile------------------\n")
        f.write("\n")
        f.write("Cooktime:%r s RearSP: %r dC MidSP:%r dC \n" % (
            CookProfile.cookTime, Heater.TemperatureSP[0], Heater.TemperatureSP[2]))
        f.write("------------------------------------------------------\n")
        f.write("----Logged Data(Time-RearTemp,MiddleTmp,FrontTemp-----\n")
        f.write("------------------------------------------------------\n")
        gflag = 0
        flag = 0
        for x in range(0, 3):
            winsound.Beep(1000, 200)
            time.sleep(0.1)
        startTime = time.time()
        done = False
        while timeCal(startTime) < CookProfile.cookTime:
            if currentTime != int(timeCal(startTime)):
                currentTime = int(timeCal(startTime))
                RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV = readTemp()
                f.write("%r,%r,%r,%r,%r,%r\n" % (currentTime, RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV))
                print "Rear heater: %r, Mid heater: %r, Front heater: %r, time: %r s\n" % (
                    RearPV, MiddlePV, FrontPV, CookProfile.cookTime - currentTime)
                if done:
                    break
            if timeCal(startTime) > CookProfile.gapTime and gflag == 0:
                gflag = 1
                #moving platen to setpoint
                setpoint_wp.movePlaten(master, CookProfile.stage2)
            if timeCal(startTime) > CookProfile.cookTime - 6 and flag == 0:
                flag = 1
                for x in range(0, 2):
                    winsound.Beep(1000, 200)
                    time.sleep(0.1)
            button = master.execute(1,cst.READ_COILS,2,1) #(slave,function,address,output)
            button = button[0]
            done = keyScan(1,button,1,1)
            RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV = readTemp()
            rearTemp, midTemp = dMod(master, rearTemp, midTemp, RearPV, MiddlePV, FrontPV)
            UpGrateTemp, LoGrateTemp = dModGrate(master, UpGrateTemp, LoGrateTemp, UpGratePV, LoGratePV)
            #f.write("%r,%r,%r,%r,%r,%r\n" % (currentTime, RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV))
        winsound.Beep(1000, 1000)
        f.close()

        #moving platen to setpoint
        setpoint_wp.movePlaten(master, CookProfile.hoodHeight)


if __name__ == "__main__":
    main()
