"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing an helper function used to configure and initialize the logger used by other
              program functions.
"""

import logging
import logging.handlers

import configs.simulation_config as simulation_config


def prepare_logger():
    """Function for preparing logger."""

    logger = logging.getLogger('ofdma_simulator')
    logger.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(simulation_config.LOGS_DIR + '/ofdma_simulation.log',
                                              maxBytes=16777216, backupCount=4)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
