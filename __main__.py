import bkp891
import pyads

from ctypes import sizeof

from threading import Thread

""" Setup Constants """
# TODO put this in a conf-file or something...

# The name of the serial port of the LCR device
LCR_SERIAL = '/dev/ttyACM0'

# The AMS NetId of the PLC. Default is localhost '127.0.0.1.1.1'
PLC_ID = '127.0.0.1.1.1'

# The variable name of the flag for activation of a measurement in PLC GVL
PLC_MEASURE_FLAG = 'GVL.meas_start'

# The variable name of the measurement type in PLC GVL - set by PLC
PLC_MEASURE_TYPE = 'GVL.meas_type'

# The variable names for the measurement results in PLC GVL - set by Script
# (most measurements return 2 values)
PLC_RESULT01 = 'GVL.meas_01'
PLC_RESULT02 = 'GVL.meas_02'

# The variable name of the flag to show completion of measurement
PLC_RESUME_FLAG = 'GVL.meas_ready'

# The variable name of the flag signifying an error occurred
PLC_ERROR_FLAG = 'GVL.meas_error'

# The variable name which holds the error message in PLC
PLC_ERROR_MSG = 'GVL.meas_errormsg'


if __name__ == "__main__":
    # main initialisation here
    plc = pyads.Connection(PLC_ID, 851)
    lcr = bkp891.connect(LCR_SERIAL)


    def start_measure():
        lcr.clear_instrument()

        meastype = plc.read_by_name(PLC_MEASURE_TYPE, pyads.PLCTYPE_STRING)

        if meastype == '':
            return

        try:
            lcr.set_function(bkp891.Measurement[meastype])
        except KeyError:
            # TODO error handling
            return

        measvalue = lcr.fetch()

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


    @plc.notification(pyads.PLCTYPE_INT)
    def callback(handle, name, timestamp, value):
        if (value > 2000) or (value < 0):
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
        attr = pyads.NotificationAttrib(sizeof(pyads.PLCTYPE_INT))

        handles = plc.add_device_notification(PLC_MEASURE_FLAG, attr,
                                              callback)

        while True:
            # TODO make this proper and allow to exit gracefully
            pass


