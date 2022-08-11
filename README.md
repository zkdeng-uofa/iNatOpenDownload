<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!--[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]-->



<!-- PROJECT LOGO -->
<!-- <br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

<h2 align="center">iNaturalist Open Download</h2>

  <p align="center">
    Python scripts to easily download images form the iNaturalist Open Data dataset
    <br />
    <!--<a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>-->
    <br />
    <!--
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>-->
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <!--<li><a href="#built-with">Built With</a></li>-->
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
    <!--<li><a href="#contributing">Contributing</a></li>-->
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--[![Product Name Screen Shot][product-screenshot]](https://example.com)-->


iNaturalist is a citizen science platform where users can upload photographs of specific organisms. As a result iNaturalist contains one of the world's largest stores of images of living organisms. The iNaturalist Open Data project is a curated subset of the overall iNaturalist dataset that specifically contains images that apply to the Creative Commons licsense. It was created specifically to aid researchers by providing over 70 million photos of living organisms.
<br />

<a href="https://github.com/inaturalist/inaturalist-open-data">iNaturalist Open Data</a>

This project, iNaturalist Open Download, aims to create a simple scipt to download the images that are associated with a specific taxonomy rank in the iNaturalist format. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!--
### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- GETTING STARTED -->
## Getting Started

This project uses the <a href="https://snakemake.github.io/">Snakemake</a> framework to create easy to use and reproducible workflows. A variety of snakemake rules are combined with user input to acquire the desired images. 

### Prerequisites

Conda is an open source package distributer and manager. This project uses conda to install packages.

* <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html">Conda Installation Page</a> 

The iNaturalist open dataset is stored on Amazon Web Services (AWS). As such the AWS Command Line Interfance (AWS CLI) is required to use this script. 
* <a href="https://docs.aws.amazon.com/cli/v1/userguide/install-macos.html">AWS CLI</a>

``` sh
curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
```

### Installation

1. Clone the repository.
   ``` sh
   git clone https://github.com/zkdeng-uofa/iNatOpenDownload
   ```
2. Move into the iNatOpenDownload folder.
   ``` sh
   cd /path/to/iNatOpenDownload
   ```
3. Create a conda environment that contains pip and snakemake using the requirement.yaml file. 
   ``` sh 
   conda env create --name iNatOpenDownload --file environment.yaml
   ```
4. Install other required packages through pip.
   ``` sh
   pip install -r requirements.txt
   ```
5. Use snakemake to download and create the iNaturalist open data sqlite database. 
   ```
   snakemake -c1
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage
The iNaturalist open download script uses a sequence of consecutive snakemake rules to download the final images. As the user of the script a simple command plus user input will download the images of interest.

#### All Images

This snakemake rule downloads all images associated with a particular taxonomy.

-The basic usage requires the user to use the snakemake command combined with a proper folder name of the taxonomy rank of interest
``` sh
snakemake imgs/[taxonomy_rank]_all-imgs -c1
```
-This will prompt the proper snakemake rules to activate and respective scripts to run.

-The user will prompted to enter a taxonomy rank, input database file, and rank level of images to download
```sh
Enter a taxon name (i.e. Cigaritis): [taxonomy_name]
Your taxon name is [taxonomy_name]

Enter an input database (i.e. inat_open_data.sq3db): [input data base]
Your taxon name is [input data base]

Enter a rank (i.e. species): [rank level]
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] Upload onto Cyverse data stores
- [ ] Bash script looping for image downloads that are very large
- [	] Improved job scheduler and tracking during csv creation, image downloading and image uploading. (Explore different options)
- [ ] Subspecies nested into species when downloading


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Please consult zkdeng@arizona.edu for use.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Your Name: Zi Deng - zkdeng@arizona.edu

Project Link: [https://github.com/zkdeng-uofa/iNatOpenDownload](https://github.com/zkdeng-uofa/iNatOpenDownload)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* University of Arizona Data Science Institute
* Nirav Merchant - nirav@arizona.edu
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 