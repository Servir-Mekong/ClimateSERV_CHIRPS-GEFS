#call activate GPM-BICO
python bin/ClimateServ_CHIPS-GEFS.py -i CHIRPS_GEFS_precip_mean -o CHIRPS_GEFSrange.zip -b 93,110,9,25 -s '2020-03-10' -t '2020-03-20' 
python bin/ClimateServ_CHIPS-GEFS.py -i CHIRPS_GEFS_precip_mean -o CHIRPS_GEFS10days.zip -b 93,110,9,25 
pause

