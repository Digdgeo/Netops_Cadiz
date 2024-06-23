# Netops_Cadiz

This is a tiny Python library that aims to facilitate the retrieval of spectral responses for a range of satellites (Sentinel 2 A&B (MSI sensor) and Landsat 4-9 (TM, ETM+, OLI & OLI2 sensors)) from field radiometry data obtained with [ASD radiometers](https://www.malvernpanalytical.com/es/products/product-range/asd-range/fieldspec-range).

![](https://i.imgur.com/mW97kxl.png)

The library has been created through the collaboration of [LAST-EBD](https://www.ebd.csic.es/servicios/laboratorio-sig-y-teledeteccion) and [Speclab](https://speclab.csic.es/index.php) in the framework of the Spanish Network of Optical Proximal Sensing ([NetOPS](https://netops.csic.es/)). The idea comes from a radiometry course held at the XX Spanish Remote Sensing Asociation Congress in Cádiz (and now y'all know where the name is coming from).


## Instalation

If you are reading this before july 2024 just copy or download the code. Very soon the library will be available on PyPI and you'd only need to do a pip install (and this comment will have been removed).

```pip install netops_cadiz```


## What's behind and what can you get

netops_cadiz have been designed to provide the theoretical values of the satellite bands that would be obtained from surface reflectivity data acquired with a radiometer.

To this end, an Excel table (we need to change this) has been created in which the spectral response function of each band for the aforementioned satellites/sensors is stored.  

Special thanks to Joan Cristian Padró because he performed the interpolation needed to correctly calculate some Landsat bands for his article [Radiometric Correction of Simultaneously Acquired Landsat-7/Landsat-8 and Sentinel-2A Imagery Using Pseudoinvariant Areas (PIA): Contributing to the Landsat Time Series Legacy](https://www.mdpi.com/2072-4292/9/12/1319).


In developing the library, our initial focus was on .txt files generated by the ViewSpecPro software. However, the advent of the wonderful [Specdal](https://pypi.org/project/specdal/) Python library has enabled us to expand our scope to encompass ASD files as well. 


## Usage

```python

from netops_cadiz import asd

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

And you should also have a profile txt saved in your current folder with the values for the bands of the satellite that you chose.

Of course, this could be runned in a loop to get all the spectra profile with all the available satellitesm but this is a work in progress that should be ready before the end of the 2024 summer... (we'll see)

There is a notebook showing more in deep the usage of the asd class. You sould find it [here]('/examples/netops_example.ipynb')


## ToDO

Lots of things, main idea right now (moreover adding more satellites to get the spectral response, such as MODIS, ASTER or Sentinel 3) is to add the possibility to work with hyperspectral satellites as inputs.
