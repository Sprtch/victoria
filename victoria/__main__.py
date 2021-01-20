from victoria.config import Config
from victoria.logger import logger
from victoria.db import db
from despinassy import Printer as PrinterTable
from daemonize import Daemonize
import threading
import logging
import argparse
import signal


def main(config):
    thrlist = []

    def signal_handler(signal, frame):
        PrinterTable.query.update(dict(hidden=True, available=False))
        db.session.commit()
        exit()

    signal.signal(signal.SIGINT, signal_handler)

    for p in config.printers:
        t = threading.Thread(target=p.listen)
        t.start()
        thrlist.append(t)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--no-daemon',
                        dest='nodaemon',
                        action='store_true',
                        help='Does not start the program as a daemon')
    parser.add_argument('--logfile',
                        dest='logfile',
                        type=str,
                        help='Log destination',
                        default=None)
    parser.add_argument('--pid',
                        dest='pidfile',
                        type=str,
                        help='Pid destination',
                        default=None)
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        help='Set the log level to show debug messages')
    parser.add_argument('-c',
                        '--config',
                        dest='config',
                        type=str,
                        help='Config file location',
                        default=("./config.yaml"))

    args = parser.parse_args()
    configfile = vars(args).pop('config')
    arguments = vars(args)

    conf = Config.from_yaml_file(configfile, **arguments)

    if args.nodaemon:
        main(conf)
    else:
        logger = logging.getLogger(Config.APPNAME)
        daemon = Daemonize(app=Config.APPNAME,
                           logger=logger,
                           pid=conf.pidfile,
                           action=lambda: main(conf),
                           keep_fds=[
                               i.stream.fileno() for i in logger.handlers
                               if hasattr(i, 'baseFilename')
                           ])
        daemon.start()
