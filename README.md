<div id="top"></div>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://gitlab-student.centralesupelec.fr/arthur.manceau/routage">
    <img src="images/logo.png" alt="Logo" width="300" height="180">
  </a>

<h3 align="center"><b><font size="+10">S6 - ROUTAGE</font></h3>


  <p align="center"><p><font size="+2">
  This is a project that analyzes the rooting of a cyclist. By providing the itenerary, the user/cyclist can have an analysis on his individual physical performance regarding this route. The analysis can give some information about the type of the route and the conditions of the route the user selected to follow. Futhermore, the analysis constists of the total distance, the velocity, the gradients and the future prediction of the time. By an elaborate automatic learning of travel times and regression models, it can provide more accurate information on the key elements of routing. </font></h3>


<div align="left">
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#launching">Launching</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
<div align="left">

## About The Project

<br />
<div align="center">
  <a href="https://gitlab-student.centralesupelec.fr/arthur.manceau/routage">
    <img src="images/interface.PNG" alt="interface" width="700" height="400">
  </a>
</div>


<div align="left">
The user can interact with the previous interface, the main tasks the app can perform are the following:

- Statistical analysis of GPS tracks
- Visualization of the route (heatmap, darkmode etc.)
- Visualization using terrain models 3D map)
- Calculation of speed
- Filtering data for accuracy
- Interactive representation
- Automated prediction with regression models

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get to run the app and set up the project you need first to intall the required libraries and execute the following instructions.

### **Prerequisites**

The required libraries:

- gpxpy >= 1.5.0
- pyproj >= 3.2.1
- dash >= 2.3.1
- plotly >= 5.4.0
- folium >= 0.12.1
- scipy >= 1.4.1
- keras >= 2.8.0
- haversine >= 2.5.1
- tensorflow >= 2.1.0
- rasterio >= 1.2.10

Use the following intallation method: 
  ```sh
  pip install <library>
  ```

### **Launching**

1. Clone the repo
   ```sh
   git clone https://gitlab-student.centralesupelec.fr/arthur.manceau/routage
   ```
2. Go to source file
   ```sh
   cd Layers
   ```
3. Run the interface:
   ```sh
   python3 dash_inteface.py
   ```
   In case the intepreter can't run the previous command, we suggest running dash_inteface.py file manually.

4. By running the file the Dash will be running on a specific IP address, for exemple: http://127.0.0.1:8050/. All the user has to do is copy the IP address, the script gives him, in a browser or simple clicking on it.
    
    The output may look like the following:
   ```js
    PS C:\Users\CHRIS KARATZIAS\Desktop\routage> conda activate base
    PS C:\Users\CHRIS KARATZIAS\Desktop\routage> & C:/Anaconda3/python.exe "c:/Users/CHRIS KARATZIAS/Desktop/routage/Layers/dash_inteface.py"
    Dash is running on http://127.0.0.1:8050/
    * Serving Flask app "dash_inteface" (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The user can insert a GPX file of his route in the GPX directory and can have it analyzed by clicling on it in the interface, he previous launched.

The user will be provided with:
- Statistics about the route
- Visualization of the route on a heatmap
- Calculation of route speed (raw & filtred)
- 3D Elevation Visualization
- Elevation error (Tif/Mesured)
- Elevation gradient (raw & filtred)
- Regression Models for prediction of data points response (polynomial, neural net & sigmoid regression)
- Evaluators/indices of regression models
- Gradient Profile Distribution

_For more examples, please refer to the [Documentation](Layers) of each script/file._

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

  Any external contribution or suggestion is  welcome and **greatly appreciated**.

If of suggestions that would make our project better and more functional, please fork the repo and create a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Adding some New Feature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License.

MIT License

Copyright (c) [2022] [Christos KARATZIAS] [Routage]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

See [LICENSE.txt](LICENCE.txt) for more information.


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://gitlab-student.centralesupelec.fr/arthur.manceau/routage](https://gitlab-student.centralesupelec.fr/arthur.manceau/routage)

Contributors/Creators:

* Christos KARATZIAS - CentraleSupélec - christos.karatzias@student-cs.fr

* Arthur MANCEAU - CentraleSupélec - arthur.manceau@student-cs.fr

* Raphaël GIBORY - CentraleSupélec - raphael.gibory@student-cs.fr

* Salahidine LEMAACHI - CentraleSupélec - salahidine.lemaachi@student-cs.fr

* Ahmed El-BAJDALI - CentraleSupélec - ahmed.el-bajdali@student-cs.fr

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
We would like to thank professors José Picheral and Emmanuel Vazquez for their advice and help throughout this project. Their guidance was helpful in finalizing our project.

List resources we find helpful and we would like to give credit to:
- [Choose an Open Source License](https://choosealicense.com/)
- [GitHub](https://github.com/)


<p align="right">(<a href="#top">back to top</a>)</p>



  <br />
  <a href="https://gitlab-student.centralesupelec.fr/arthur.manceau/routage"><strong>Explore the docs in gitlab »</strong></a>
  <br />
  <a href="mailto:salahidine.lemaachi@student-cs.fr">Demand Help & Support!</a> and/or <a href="mailto:christos.karatzias@student-cs.fr">Report Bug</a>
  <br />
  </p>
</div>
