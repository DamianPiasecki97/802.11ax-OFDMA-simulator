"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: File containing helper functions used to calculate transmission statistics such as the amount of data
              transferred, network throughput and the number of retransmissions.
"""

import sys


class Stats:
    """Class containing functions and settings used to calculate transmission statistics."""

    def __init__(self):
        """Stats class constructor."""

        self.transmission_time = 0
        self.latency_per_station = {}
        self.data_transferred_per_station = {}
        self.throughput_per_station = {}
        self.number_of_transmissions_per_station = {}
        self.number_of_transmissions_per_ap = {}
        self.number_of_retransmissions_per_ap = {}

    def increase_latency_for_station_that_are_not_transmitting(self, stations_in_transmission, latency):
        station_names = []
        for station in stations_in_transmission:
            station_names.append(station.name)
        for key in self.latency_per_station:
            if key not in station_names:
                self.latency_per_station[key] += latency

    def calculate_latency_per_station(self):
        for key in self.latency_per_station:
            latency = (self.latency_per_station[key] / self.number_of_transmissions_per_station[key]) / 1000
            self.latency_per_station[key] = round(latency, 3)

    def calculate_average_latency(self):
        latency = 0
        number_of_stations = 0
        self.calculate_latency_per_station()
        for key in self.latency_per_station:
            latency += self.latency_per_station[key]
            number_of_stations += 1
        average_latency = round((latency / number_of_stations), 3)
        return average_latency

    def calculate_throughput(self):
        data_transferred = 0
        for key in self.data_transferred_per_station:
            data_transferred += self.data_transferred_per_station[key]
        thr = round(data_transferred / (self.transmission_time / 1000000)) / 1000000
        thr = round(thr, 3)
        return thr

    def calculate_throughput_per_station(self):
        for key in self.data_transferred_per_station:
            self.throughput_per_station[key] = 0
        for key in self.throughput_per_station:
            thr = round(self.data_transferred_per_station[key] / (self.transmission_time / 1000000)) / 1000000
            thr = round(thr, 3)
            self.throughput_per_station[key] = thr

    def calculate_number_of_transmissions(self):
        number_of_transmissions = 0
        for key in self.number_of_transmissions_per_ap:
            number_of_transmissions += self.number_of_transmissions_per_ap[key]
        return number_of_transmissions

    def calculate_number_of_retransmissions(self):
        number_of_retransmissions = 0
        for key in self.number_of_retransmissions_per_ap:
            number_of_retransmissions += self.number_of_retransmissions_per_ap[key]
        return number_of_retransmissions

    def print_average_latency(self):
        thr = self.calculate_average_latency()
        print(f"Average latency obtained for the entire network: {thr} ms")

    def print_latency_per_station(self):
        self.calculate_latency_per_station()
        for key in self.latency_per_station:
            print(f"{self.latency_per_station[key]}")

    def print_throughput(self):
        thr = self.calculate_throughput()
        print(f"Throughput obtained for the entire network: {thr} Mbps")

    def print_throughput_per_station(self):
        self.calculate_throughput_per_station()
        for key in self.throughput_per_station:
            print(f"Throughput obtained for {key}: {self.throughput_per_station[key]} Mbps")

    def print_number_of_transmissions(self):
        number_of_transmissions = self.calculate_number_of_transmissions()
        print(f"Number of transmissions performed in entire network: {number_of_transmissions}")

    def print_number_of_transmissions_per_station(self):
        for key in self.number_of_transmissions_per_station:
            print(f"Number of transmissions performed by {key}: {self.number_of_transmissions_per_station[key]}")

    def print_number_of_transmissions_per_ap(self):
        for key in self.number_of_transmissions_per_ap:
            print(f"Number of transmissions performed by {key}: {self.number_of_transmissions_per_ap[key]}")

    def print_number_of_retransmissions(self):
        number_of_retransmissions = self.calculate_number_of_retransmissions()
        print(f"Number of retransmissions occurred in entire network: {number_of_retransmissions}")

    def print_number_of_retransmissions_per_ap(self):
        for key in self.number_of_retransmissions_per_ap:
            print(f"Number of retransmissions occurred for {key}: {self.number_of_retransmissions_per_ap[key]}")

    def print_statistics(self):
        self.print_number_of_transmissions()
        self.print_number_of_retransmissions()
        self.print_throughput_per_station()
        self.print_throughput()
        self.print_average_latency()

    def print_simulation_progress(self, env, simulation_time):
        print("Simulation started\n")
        while True:
            simulation_percent = round((env.now / simulation_time) * 100)
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            print("Simulation in progress [%-100s] %d%%" % ('=' * simulation_percent, simulation_percent))
            if simulation_percent >= 95:
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print("Simulation in progress [%-100s] %d%%" % ('=' * 100, 100))
                print("Simulation finished")
            yield env.timeout(10000)
