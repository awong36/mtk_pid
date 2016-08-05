#!/usr/bin/env python
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
from CommonFunction import signedInt

class movePlaten():
    def __init__(self, master, sp):
        self.master = master
        self.sp = sp

        try:
            print "******* Moving to Set Point *********"
            master.execute(1, cst.WRITE_SINGLE_REGISTER, 0, output_value=sp)

        # print current position to terminal
            currentPosition = -0
            ready = -0
            # while ready != -32768:
            #     ready = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1)
            #     ready = signedInt(ready[0])
            #     currentPosition = master.execute(1, cst.READ_HOLDING_REGISTERS, 3, 1)
            #     currentPosition = signedInt(currentPosition[0])
            # print "******* Platen at %r *********" %currentPosition
        except IOError:
            print "Moving to setpoint failed (IOError)... ..."
            pass

