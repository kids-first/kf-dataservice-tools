import logging
import sys
from pathlib import Path

import colorlog

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_logger(dunder_name, testing_mode, log_format) -> logging.Logger:
    if log_format == "simple":
        log_format = "%(message)s"
    else:
        log_format = (
            "%(asctime)s - "
            "%(name)s - "
            "%(funcName)s - "
            "%(levelname)s - "
            "%(message)s"
        )
    bold_seq = "\033[1m"
    colorlog_format = f"{bold_seq} " "%(log_color)s " f"{log_format}"
    colorlog.basicConfig(format=colorlog_format)
    logger = logging.getLogger(dunder_name)

    if testing_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    Path("/tmp/kf_dscopy/logs").mkdir(parents=True, exist_ok=True)
    # Output full log
    fh = logging.FileHandler("/tmp/kf_dscopy/logs/app.log")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Output warning log
    fh = logging.FileHandler("/tmp/kf_dscopy/logs/app.warning.log")
    fh.setLevel(logging.WARNING)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Output error log
    fh = logging.FileHandler("/tmp/kf_dscopy/logs/app.error.log")
    fh.setLevel(logging.ERROR)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
