import urllib.request
import shutil

base_path = "http://dapds00.nci.org.au/thredds/fileServer/rs0/tiles/EPSG4326_1deg_0.00025pixel/LS8_OLI_TIRS"
base_name = "LS8_OLI_TIRS_NBAR"

coordinates = [
 "148_-035",
 "148_-036",
 "149_-035",
 "149_-036"
]
timestamps = [
 ("2013", "2013-05-27T23-58-20"),
 ("2014", "2014-01-15T23-51-15"),
 ("2014", "2014-05-30T23-55-52"),
 ("2015", "2015-01-02T23-50-08"),
 ("2015", "2015-06-02T23-55-26"),
 ("2016", "2016-01-12T23-56-21"),
 ("2016", "2016-05-19T23-55-52"),
]

def get_file(coords, year, time):
    name = base_name + '_' + coords + '_' + time + '.tif'
    url = base_path + '/' + coords + '/' + year + '/' + name
    print("Retrieving " + name + " ...", end="", flush=True)

    with urllib.request.urlopen(url) as response, open(name, 'wb') as file:
        shutil.copyfileobj(response, file)
        
    print(" Done")

if __name__ == '__main__':
    for i, coords in enumerate(coordinates):
        for j, t in enumerate(timestamps):
            year, time = t
            print(str(j + i*len(timestamps)) + "/" + str(len(timestamps)*len(coordinates)) + " ", end="", flush=True)
            get_file(coords, year, time)