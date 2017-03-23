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
    except ValueError as error:
        logger.critical(error)
        exit(1)

    run(logger, src, target)
    exit(0)


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


def run(logger: Logger, src: Config, target: Config):
    logger.debug(
        '%s | %s' % (
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
    )

    dumpOutput = Db.copyDb(src, target)
    maxValue = (Db.numberOfTables(src) * 4) + 6

    with progressbar.ProgressBar(max_value=maxValue) as bar:
        i = 0
        errors = []
        while True:
            i = i + 1
            output = dumpOutput.stderr.readline().decode('utf8').strip()
            errors.append(output)
            bar.update(i)
            if not output:
                if i < maxValue:
                    print('\n'.join(errors))
                break
