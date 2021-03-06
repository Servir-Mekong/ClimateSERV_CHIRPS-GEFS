# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:49:07 2020

Download from ClimateServ
https://pypi.org/project/climateserv/#modal-close

@author: SERVIR Mekong
@contact: miguel.barajas@adpc.net
@update: 27 Oct 2020

"""

import climateserv.api
from datetime import date, timedelta
import sys, getopt,os
from pathlib import Path
from PIL import Image
import numpy as np
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def main():  
  
    print('=============================================================')
    print('            Get CHIRPS-GEFS from ClimateSERV                 ')
    print('=============================================================')
    print(' tool for the Regional Flood and Drought Management Center (RFDMC) ')
    print('   Mekong River commision  			      					')	
    print('     Developed by SERVIR-MEKONG                              ')
    print('     version 2.0                                             ')
    print('     last updated (27/10/2020)                               ')
    print('     contact: miguel.barajas@adpc.net                        ')
    print('                                                             ')
    print('                                       Please wait   ...     ')
	
#    PixelRes = 0.05 #degrees
    [MinLon,MaxLon, MinLat, MaxLat] = [89,112,3,36]
    boundary= '89,112,3,36' 
    DatasetType = 'CHIRPS_GEFS_precip_mean'
    OperationType = 'Download' 
    PixelRes = 0.05
   
    # Dates for operational
    EarliestDate = date.today()
    LatestDate = date.today()  + timedelta(days=15)

    SeasonalEnsemble = 'ens01'
    SeasonalVariable = 'Precipitation'
    Outfile = r'CHIRPS_GEFS15days.zip'    
    post_netcdf = 'no'
	
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:b:s:t:n:")
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
            # [MinLon,MaxLon, MinLat, MaxLat] = [float(MinLon),float(MaxLon), float(MinLat), float(MaxLat)]  
            [MinLon,MaxLon, MinLat, MaxLat] = [float(MinLon),float(MaxLon), float(MinLat), float(MaxLat)]  
        if opt == "-s" :
            Date = arg
            [year,month,day] = Date.split('-')   
            EarliestDate = date(int(year.replace("'", "")), int(month), int(day.replace("'", "")))                                
        if opt == "-t" : 
            DateE = arg            
            [year,month,day] = DateE.split('-')   
            LatestDate = date(int(year.replace("'", "")), int(month), int(day.replace("'", "")))  
        if opt == "-n" : post_netcdf = arg 

    EarliestDate = EarliestDate.strftime("%m/%d/%Y")
    LatestDate = LatestDate.strftime("%m/%d/%Y")
    
    MaxLat = MaxLat -1
    MaxLon = MaxLon -1
    GeometryCoords = [[MinLon,MaxLat],[MaxLon, MaxLat],
                      [MaxLon, MinLat],[MinLon,MinLat],
                      [MinLon,MaxLat]]
    
    OutFolder= os.path.join(os.getcwd(),'CHIRPS-GEFS')
    if not os.path.exists(OutFolder):    
        os.mkdir(OutFolder)
    os.chdir(OutFolder)
    Output_path = os.path.join(OutFolder,Outfile)
   
    climateserv.api.request_data(DatasetType, OperationType, 
                 EarliestDate, LatestDate,GeometryCoords, 
                 SeasonalEnsemble, SeasonalVariable,Output_path)
    
    if post_netcdf == 'yes':
        print('transforming files to netCDF')
        # Transform to netcdf    
        def youCanQuoteMe(item):
            return "\"" + item + "\""
        
        Unzip = 'tar -xf ' + str(Outfile)
        os.system(Unzip)
    
        fullCmd = ' '.join(['for %i in (*.tif) do gdal_translate -of', youCanQuoteMe('netcdf'), '%i %i.nc'])
        os.system(fullCmd)
        
    elif post_netcdf == 'ascii':
        print('transforming files to ascii')
        # Transform to netcdf    
        def youCanQuoteMe(item):
            return "\"" + item + "\""
        
        Unzip = 'tar -xf ' + str(Outfile)
        os.system(Unzip)
        
        Rasters = [f for f in os.listdir('.')  if f.endswith('.tif')] 
        
        for file in Rasters:
            Date = file.replace('.tif','')
            [year,month,day] = Date.split('-')   
            ascii_name = 'forecast_{0}{1:02d}{2:02d}000000.asc'.format(int(year),int(month),int(day))    
            
            # fullCmd = ' '.join([ 'gdal_translate -of', youCanQuoteMe('AAIGrid'),file,ascii_name,'-projwin', str(MinLon), str(MaxLat), str(MaxLon), str(MinLat),'-tr 0.05 0.05'])    
            # # fullCmd = ' '.join(['for %i in (*.tif) do gdal_translate -of', youCanQuoteMe('AAIGrid'), '%i %~ni_fews.ascii'])
            # os.system(fullCmd)
                        
            img = Image.open(file)
            temp = np.array(img)
            
            f = StringIO()
            np.savetxt(f,temp, fmt='%.3f')
            f.seek(0)
            fs = f.read().replace('-9999.000', '-9999', -1)
            f.close()
            f = open(ascii_name, 'w')
            f.write("ncols " + str(temp.shape[1]) + "\n")
            f.write("nrows " + str(temp.shape[0]) + "\n")
            f.write("xllcorner " + str( MinLon) + "\n")
            f.write("yllcorner " + str(MinLat) + "\n")
            f.write("cellsize " + str(PixelRes) + "\n")
            f.write("NODATA_value " + str(-9999) + "\n")
            f.write(fs)
            f.close() 

    else:
        pass

if __name__ == "__main__":
   main()