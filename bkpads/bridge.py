""" Provide a Bridge between the BK Precision 891 Library and a Beckhoff
    PLC """
from threading import Thread

import pyads
import bkp891
from ctypes import sizeof


class LCRBridge(object):
    """ An object to hold the connections and manage measurements """

    def __init__(self, plc_amsid, lcr_serialport):
        self.plc = pyads.Connection(plc_amsid, 851)
        self.lcr = bkp891.connect(lcr_serialport)

        self.plc.open()
        self.lcr.clear_instrument()

    def reset_plc(self):
        self.plc.write_by_name('GVL.btest', True, pyads.PLCTYPE_BOOL)
        print('=== value reset ===')

    @plc.notification(pyads.PLCTYPE_INT)
    def callback(self, handle, name, timestamp, value):
        if (value > 2000) or (value < 0):
            t = Thread(target=self.reset_plc)
            t.start()

        print('handle: {0} | name: {1} | timestamp: {2} | value: {3}'.format(
            handle, name, timestamp, value))


with plc:
    attr = pyads.NotificationAttrib(sizeof(pyads.PLCTYPE_INT))

    handles = plc.add_device_notification('GVL.ntest', attr, callback)

    while True:
        pass
