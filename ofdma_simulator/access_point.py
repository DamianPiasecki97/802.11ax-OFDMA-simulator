"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing the AccessPoint class. The AccessPoint class includes Access Point specific functions
              for scheduling and performing transmissions.
"""

import random
import logging
import simpy
import math

from helpers import times
from node import Node

logger = logging.getLogger('ofdma_simulator')


class AccessPoint(Node):
    """Class containing functions and settings specific to an Access Point."""

    def __init__(self, name, env, config, channel, stats):
        """AccessPoint class constructor."""

        super().__init__(env, channel)
        self.name = name
        self.env = env
        self.config = config
        self.channel = channel
        self.stats = stats
        self.is_ap = True
        self.assigned_stations = []
        self.destination_stations = []
        self.expected_destinations_number = None
        self.received_packets_number = 0
        self.sensing_process = None
        self.backoff_process = None
        self.backoff_suspended = None
        self.retransmission_counter = 0
        self.stats.number_of_transmissions_per_ap[self.name] = 0
        self.stats.number_of_retransmissions_per_ap[self.name] = 0
        self.transmission_complete = False
        self.type_of_packet_to_wait = None
        self.set_initial_type_of_packet_to_wait()

    def perform_transmission(self, all_destinations):
        """Function for scheduling and performing subsequent transmissions."""

        # Assign the Stations to the Access Point for the duration of the simulation
        self.assign_stations_to_ap(all_destinations)
        # Schedule transmission in Access Point
        while True:
            logger.info(f'[{self.env.now}] - [{self.name}] Transmission scheduling is started.')
            self.transmission_complete = False
            self.destination_stations = []
            # Choose Stations to new transmission
            self.select_stations_for_current_transmission()
            # Allocate channel resources to each Station
            self.allocate_resources()
            # Start new transmission
            logger.info(f'[{self.env.now}] - [{self.name}] New transmission is started.')
            self.sensing_process = self.env.process(self.compete_for_channel_and_start_transmission())
            yield self.sensing_process
            while not self.transmission_complete:
                yield self.env.timeout(1)
            self.stats.number_of_transmissions_per_ap[self.name] += 1
            for station in self.destination_stations:
                self.stats.number_of_transmissions_per_station[station.name] += 1
            logger.info(f'[{self.env.now}] - [{self.name}] Transmission complete.')

    def compete_for_channel_and_start_transmission(self):
        """Function to compete for channel and start transmission."""

        logger.info(f'[{self.env.now}] - [{self.name}] New channel sensing process is started.')
        while True:
            try:
                # Perform backoff procedure
                self.backoff_process = self.env.process(self.backoff_procedure())
                yield self.backoff_process
                self.backoff_process = None
                # Send first packet to start transmission
                logger.info(f'[{self.env.now}] - [{self.name}] Backoff procedure complete. Data sending started.')
                self.channel.transmitting_ap.append(self)
                if self.config.direction == 'DL':
                    if self.config.rts_procedure:
                        yield self.env.process(self.send_mu_rts())
                    else:
                        yield self.env.process(self.send_data_packet())
                elif self.config.direction == 'UL':
                    if self.config.bsrp_procedure:
                        yield self.env.process(self.send_bsrp_trigger())
                    else:
                        if self.config.rts_procedure:
                            yield self.env.process(self.send_mu_rts())
                        else:
                            yield self.env.process(self.send_basic_trigger())
                self.sensing_process = None
                self.channel.transmitting_ap.remove(self)
                self.retransmission_counter = 0
                break
            except simpy.Interrupt as packet:
                # Handle the situation that collision occurred
                yield self.env.timeout(1)
                self.retransmission_counter += 1
                self.stats.number_of_retransmissions_per_ap[self.name] += 1
                self.stats.transmission_time -= ((packet.cause.packet_time + times.sifs_time) / 2)
                self.channel.transmitting_ap.remove(self)
                logger.info(f'[{self.env.now}] - [{self.name}] Collision occurred. Backoff procedure will be '
                            f'repeated. Current retransmission counter: {self.retransmission_counter} ')
                # Drop packet if too many tries
                if self.retransmission_counter > 7:
                    logger.info(f'[{self.env.now}] - [{self.name}] Too many tries to perform transmission, packet '
                                f'will be dropped')
                    self.transmission_complete = True
                    self.retransmission_counter = 0
                    self.stats.number_of_transmissions_per_ap[self.name] -= 1
                    for station in self.destination_stations:
                        self.stats.number_of_transmissions_per_station[station.name] -= 1
                    break
                yield self.env.timeout(1)
                continue

    def backoff_procedure(self):
        """Function to perform backoff procedure."""

        # Generate new backoff time value
        backoff_time = times.get_random_backoff_time(self.retransmission_counter) + times.aifs_time
        timeout = backoff_time
        logger.info(f'[{self.env.now}] - [{self.name}] New backoff time: {backoff_time}')
        while True:
            try:
                # Wait for channel is available
                while not self.channel.channel_available:
                    yield self.env.timeout(1)
                self.backoff_suspended = False
                # Countdown backoff time
                backoff_time = timeout
                while timeout > 0:
                    yield self.env.timeout(times.slot_time)
                    timeout -= times.slot_time
                self.stats.transmission_time += backoff_time
                self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations,
                                                                                  backoff_time)
                break
            except simpy.Interrupt:
                # Handle the situation that channel becomes busy
                logger.info(f'[{self.env.now}] - [{self.name}] Sensing process suspended because the channel is busy. '
                            f'Remaining backoff time: {timeout}')
                self.backoff_suspended = True
                continue

    def check_available_stations(self, all_destinations):
        """Function for getting the list of available stations."""

        available_stations = []
        for station in all_destinations:
            if not station.station_associated:
                available_stations.append(station)
        return available_stations

    def assign_stations_to_ap(self, all_destinations):
        """Function for assigning destination stations to Access Point for duration of simulation."""

        stations_per_ap = math.floor(self.config.number_of_stations / self.config.number_of_ap)
        # Get the list of available stations
        available_stations = self.check_available_stations(all_destinations)
        # Select randomly the stations
        self.assigned_stations = random.sample(available_stations, stations_per_ap)
        # Set the stations as already associated, so they cannot be selected by another Access Point
        for station in self.assigned_stations:
            station.station_associated = True
        # Assign remaining stations if you are the last Access Point
        available_stations = self.check_available_stations(all_destinations)
        if len(available_stations) < len(self.assigned_stations):
            for station in available_stations:
                self.assigned_stations.append(station)
                station.station_associated = True
        # Print names of assigned stations
        assigned_stations_names = []
        for station in self.assigned_stations:
            assigned_stations_names.append(station.name)
        logger.info(f'[{self.env.now}] - [{self.name}] List of stations assigned to Access Point:'
                    f' {assigned_stations_names}')

    def select_stations_for_current_transmission(self):
        """Function for selecting destination stations for current transmission."""

        number_of_destinations = len(self.assigned_stations)
        bandwidth = self.channel.bandwidth
        # Calculate how many stations can be served by the Access Point for a given channel bandwidth
        if self.config.ru_predefined:
            max_number_of_stations = len(self.config.ru_list)
        else:
            max_number_of_stations = self.channel.max_stations_in_transmission[bandwidth]
        if number_of_destinations > max_number_of_stations:
            # Select random stations if their number is greater than maximum possible number
            selected_stations = random.sample(self.assigned_stations, max_number_of_stations)
        else:
            # Select all available stations when their number is less than the maximum possible number
            selected_stations = self.assigned_stations
        self.destination_stations = selected_stations
        # Print names of destination stations
        destination_stations_names = []
        for station in self.destination_stations:
            destination_stations_names.append(station.name)
        logger.info(f'[{self.env.now}] - [{self.name}] Stations selected for current transmission:'
                    f' {destination_stations_names}')

    def allocate_resources(self):
        """Function for allocating channel resources to each selected station."""

        if self.config.ru_predefined:
            resources_units = self.config.ru_list
            used_resources_units = []
            # Randomly assign a RU to each station
            for station in self.destination_stations:
                allocated_bw = random.choice(resources_units)
                station.allocated_bw = allocated_bw
                resources_units.remove(allocated_bw)
                used_resources_units.append(allocated_bw)
                logger.info(f'[{self.env.now}] - [{self.name}] {station.allocated_bw}MHz allocated for {station.name}')
            self.config.ru_list = used_resources_units
        else:
            number_of_destinations = len(self.destination_stations)
            possible_subchannels = self.channel.possible_subchannels
            number_of_possible_subchannels = len(possible_subchannels)
            free_bandwidth = self.channel.bandwidth
            # Initialize RU list
            resources_units = []
            # Prepare a RU list suitable for the channel bandwidth and stations number
            for i in range(0, number_of_destinations):
                resources_units.append(0)
            for i in range(0, number_of_possible_subchannels):
                for j in range(0, number_of_destinations):
                    resources_units[j] = possible_subchannels[i]
                    free_bandwidth = round(self.channel.bandwidth - sum(resources_units))
                    if free_bandwidth <= 0:
                        break
                if free_bandwidth <= 0:
                    break
            # Randomly assign a RU to each station
            for station in self.destination_stations:
                allocated_bw = random.choice(resources_units)
                station.allocated_bw = allocated_bw
                resources_units.remove(allocated_bw)
                logger.info(f'[{self.env.now}] - [{self.name}] {station.allocated_bw}MHz allocated for {station.name}')

    def set_initial_type_of_packet_to_wait(self):
        """Function for setting packet type expected by Access Point after transmission is started."""

        if self.config.direction == 'DL':
            if self.config.rts_procedure:
                self.type_of_packet_to_wait = 'CTS'
            else:
                self.type_of_packet_to_wait = 'TB_BACK'
        elif self.config.direction == 'UL':
            if self.config.bsrp_procedure:
                self.type_of_packet_to_wait = 'BSR'
            else:
                if self.config.rts_procedure:
                    self.type_of_packet_to_wait = 'CTS'
                else:
                    self.type_of_packet_to_wait = 'UL_A_MPDU'

    def handle_received_packet(self, packet):
        """Function for handling the received packet by Access Point."""

        # Ignore packet to other destination
        if self in packet.destination_nodes:
            # Ignore incorrect packet type
            if packet.packet_type == self.type_of_packet_to_wait:
                # Handle BSR packet in AP
                if packet.packet_type == 'BSR':
                    self.received_packets_number += 1
                    if self.received_packets_number == self.expected_destinations_number:
                        self.received_packets_number = 0
                        time_to_add = packet.packet_time + times.sifs_time
                        self.stats.transmission_time += time_to_add
                        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations,
                                                                                          time_to_add)
                        if self.config.rts_procedure:
                            self.type_of_packet_to_wait = 'CTS'
                            yield self.env.process(self.send_mu_rts())
                        else:
                            if self.config.direction == 'DL':
                                self.type_of_packet_to_wait = 'TB_BACK'
                                yield self.env.process(self.send_data_packet())
                            elif self.config.direction == 'UL':
                                self.type_of_packet_to_wait = 'UL_A_MPDU'
                                yield self.env.process(self.send_basic_trigger())
                # Handle CTS packet in AP
                if packet.packet_type == 'CTS':
                    self.received_packets_number += 1
                    if self.received_packets_number == self.expected_destinations_number:
                        self.received_packets_number = 0
                        time_to_add = packet.packet_time + times.sifs_time
                        self.stats.transmission_time += time_to_add
                        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations,
                                                                                          time_to_add)
                        if self.config.direction == 'DL':
                            self.type_of_packet_to_wait = 'TB_BACK'
                            yield self.env.process(self.send_data_packet())
                        elif self.config.direction == 'UL':
                            self.type_of_packet_to_wait = 'UL_A_MPDU'
                            yield self.env.process(self.send_basic_trigger())
                # Handle UL A-MPDU packet in AP
                elif packet.packet_type == 'UL_A_MPDU':
                    self.received_packets_number += 1
                    if self.received_packets_number == self.expected_destinations_number:
                        self.received_packets_number = 0
                        packet_time_list = []
                        for station in self.destination_stations:
                            packet_time = times.get_packet_time(packet.packet_type, station.allocated_bw,
                                                                self.expected_destinations_number)
                            packet_time_list.append(packet_time)
                        packet_time = max(packet_time_list)
                        time_to_add = packet_time + times.sifs_time
                        self.stats.transmission_time += time_to_add
                        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations,
                                                                                          time_to_add)
                        self.set_initial_type_of_packet_to_wait()
                        yield self.env.process(self.send_ms_back())
                # Handle TB BACK packet in AP
                elif packet.packet_type == 'TB_BACK':
                    self.received_packets_number += 1
                    if self.received_packets_number == self.expected_destinations_number:
                        self.received_packets_number = 0
                        time_to_add = packet.packet_time
                        self.stats.transmission_time += time_to_add
                        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations,
                                                                                          time_to_add)
                        self.set_initial_type_of_packet_to_wait()
                        self.channel.channel_available = True
                        self.transmission_complete = True

    def send_bsrp_trigger(self):
        """Function for sending BSRP Trigger packet."""

        packet_type = 'BSRP_TRIGGER'
        source_node = self
        destination_nodes = self.destination_stations
        packet_time = times.get_packet_time(packet_type)
        bsrp_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_nodes)
        self.expected_destinations_number = len(destination_nodes)
        time_to_add = packet_time + times.sifs_time
        self.stats.transmission_time += time_to_add
        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations, time_to_add)
        yield self.env.process(self.send_packet(bsrp_packet))

    def send_mu_rts(self):
        """Function for sending MU-RTS packet."""

        packet_type = 'MU_RTS'
        source_node = self
        destination_nodes = self.destination_stations
        number_of_destinations = len(destination_nodes)
        bandwidth = None
        packet_time = times.get_packet_time(packet_type, bandwidth, number_of_destinations)
        rts_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_nodes)
        self.expected_destinations_number = len(destination_nodes)
        time_to_add = packet_time + times.sifs_time
        self.stats.transmission_time += time_to_add
        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations, time_to_add)
        yield self.env.process(self.send_packet(rts_packet))

    def send_data_packet(self):
        """Function for sending A-MPDU packet."""

        packet_type = 'DL_A_MPDU'
        source_node = self
        destination_nodes = self.destination_stations
        number_of_destinations = len(destination_nodes)
        packet_time_list = []
        for station in self.destination_stations:
            packet_time = times.get_packet_time(packet_type, station.allocated_bw, number_of_destinations)
            packet_time_list.append(packet_time)
        packet_time = max(packet_time_list)
        a_mpdu_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_nodes)
        self.expected_destinations_number = len(self.destination_stations)
        time_to_add = packet_time + times.sifs_time
        self.stats.transmission_time += time_to_add
        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations, time_to_add)
        yield self.env.process(self.send_packet(a_mpdu_packet))

    def send_basic_trigger(self):
        """Function for sending Basic Trigger packet."""

        packet_type = 'BASIC_TRIGGER'
        source_node = self
        destination_nodes = self.destination_stations
        number_of_destinations = len(destination_nodes)
        bandwidth = None
        packet_time = times.get_packet_time(packet_type, bandwidth, number_of_destinations)
        basic_trigger_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_nodes)
        self.expected_destinations_number = len(destination_nodes)
        time_to_add = packet_time + times.sifs_time
        self.stats.transmission_time += time_to_add
        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations, time_to_add)
        yield self.env.process(self.send_packet(basic_trigger_packet))

    def send_ms_back(self):
        """Function for sending MS-Back packet."""

        packet_type = 'MS_BACK'
        source_node = self
        destination_nodes = self.destination_stations
        number_of_destinations = len(destination_nodes)
        bandwidth = None
        packet_time = times.get_packet_time(packet_type, bandwidth, number_of_destinations)
        ms_back_packet = self.generate_new_packet(packet_type, packet_time, source_node, destination_nodes)
        self.expected_destinations_number = 0
        time_to_add = packet_time + times.aifs_time
        self.stats.transmission_time += time_to_add
        self.stats.increase_latency_for_station_that_are_not_transmitting(self.destination_stations, time_to_add)
        yield self.env.process(self.send_packet(ms_back_packet))
        self.transmission_complete = True
