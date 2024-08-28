"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing the Packet class. The Packet data class defines the MAC packet structure. Objects of this
              class are transferred during transmission between the Access Point object and the User Station object.
"""

from dataclasses import dataclass


@dataclass
class Packet:
    """Dataclass defining the structure of a MAC packet."""

    packet_type: str
    packet_time: float
    source_node: list
    destination_nodes: list
