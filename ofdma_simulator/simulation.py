"""
:copyright: Copyright (C) 2022 Damian Piasecki
:author: Damian Piasecki
:email: piasecki.damian97@gmail.com
:description: The main ofdma_simulator file containing the implementation of the Config class and the Simulator class.
              The Config data class is used to initialize the parameters with which the simulation was run.
              The Simulator class includes functions for initializing the simulator (creating Access Point objects
              and User Station objects) and for running a simulation.
"""

import sys
import simpy
import logging
import random
from dataclasses import dataclass

import configs.simulation_config as simulation_config
from helpers.logger import prepare_logger
from helpers.stats import Stats
from channel import Channel
from access_point import AccessPoint
from station import Station


logger = logging.getLogger('ofdma_simulator')


@dataclass()
class Config:
    """Dataclass containing simulation settings."""

    simulation_time: int = simulation_config.SIM_TIME
    number_of_ap: int = simulation_config.NUMBER_OF_AP
    number_of_stations: int = simulation_config.NUMBER_OF_STATIONS
    seed: int = simulation_config.SEED
    direction: str = simulation_config.DIRECTION
    mcs: int = simulation_config.MCS
    data_rate: float = simulation_config.DATA_RATE
    ru_list = simulation_config.RU_LIST
    rts_procedure: bool = simulation_config.RTS_PROCEDURE_ENABLED
    bsrp_procedure: bool = simulation_config.BSRP_PROCEDURE_ENABLED
    mpdu_aggregation: bool = simulation_config.MPDU_AGGREGATION_ENABLED
    ru_predefined: bool = simulation_config.RU_PREDEFINED
    data_rate_predefined: bool = simulation_config.DATA_RATE_PREDEFINED


class Simulator:
    """Main simulator class."""

    def __init__(self):
        """Simulator class constructor."""

        self.env = simpy.Environment()
        self.config = Config()
        self.channel = Channel()
        self.stats = Stats()
        self.simulator_initialized = False
        self.ap_list = []
        self.stations_list = []

    def initialize_simulator(self):
        """Function for initializing simulator."""

        # Create list of Access Points
        for i in range(0, self.config.number_of_ap):
            ap_name = "AccessPoint" + str(i)
            self.ap_list.append(AccessPoint(ap_name, self.env, self.config, self.channel, self.stats))
        # Create list of Stations
        for i in range(0, self.config.number_of_stations):
            station_name = "Station" + str(i)
            self.stations_list.append(Station(station_name, self.env, self.config, self.channel, self.stats))
        # Set the status of the simulator as initialized
        self.simulator_initialized = True
        logger.info(f'[{self.env.now}] - Simulator is initialized.')

    def run_simulation(self):
        """Function for running the simulation."""

        # Check if simulator is initialized
        if not self.simulator_initialized:
            logger.info(f'[{self.env.now}] - Initialize the simulator before running the simulation.')
            sys.exit(1)
        # Set list of stations as all possible destinations
        all_destinations = self.stations_list
        # Create transmission process for each Access Point
        for access_point in self.ap_list:
            self.env.process(access_point.perform_transmission(all_destinations))
        # Start simulation
        random.seed(self.config.seed)
        self.env.process(self.stats.print_simulation_progress(self.env, self.config.simulation_time))
        logger.info(f'[{self.env.now}] - Simulation is started.')
        self.env.run(until=self.config.simulation_time)
        self.stats.print_statistics()


def main():
    """Main ofdma_simulator function."""

    prepare_logger()
    logger.info('App initialized. Starting simulation.')
    simulation = Simulator()
    simulation.initialize_simulator()
    simulation.run_simulation()


if __name__ == '__main__':
    main()
