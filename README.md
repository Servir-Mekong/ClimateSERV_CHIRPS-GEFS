# ClimateSERV_CHIRPS-GEFS
Automatic extraction of CHIRPS-GEFS rainfall forecast data using ClimateSERV 


This is a package uses the ClimateSERV API for CHIRPS-GEFS extraction(https://climateserv.servirglobal.net/)
you can be install ClimateServ API using pip:

    pip install climateserv

    CHIRPS-GEFS variables:
          Mean
          Variable: CHIRPS_GEFS_precip_mean
          25th percentile
          Variable: CHIRPS_GEFS_precip_25
          75th percentile
          Variable: CHIRPS_GEFS_precip_75

    Runner.bat 
    -i <DatasetVariable> 
    -o <Outfile in format .zip> 
    -b <boundary[MinLon,Maxlon,Minlat,Maxlat]>
    -s <EarliestDate>
    -t <LatestDate>'

Examples: 

Range based
    python bin/ClimateServ_CHIPS-GEFS.py -i CHIRPS_GEFS_precip_mean -o testrange.zip -b 93,110,9,25 -s '2020-03-10' -t '2020-03-20' 

Operarional CHIRPS-GEFS 10 days forecast
    python bin/ClimateServ_CHIPS-GEFS.py -i CHIRPS_GEFS_precip_mean -o test10days.zip -b 93,110,9,25 

