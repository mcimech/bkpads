bkpADS
======

bkpADS provides an Interface between Beckhoff PLCs and a BK Precision 891 LCR meter
which communicates via the bkp891 library.

Configuration
=============

bkpADS takes up to two commandline options:

    --plc_id TEXT   ADS Id of PLC  [default: 127.0.0.1.1.1]
    
    -c, --com TEXT  Port to use for serial device communication. COMx on Windows
          [required] 

The variables to communicate with the PLC are

    GVL.bMeas_start |
    The variable name of the flag for activation of a measurement in PLC
    GVL

    GVL.sMeas_type |
    The variable name of the measurement type in PLC GVL - set by PLC


    GVL.rMeas_01, GVL.rMeas_02 |
    The variable names for the measurement results in PLC GVL - set by the
    Script (most measurements return 2 values)

    GVL.bMeas_ready |
    The variable name of the flag to show completion of measurement

    GVL.bMeas_error |
    The variable name of the flag signifying an error occurred

    GVL.sMeas_errormsg |
    The variable name which holds the error message in PLC
    
The names are configured in `settings.py`, which you can find in the installation directory.

Type `pip show bkpads` in a terminal to locate the directory.

Usage
=====

**Important:** bkpADS expects the PLC to be in Run Mode **before** it is started.
If you want to test different command line parameters, make sure that the PLC is running
before you start bkpADS.

To start bkpADS from the PLC, use [NT_StartProcess](https://infosys.beckhoff.com/english.php?content=../content/1033/tcplclibutilities/html/tcplclibutilities_nt_startprocess.htm&id),
which needs the `TC2_Utilities` Library enabled on the PLC. See the following example
PLC code:

        PROGRAM MAIN
        VAR
            bStartscript : BOOL := TRUE;
            bBusy : BOOL := FALSE;
            Start_py_script : NT_StartProcess;
        END_VAR

        IF bStartscript = TRUE AND bBusy = FALSE THEN
            Start_py_script(
                NETID := '',
                PATHSTR := 'bkpads',
                DIRNAME := 'C:\Users\Administrator\Desktop',
                COMNDLINE := '-c COM4',
                    START := TRUE,
                BUSY => bBusy
            );
            bStartscript := FALSE;
        END_IF
        
Edit the `COMNDLINE` parameter to match the serial port of your device.