#!/usr/bin/env python2

import urllib2
import re
import datetime
import time
import os

f_s = '/'
u_s = '_'



def read_long_lat(url, longitude_start, longitude_end, latitude_start, latitude_end):
    """ Read the available longitude and latitude list
    """
    
    # Download the list of the available coordinates from the server
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    try:
        data = response.read()
    except URLError as e:
        print e.reason
    lines = data.splitlines()
    del lines[-1]
    long_lat_list = []
    
    # Create the long/lat coordinate list
    for loc in lines:
        loc_conv = loc.split('_-')
        loc_conv = [int(i) for i in loc_conv] 
        if loc_conv[0] >= longitude_start and loc_conv[0] <= longitude_end and loc_conv[1] >= latitude_start and loc_conv[1] <= latitude_end:
            long_lat_list.append(loc);
    return long_lat_list


def read_data_from_server(long_lat_list, start_year, start_month, end_year, end_month):
    """ Read the data from the server
    """
    
    # Create a new directory for the data
    cur_time = time.time()
    time_stamp = datetime.datetime.fromtimestamp(cur_time).strftime('%Y-%m-%d_%H:%M:%S')
    os.makedirs("/short/ir5/yxs659/data/"+time_stamp)

    # Set the url
    dom_url = 'http://dapds00.nci.org.au/'
    server = 'thredds/fileServer/rs0/tiles/EPSG4326_1deg_0.00025pixel/'
    sat_id = 'LS7'
    sensor_id = 'ETM'
    product_code = 'NBAR'
    file_type ='.tif'
    data_url_1 = dom_url + server + sat_id + u_s + sensor_id + f_s

    catalog_url_1 = 'http://dapds00.nci.org.au/thredds/catalog/rs0/tiles/EPSG4326_1deg_0.00025pixel/LS7_ETM/'

    for long_lat in long_lat_list:
        print long_lat
        for year in range(start_year, end_year+1):
            # Read the catalog of the availabe files
            url = catalog_url_1 + long_lat + '/' + str(year) + '/catalog.html'
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            try:
                catalog_data = response.read()
            except URLError as e:
                print e.reason
            # Download the data files for each year
            for month in range(start_month, end_month+1):
                year_str = str(year)
                print year, month
                if month < 10:
                    month_str = '0'+str(month)
                else:
                    month_str = str(month)
                # Search the names of the data files
                pattern_string =  sat_id + u_s + sensor_id + f_s + long_lat + f_s + year_str + f_s + sat_id + u_s + sensor_id + u_s + product_code + u_s + long_lat + u_s + year_str + '-' + month_str + '-' + '.*tif\''
                pattern = re.compile(pattern_string)
                tiff_list = pattern.findall(catalog_data)
                for item in tiff_list:
                    # Download the data file
                    data_url = dom_url + server + item[:-1]
                    request = urllib2.Request(data_url)
                    response = urllib2.urlopen(request)
                    try:
                        img_data = response.read()
                    except URLError as e:
                        print e.reason
                    # Store the file
                    fh = open("/short/ir5/yxs659/data/" + time_stamp + '/' + item[22:-1],"w")
                    fh.write(img_data)
                    fh.close()


if __name__ == '__main__':
    # Set the longitude and latitude and the period of the data
    longitude_start = 149
    longitude_end = 149
    latitude_start = 35
    latitude_end = 36
    start_year = 2012
    start_month = 1
    end_year = 2013
    end_month = 12
    long_lat_url = 'http://dapds00.nci.org.au/thredds/fileServer/rs0/tiles/EPSG4326_1deg_0.00025pixel/LS7_ETM/dl.txt'

    # Read the long, lat list
    long_lat_list = read_long_lat(long_lat_url, longitude_start, longitude_end, latitude_start, latitude_end)
	
    # Read the data from the server
    read_data_from_server(long_lat_list, start_year, start_month, end_year, end_month)

