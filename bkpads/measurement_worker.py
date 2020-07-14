import threading
from logging import getLogger

logger = getLogger(__name__)


class MeasurementWorker(threading.Thread):

    def __init__(self, queue, start_measure):
        threading.Thread.__init__(self)

        self.queue = queue
        self.start_measure = start_measure

        logger.debug('MeasurementWorker created')

    def run(self):
        logger.debug('Starting working loop...')
        while True:
            q = self.queue.get()
            
            if q:
                self.start_measure()
            else:
                logger.debug('Terminating.')
                break
