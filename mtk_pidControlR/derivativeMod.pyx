import modbus_tk, time
import modbus_tk.defines as cst
from math import copysign

def dMod(master,rearPreTemp, midPreTemp, RearPV, MiddlePV, FrontPV):
    cdef int RPV, MPV, FPV, rPreTemp, mPreTemp
    RPV = RearPV
    MPV = MiddlePV
    FPV = FrontPV
    rPreTemp = rearPreTemp
    mPreTemp = midPreTemp
    cdef int rear = RearPV - rPreTemp
    cdef int mid = MiddlePV - mPreTemp

    if rear < -5:  #going down
        #instruments[1].write_register(132, 22222, 0, 6, signed=True)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 132, output_value=22222)
        time.sleep(0.02)
    elif rear > 5:  #going up
        #instruments[1].write_register(132, -22222, 0, 6, signed=True)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 132, output_value=-22222)
        time.sleep(0.02)
    if mid < -5:
        #instruments[1].write_register(150, 22222, 0, 6, signed=True)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 150, output_value=22222)
        time.sleep(0.02)
    elif mid > 5:
        #instruments[1].write_register(150, -22222, 0, 6, signed=True)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 150, output_value=-22222)
        time.sleep(0.02)

    if copysign(rear, 1) > 5 and copysign(mid, 1) > 5:
        return RPV, MPV
    elif copysign(rear, 1) > 5 and copysign(mid, 1) < 5:
        return RPV, mPreTemp
    elif copysign(rear, 1) < 5 and copysign(mid, 1) > 5:
        return rPreTemp, MPV
    else:
        return rPreTemp, mPreTemp


def dModGrate(master, UpGratePreTemp, LoGratePreTemp, UpGratePV, LoGratePV):
    cdef int UpPV, LoPV, UpPreTemp, LoPreTemp
    UpPV = UpGratePV
    LoPV = LoGratePV
    UpPreTemp = UpGratePreTemp
    LoPreTemp = LoGratePreTemp
    cdef int UpGrate = UpPV - UpPreTemp
    cdef int LoGrate = LoPV - LoPreTemp

    if UpGrate < -5:
        #instruments[1].write_register(141, 22222, 0, 6, signed=True)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 141, output_value=22222)
        time.sleep(0.02)
    elif UpGrate > 5:
        #instruments[1].write_register(141, -22222, 0, 6, signed=True)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 141, output_value=-22222)
        time.sleep(0.02)
    if LoGrate < -5:
        #instruments[1].write_register(159, 22222, 0, 6, signed=True)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 159, output_value=22222)
        time.sleep(0.02)
    elif LoGrate > 5:
        #instruments[1].write_register(159, -22222, 0, 6, signed=True)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 159, output_value=-22222)
        time.sleep(0.02)

    if copysign(UpGrate, 1) > 5 and copysign(LoGrate, 1) > 5:
        return UpPV, LoPV
    elif copysign(UpGrate, 1) > 5 and copysign(LoGrate, 1) < 5:
        return UpPV, LoPreTemp
    elif copysign(UpGrate, 1) < 5 and copysign(LoGrate, 1) > 5:
        return UpPreTemp, LoPV
    else:
        return UpPreTemp, LoPreTemp