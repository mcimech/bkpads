import logging

import click

from bkpads import settings
from bkpads.bridge import Bridge

logger = logging.getLogger('bkpads.main')


@click.command()
@click.option('--plc_id', default=settings.PLC_ID, show_default=True,
              help='ADS Id of PLC')
@click.option('-c', '--com', 'com_port',
              required=True,
              help='''Port to use for serial device communication.
                      COMx on Windows''')
def main(plc_id, com_port):
    """
    BKPADS handles communication between the BK Precision 891 LCR meter
    and a Beckhoff PLC with ADS.

    By default, the following PLC variables are used for communication:

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

    \b
    These values can be edited in settings.py. To locate the file, type
    pip show bkpads
    settings.py is located in the installation folder.

    """
    logging.basicConfig(level=logging.INFO)
    logger.info('Running...')

    context = {key: value for key, value in vars(settings).items()
               if key.isupper()}

    context['PLC_ID'] = plc_id
    context['LCR_SERIAL'] = com_port

    bridge = Bridge(context)

    bridge.start()


if __name__ == "__main__":
    main()
