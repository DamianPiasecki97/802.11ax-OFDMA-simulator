"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing the definition of constants used as simulation parameters.
"""


# Simulation parameters
LOGS_DIR = '/var/log/ofdma_simulator'
SIM_TIME = 100000
NUMBER_OF_AP = 1
NUMBER_OF_STATIONS = 60
SEED = 1
DIRECTION = 'DL'  # DL or UL
MCS = 11  # modulation and coding scheme
DATA_RATE = 72  # [Mb/s]
RU_LIST = [10, 10, 10, 10]  # subchannels BW list


# Simulation options
RTS_PROCEDURE_ENABLED = False
BSRP_PROCEDURE_ENABLED = False
MPDU_AGGREGATION_ENABLED = False
RU_PREDEFINED = True
DATA_RATE_PREDEFINED = False
