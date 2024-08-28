"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing the Station class. The Station class includes functions specific to the User Station.
"""

import logging

from helpers import times
from node import Node

logger = logging.getLogger('ofdma_simulator')


class Station(Node):
    """Class containing functions and settings specific to a Station."""

    def __init__(self, name, env, config, channel, stats):
        """Station class constructor."""

        super().__init__(env, channel)
        self.name = name
        self.env = env
        self.config = config
        self.channel = channel
        self.stats = stats
        self.is_ap = False
        self.allocated_bw = None
        self.station_associated = False
        self.stats.latency_per_station[self.name] = 0
        self.stats.data_transferred_per_station[self.name] = 0
        self.stats.number_of_transmissions_per_station[self.name] = 0
        self.type_of_packet_to_wait = None
        self.set_initial_type_of_packet_to_wait()

    def set_initial_type_of_packet_to_wait(self):
        """Function for setting packet type expected by Station after transmission is started."""

        if self.config.direction == 'DL':
            if self.config.rts_procedure:
                self.type_of_packet_to_wait = 'MU_RTS'
            else:
                self.type_of_packet_to_wait = 'DL_A_MPDU'
        elif self.config.direction == 'UL':
            if self.config.bsrp_procedure:
                self.type_of_packet_to_wait = 'BSRP_TRIGGER'
            else:
                if self.config.rts_procedure:
                    self.type_of_packet_to_wait = 'MU_RTS'
                else:
                    self.type_of_packet_to_wait = 'BASIC_TRIGGER'

    def handle_received_packet(self, packet):
        """Function for handling the received packet by Station."""

        # Ignore packet to other destination
        if self in packet.destination_nodes:
            # Ignore incorrect packet type
            if packet.packet_type == self.type_of_packet_to_wait:
                # Handle BSRP Trigger packet in Station
                if packet.packet_type == 'BSRP_TRIGGER':
                    if self.config.rts_procedure:
                        self.type_of_packet_to_wait = 'MU_RTS'
                    else:
                        if self.config.direction == 'DL':
                            self.type_of_packet_to_wait = 'DL_A_MPDU'
                        elif self.config.direction == 'UL':
                            self.type_of_packet_to_wait = 'BASIC_TRIGGER'
                    destination = packet.source_node
                    yield self.env.process(self.send_bsr(destination))
                # Handle MU RTS packet in Station
                if packet.packet_type == 'MU_RTS':
                    if self.config.direction == 'DL':
                        self.type_of_packet_to_wait = 'DL_A_MPDU'
                    elif self.config.direction == 'UL':
                        self.type_of_packet_to_wait = 'BASIC_TRIGGER'
                    destination = packet.source_node
                    yield self.env.process(self.send_cts(destination))
                # Handle data packet in Station
                elif packet.packet_type == 'DL_A_MPDU':
                    self.set_initial_type_of_packet_to_wait()
                    destination = packet.source_node
                    number_of_destinations = len(packet.destination_nodes)
                    received_data = times.get_sent_data(self.allocated_bw, number_of_destinations)
                    self.stats.data_transferred_per_station[self.name] += received_data
                    yield self.env.process(self.send_tb_back(destination))
                # Handle Basic Trigger in Station
                elif packet.packet_type == 'BASIC_TRIGGER':
                    self.type_of_packet_to_wait = 'MS_BACK'
                    destination = packet.source_node
                    number_of_destinations = len(packet.destination_nodes)
                    yield self.env.process(self.send_data_packet(destination, number_of_destinations))
                # Handle MS back in Station
                elif packet.packet_type == 'MS_BACK':
                    self.set_initial_type_of_packet_to_wait()
                    self.channel.channel_available = True

    def send_bsr(self, destination):
        """Function for sending BSR packet."""

        packet_type = 'BSR'
        source_node = self
        destination_node = [destination]
        packet_time = times.get_packet_time(packet_type)
        bsr_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_node)
        yield self.env.process(self.send_packet(bsr_packet))

    def send_cts(self, destination):
        """Function for sending MU CTS packet."""

        packet_type = 'CTS'
        source_node = self
        destination_node = [destination]
        packet_time = times.get_packet_time(packet_type)
        cts_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_node)
        yield self.env.process(self.send_packet(cts_packet))

    def send_data_packet(self, destination, number_of_destinations):
        """Function for sending A-MPDU packet."""

        packet_type = 'UL_A_MPDU'
        source_node = self
        destination_node = [destination]
        packet_time = times.get_packet_time(packet_type, self.allocated_bw, number_of_destinations)
        data_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_node)
        sent_data = times.get_sent_data(self.allocated_bw, number_of_destinations)
        self.stats.data_transferred_per_station[self.name] += sent_data
        yield self.env.process(self.send_packet(data_packet))

    def send_tb_back(self, destination):
        """Function for sending TB-Back packet."""

        packet_type = 'TB_BACK'
        source_node = self
        destination_node = [destination]
        packet_time = times.get_packet_time(packet_type, self.allocated_bw)
        tb_back_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_node)
        yield self.env.process(self.send_packet(tb_back_packet))
