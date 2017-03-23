import configparser
from functools import reduce
from typing import (Dict, List)


class Config:
    db = {}
    options = []

    def __init__(self, filePath: str):
        config = configparser.ConfigParser()
        config.read(filePath)

        self.db = self._getDbSettings(config, filePath)
        self.options = self._getDbOptions(config, filePath)

    def _getDbSettings(self, config: configparser, filePath: str) -> Dict:
        try:
            return reduce(
                lambda x, y: x.update(y) or x,
                map(lambda x: {x: config.get('DB', x)}, config.options('DB'))
            )
        except ValueError as error:
            raise ValueError('Unable to parse DB settings in %s' % filePath)

    def _getDbOptions(self, config: configparser, filePath: str) -> List:
        try:
            return list(map(
                lambda x: " --%s" % config.get('Options', x),
                config.options('Options')
            ))
        except ValueError as error:
            raise ValueError('Unable to parse Options in %s' % filePath)
