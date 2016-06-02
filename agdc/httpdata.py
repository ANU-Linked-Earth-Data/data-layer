import urllib.request
import shutil
import sys

def landsat():
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
     ("2014", "2014-01-22T23-57-25"),
     ("2014", "2014-05-30T23-55-52"),
     ("2015", "2015-01-25T23-56-14"),
     ("2015", "2015-06-02T23-55-26"),
     ("2016", "2016-01-12T23-56-21"),
     ("2016", "2016-05-19T23-55-52")
    ]

    def get_file(coords, year, time):
        name = base_name + '_' + coords + '_' + time + '.tif'
        url = base_path + '/' + coords + '/' + year + '/' + name
        print("Retrieving " + name + " ...", end="", flush=True)

        with urllib.request.urlopen(url) as response, open(name, 'wb') as file:
            shutil.copyfileobj(response, file)

        print(" Done")

    for i, coords in enumerate(coordinates):
        for j, t in enumerate(timestamps):
            year, time = t
            print(str(j + i*len(timestamps)) + "/" + str(len(timestamps)*len(coordinates)) + " ", end="", flush=True)
            get_file(coords, year, time)

def fractional_cover():
    base_path = "http://dapds00.nci.org.au/thredds/fileServer/rs0/scenes/FC25_V0.0"
    base_name = "LS8_OLI_TIRS_FC_P54_GAFC01-032"
    fraction = "PV"
    """
       PV: Green Cover Fraction. Fraction of green cover including green groundcover and green leaf material over all strata, within the Landsat pixel. Expressed as 100% = 10000.
       NPV: Non-green cover fraction. Fraction of non green cover including litter, dead leaf and branches over all strata, within the Landsat pixel. Expressed as 100% = 10000.
       BS: Bare ground fraction. Fraction of bare ground including rock, bare and disturbed soil, within the Landsat pixel. Expressed as 100% = 10000.
       UE: Unmixing Error. The residual error, defined as the Euclidean Norm of the Residual Vector. High values express less confidence in the fractional components.
    """

    month_scene_date = [
     ("2013-05", "091_084", "20130527"),
     ("2014-01", "091_084", "20140122"),
     ("2014-05", "091_084", "20140530"),
     ("2015-01", "091_084", "20150125"),
     ("2015-06", "091_084", "20150602"),
     ("2016-01", "091_084", "20160112"),
     ("2016-05", "091_084", "20160519")
    ]

    def get_file(month, scene, date):
        name = base_name + '_' + scene + '_' + date + '_' + fraction + '.tif'
        url = base_path + '/' + month + '/' + base_name + '_' + scene + '_' + date + '/' + 'scene01' + '/' + name
        print("Retrieving " + name + " ...", end="", flush=True)
        print(url)

        with urllib.request.urlopen(url) as response, open(name, 'wb') as file:
            shutil.copyfileobj(response, file)

        print(" Done")

    for i, t in enumerate(month_scene_date):
        month, scene, date = t
        print(str(i) + "/" + str(len(month_scene_date)) + " ", end="", flush=True)
        get_file(month, scene, date)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ("landsat", "fraccover"):
        if sys.argv[1] == "landsat":
            landsat()
        else:
            fractional_cover()
    else:
        print("-------------------------------------------------------------")
        print("Usage:")
        print("httpdata.py landsat")
        print("httpdata.py fraccover")
        print("-------------------------------------------------------------")