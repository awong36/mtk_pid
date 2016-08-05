#!/usr/bin/env python
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import serial,time
from CommonFunction import signedInt

class goHome():
    def __init__(self, master, device):
        self.master = master
        self.device = device
        try:
            HomingStatus = master.execute(1, cst.READ_HOLDING_REGISTERS, 25, 1)
            #time.sleep(0.2)
        except IOError:
            print "Device %r reading home register failed (IOError)...proceed with homing" % device
            HomingStatus = 0
            pass
        # print "Homing Status:", HomingStatus
        HomingStatus = int(HomingStatus[0])
        currentPosition = -0
        ready = -0
        if HomingStatus == 0:
            print "*******Homing Sequence Starts*********"
            try:
                master.execute(1, cst.WRITE_SINGLE_REGISTER, 255, output_value=1)
                time.sleep(0.2)
            except IOError:
                print "Device %r homing failed (IOError)" % device
                pass
            status = 0
        else:
            print "Device # %s already Homed" % device
            status = 1

         #print current position to terminal	(must disable if running multiple units)
        while status !=1:
            if HomingStatus != 5:
                HomingStatus = master.execute(1, cst.READ_HOLDING_REGISTERS,25,1)
                HomingStatus = signedInt(HomingStatus[0])

            elif HomingStatus == 5:
                HomingStatus = master.execute(1, cst.READ_HOLDING_REGISTERS,25,1)
                HomingStatus = signedInt(HomingStatus[0])
                status = 1
                print "Homing Sequence...Completed"