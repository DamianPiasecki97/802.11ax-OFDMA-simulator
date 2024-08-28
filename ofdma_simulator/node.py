"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing the Node class. The Node class includes functions used to perform transmission both
              by Access Point objects and User Station objects - the AccessPoint and Station classes inherit from
              the Node class.
"""

import simpy
import logging
from abc import ABC, abstractmethod

from helpers import times
from packet import Packet

logger = logging.getLogger('ofdma_simulator')


class Node(ABC):
    """Class containing common functions and settings for the Station and Access Point."""

    def __init__(self, env, channel):
        """Node class constructor."""

        self.env = env
        self.channel = channel
        self.nodes_in_channel = channel.nodes_in_channel
        self.channel_store = None
        self.waiting_process = env.process(self.wait_for_new_packet())
        self.sensing_process = None
        self.backoff_process = None
        self.backoff_suspended = None
        self.name = None
        self.is_ap = False
        self.received_packets = []

    def generate_new_packet(self, packet_type, packet_time, source_node, destination_nodes):
        """Function for generating new packet."""

        # Generate new packet
        packet = Packet(packet_type, packet_time, source_node, destination_nodes)
        # Get the name of source node
        source_node_name = packet.source_node.name
        # Get the names of all target nodes
        destination_nodes_name = []
        for node in destination_nodes:
            destination_nodes_name.append(node.name)
        logger.info(f'[{self.env.now}] - New {packet.packet_type} packet from {source_node_name} to '
                    f'{destination_nodes_name}')
        return packet

    def send_packet(self, packet):
        """Function for sending the packet which is put as argument."""

        yield self.env.timeout(1)
        self.waiting_process.interrupt(packet)

    def transmit_in_channel(self, packet):
        """Function for forwarding the packet to all nodes participating in the transmission."""

        yield self.env.timeout(1)
        self.channel.channel_available = False
        for node in self.nodes_in_channel:
            node.channel_store.put(packet)

    def check_if_collision_occurred(self):
        """Function for checking if collision occurred."""

        number_of_transmitting_ap = len(self.channel.transmitting_ap)
        if number_of_transmitting_ap > 1:
            return True

    def start_listening(self):
        """Function for creating simpy.Store object so that it is possible to start listening."""

        self.nodes_in_channel.append(self)
        self.channel_store = simpy.Store(self.env, capacity=simpy.core.Infinity)

    def wait_for_new_packet(self):
        """Function for waiting for the new packet."""

        self.start_listening()
        while True:
            try:
                packet = yield self.channel_store.get()
                if self.is_ap:
                    if not self == packet.source_node:
                        if self.backoff_process and not self.backoff_suspended:
                            self.backoff_process.interrupt()
                yield self.env.process(self.handle_received_packet(packet))
            except simpy.Interrupt as packet:
                collision = self.check_if_collision_occurred()
                if collision:
                    self.sensing_process.interrupt(packet.cause)
                    self.channel_store = None
                    self.channel_store = simpy.Store(self.env, capacity=simpy.core.Infinity)
                    continue
                yield self.env.process(self.transmit_in_channel(packet.cause))

    @abstractmethod
    def handle_received_packet(self, packet):
        raise NotImplementedError("handle_received_packet must be override")
