# Netops_Cadiz

This is a tiny Python library that aims to facilitate the retrieval of spectral responses for a range of satellites (Sentinel 2 A&B (MSI sensor), Landsat 4-9 (TM, ETM+, OLI & OLI2 sensors)) and drone cameras (just Sequoia at this point, but more will be added) from field spectroradiometry data obtained with [ASD Spectroradiometers](https://www.malvernpanalytical.com/es/products/product-range/asd-range/fieldspec-range).

![](https://i.imgur.com/mW97kxl.png)

The library has been created through the collaboration of [LAST-EBD](https://www.ebd.csic.es/servicios/laboratorio-sig-y-teledeteccion) and [Speclab](https://speclab.csic.es/index.php) in the framework of the Spanish Network of Optical Proximal Sensing ([NetOPS](https://netops.csic.es/)). The idea comes from a radiometry course held at the XX Spanish Remote Sensing Asociation Congress in Cádiz (and now y'all know where the name is coming from).


## Instalation

Just go with pip install.

```pip install netops_cadiz```


## What's behind and what can you get

netops_cadiz have been designed to provide the theoretical values of the satellite bands that would be obtained from surface reflectivity data acquired with a radiometer.

To this end, an Excel table (we need to change this) has been created in which the spectral response function of each band for the aforementioned satellites/sensors is stored. 
  
![](https://i.imgur.com/jKvuZkj.jpeg)


The objective is to combine each measured spectrum with each spectral response function of the sensor in order to obtain a weighted measurement that reflects how the spectrum would be captured by the sensor.
This is achieved by combining the sensor's spectral response function with the measured spectrum in order to obtain a weighted measurement that reflects how the sensor would capture the spectrum.

In developing the library, our initial focus was on .txt files generated by the ViewSpecPro software. However, the advent of the wonderful [Specdal](https://pypi.org/project/specdal/) Python library has enabled us to expand our scope to encompass ASD files as well. 


## Usage

Basic usage would be use the method *spec2sat*. Where one spectrum should be passed and one satellite should be selected to get the expected response for each one of its bands.

```python
from netops_cadiz.netops import asd

# path to srf table (should be fixed)
srf_table = 'path/to/sensores_srs.xlsx' 
# path to spectral profile 
spec_path = "path/to/asd_or_txt_file"

# instance the class and choose wich sat you want data for
a = asd(srf_table, spec_path, 'S2A')
a.txt2sat(spec_path, "Vegetación")
```

Output would be something like this:  

![](https://i.imgur.com/ZK77imQ.png)

There are also 4 more methods:

* *plotSpecs* To plot several spectrum and satellite response profiles.
* *satTable* To generate a table with teh response for the selected satellite for all the spectrums inside a folder.
* *specsTable* To generate one table for each specturm inside a folder with the expected values for all the satellites.
* *ndiCalc* To compute a Normalized Difference Index between 2 parts of the spectrum and its equivalent bands in all the satellites/sensors available. 

There's a tutorial that goes into more detail about how to use the ***asd*** class and all its methods.. You sould find it [here](https://github.com/Digdgeo/Netops_Cadiz/blob/master/examples/netops_example.ipynb)


## ToDo

Lots of things, main idea right now (moreover adding more satellites and drone cameras to get the spectral response, such as MODIS, ASTER, Sentinel 3, Micasense, etc...) is to add the possibility to work with hyperspectral satellites as inputs (also outputs?). 

*working with other spectrometers should be immediate, but I have not had access to other data to test it yet.*

## Acknowledgements

 - [PTI Teledetec](https://awesomeopensource.com/project/elangosundar/awesome-README-templates): An interdisciplinary thematic platform to coordinate and integrate the remote sensing activities of Spanish Research Council.
 - To all the teachers of the course [Spectroradiometry as a support for Remote Sensing research: Fundamentals and applications.](https://netops.csic.es/2024/03/30/curso-espectro-radiometria-como-soporte-a-la-investigacion-en-teledeteccion-fundamentos-y-aplicaciones/)
 - Special thanks to **Joan Cristian Padró** because he performed the interpolation needed to correctly calculate some Landsat bands for his article [Radiometric Correction of Simultaneously Acquired Landsat-7/Landsat-8 and Sentinel-2A Imagery Using Pseudoinvariant Areas (PIA): Contributing to the Landsat Time Series Legacy](https://www.mdpi.com/2072-4292/9/12/1319).