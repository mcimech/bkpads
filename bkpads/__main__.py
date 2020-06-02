from pyads import ADSError

import bkp891
import pyads

from ctypes import sizeof

from threading import Thread

from time import sleep

""" Setup Constants """
# TODO put this in a conf-file or something...

# The name of the serial port of the LCR device
LCR_SERIAL = 'COM4'

# Time to wait between setting the measurement mode and fetching the result
LCR_TIME_TO_WAIT = 1.0  # in seconds

# The AMS NetId of the PLC. Default is localhost '127.0.0.1.1.1'
PLC_ID = '127.0.0.1.1.1'

# The variable name of the flag for activation of a measurement in PLC GVL
PLC_MEASURE_FLAG = 'GVL.bMeas_start'

# The variable name of the measurement type in PLC GVL - set by PLC
PLC_MEASURE_TYPE = 'GVL.sMeas_type'

# The variable names for the measurement results in PLC GVL - set by Script
# (most measurements return 2 values)
PLC_RESULT01 = 'GVL.rMeas_01'
PLC_RESULT02 = 'GVL.rMeas_02'

# The variable name of the flag to show completion of measurement
PLC_RESUME_FLAG = 'GVL.bMeas_ready'

# The variable name of the flag signifying an error occurred
PLC_ERROR_FLAG = 'GVL.bMeas_error'

# The variable name which holds the error message in PLC
PLC_ERROR_MSG = 'GVL.sMeas_errormsg'

# The variable name of the flag to stop this script
PLC_KILL_FLAG = 'GVL.bKill_proc'


if __name__ == "__main__":
    # main initialisation here
    plc = pyads.Connection(PLC_ID, 851)
    lcr = bkp891.connect(LCR_SERIAL)


    def error_notification(errormesg):
        plc.write_by_name(PLC_MEASURE_FLAG, False, pyads.PLCTYPE_BOOL)
        plc.write_by_name(PLC_ERROR_FLAG, True, pyads.PLCTYPE_BOOL)
        plc.write_by_name(PLC_ERROR_MSG, errormesg, pyads.PLCTYPE_STRING)

        lcr.clear_instrument()


    def start_measure():
        lcr.clear_instrument()

        meastype = plc.read_by_name(PLC_MEASURE_TYPE, pyads.PLCTYPE_STRING)

        if meastype == '':
            return

        try:
            lcr.set_function(bkp891.Measurement[meastype])
        except KeyError:
            error_notification('Invalid Measurement Type')
            return

        print('Set measurement type: {0}'.format(meastype))

        sleep(LCR_TIME_TO_WAIT)

        measvalue = lcr.fetch()

        print('Fetched measurement: {0}'.format(measvalue))

        if isinstance(measvalue, tuple):
            plc.write_by_name(PLC_RESULT01, float(measvalue[0]),
                              pyads.PLCTYPE_REAL)
            plc.write_by_name(PLC_RESULT02, float(measvalue[1]),
                              pyads.PLCTYPE_REAL)
        else:
            plc.write_by_name(PLC_RESULT01, float(measvalue),
                              pyads.PLCTYPE_REAL)
            plc.write_by_name(PLC_RESULT02, 0.0, pyads.PLCTYPE_REAL)

        plc.write_by_name(PLC_MEASURE_FLAG, False, pyads.PLCTYPE_BOOL)
        plc.write_by_name(PLC_RESUME_FLAG, True, pyads.PLCTYPE_BOOL)


    @plc.notification(pyads.PLCTYPE_BOOL)
    def callback(handle, name, timestamp, value):
        if value:
            t = Thread(target=start_measure)
            t.start()

        print(
            'handle: {0} | name: {1} | timestamp: {2} | value: {3}'.format(
                handle, name, timestamp, value))


    plc.open()

    # Set up measuring instrument
    lcr.clear_instrument()
    lcr.set_format(True)        # Set format to 'binary'

    with plc:
        attr = pyads.NotificationAttrib(sizeof(pyads.PLCTYPE_BOOL))

        handles_meas = plc.add_device_notification(PLC_MEASURE_FLAG, attr,
                                                   callback)

        # handles_kill = plc.add_device_notification(PLC_KILL_FLAG, attr,
        #                                           killme)

        print('Callback set...')

        while True:
            sleep(10)

            try:
                plc.read_state()
            except ADSError:
                break
