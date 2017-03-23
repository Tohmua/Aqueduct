from config.config import Config
import subprocess


def test(db: Config):
    numberOfTables(db)
    return True


def numberOfTables(db: Config):
    info = subprocess.Popen(
        'mysql -h %s -P %s -e "SELECT count(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'%s\'"' % (
            db.db['host'],
            db.db['port'],
            db.db['database']
        ),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    success, error = info.communicate()

    if error:
        raise ValueError(error.decode('utf8').strip())

    tableCount = int(success.decode('utf8').strip().split('\n')[1])

    if tableCount == 0:
        raise ValueError('Connection issue to %s on %s:%s' % (
            db.db['database'],
            db.db['host'],
            db.db['port']
        ))

    return tableCount


def copyDb(src: Config, target: Config):
    mysqldump = subprocess.Popen(
        'mysqldump %s -h %s -P %s --verbose%s' % (
            src.db['database'],
            src.db['host'],
            src.db['port'],
            ''.join(src.options)
        ),
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    subprocess.Popen(
        'mysql %s -h %s -P %s%s' % (
            target.db['database'],
            target.db['host'],
            target.db['port'],
            ''.join(target.options)
        ),
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stdin=mysqldump.stdout
    )

    return mysqldump
