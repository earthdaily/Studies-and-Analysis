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

 <h1 align="center">Cloud mask benchmark</h3>

  <p align="center">
    Cloud mask benchmark highlighting how Earthdaily Agro delivers 15% higher accuracy than public model on Sentinel images
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

The followinfg study contains a python  notebook python comparing cloud masks from different provider : 
- ACM : cloud mask generated by EarthDailyAgro
- SCL : Sentinel 2 L2A Scene Classification
- WQR : Reference mask based on human-corrected ACM mask (World Quality Reference)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- DATASETS -->
## Datasets
The datasets are availables in the following bucket AWS S3: https://clear-mask-quality-comparer.s3-us-east-2.amazonaws.com/

Each dataset will have its own folder within the bucket, containing the ACM and WQR mask. The S3 URI of the SCL mask can be deduced from the dataset's name.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- SCLINTERPREATION -->
## SCL Interpretation
The table below details our interpretation of the SCL mask for comparison with the ACM mask.
<p align="center">
  <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Cloud-Mask-Performance/Images/SCLClasses.png?raw=true">
</p>

| Label | SCL   classification   |  SCL   classification for analysis (equivalent to the ACM interpretation) |
|-------|------------------------|---------------------------------------------------------------------------|
| 0     | NO_DATA                | NO_DATA                                                                   |
| 1     | SATURATED_OR_DEFECTIVE | CLEAR                                                                     |
| 2     | DARK_AREA_PIXELS       | CLEAR                                                                     |
| 3     | CLOUD_SHADOWS          | CLOUD                                                                     |
| 4     | VEGETATION             | CLEAR                                                                     |
| 5     | NOT_VEGETATED          | CLEAR                                                                     |
| 6     | WATER                  | CLEAR                                                                     |
| 7     | UNCLASSIFIED           | CLEAR                                                                     |
| 8     | CLOUD_MEDIUM_PROB      | CLOUD                                                                     |
| 9     | CLOUD_HIGH_PROB        | CLOUD                                                                     |
| 10    | THIN_CIRRUS            | CLOUD                                                                     |
| 11    | SNOW                   | CLOUD                                                                     |


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ANALYSIS -->
## Analysis

The initial step is to create a conda environement to use the notebook. You can use the file requirements.txt.
```
conda create --name myenv --file requirements.txt
```
 
1 - open a AWS session
<p align="center">
  <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Cloud-Mask-Performance/Images/NoteBookCode.png?raw=true">
</p>

2 - List available data on a dedicated bucket in AWS S3
<p align="center">
  <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Cloud-Mask-Performance/Images/assetlist.png?raw=true">
</p>
The result is a dataframe with the S3 URI of ACM, WQR and SCL mask.

3 -Compute confusion matrix from the dataframe (process time : 2 minutes by dataset)
<p align="center">
  <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Cloud-Mask-Performance/Images/ComputeMatrix.png?raw=true">
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- RESULTS -->
## Results

Following are the result on 5 datasets (time process => 10min)

| Comparison             |  Confusion Matrix |
:-------------------------:|:-------------------------:
ACM vs WQR | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Cloud-Mask-Performance/Images/ACMWQR.png?raw=true">
SCL vs WQR | <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Cloud-Mask-Performance/Images/SCLWQR.png?raw=true">
SCL vs ACM|  <img src="https://github.com/GEOSYS/Studies-and-Analysis/blob/main/Cloud-Mask-Performance/Images/SCLACM.png?raw=true">

Key outcomes of the analysis:
- EathDaily Cloud mask provides **15% higher accuracy** compared to public masks
- EathDaily Cloud mask is **more than 3 times better** than public mask on over cloud detection 

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


