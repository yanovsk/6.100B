"""
massdbfloader contains functions to load information about properies, their locations, and their values, from a massgis database downloaded from:

https://massgis.maps.arcgis.com/apps/View/index.html?appid=4d99822d17b9457bb32d7f953ca08416

Given a path to an assessors dbf file, it coverts the coordinates in the dbf file from Mass state plane coordinates to wgs84 coordinates, which is 
coordinate system most commonly used to express US lat/lon coordinates.

    Author: Sam Madden
    Data: Oct 2021


"""
from dbfread import DBF
from pyproj import Transformer,transform,Proj
from pyproj import CRS

class massdbfloader(object):

    """Create a massdbfloader for a specified dbf file -- assumes file is in the format specified here:

    """
    def __init__(self,dbf_file_path):
        self.table = DBF(dbf_file_path, load=True)
        #epsg:2094 is the code for MA state coords, epsg:4326 is wgs84 (conventional lat/lon)
        self.transformer = Transformer.from_crs("epsg:2894", "epsg:4326")

    """Filter the points to those within the specified tl/br bounding box, where both tl and br are of pairs of the
        form (lat,lon)
    """
    def get_points_in_box(self, tl, br):

        locs = []
        for t in self.table:
            l = t["LOC_ID"]
            # locations have the form F_769760_2961183
            (f,left,right) = l.split("_")

            #convert mass GIS coords to lat/lon
            (lat,lon) = self.transformer.transform(float(left),float(right))
            #print(lat,lon)

            #check if points are in bounding box
            if (lat <= tl[0] and lat >= br[0] and lon >= tl[1] and lon <= br[1]):
                locs.append((t["SITE_ADDR"], lat, lon, t["TOTAL_VAL"]))
        return locs

if __name__ == "__main__":
    dbf = massdbfloader('cambridge_2021.dbf')
    #define the region we extract from the DBF
    mit_tl = [42.393497, -71.208874]
    mit_br = [42.345307, -71.068899]
    print(dbf.get_points_in_box(mit_tl, mit_br))
