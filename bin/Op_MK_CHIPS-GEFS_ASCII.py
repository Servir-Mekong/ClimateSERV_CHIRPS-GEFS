# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:49:07 2020

Download from ClimateServ
https://pypi.org/project/climateserv/#modal-close

@author: SERVIR Mekong
@contact: miguel.barajas@adpc.net
@update: 5 Nov 2020

"""

# from osgeo import gdal
from datetime import timedelta, datetime, date
import sys, getopt,os
# from pathlib import Path
from ftplib import FTP
import warnings
warnings.filterwarnings("ignore")
import netCDF4 as nc
import numpy as np
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import pandas as pd
import time

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r%s |%s| %s%% %s\r' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print()
 
    return  

def main():  
  
    print('=============================================================')
    print('  Operational CHIRPS-GEFS for the Mekong Basin               ')
    print('=============================================================')
    print(' tool for the Regional Flood and Drought Management Center (RFDMC) ')
    print('   Mekong River commision  			      					')	
    print('     Developed by SERVIR-MEKONG                              ')
    print('     version 1.3                                            ')
    print('     last updated (05/11/2020)                               ')
    print('     contact: miguel.barajas@adpc.net                        ')
    print('                                                             ')
    print('                                       Please wait   ...     ')
	
    PixelRes = 0.05 #degrees
    [MinLon,MaxLon, MinLat, MaxLat] = [89,112,3,36]
    boundary= '89,112,3,36' 
    numdays = 10
    Output_name = 'CHIRPSGEFS_ascii'
    operat = 1
    EarliestDate = date(2020, 9, 21)
    LatestDate = date(2020, 10, 6)	
	
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:b:f:s:t:n:")
    except getopt.GetoptError:
        print('Op_MK_CHIPS-GEFS.py -o <Outfile> -b <boundary> -f <days_forecast> -s <EarliestDate> -t <LatestDate>')
        print('no run')
#        print('ClimateServ_CHIPS-GEFS.py -i {0} -o {1} -b {2} -s {3} -t {4}'.format(DatasetType,Outfile,boundary,EarliestDate,LatestDate))
        sys.exit(2)
  
    for opt, arg in opts:
        if opt == '-h':
            print('Op_MK_CHIPS-GEFS.py  -o {0} -b {1} -f {2}'.format(Output_name,boundary,numdays))
            sys.exit()         
        if opt == "-o" : Output_name = arg             
        if opt == "-b" : 
            boundary = arg
            [MinLon,MaxLon, MinLat, MaxLat] =  boundary.split(',')    
            [MinLon,MaxLon, MinLat, MaxLat] = [float(MinLon),float(MaxLon), float(MinLat), float(MaxLat)]                               
        if opt == "-f" : 
            numdays = int(arg) 
			
        if opt == "-s" :
            Date = arg
            [year,month,day] = Date.split('-')   
            EarliestDate = date(int(year.replace("'", "")), int(month), int(day.replace("'", "")))
            operat = 0
				
        if opt == "-t" : 
            DateE = arg            
            [year,month,day] = DateE.split('-')   
            LatestDate = date(int(year.replace("'", "")), int(month), int(day.replace("'", "")))			
    
    if  operat == 1:   
        base = datetime.today()# - timedelta(days=15)
        Dates = [ timedelta(days=x) + base for x in range(numdays)]	
        # message
        print('DatasetType: CHIRPS-GEFS_ mean')
        print('spatial resolution: 0.05 degrees')
        print("Rainfall forecast for today "  + base.strftime("%d-%b-%Y"))
        print( "Num days forecast: {0}/15 (operational)".format(numdays))
        print('Boundaries MinLon: {0}, MaxLon: {1}, MinLat: {2}, MaxLat: {3}'.format(MinLon,MaxLon, MinLat, MaxLat))
        print( 'lonlat domain for MK= [89,112,3,36]')
        
    else: 
        EarliestDate = EarliestDate.strftime("%m/%d/%Y")
        LatestDate = LatestDate.strftime("%m/%d/%Y")
        Dates = pd.date_range(EarliestDate,LatestDate, freq='d')
        # message
        print('DatasetType: CHIRPS-GEFS_ mean')
        print('spatial resolution: 0.05 degrees')
        print("Rainfall forecast "  + EarliestDate +' - ' + LatestDate)
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
    
    i= 0
    for Date in Dates:
        try:
            File = 'mb_cgefs_precip_0p05_{0:02d}.{1:02d}{2:02d}.nc'.format(Date.year,Date.month,Date.day)
            ftpPath = [f for f in Files  if f.endswith(File)][0] 
            chirpsgefs_file = os.path.join(MK_files,File)
            with open(chirpsgefs_file, 'wb') as outfile:
                ftp.retrbinary("RETR " + ftpPath, outfile.write)     
    
            # MinLon,MinLat,MaxLon,MaxLat
            f = nc.Dataset(chirpsgefs_file) # read file
            Lat = f.variables['lat'][:]
            Lon = f.variables['lon'][:]
            Lon_index = np.asanyarray(np.where( (Lon >= MinLon ) & (Lon <= MaxLon) ) )
            Lat_index = np.asanyarray(np.where( (Lat >= MinLat ) & (Lat <= MaxLat) ) )
            temp = f.variables['precip'][Lat_index.min():Lat_index.max()+1, Lon_index.min():Lon_index.max()+1]
            temp = np.flipud(temp)
            f.close()
            
            # SAVE ASCII
            Raster_name = 'forecast_{0}{1:02d}{2:02d}000000.asc'.format(Date.year,Date.month,Date.day)
            Raster_path = os.path.join(Output,Raster_name)
    
            f = StringIO()
            np.savetxt(f,temp, fmt='%.3f')
            f.seek(0)
            fs = f.read().replace('-9999.000', '-9999', -1)
            f.close()
            f = open(Raster_path, 'w')
            f.write("ncols " + str(temp.shape[1]) + "\n")
            f.write("nrows " + str(temp.shape[0]) + "\n")
            f.write("xllcorner " + str( MinLon) + "\n")
            f.write("yllcorner " + str(MinLat) + "\n")
            f.write("cellsize " + str(PixelRes) + "\n")
            f.write("NODATA_value " + str(-9999) + "\n")
            f.write(fs)
            f.close() 
            time.sleep(0.01)
            printProgressBar(i + 1, len(Dates), prefix='Download Progress:', suffix='Complete', length=40)
            i=i+1
 
        except:
            print('Error in '+ Date.strftime('%m/%d/%Y'))
            i=i+1
        

if __name__ == "__main__":
   main()