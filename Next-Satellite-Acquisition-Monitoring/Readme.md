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

 <h1 align="center">Next satellite acquisition monitoring</h3>

  <p align="center">
    Next satellite acquisition highlighting how Earthdaily Agro supports their clients to anticipate next clear satellite image at field level
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

The following study contains a python notebook to provide next satellites acquisitions dates with cloud cover estimation at field level using geosys Platform.
Requirements:
- EarthDaily Agro WeatherHub API access
- Earth Spectator API key

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- DATASETS -->
## Datasets

This script is field level based, so, as an input the geometry is mandatory. 
Geometry can be provided in WKT or in CSV with a field id and centroid or calling Geosys Domain Management API to retrieve the geometry by the seasonfield id.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- SCLINTERPREATION -->
## Interpretation
The table below details our interpretation of the cloud cover percent to the probability to have a CLEAR image.

| Label | Cloud Cover %   		 | Probability to have a CLEAR image  |
|-------|------------------------|------------------------------------|
| Green |  < 20                  | High                               |
| Yellow| 20 -> 60 			     | Medium                             |
| Orange| 60 -> 80     			 | Low                                |
| Red   |  > 80          		 | Near to zero                       |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ANALYSIS -->
## Analysis

The initial step is to create a conda environement to use the notebook. You can use the file requirements.txt. 
```
conda create --name myenv --file requirements.txt
```
Then 
```
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```
And define your path.
 
1 - log in on Geosys API & Earth Spectrator API with your credentials

username = '*****'

password = '*****'

api_key_earth_spectator = '*****'

2 - Import your fields, 3 options:
- import a csv with:
	- seasonfield id (default colunm name in the script : "idseasonfield")
	- centroid of the seasonfield (default colunm name in the script : "GPS")
	- geometry of the seasonfield (default colunm name in the script : "WKT")
	
- Import geometry in WKT format
	- centroid of the geometry will be automatically computed 
	
- Import seasonfields by calling Geosys Domain Management APIs using seasonfiel id
	
3 - Call Earth Spectator API to get next satellite acquisition at field level

4 - Call EarthDaily Agro WeatherHub API to get the cloud cover for each satellite acquisition 

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- RESULTS -->
## Results

Following are the result for 2 seasonfields on the next 9 days (time process => < 1min)


|location	|GPS									 |date		 |hour	   |satellite	|cloudcover |color	|
|-------	|----------------------------------------|-----------|---------|------------|-----------|-------|
|q1azyxv	|POINT (23.787239760000002 -29.27996104) |10/08/2023 |08:21:35 |Landsat-8	|0.0 		|green  |
|q1azyxv	|POINT (23.787239760000002 -29.27996104) |10/08/2023 |08:37:45 |Sentinel-2B	|0.0 		|green  |
|q1azyxv	|POINT (23.787239760000002 -29.27996104) |15/08/2023 |08:37:34 |Sentinel-2A	|9.8 		|green  |
|pr7p3wv	|POINT (23.787239760000002 -29.27996104) |10/08/2023 |08:21:35 |Landsat-8	|0.0 		|green  |
|pr7p3wv	|POINT (23.787239760000002 -29.27996104) |10/08/2023 |08:37:45 |Sentinel-2B	|0.0 		|green  |
|pr7p3wv	|POINT (23.787239760000002 -29.27996104) |15/08/2023 |08:37:34 |Sentinel-2A	|9.8 		|green  |


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


