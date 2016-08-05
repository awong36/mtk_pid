#!/usr/bin/env python
# heater setup version 1.0
# updates: setup heater parameters
#Program designed by Adrian Wong
import sys, serial, time
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


class motorConfig(object):
    motorPIDReg = [300, 319, 338, 357, 376, 395]
    fullSpeed_motorPID0 = [5, 1, 1, 5, 30, 1, 500, 250, 700, 20, 700, 600, 1000, 50, 20, 800, 800, 2,
                           600]  #Angular region up
    fullSpeed_motorPID1 = [20, 1, 1, 2, 30, 1, 500, 170, 30000, 20, 700, 400, 700, 40, 20, 350, 700, 2,
                           600]  #Angular region down
    fullSpeed_motorPID2 = [20, 1, 1, 2, 30, 1, 500, 170, 30000, 20, 700, 600, 1000, 50, 50, 800, 800, 2,
                           600]  #Pivot region up
    fullSpeed_motorPID3 = [20, 1, 1, 2, 30, 1, 500, 170, 30000, 20, 700, 300, 400, 40, 50, 350, 400, 2,
                           600]  #Pivot region down
    fullSpeed_motorPID4 = [10, 1, 1, 10, 50, 1, 500, 250, 30000, 20, 700, 100, 1000, 20, 2, 800, 700, 2,
                           600]  #Cook region up
    fullSpeed_motorPID5 = [25, 10, 1, 50, 40, 1, 500, 250, 30000, 20, 700, 65, 350, 20, 2, 350, 500, 2,
                           600]  #Cook region down

    incfullSpeed_motorPID0 = [5, 1, 1, 5, 30, 1, 500, 250, 700, 20, 700, 600, 1000, 50, 20, 800, 800, 2,
                              600]  #Angular region up
    incfullSpeed_motorPID1 = [20, 1, 1, 2, 30, 1, 500, 170, 30000, 20, 700, 400, 700, 40, 20, 350, 700, 2,
                              600]  #Angular region down
    incfullSpeed_motorPID2 = [20, 1, 1, 2, 30, 1, 500, 170, 30000, 20, 700, 600, 1000, 50, 50, 800, 800, 2,
                              600]  #Pivot region up
    incfullSpeed_motorPID3 = [20, 1, 1, 2, 30, 1, 500, 170, 30000, 20, 700, 300, 400, 40, 50, 350, 400, 2,
                              600]  #Pivot region down
    incfullSpeed_motorPID4 = [10, 1, 1, 10, 50, 1, 500, 250, 30000, 20, 700, 100, 1000, 20, 2, 800, 700, 2,
                              600]  #Cook region up
    incfullSpeed_motorPID5 = [25, 10, 1, 50, 40, 1, 500, 250, 30000, 20, 700, 65, 350, 20, 2, 350, 500, 2,
                              600]  #Cook region down

    halfSpeed_motorPID0 = [5, 1, 1, 5, 20, 1, 500, 170, 700, 50, 700, 100, 1000, 100, 5, 1000, 1000, 2,
                           700]  #Angular region up
    halfSpeed_motorPID1 = [5, 1, 1, 2, 30, 1, 500, 170, 30000, 50, 700, 100, 1000, 100, 5, 800, 800, 2,
                           700]  #Angular region down
    halfSpeed_motorPID2 = [5, 1, 1, 5, 20, 1, 500, 170, 700, 50, 700, 100, 1000, 100, 5, 1000, 1000, 2,
                           700]  #Pivot region up
    halfSpeed_motorPID3 = [5, 1, 1, 2, 30, 1, 500, 170, 30000, 50, 700, 100, 1000, 100, 5, 800, 800, 2,
                           700]  #Pivot region down
    halfSpeed_motorPID4 = [5, 1, 1, 5, 20, 1, 500, 170, 700, 50, 700, 100, 1000, 100, 5, 1000, 1000, 2,
                           700]  #Cook region up
    halfSpeed_motorPID5 = [5, 1, 1, 2, 30, 1, 500, 170, 30000, 50, 700, 100, 1000, 100, 5, 800, 800, 2,
                           700]  #Cook region down

    def __init__(self):
        motorPIDReg = self.motorPIDReg
        fullSpeed_motorPID0 = self.fullSpeed_motorPID0
        fullSpeed_motorPID1 = self.fullSpeed_motorPID1
        fullSpeed_motorPID2 = self.fullSpeed_motorPID2
        fullSpeed_motorPID3 = self.fullSpeed_motorPID3
        fullSpeed_motorPID4 = self.fullSpeed_motorPID4
        fullSpeed_motorPID5 = self.fullSpeed_motorPID5

        incfullSpeed_motorPID0 = self.incfullSpeed_motorPID0
        incfullSpeed_motorPID1 = self.incfullSpeed_motorPID1
        incfullSpeed_motorPID2 = self.incfullSpeed_motorPID2
        incfullSpeed_motorPID3 = self.incfullSpeed_motorPID3
        incfullSpeed_motorPID4 = self.incfullSpeed_motorPID4
        incfullSpeed_motorPID5 = self.incfullSpeed_motorPID5

        halfSpeed_motorPID0 = self.halfSpeed_motorPID0
        halfSpeed_motorPID1 = self.halfSpeed_motorPID1
        halfSpeed_motorPID2 = self.halfSpeed_motorPID2
        halfSpeed_motorPID3 = self.halfSpeed_motorPID3
        halfSpeed_motorPID4 = self.halfSpeed_motorPID4
        halfSpeed_motorPID5 = self.halfSpeed_motorPID5

    def setPIDfullSpeed(self, master):
        print "Motor PID Full Speed Setup..."
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[0]+ x, output_value=self.fullSpeed_motorPID0[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[1]+ x, output_value=self.fullSpeed_motorPID1[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[2]+ x, output_value=self.fullSpeed_motorPID2[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[3]+ x, output_value=self.fullSpeed_motorPID3[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[4]+ x, output_value=self.fullSpeed_motorPID4[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[5]+ x, output_value=self.fullSpeed_motorPID5[x])
            time.sleep(0.02)
        print "..............Completed"

    def setPIDincfullSpeed(self, master):
        print "Motor PID Inc Full Speed Setup..."
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[0]+ x, output_value=self.incfullSpeed_motorPID0[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[1]+ x, output_value=self.incfullSpeed_motorPID1[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[2]+ x, output_value=self.incfullSpeed_motorPID2[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[3]+ x, output_value=self.incfullSpeed_motorPID3[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[4]+ x, output_value=self.incfullSpeed_motorPID4[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[5]+ x, output_value=self.incfullSpeed_motorPID5[x])
            time.sleep(0.02)
        print "..............Completed"

    def setPIDhalfSpeed(self, master):
        print "Motor PID Half Speed Setup..."
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[0]+ x, output_value=self.halfSpeed_motorPID0[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[1]+ x, output_value=self.halfSpeed_motorPID1[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[2]+ x, output_value=self.halfSpeed_motorPID2[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[3]+ x, output_value=self.halfSpeed_motorPID3[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[4]+ x, output_value=self.halfSpeed_motorPID4[x])
            time.sleep(0.02)
        for x in range(0, 19):
            master.execute(1, cst.WRITE_SINGLE_REGISTER, self.motorPIDReg[5]+ x, output_value=self.halfSpeed_motorPID5[x])
            time.sleep(0.02)
        print ".................Completed"


def main():
    global instruments
    master = setup()
    motor = motorConfig()
    motor2 = motorConfig()
    motor3 = motorConfig()


    motor.setPIDfullSpeed(master)
    motor2.setPIDincfullSpeed(master)
    motor3.setPIDhalfSpeed(master)

if __name__ == "__main__":
    main()