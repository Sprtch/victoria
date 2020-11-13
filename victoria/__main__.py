from victoria.config import APPNAME, Config
from victoria.logger import logger
from daemonize import Daemonize
import logging
import argparse

def main(config):
    for p in config.printers:
        # TODO THREAD
        p.listen()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--no-daemon', dest='nodaemon', action='store_true', help='Does not start the program as a daemon')
    parser.add_argument('--logfile', dest='logfile', type=str, help='Log destination', default=("/var/log/%s.log" % APPNAME))
    parser.add_argument('--pid', dest='pid', type=str, help='Pid destination', default=("/var/run/%s.pid" % APPNAME))
    parser.add_argument('-c', '--config', dest='config', type=str, help='Config file location', default=("./config.yaml"))

    args = parser.parse_args()

    conf = Config(args.config)

    if args.nodaemon:
        logger.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        main(conf)
    else:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        fh = logging.FileHandler(args.logfile, "w")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        keep_fds = [fh.stream.fileno()]

        daemon = Daemonize(app=APPNAME, logger=logger, pid=args.pid, action=lambda: main(conf), keep_fds=keep_fds)
        daemon.start()
