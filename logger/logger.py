import logging


class Logger:
    def __init__(self, verbose=False):
        logLevel = logging.DEBUG if verbose else logging.WARNING
        logging.basicConfig(level=logLevel, format="%(msg)s")
        self.logger = logging.getLogger('Aqueduct')

    def getLogger(self):
        return self.logger
