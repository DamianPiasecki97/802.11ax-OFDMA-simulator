"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing the definition of constants used to calculate the length and duration of each packet.
"""

# Channel parameters
CHANNEL_BW = 40
SUBCHANNELS = [2.22, 5, 10, 20, 40, 80, 160]
SPATIAL_STREAMS_NUMBER = 1

# EDCA related parameters
CW_MIN = 15
CW_MAX = 63
AIFSN = 3

# Maximum number of stations in transmission for given subchannel bandwidth
STATIONS_NUMBER_DICT = {
    20: 9,
    40: 18,
    80: 37,
    160: 74
}

# Transmission related times
SLOT_TIME = 9  # [us]
SIFS_TIME = 16  # [us]
AIFS_TIME = (AIFSN * SLOT_TIME) + SIFS_TIME  # [us]
DIFS_TIME = (2 * SLOT_TIME) + SIFS_TIME  # [us]
TXOP_TIME = 2.528 * 1000  # [us]

# A-MPDU packets
MPDU_SIZE = 12000  # [b]

# Frame lengths
SERVICE_FIELD = 16  # [b]
MPDU_DELIMITER = 32  # [b]
MAC_HEADER = 320  # [b]
TAIL_BITS = 18  # [b]
RTS_LENGTH = 160  # [b]
CTS_LENGTH = 112  # [b]
BLOCK_ACK_LENGTH = 256  # [b]
BSRP_LENGTH = 160  # [b]
BSR_LENGTH = 112  # [b]


# Preamble durations
LEGACY_PREAMBLE = 20  # [us]
HE_MU_PREAMBLE = 48  # [us]
HE_TB_PREAMBLE = 48  # [us]

# OFDM symbol durations
OFDM_LEGACY = 3.6  # [us]
OFDM = 13.6  # [us]

# Legacy transmission rate
LEGACY_DATA_RATE = 24

# Data subcarriers for given subchannel bandwidth
SUBCARRIERS_DICT = {
    2.22: 24,
    5: 48,
    10: 102,
    20: 234,
    40: 468,
    80: 980,
    160: 1960
}

# Modulation type and coding scheme for given MCS
MCS_DICT = {
    0: ['BPSK', 1/2],
    1: ['QPSK', 1/2],
    2: ['QPSK', 3/4],
    3: ['16-QAM', 1/2],
    4: ['16-QAM', 3/4],
    5: ['64-QAM', 2/3],
    6: ['64-QAM', 3/4],
    7: ['64-QAM', 5/6],
    8: ['256-QAM', 3/4],
    9: ['256-QAM', 5/6],
    10: ['1024-QAM', 3/4],
    11: ['1024-QAM', 5/6]
}
