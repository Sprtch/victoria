from victoria.config import Config
from victoria.logger import logger
from daemonize import Daemonize
import threading
import logging
import argparse


def main(config):
    thrlist = []
    for p in config.printers:
        t = threading.Thread(target=p.listen)
        t.start()
        thrlist.append(t)

    for t in thrlist:
        t.join()


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
                        default=("/var/log/%s.log" % Config.APPNAME))
    parser.add_argument('--pid',
                        dest='pid',
                        type=str,
                        help='Pid destination',
                        default=("/var/run/%s.pid" % Config.APPNAME))
    parser.add_argument('--debug',
                        dest='debuglevel',
                        action='store_true',
                        help='Set the log level to show debug messages')
    parser.add_argument('-c',
                        '--config',
                        dest='config',
                        type=str,
                        help='Config file location',
                        default=("./config.yaml"))

    args = parser.parse_args()
    conf = Config().from_yaml_file(args.config)
    loglevel = logger.DEBUG if args.debuglevel else logger.INFO
    if args.nodaemon:
        logger.basicConfig(format='[%(asctime)s] %(message)s',
                           datefmt='%m/%d/%Y %I:%M:%S %p',
                           level=loglevel)
        main(conf)
    else:
        logger = logging.getLogger(__name__)
        logger.setLevel(loglevel)
        logger.propagate = False

        fh = logging.FileHandler(args.logfile, "w")
        fh.setLevel(loglevel)
        formatter = logging.Formatter(fmt='[%(asctime)s] %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        keep_fds = [fh.stream.fileno()]

        daemon = Daemonize(app=Config.APPNAME,
                           logger=logger,
                           pid=args.pid,
                           action=lambda: main(conf),
                           keep_fds=keep_fds)
        daemon.start()
