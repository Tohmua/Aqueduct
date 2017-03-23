from argparse import ArgumentParser
from logger.logger import Logger
from config.config import Config
import shell.db as Db
import progressbar


def main():
    args = getCliArguments()
    logger = Logger(args.verbose).getLogger()

    try:
        logger.debug('Parsing source configuration file')
        src = Config(args.src)
        logger.debug('Testing src DB connection')
        Db.test(src)

        logger.debug('Parsing target configuration file')
        target = Config(args.target)
        logger.debug('Testing target DB connection')
        Db.test(target)

        logger.debug(getSQLCommandForLogging(src, target))
        run(logger, src, target)
    except ValueError as error:
        logger.critical(error)
        exit(1)


def getCliArguments():
    ap = ArgumentParser()

    ap.add_argument(
        '-v',
        '--verbose',
        default=False,
        action='store_true',
        help='Increase output verbosity'
    )
    ap.add_argument('src', help='Source DB Config File')
    ap.add_argument('target', help='Target DB Config File')

    return ap.parse_args()


def getSQLCommandForLogging(src: Config, target: Config):
    return '%s | %s' % (
        'Running: mysqldump %s -h %s -P %s --verbose%s' % (
            src.db['database'],
            src.db['host'],
            src.db['port'],
            ''.join(src.options),
        ),
        'mysql %s -h %s -P %s%s' % (
            target.db['database'],
            target.db['host'],
            target.db['port'],
            ''.join(target.options)
        )
    )


def run(logger: Logger, src: Config, target: Config):
    dumpOutput = Db.copyDb(src, target)

    # MySQL Dump Verbose Mode outputs 3 lines at the start
    # 3 lines at the end and 4 lines per table. So we use this
    # to calculate the number of rows we expect to be output
    maxValue = (Db.numberOfTables(src) * 4) + 6

    with progressbar.ProgressBar(max_value=maxValue) as bar:
        output = []

        while True:
            response = dumpOutput.stderr.readline().decode('utf8').strip()
            output.append(response)
            bar.update(output.length())
            if not output:
                if output.length() < maxValue:
                    raise ValueError('\n'.join(output))
                break
