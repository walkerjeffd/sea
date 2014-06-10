NOAA Quantitative Precipitation Forecast
========================================

Jeff Walker
2014-05-20

Goal: use python to extract QPF at a single point

packages: shapely (via exe), fiona, qgis?

install OSGeo4W (only GDAL)

set env variables
    add C:\OSGeo4W\bin to PATH
    set GDAL_DATA to C:\OSGeo4W\share\gdal

install shapely via exe (http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)
    download to virtualenv\src
    extract with 7zip
    copy contents to virtualenv\Lib\site-packages\
install fiona via exe (http://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
    download to virtualenv\src
    easy_install Fiona-1.1.5dev.wind32-py2.7.exe
install pyproj via pip
    pip install pyproj

download shapefile from ftp: ftp.hpc.ncep.noaa.gov/shapefiles/qpf/7day/QPF168hr_Day1-7_latest.tar
untar
    7z e -oshp tar/QPF168hr_Day1-7_latest.tar

open in qgis
projection: GEOGCS["GCS_Sphere_EMEP",DATUM["D_Sphere_EMEP",SPHEROID["Sphere_EMEP",6371200.0,0.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]

reproject in QGIS to NAD83/Conus Albers (EPSG:5070) -> 97e2012_albers.shp

note that you can do the reprojection in python using pyproj

see ipython notebook

virtualenv: qpf