# Op_MK_CHIPS-GEFS
Automatic extraction of CHIRPS-GEFS rainfall forecast for the Mekong region

requires gdal available in (https://gdal.org/) 


   CHIRPS-GEFS variables:   
          
          Variable: CHIRPS_GEFS_precip_mean
          Forecast: Up to 10 days (operational)
          spatial resolution: 0.05 degrees
          Max lonlatbox domain for MK= [89,112,3,36]


   OP_forecast.bat file
    
    'Op_MK_CHIPS-GEFS.py 
    -o <Outfile>
    -b <boundary>
    -f <days_forecast>
    -n <postNETCDF>  'yes' (optional)
    


Examples: 


Operarional CHIRPS-GEFS 10 days forecast

    python bin/Op_MK_CHIPS-GEFS.py -o CHIRPS_GEFS10days -b 93,110,9,25 -f 10 -n yes


