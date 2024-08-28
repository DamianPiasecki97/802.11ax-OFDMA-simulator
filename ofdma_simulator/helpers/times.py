"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing helper functions used to calculate the duration of each packet.
"""

import random
import math

import configs.channel_config as channel_config
import configs.simulation_config as simulation_config

mcs = simulation_config.MCS
predefined_data_rate = simulation_config.DATA_RATE
direction = simulation_config.DIRECTION
mcs_dict = channel_config.MCS_DICT
subcarriers_dict = channel_config.SUBCARRIERS_DICT
l_d = channel_config.MPDU_SIZE
l_sf = channel_config.SERVICE_FIELD
l_md = channel_config.MPDU_DELIMITER
l_mh = channel_config.MAC_HEADER
l_tb = channel_config.TAIL_BITS
l_rts = channel_config.RTS_LENGTH
l_cts = channel_config.CTS_LENGTH
l_bsrp = channel_config.BSRP_LENGTH
l_bsr = channel_config.BSR_LENGTH
l_back = channel_config.BLOCK_ACK_LENGTH
tphy_legacy = channel_config.LEGACY_PREAMBLE
tphy_he_mu = channel_config.HE_MU_PREAMBLE
tphy_he_tb = channel_config.HE_TB_PREAMBLE
ofdm_legacy = channel_config.OFDM_LEGACY
ofdm = channel_config.OFDM
r_legacy = channel_config.LEGACY_DATA_RATE
spatial_streams_number = channel_config.SPATIAL_STREAMS_NUMBER
cw_min = channel_config.CW_MIN
cw_max = channel_config.CW_MAX
sifs_time = channel_config.SIFS_TIME
slot_time = channel_config.SLOT_TIME
difs_time = channel_config.DIFS_TIME
aifs_time = channel_config.AIFS_TIME
txop_time = channel_config.TXOP_TIME


def get_packet_time(packet_type, bandwidth=None, number_of_destinations=None):
    if packet_type == 'BSRP_TRIGGER':
        time = get_bsrp_time()
    elif packet_type == 'BSR':
        time = get_bsr_time()
    elif packet_type == 'MU_RTS':
        time = get_mu_rts_time(number_of_destinations)
    elif packet_type == 'CTS':
        time = get_cts_time()
    elif packet_type == 'DL_A_MPDU':
        time = get_dl_data_frame_time(bandwidth, number_of_destinations)
    elif packet_type == 'UL_A_MPDU':
        time = get_ul_data_frame_time(bandwidth, number_of_destinations)
    elif packet_type == 'BASIC_TRIGGER':
        time = get_trigger_time(number_of_destinations)
    elif packet_type == 'TB_BACK':
        time = get_tb_back_time(bandwidth)
    elif packet_type == 'MS_BACK':
        time = get_ms_back_time(number_of_destinations)
    else:
        time = None
    return time


def get_rts_time():
    rts_time = tphy_legacy + ((l_sf + l_rts + l_tb) / r_legacy) * ofdm_legacy
    return rts_time


def get_mu_rts_time(number_of_destinations):
    l_mu_rts = _get_mu_rts_length(number_of_destinations)
    mu_rts_time = tphy_legacy + ((l_sf + l_mu_rts + l_tb) / r_legacy) * ofdm_legacy
    return mu_rts_time


def get_cts_time():
    cts_time = tphy_legacy + ((l_sf + l_cts + l_tb) / r_legacy) * ofdm_legacy
    return cts_time


def get_bsrp_time():
    cts_time = tphy_legacy + ((l_sf + l_bsrp + l_tb) / r_legacy) * ofdm_legacy
    return cts_time


def get_bsr_time():
    cts_time = tphy_legacy + ((l_sf + l_bsr + l_tb) / r_legacy) * ofdm_legacy
    return cts_time


def get_trigger_time(number_of_destinations):
    l_basic_trigger = _get_basic_trigger_length(number_of_destinations)
    trigger_time = tphy_legacy + ((l_sf + l_basic_trigger + l_tb) / r_legacy) * ofdm_legacy
    return trigger_time


def get_back_time():
    back_time = tphy_legacy + ((l_sf + l_back + l_tb) / r_legacy) * ofdm_legacy
    return back_time


def get_tb_back_time(bandwidth):
    if simulation_config.DATA_RATE_PREDEFINED:
        r = (predefined_data_rate * ofdm)
    else:
        r = _get_data_rate(bandwidth)
    tb_back_time = tphy_he_tb + ((l_sf + l_back + l_tb) / r) * ofdm
    return tb_back_time


def get_ms_back_time(number_of_destinations):
    l_ms_back = _get_ms_back_length(number_of_destinations)
    ms_back_time = tphy_legacy + ((l_sf + l_ms_back + l_tb) / r_legacy) * ofdm_legacy
    return ms_back_time


def get_dl_data_frame_time(bandwidth, number_of_destinations):
    if simulation_config.DATA_RATE_PREDEFINED:
        r = (predefined_data_rate * ofdm)
    else:
        r = _get_data_rate(bandwidth)
    number_of_mpdu = _get_number_of_sent_mpdu(r, bandwidth, number_of_destinations)
    if simulation_config.MPDU_AGGREGATION_ENABLED:
        dl_data_frame_time = tphy_he_mu + ((l_sf + number_of_mpdu * (
                l_md + l_mh + l_d) + l_tb) / r) * ofdm
    else:
        dl_data_frame_time = tphy_he_mu + ((l_sf + l_md + l_mh + l_d + l_tb) / r) * ofdm
    return dl_data_frame_time


def get_ul_data_frame_time(bandwidth, number_of_destinations):
    if simulation_config.DATA_RATE_PREDEFINED:
        r = (predefined_data_rate * ofdm)
    else:
        r = _get_data_rate(bandwidth)
    number_of_mpdu = _get_number_of_sent_mpdu(r, bandwidth, number_of_destinations)
    if simulation_config.MPDU_AGGREGATION_ENABLED:
        ul_data_frame_time = tphy_he_tb + ((l_sf + number_of_mpdu * (
                l_md + l_mh + l_d) + l_tb) / r) * ofdm
    else:
        ul_data_frame_time = tphy_he_tb + ((l_sf + l_md + l_mh + l_d + l_tb) / r) * ofdm
    return ul_data_frame_time


def get_random_backoff_time(retransmission_counter):
    retransmission_counter += 4
    cw = min((pow(2, retransmission_counter) - 1), cw_max)
    random_backoff_time = random.randint(0, cw)
    return random_backoff_time * slot_time


def get_sent_data(bandwidth, number_of_destinations):
    if simulation_config.MPDU_AGGREGATION_ENABLED:
        data_rate = _get_data_rate(bandwidth)
        number_of_mpdu = _get_number_of_sent_mpdu(data_rate, bandwidth, number_of_destinations)
        sent_data = (number_of_mpdu * l_d)
    else:
        sent_data = l_d
    return sent_data


def _get_data_rate(bandwidth):
    vs = spatial_streams_number
    ysc = _get_number_of_subcarriers(bandwidth)
    yc = _get_coding_rate()
    modulation = mcs_dict[mcs][0]
    ym = _get_modulation_rate(modulation)
    data_rate = (vs * ym * yc * ysc)
    return data_rate


def _get_modulation_rate(modulation):
    if modulation == 'BPSK':
        modulation_rate = 1
    elif modulation == 'QPSK':
        modulation_rate = 2
    elif modulation == '16-QAM':
        modulation_rate = 4
    elif modulation == '64-QAM':
        modulation_rate = 6
    elif modulation == '256-QAM':
        modulation_rate = 8
    elif modulation == '1024-QAM':
        modulation_rate = 10
    else:
        modulation_rate = None
    return modulation_rate


def _get_coding_rate():
    coding_rate = mcs_dict[mcs][1]
    return coding_rate


def _get_number_of_subcarriers(bandwidth):
    number_of_subcarriers = subcarriers_dict[bandwidth]
    return number_of_subcarriers


def _get_basic_trigger_length(number_of_destinations):
    l_basic_trigger = 224 + (48 * number_of_destinations)
    return l_basic_trigger


def _get_mu_rts_length(number_of_destinations):
    mu_rts_length = 224 + (40 * number_of_destinations)
    return mu_rts_length


def _get_ms_back_length(number_of_destinations):
    ms_back_length = 176 + (64 * number_of_destinations)
    return ms_back_length


def _get_number_of_sent_mpdu(data_rate, bandwidth, number_of_destinations=None):
    txop_remained_time = txop_time
    if simulation_config.RTS_PROCEDURE_ENABLED:
        mu_rts_time = get_mu_rts_time(number_of_destinations)
        cts_time = get_cts_time()
        txop_remained_time -= (mu_rts_time + cts_time + (2 * sifs_time))
    if direction == 'DL':
        tb_back_time = get_tb_back_time(bandwidth)
        txop_remained_time -= (tb_back_time + sifs_time + aifs_time + tphy_he_mu)
        mpdu_time = ((l_sf + l_md + l_mh + l_d + l_tb) / data_rate) * ofdm
        number_of_mpdu = math.floor(txop_remained_time / mpdu_time)
    if direction == 'UL':
        trigger_time = get_trigger_time(number_of_destinations)
        ms_back_time = get_ms_back_time(number_of_destinations)
        txop_remained_time -= (trigger_time + ms_back_time + (2 * sifs_time) + aifs_time + tphy_he_tb)
        mpdu_time = ((l_sf + l_md + l_mh + l_d + l_tb) / data_rate) * ofdm
        number_of_mpdu = math.floor(txop_remained_time / mpdu_time)
    return number_of_mpdu

