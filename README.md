# 802.11ax-OFDMA-simulation

<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="left">

  <!-- <h3 align="center">802.11ax-OFDMA-simulation</h3> -->

  <p align="left">
    Simulator of the OFDMA mechanism of the IEEE 802.11ax standard
    <br />
    <a href="https://github.com/DamianPiasecki97/802.11ax-OFDMA-simulator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#simulation-settings">Simulation settings</a></li>
        <li><a href="#starting-the-simulation">Starting the simulation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

One of the latest extensions of the IEEE 802.11 standard is the 802.11ax extension. Its main goal is to improve the efficiency of using the available bandwidth and increase the overall transmission performance. This has been achieved by enabling transmission to multiple users simultaneously, both for uplink (UL) and downlink (DL). Due to its specific features, 802.11ax networks are also referred to as high-efficiency WLANs (HE) or, according to the new nomenclature, Wi-Fi 6. This extension is dedicated to dense networks consisting of many client stations and access points.

The increase in transmission efficiency has been made possible by employing techniques such as MU-MIMO (multi-user multiple input multiple output) and OFDMA (orthogonal frequency-division multiple access), which allow for the simultaneous handling of multiple end users.

The goal of the project was to create a simulator for the operation of an IEEE 802.11ax network, implementing the OFDMA mechanism. It was decided that the developed program would meet the following assumptions:

* The implementation of the network operation, particularly the OFDMA mechanism, will comply with the IEEE 802.11ax extension.
* During the simulation, transmission will occur in only one selected direction — either uplink (UL) or downlink (DL).
* The simulation will be able to run using multiple local wireless networks — the program will implement the possibility of using multiple access points within a given area, each communicating with a different group of stations. The access points will operate within a common range.
* Data frames transmitted during the transmission can be aggregated to improve network throughput. The number of aggregated frames will be determined to use the TXOPlimit time as efficiently as possible. This is a parameter of the EDCA mechanism (enhanced distributed channel access), which represents the period during which the access point can conduct transmission.
* The user will have the option to choose simulation parameters, such as the transmission direction, the modulation and coding scheme used, the number of stations and access points involved in the transmission, and the duration of the simulation.

This project was moved from a previous private repository.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Python][Python]][Python-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

All Python modules required to run the program are listed in `requirements.txt` file.
You can install all modules using below command:
```sh
pip install -r requirements.txt
```

### Installation

The program does not require special installation. It is only necessary to clone the repository: 
   ```sh
   git clone https://github.com/DamianPiasecki97/802.11ax-OFDMA-simulator.git
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Simulation settings

The program has been implemented in such a way that the user can modify the simulation parameters. The simulation settings can be changed by modifying the values of constants defined in the simulation_config.py file.
Below is the definition of the simulation parameters:
* LOGS_DIR - path to the file where events occurring in the program are logged
* SIM_TIME - simulation time
* NUMBER_OF_AP - number of access points participating in the transmission
* NUMBER_OF_STATIONS - number of stations participating in the transmission
* SEED - seed value of the generator
* DIRECTION - transmission direction (UL or DL)
* MCS - number specifying the modulation and coding scheme, in accordance with the IEEE 802.11ax extension
* DATA_RATE - data rate, this value is used in the program when the DATA_RATE_PREDEFINED parameter is set to true
* RU_LIST - list of Resource Units (RUs) that can be assigned to stations during the simulation, this list is used in the program when the RU_PREDEFINED parameter is set to true
* RTS_PROCEDURE_ENABLED - boolean variable indicating whether the MU-RTS/CTS procedure should be part of the transmission.
* BSRP_PROCEDURE_ENABLED - boolean variable indicating whether the BSRP procedure should be part of the transmission
* MPDU_AGGREGATION_ENABLED - boolean variable indicating whether frame aggregation will be active during the transmission
* RU_PREDEFINED - boolean variable indicating whether the list of Resource Units (RUs) should be predefined. If set to true, the list defined as the RU_LIST parameter will be used for calculations in the program
* DATA_RATE_PREDEFINED - boolean variable indicating whether the data rate should be predefined. If set to true, the value defined as the DATA_RATE parameter will be used for calculations in the program

### Starting the simulation

To run the program, it is necessary to execute the simulation.py script, for example, using the python3 command : 
   ```sh
   https://github.com/DamianPiasecki97/802.11ax-OFDMA-simulator.git
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE 
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->

<!-- CONTACT -->
## Contact

Damian Piasecki - https://www.linkedin.com/in/piasecki-damian/

Project Link: https://github.com/DamianPiasecki97/802.11ax-OFDMA-simulator

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/piasecki-damian/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
