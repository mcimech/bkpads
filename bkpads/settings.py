""" Setup Constants """

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
