"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing the Channel class. The Channel data class is used to initialize the parameters
              specific to the radio channel.
"""

from dataclasses import dataclass

import configs.channel_config as channel_config


@dataclass()
class Channel:
    """Dataclass containing channel settings."""

    bandwidth: int = channel_config.CHANNEL_BW
    max_stations_in_transmission = channel_config.STATIONS_NUMBER_DICT
    possible_subchannels = channel_config.SUBCHANNELS
    channel_available: bool = True
    nodes_in_channel = []
    transmitting_ap = []
