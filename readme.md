# Get CHIRPS-GEFS daily forecast data (16 days)

 Automatic extraction of daily CHIRPS-GEFS forecasts. Up to 16 days forecast.

   DatasetType: CHIRPS-GEFS_ mean
   spatial resolution: 0.05 degrees
   Num days forecast:   1 to 16 days

## Data extraction methods 
Range-based:
   ClimateServ_CHIPS-GEFS.bat: Historical data extraction at global scale using the ClimateSERV API https://climateserv.servirglobal.net/

Operational extraction for the Mekong Basin region Domain [minLon: 89, Maxlon: 112, Minlat: 3 , MaxLat:36]
   OP_CHIRPS-GEFS_Tiff_NetCDF.bat: Operational forecast for the Mekong region [ format tif and/or NetCDF]. 
   OP_CHIRPS-GEFS_ASCII.bat:  Operational forecast for the Mekong region adapted to the FEWS system (http://www.delft-fews.nl/)

## requirements
Range-based:
  climateserv  =  0.0.12 

Operational Mekong Basin:
netCDF4 >= 1.4.2

gdal >= 2.3.3 

## Python pip Installation
Run this command to start installing all python dependencies:

  conda env create -f environment.yml

## Parameters

ClimateServ_CHIPS-GEFS.bat:     
    -i [DatasetVariable] CHIRPS_GEFS_precip_mean
    -o [Outfile in format .zip] 
    -b [boundary MinLon,Maxlon,Minlat,Maxlat]
    -s [EarliestDate]
    -t [LatestDate]
    -n [post_netcdf] 'yes' (optional)

OP_CHIRPS-GEFS_Tiff_NetCDF.bat
    -o [Outfile] 
    -b [boundary]
    -f [days_forecast] 1/16 days
    -n [postNETCDF]  'yes' (optional)

OP_CHIRPS-GEFS_ASCII.bat
    -o [Outfile] 
    -b [boundary]
    -f [days_forecast] 1/16 days

## Examples: 

ClimateServ_CHIPS-GEFS.bat: 
    python bin/ClimateServ_CHIPS-GEFS.py -i CHIRPS_GEFS_precip_mean -o CHIRPS_GEFSrange.zip -b 93,110,9,25 -s '2020-03-10' -t '2020-03-20'  -n yes

OP_CHIRPS-GEFS_Tiff_NetCDF.bat
    python bin/Op_MK_CHIPS-GEFS.py -o CHIRPS_GEFS -b 93,110,9,25 -f 10 

OP_CHIRPS-GEFS_ASCII.bat
    python bin/Op_MK_CHIPS-GEFS_ASCII.py -o CHIRPS_GEFS_ascii -b 89,112,3,36 -f 10
