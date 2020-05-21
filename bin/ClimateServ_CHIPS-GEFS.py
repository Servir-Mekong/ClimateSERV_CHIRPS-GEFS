# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:49:07 2020

Download from ClimateServ
https://pypi.org/project/climateserv/#modal-close

@author: SERVIR Mekong
@contact: miguel.barajas@adpc.net
@update: 5 May 2020

"""

import climateserv.api
from datetime import date, timedelta
import sys, getopt
from pathlib import Path

def main():  
  
    print('=============================================================')
    print('            Get CHIRPS-GEFS from ClimateSERV                 ')
    print('=============================================================')
    print(' tool for the Regional Flood and Drought Management Center (RFDMC) ')
    print('   Mekong River commision  			      					')	
    print('     Developed by SERVIR-MEKONG                              ')
    print('     version 1.0                                             ')
    print('     last updated (05/05/2020)                               ')
    print('     contact: miguel.barajas@adpc.net                        ')
    print('                                                             ')
    print('                                       Please wait   ...     ')
	
#    PixelRes = 0.05 #degrees
    [MinLon,MaxLon, MinLat, MaxLat] = [93,110,9,35]
    boundary= '93,110,9,25' 
    DatasetType = 'CHIRPS_GEFS_precip_mean'
    OperationType = 'Download'    
   
    # Dates for operational
    EarliestDate = date.today()
    LatestDate = date.today()  + timedelta(days=10)

    SeasonalEnsemble = 'ens01'
    SeasonalVariable = 'Precipitation'
    Outfile = r'D:\CHIRPS_GEFS10days.zip'    

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:b:s:t:")
    except getopt.GetoptError:
        print('ClimateServ_CHIPS-GEFS.py -i <DatasetType> -o <Outfile> -b <boundary> -s <EarliestDate> -t <LatestDate>')
        print('no run')
#        print('ClimateServ_CHIPS-GEFS.py -i {0} -o {1} -b {2} -s {3} -t {4}'.format(DatasetType,Outfile,boundary,EarliestDate,LatestDate))
        sys.exit(2)
  
    for opt, arg in opts:
        if opt == '-h':
            print('ClimateServ_CHIPS-GEFS.py -i {0} -o {1} -b {2} -s {3} -t {4}'.format(DatasetType,Outfile,boundary,EarliestDate,LatestDate))
            sys.exit()
        if opt == "-i" : DatasetType = arg            
        if opt == "-o" : Outfile = Path(arg)               
        if opt == "-b" : 
            boundary = arg
            [MinLon,MaxLon, MinLat, MaxLat] =  boundary.split(',')    
            [MinLon,MaxLon, MinLat, MaxLat] = [float(MinLon),float(MaxLon), float(MinLat), float(MaxLat)]  
        if opt == "-s" :
            Date = arg
            [year,month,day] = Date.split('-')   
            EarliestDate = date(int(year.replace("'", "")), int(month), int(day.replace("'", "")))                                
        if opt == "-t" : 
            DateE = arg            
            [year,month,day] = DateE.split('-')   
            LatestDate = date(int(year.replace("'", "")), int(month), int(day.replace("'", "")))    

    EarliestDate = EarliestDate.strftime("%m/%d/%Y")
    LatestDate = LatestDate.strftime("%m/%d/%Y")
    
    GeometryCoords = [[MinLon,MaxLat],[MaxLon, MaxLat],
                      [MaxLon, MinLat],[MinLon,MinLat],
                      [MinLon,MaxLat]]
   
    climateserv.api.request_data(DatasetType, OperationType, 
                 EarliestDate, LatestDate,GeometryCoords, 
                 SeasonalEnsemble, SeasonalVariable,Outfile)

if __name__ == "__main__":
   main()