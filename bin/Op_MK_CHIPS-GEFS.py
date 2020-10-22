# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:49:07 2020

Download from ClimateServ
https://pypi.org/project/climateserv/#modal-close

@author: SERVIR Mekong
@contact: miguel.barajas@adpc.net
@update: 5 May 2020

"""

from osgeo import gdal
from datetime import timedelta, datetime
import sys, getopt,os
# from pathlib import Path
from ftplib import FTP
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def main():  
  
    print('=============================================================')
    print('  Operational CHIRPS-GEFS for the Mekong Basin               ')
    print('=============================================================')
    print(' tool for the Regional Flood and Drought Management Center (RFDMC) ')
    print('   Mekong River commision  			      					')	
    print('     Developed by SERVIR-MEKONG                              ')
    print('     version 1.2                                             ')
    print('     last updated (11/09/2020)                               ')
    print('     contact: miguel.barajas@adpc.net                        ')
    print('                                                             ')
    print('                                       Please wait   ...     ')
	
#    PixelRes = 0.05 #degrees
    [MinLon,MaxLon, MinLat, MaxLat] = [93,110,9,35]
    boundary= '93,110,9,25' 
    numdays = 10
    Output_name = 'CHIRPS-GEFS'
    post_netcdf = 'yes'
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:b:f:n:")
    except getopt.GetoptError:
        print('Op_MK_CHIPS-GEFS.py -o <Outfile> -b <boundary> -f <days_forecast> -n <postNETCDF>')
        print('no run')
#        print('ClimateServ_CHIPS-GEFS.py -i {0} -o {1} -b {2} -s {3} -t {4}'.format(DatasetType,Outfile,boundary,EarliestDate,LatestDate))
        sys.exit(2)
  
    for opt, arg in opts:
        if opt == '-h':
            print('Op_MK_CHIPS-GEFS.py  -o {0} -b {1} -f {2} -n {3}'.format(Output_name,boundary,numdays,post_netcdf))
            sys.exit()         
        if opt == "-o" : Output_name = arg             
        if opt == "-b" : 
            boundary = arg
            [MinLon,MaxLon, MinLat, MaxLat] =  boundary.split(',')    
            [MinLon,MaxLon, MinLat, MaxLat] = [float(MinLon),float(MaxLon), float(MinLat), float(MaxLat)]                               
        if opt == "-f" : 
            numdays = int(arg)                
        if opt == "-n" : post_netcdf = arg 
    
    base = datetime.today()
    Dates = [ timedelta(days=x) + base for x in range(numdays)]    
    
    # message
    print('DatasetType: CHIRPS-GEFS_ mean')
    print('spatial resolution: 0.05 degrees')
    print("Rainfall forecast for today "  + base.strftime("%d-%b-%Y"))
    print( "Num days forecast: {0}/10 (operational)".format(numdays))
    print('Boundaries MinLon: {0}, MaxLon: {1}, MinLat: {2}, MaxLat: {3}'.format(MinLon,MaxLon, MinLat, MaxLat))
    print( 'lonlat domain for MK= [89,112,3,36]')

    ftp = FTP('216.218.240.199')
    ftp.login(user='ftpuser',passwd=  '@Smekong')
    Files = ftp.nlst('cgefs_precip_a0p05/daily_new/')    
    
    Output = os.path.join(os.getcwd(),Output_name)
    if not os.path.exists(Output):    
        os.mkdir(Output)
    os.chdir(Output)
    MK_files = os.path.join(Output,'MK_files_nc')    
    if not os.path.exists(MK_files):   
        os.mkdir(MK_files)
        
    for Date in Dates:
        File = 'mb_cgefs_precip_0p05_{0:02d}.{1:02d}{2:02d}.nc'.format(Date.year,Date.month,Date.day)
        ftpPath = [f for f in Files  if f.endswith(File)][0] 
        chirpsgefs_file = os.path.join(MK_files,File)
        with open(chirpsgefs_file, 'wb') as outfile:
            ftp.retrbinary("RETR " + ftpPath, outfile.write)                 
        PixelRes = 0.05
        gdal.Warp(os.path.join(Output,File[:-2]+'tif'),chirpsgefs_file, xRes=PixelRes, yRes=PixelRes,outputBounds=[MinLon,MinLat,MaxLon,MaxLat],dstSRS='EPSG:4326')        
        
    
    if post_netcdf == 'yes':
        print('transforming files to netCDF')
        # Transform to netcdf    
        def youCanQuoteMe(item):
            return "\"" + item + "\""        
    
        fullCmd = ' '.join(['for %i in (*.tif) do gdal_translate -of', youCanQuoteMe('netcdf'), '%i %i.nc'])
        os.system(fullCmd)
    else:
        pass

if __name__ == "__main__":
   main()