import logging

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
datefmt = "%Y-%m-%d-%H:%M:%S"

log = logging.getLogger(__name__)

logging.basicConfig(filename="output.log", level=logging.INFO,
                    format=FORMAT, datefmt=datefmt)


def log_test():
    log.info('Info')
    log.warning('Warning')
    log.critical('Critical')


if __name__ == '__main__':
    log_test()
