<div id="top"></div>
<!-- PROJECT SHIELDS -->
<!--
*** See the bottom of this document for the declaration of the reference variables
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href=https://github.com/GEOSYS/>
    <img src=https://earthdailyagro.com/wp-content/uploads/2022/01/Logo.svg alt="Logo" width="400" height="200">
  </a>

 <h1 align="center">EarthDailyAgro Auto Cloud Mask quality</h3>

  <p align="center">
    Cloud mask comparison highlighting how EarthDaily Agro ACM accuracy is more than 90% per month on Sentinel-2 images and more than 85% per month on Landsat8&9 images
    <br />
    <a href=https://earthdailyagro.com/><strong>Who we are</strong></a>
    <br />
    <br />
    <a href=https://github.com/GEOSYS/Examples-and-showcases>Project description</a>
    ·
    <a href=https://github.com/GEOSYS/Examples-and-showcases/issues>Report Bug</a>
    ·
    <a href=https://github.com/GEOSYS/Examples-and-showcases/issues>Request Feature</a>
  </p>
</p>

<div align="center">
  
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Twitter][twitter-shield]][twitter-url]
[![Youtube][youtube-shield]][youtube-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
  
</div>

<!--[![Stargazers][GitStars-shield]][GitStars-url]-->
<!--[![languages][NETcore-shield]][NETcore-url]-->
<!--[![Forks][forks-shield]][forks-url]-->
<!--[![Stargazers][stars-shield]][stars-url]-->
<!--[![CITest][CITest-shield]][CITest-url]-->
<!--[![languages][language-python-shiedl]][]-->

<!-- TABLE OF CONTENTS -->
<details close>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#context">Context</a></li>
    <li><a href="#datasets">Datasets</a></li>
    <li><a href="#sclinterpretation">SCL Interpretation</a></li>
    <li><a href="analysis">Analysis</a></li>
    <li><a href="#results">Results</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#copyrights">Copyrights</a></li>
  </ol>
</details>

<!-- CONTEXT -->
## Context

The followinfg study contains a python notebook comparing ACM and HQco cloud masks: 
- ACM : Automated Cloud Mask generated by EarthDailyAgro in less than 1min
- HQco : Automated Cloud Mask corrected by EarthDaily Agro or his HQco cloud mask provider (dataset manually digitized, request 30min of work at least per image). Production of two shapefiles, one with clear and the other with cloud areas missed by ACM.

ACM masks are available on Sentinel-2 and Landsat8&9 images. It will be available on EarthDaily Constellation images as launch.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- DATASETS -->
## Datasets
The datasets are available in the GitHub folder.
To get more ACM and/or HQco masks, please [email us](mailto:sales@earthdailyagro.com).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- SCLINTERPREATION -->
## ACM Interpretation
The table below details our interpretation of the ACM mask for comparison with the HQCo mask.
<p align="center">
</p>

| Label | ACM   classification   |
|-------|------------------------|
| 0     | NO_DATA                |
| 1     | CLEAR		  	           |
| 2     | CLOUD       		       |

## HQco Interpretation
HQco masks are delivered with two shapefiles:
- clear areas as a correction of the ACM mask (can also include ACM clear areas)
- cloud areas as a correction of the ACM mask (can also include ACM cloud areas)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ANALYSIS -->
## Analysis

The initial step is to create a conda environement to use the notebook. You can use the file requirements.txt.
```
conda create --name myenv --file requirements.txt
```
 
1 - Intersect Fields with ACM masks and merge results

The result is two shapefiles: 
<br />
- fields with clear coverage using EDAgro ACM mask (ACM average = 1)
- fields with cloud coverage using EDAgro ACM mask (ACM average > 1)

2 - Intersect Fields with HQco masks and merge results

The result is two shapefiles: 
<br />
- fields that intersect HQco clear mask correction
- fields that intersect HQco cloud mask correction

3 -  Join ACM and HQco results & compute metrics
<p align="center">
</p>

4- Create the confusion matrix
<p align="center">
  <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/0230116_UK_final_matrix_1.JPG?raw=true">
</p>
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- RESULTS -->
## Results

Key outcomes of the analysis:
- EathDaily Cloud mask provides **15% higher accuracy** compared to public masks
- EathDaily Cloud mask is **more than 3 times better** than public mask on over cloud detection 

<img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/ACM_compare_to_other.JPG?raw=true">

Following are the result this dataset (time process => 2min)

Analysis of ACM vs HQco: accuracy 98.0%, over cloud detection 0.0%, under cloud detection 2.0%

- Percent of fields clear in HQco and ACM = 2.0%
- Percent of fields clear in ACM and cloud in HQco = 2.0%
- Percent of fields clear in HQco and cloud in ACM = 0.0%
- Percent of fields cloud in HQco and ACM = 96.0%



| Comparison             | Accuracy (%) |  Confusion Matrix |
:-------------------------:|:-------------------------:|:-------------------------:
ACM vs HQco on the data available on GitHub | Accuracy 98.0%, over cloud detection 0.0%, under cloud detection 2.0% | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/0230116_UK_final_matrix_1.JPG?raw=true">
ACM vs HQco on all Sentinel-2 images in France from January to April 2022 | Accuracy 92.6%, over cloud detection 4.4%, under cloud detection 3.0% | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/2022_FR_S2.png?raw=true">
ACM vs HQco on all Sentinel-2 images in UK from January to April 2022 | Accuracy 92.9%, over cloud detection 4.2%, under cloud detection 2.9% | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/2022_UK_S2.png?raw=true">
ACM vs HQco on all Sentinel-2 images in Sweden from February to May 2022 | Accuracy 87.1%, over cloud detection 10.6%, under cloud detection 2.4% | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/2022_SW_S2.png?raw=true">
ACM vs HQco on all Landsat images in France from January to April 2022 | Accuracy 89.7%, over cloud detection 8.8%, under cloud detection 1.6% | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/2022_FR_L8.png?raw=true">
ACM vs HQco on all Landsat images in UK from January to April 2022 | Accuracy 84.5%, over cloud detection 14.1%, under cloud detection 1.5% | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/2022_UK_L8.png?raw=true">
ACM vs HQco on all Landsat images in Sweden from February to May 2022 | Accuracy 85.5%, over cloud detection 13.1%, under cloud detection 1.4% | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Auto-Cloud-Mask-Accuracy/Images/2022_SW_L8.png?raw=true">



<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

For any additonal information, please [email us](mailto:sales@earthdailyagro.com).

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- COPYRIGHTs -->
## Copyrights

© 2023 Geosys Holdings ULC, an Antarctica Capital portfolio company | All Rights Reserved.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- List of available shields https://shields.io/category/license -->
<!-- List of available shields https://simpleicons.org/ -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=social
[NETcore-shield]: https://img.shields.io/badge/.NET%20Core-6.0-green
[NETcore-url]: https://github.com/dotnet/core
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=plastic&logo=appveyor
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/qgis-plugin/repo.svg?style=plastic&logo=appveyor
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/GEOSYS/qgis-plugin/repo.svg?style=social
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://opensource.org/licenses/MIT
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=social&logo=linkedin
[linkedin-url]: https://www.linkedin.com/company/earthdailyagro/mycompany/
[twitter-shield]: https://img.shields.io/twitter/follow/EarthDailyAgro?style=social
[twitter-url]: https://img.shields.io/twitter/follow/EarthDailyAgro?style=social
[youtube-shield]: https://img.shields.io/youtube/channel/views/UCy4X-hM2xRK3oyC_xYKSG_g?style=social
[youtube-url]: https://img.shields.io/youtube/channel/views/UCy4X-hM2xRK3oyC_xYKSG_g?style=social
[language-python-shiedl]: https://img.shields.io/badge/python-3.7-green?logo=python
[language-python-url]: https://pypi.org/ 
[GitStars-shield]: https://img.shields.io/github/stars/GEOSYS?style=social
[GitStars-url]: https://img.shields.io/github/stars/GEOSYS?style=social
[CITest-shield]: https://img.shields.io/github/workflow/status/GEOSYS/qgis-plugin/Continous%20Integration
[CITest-url]: https://img.shields.io/github/workflow/status/GEOSYS/qgis-plugin/Continous%20Integration


