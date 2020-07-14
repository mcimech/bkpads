from ctypes import sizeof
from logging import getLogger
from queue import Queue
from time import sleep

import bkp891
import pyads

from bkpads.measurement_worker import MeasurementWorker

logger = getLogger(__name__)


class Bridge:

    def __init__(self, config):
        self.config = config

        self.plc = pyads.Connection(config['PLC_ID'], 851)
        self.lcr = bkp891.connect(config['LCR_SERIAL'])

        self.queue = Queue()
        self.worker = MeasurementWorker(self.queue, self.start_measure)

        self.callback = self.plc.notification(pyads.
                                              PLCTYPE_BOOL)(self._callback)

        logger.debug("Bridge created")

    def start(self):
        logger.info('Starting Bridge...')
        self.plc.open()

        logger.debug('Connecting to LCR device...')
        # Set up measuring instrument
        self.lcr.clear_instrument()
        self.lcr.set_format(True)  # Set format to 'binary'

        self.worker.start()

        with self.plc:
            logger.debug('Entering plc context...')
            attr = pyads.NotificationAttrib(sizeof(pyads.PLCTYPE_BOOL))

            self.plc.add_device_notification(
                self.config['PLC_MEASURE_FLAG'],
                attr,
                self.callback)

            logger.info('Callback registered with pyADS...')

            while True:
                sleep(10)

                try:
                    self.plc.read_state()
                except pyads.ADSError:
                    self.queue.put(False)
                    self.worker.join()
                    break

        self.worker.join()

        logger.info('Bridge terminated')

    def _callback(self, handle, name, timestamp, value):
        if value:
            logger.debug('Pushed True on worker queue')
            self.queue.put(True)

        logger.debug(
            'handle: {0} | name: {1} | timestamp: {2} | value: {3}'.format(
                handle, name, timestamp, value))

    def write_results(self, val1, val2=0.0):
        logger.debug('Writing results: {0}, {1}'.format(val1, val2))

        self.plc.write_by_name(self.config['PLC_RESULT01'],
                               float(val1),
                               pyads.PLCTYPE_REAL)
        self.plc.write_by_name(self.config['PLC_RESULT02'],
                               float(val2),
                               pyads.PLCTYPE_REAL)

    def start_measure(self):
        self.clear_error()

        meastype = self.plc.read_by_name(self.config['PLC_MEASURE_TYPE'],
                                         pyads.PLCTYPE_STRING)

        logger.info('Starting measurement of type {0}'.format(meastype))

        if meastype == '':
            return

        try:
            self.lcr.set_function(bkp891.Measurement[meastype])
        except KeyError:
            self.error_notification('Invalid Measurement Type')
            return

        sleep(self.config['LCR_TIME_TO_WAIT'])

        measvalue = self.lcr.fetch()

        logger.debug('Fetched measurement: {0}'.format(measvalue))

        if isinstance(measvalue, tuple):
            self.write_results(measvalue[0], measvalue[1])
        else:
            self.write_results(measvalue)

        self.plc.write_by_name(self.config['PLC_MEASURE_FLAG'],
                               False,
                               pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(self.config['PLC_RESUME_FLAG'],
                               True,
                               pyads.PLCTYPE_BOOL)

    def error_notification(self, errormesg):
        logger.error('Caught error from LCR: {0}'.format(errormesg))
        self.plc.write_by_name(self.config['PLC_MEASURE_FLAG'], False,
                               pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(self.config['PLC_ERROR_FLAG'], True,
                               pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(self.config['PLC_ERROR_MSG'], errormesg,
                               pyads.PLCTYPE_STRING)

        self.lcr.clear_instrument()

    def clear_error(self):
        logger.debug('Clearing error states...')
        self.plc.write_by_name(self.config['PLC_ERROR_FLAG'], False,
                               pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(self.config['PLC_ERROR_MSG'], '',
                               pyads.PLCTYPE_STRING)

        self.lcr.clear_instrument()
