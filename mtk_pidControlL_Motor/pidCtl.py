#!/usr/bin/env python
# heater PID Control
# updates: egg cooking PID control, derivative parameter change control during cooking, platen control
# Program designed by Adrian Wong
import sys, serial, time, msvcrt, winsound, csv
import heaterSetup_mtk, motorSetup_mtk, homing_mtk, setpoint_wp
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
from CommonFunction import timeCal, signedInt, keyScan
from derivativeMod import dMod, dModGrate
from time import gmtime, strftime


def setup():  # communication setup
    # Configure Hardware
    com_port = cookInfo[0]  # For windows
    # com_port = '/dev/ttyO4' #For UART4
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


class CookProfile():
    #default values (not used), modify cookProfile.csv to change settings
    #csv file defined as COM_PORT,platenTime,cookTime,cookZone,hoodHeight,KeyControl,file_name
    platenTime = 10
    cookTime = 152
    cookZone = 3050
    hoodHeight = -5200
    KeyControl = 'l'
    file_name = strftime("log\_", time.localtime())
    totalTime = cookTime + platenTime

    def setProfile(self, arg):
        self.platenTime = int(arg[1])
        self.cookTime = int(arg[2])
        self.cookZone = int(arg[3])
        self.hoodHeight = int(arg[4])
        self.KeyControl = arg[5]
        self.file_name = strftime(arg[6], time.localtime())
        self.totalTime = self.cookTime + self.platenTime


def readTemp():
    rear = master.execute(1, cst.READ_HOLDING_REGISTERS, Heater.TempReg[0], 1)
    rear = signedInt(rear[0])
    mid = master.execute(1, cst.READ_HOLDING_REGISTERS, Heater.TempReg[2], 1)
    mid = signedInt(mid[0])
    front = master.execute(1, cst.READ_HOLDING_REGISTERS, Heater.TempReg[4], 1)
    front = signedInt(front[0])
    UpGrate = master.execute(1, cst.READ_HOLDING_REGISTERS, Heater.TempReg[1], 1)
    UpGrate = signedInt(UpGrate[0])
    LoGrate = master.execute(1, cst.READ_HOLDING_REGISTERS, Heater.TempReg[3], 1)
    LoGrate = signedInt(LoGrate[0])
    return rear, mid, front, UpGrate, LoGrate


def main():
    global master
    global cookInfo
    global Heater

    #load settings from file
    cooker = CookProfile()
    with open('cookProfile.csv', 'rb') as cook:
        reader = csv.reader(cook)
        for cookInfo in reader:
            x = 1
    cook.close()
    cooker.setProfile(cookInfo)
    print "Load cookProfile.csv...Completed"
    master = setup()

    motor = motorSetup_mtk.motorConfig()
    motor.setPIDhalfSpeed(master)

    Heater = heaterSetup_mtk.HeaterConfig()  # initizalize class instance
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
    setpoint_wp.movePlaten(master, cooker.hoodHeight)

    currentTime = 0
    rearTemp, midTemp, frontTemp, UpGrateTemp, LoGrateTemp = readTemp()
    button = 1
    while True:
        print "\n "
        print "Press %r to start | Cook time:%rs Platen Time:%rs RearSP:%r dC MidSP:%r dC" % (
            cooker.KeyControl, cooker.cookTime, cooker.platenTime, Heater.TemperatureSP[0], Heater.TemperatureSP[2])
        done = False

        while not done:
            Heater.setTemp(master)
            RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV = readTemp()
            rearTemp, midTemp = dMod(master, rearTemp, midTemp, RearPV, MiddlePV, FrontPV)
            UpGrateTemp, LoGrateTemp = dModGrate(master, UpGrateTemp, LoGrateTemp, UpGratePV, LoGratePV)
            button = master.execute(1, cst.READ_COILS, 2, 1)  # (slave,function,address,output)
            button = button[0]

            done = keyScan(1, 15, button, 1, 1)
            if msvcrt.kbhit():
                Key = msvcrt.getch()
                done = keyScan(2, 15, 1, Key, cooker.KeyControl)


        # moving platen to setpoint
        setpoint_wp.movePlaten(master, cooker.cookZone)
        openName = cooker.file_name + strftime("%Y%b%d_%H.%M.%S", time.localtime()) + ".csv"
        with open(openName, 'w') as log:
            fieldInfo = (
                'StartTime', 'CookTime', 'PlatenTime', 'CookZone', 'RearSP', 'MidSP', 'FrontSP', 'RearPID', 'MidPID',
                'FrontPID')
            targetInfo = csv.DictWriter(log, delimiter=',', lineterminator='\n', fieldnames=fieldInfo)
            Infoheaders = dict((n, n) for n in fieldInfo)
            targetInfo.writerow(Infoheaders)
            targetInfo.writerow(
                {'StartTime': strftime("Time: %Y %b %d %H:%M:%S", time.localtime()), 'CookTime': cooker.cookTime,
                 'PlatenTime': cooker.platenTime, 'CookZone': cooker.cookZone, 'RearSP': Heater.TemperatureSP[0],
                 'MidSP': Heater.TemperatureSP[2], 'FrontSP': Heater.TemperatureSP[4], 'RearPID': Heater.Rpid,
                 'MidPID': Heater.Mpid, 'FrontPID': Heater.Fpid})

            fieldnames = (
                'Time', 'RearTemp', 'MiddleTemp', 'FrontTemp', 'UpGrate', 'LoGrate', 'RearPWM', 'UpPWM', 'MiddlePWM',
                'LoPWM', 'FrontPWM')
            targetWriter = csv.DictWriter(log, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            headers = dict((n, n) for n in fieldnames)
            targetWriter.writerow(headers)

            flag = 0
            for x in range(0, 3):
                winsound.Beep(1000, 200)
                time.sleep(0.1)
            startTime = time.time()
            done = False
            while timeCal(startTime) < cooker.totalTime:
                if currentTime != int(timeCal(startTime)):
                    currentTime = int(timeCal(startTime))
                    RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV = readTemp()
                    pwm = Heater.readPWM(master)
                    targetWriter.writerow(
                        {'Time': currentTime, 'RearTemp': RearPV, 'MiddleTemp': MiddlePV, 'FrontTemp': FrontPV,
                         'UpGrate': UpGratePV, 'LoGrate': LoGratePV, 'RearPWM': pwm[0], 'UpPWM': pwm[1],
                         'MiddlePWM': pwm[2], 'LoPWM': pwm[3], 'FrontPWM': pwm[4]})
                    print "Rear heater: %r, Mid heater: %r, Front heater: %r, time: %r s\n" % (
                        RearPV, MiddlePV, FrontPV, cooker.totalTime - currentTime)
                    if done:
                        break
                if timeCal(startTime) > cooker.totalTime - 6 and flag == 0:
                    flag = 1
                    for x in range(0, 2):
                        winsound.Beep(1000, 200)
                        time.sleep(0.1)
                button = master.execute(1, cst.READ_COILS, 2, 1)  # (slave,function,address,output)
                button = button[0]
                done = keyScan(1, int(timeCal(startTime)), button, 1, 1)
                RearPV, MiddlePV, FrontPV, UpGratePV, LoGratePV = readTemp()
                rearTemp, midTemp = dMod(master, rearTemp, midTemp, RearPV, MiddlePV, FrontPV)
                UpGrateTemp, LoGrateTemp = dModGrate(master, UpGrateTemp, LoGrateTemp, UpGratePV, LoGratePV)
        log.close()
        winsound.Beep(1000, 1000)


        # moving platen to setpoint
        setpoint_wp.movePlaten(master, cooker.hoodHeight)


if __name__ == "__main__":
    main()
