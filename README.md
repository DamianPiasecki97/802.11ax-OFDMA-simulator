# 802.11ax-OFDMA-simulation

<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <!-- <h3 align="center">802.11ax-OFDMA-simulation</h3> -->

  <p align="right">
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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

One of the latest extensions of the IEEE 802.11 standard is the 802.11ax extension. Its main goal is to improve the efficiency of using the available bandwidth and increase the overall transmission performance. This has been achieved by enabling transmission to multiple users simultaneously, both for uplink (UL) and downlink (DL). Due to its specific features, 802.11ax networks are also referred to as high-efficiency WLANs (HE) or, according to the new nomenclature, Wi-Fi 6. This extension is dedicated to dense networks consisting of many client stations and access points.

The increase in transmission efficiency has been made possible by employing techniques such as MU-MIMO (multi-user multiple input multiple output) and OFDMA (orthogonal frequency-division multiple access), which allow for the simultaneous handling of multiple end users.

The goal of the project was to create a simulator for the operation of an IEEE 802.11ax network, implementing the OFDMA mechanism. It was decided that the developed program would meet the following assumptions:

➢ The implementation of the network operation, particularly the OFDMA mechanism, will comply with the IEEE 802.11ax extension.
➢ During the simulation, transmission will occur in only one selected direction — either uplink (UL) or downlink (DL).
➢ The simulation will be able to run using multiple local wireless networks — the program will implement the possibility of using multiple access points within a given area, each communicating with a different group of stations. The access points will operate within a common range.
➢ Data frames transmitted during the transmission can be aggregated to improve network throughput. The number of aggregated frames will be determined to use the TXOPlimit time as efficiently as possible. This is a parameter of the EDCA mechanism (enhanced distributed channel access), which represents the period during which the access point can conduct transmission.
➢ The user will have the option to choose simulation parameters, such as the transmission direction, the modulation and coding scheme used, the number of stations and access points involved in the transmission, and the duration of the simulation.

This project was transferred from a previous private repository.
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/othneildrew/Best-README-Template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=othneildrew/Best-README-Template" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Damian Piasecki - [([https://twitter.com/your_username](https://www.linkedin.com/in/piasecki-damian/)) 

Project Link: https://github.com/DamianPiasecki97/802.11ax-OFDMA-simulator

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/piasecki-damian/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
