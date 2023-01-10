"""
maptileloader loads map tiles and elevation data from mapbox that cover a specific geographic region.

It then provides methods to:
    get a composite image representing the map data in the specified region (get_satellite_image)
    get the elevation data as a np array with the same dimension at the map image (get_elevation_array)
    get an image of the elevation data with the same dimension as the map image (get_elevation_image)

Because loading map tiles can be very slow, this class automatically caches downlodaed map tiles in a local directory, so 
that tiles don't need to be repeatedly reloaded.

Portions of this code were adapted from:

https://www.kaggle.com/kapastor/flood-map-with-mapbox-and-python
KYLE PASTOR

    Author: Sam Madden
    Data: Oct 2021


"""

import mercantile
import requests
import shutil
import PIL, PIL.Image
import math
from os import listdir, mkdir
from os.path import isfile, join, exists
import json
import numpy as np

class maptileloader(object):
    """mapbox token, hardcoded to Prof Madden's map box account"""
    token = "sk.eyJ1Ijoic21hZGRlbiIsImEiOiJja3Y2b3lnaXcyMGl5MzJtczh6NmFsamo1In0.3C_erpoGd8dMlspfZ_ZOvg"

    """Construct a maptileloader, with the specified tl/br bounding box and zoom factor
    Both tl and br are (lat,lon) pairs and z is a map box zoom factor specifying the level of detail for the
    requesteed maps.
    """
    def __init__(self,tl, br, z):
        self.tl = tl
        self.br = br
        self.z = z

        self.tl_tiles = mercantile.tile(tl[1],tl[0],z)
        self.br_tiles = mercantile.tile(br[1],br[0],z)
        self.directory_prefix = f"tiles.{tl[0]}.{tl[1]}.{br[0]}.{br[1]}.{z}"
        try:
            mkdir(self.directory_prefix)
            mkdir(join(self.directory_prefix,"elevation_images"))
            mkdir(join(self.directory_prefix,"satellite_images"))
            mkdir(join(self.directory_prefix,"composite_images"))
        except FileExistsError:
            pass

    """Returns a pair of (tl,br) of the composite image downloaded from mapbox.  This may differ from the
     (tl,br) region passed to the constructor if the map tiles on mapbox don't exactly align with (tl,br) region
     passed to the constructor.
    """
    def get_tile_extents(self):
        ul = mercantile.ul(self.tl_tiles.x,self.tl_tiles.y, self.z)
        br = mercantile.ul(self.br_tiles.x,self.br_tiles.y, self.z)
        return (ul,br)

    """Fetch the map tiles and cache the images and elevation data.  Caches images and elevation data into a directory
        named for the (tl,br) region passed to the constructor;  it is not necessary to call this method again if it has
        previous been run.  Methods below will fail if this has not been previously called.
    """
    def download_tiles(self):
        x_tile_range = [self.tl_tiles.x,self.br_tiles.x]
        y_tile_range = [self.tl_tiles.y,self.br_tiles.y]

        for i,x in enumerate(range(x_tile_range[0],x_tile_range[1]+1)):
            for j,y in enumerate(range(y_tile_range[0],y_tile_range[1]+1)):
                print(x,y)
                r = requests.get(f'https://api.mapbox.com/v4/mapbox.terrain-rgb/{self.z}/{x}/{y}@2x.pngraw?access_token={self.token}', stream=True)
                if r.status_code == 200:
                    with open(join(self.directory_prefix,"elevation_images",str(i) + '.' + str(j) + '.png'), 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)  
                
                #switch urls below to switch from satellite imagery to road maps
                #r = requests.get(f'https://api.mapbox.com/v4/mapbox.satellite/{self.z}/{x}/{y}@2x.png?access_token={self.token}', stream=True)
                url=f'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{self.z}/{x}/{y}@2x.png?access_token={self.token}'
                print(url)
                r = requests.get(f'https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/{self.z}/{x}/{y}?access_token={self.token}', stream=True)
                if r.status_code == 200:
                    with open(join(self.directory_prefix,"satellite_images",str(i) + '.' + str(j) + '.png'), 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                else:
                    print("FAILED TO DOWNLOAD")



        print("compositing")

        for img_name in ['elevation','satellite']:
            image_files = []
            for f in listdir(join(self.directory_prefix,img_name+'_images')):
                image_files.append(join(self.directory_prefix,img_name+'_images',f))
            images = [PIL.Image.open(x) for x in image_files]

            edge_length_x = x_tile_range[1] - x_tile_range[0]
            edge_length_y = y_tile_range[1] - y_tile_range[0]
            edge_length_x = max(1,edge_length_x)
            edge_length_y = max(1,edge_length_y)
            width, height = images[0].size

            total_width = width*edge_length_x
            total_height = height*edge_length_y

            composite = PIL.Image.new('RGB', (total_width, total_height))

            anim_idx = 0
            y_offset = 0
            for i in range(0,edge_length_x):
                x_offset = 0
                for j in range(0,edge_length_y):
                    tmp_img = PIL.Image.open(join(self.directory_prefix,img_name+'_images',str(i) + '.' + str(j) + '.png'))
                    composite.paste(tmp_img, (y_offset,x_offset))
                    x_offset += width

                    
                y_offset += height

            composite.save(join(self.directory_prefix,"composite_images",img_name+'.png'))

        elevation_raw = PIL.Image.open(join(self.directory_prefix,"composite_images","elevation.png"))
        rgb_elevation = elevation_raw.convert('RGBA')

        print("extracting depth to elevation.json")
        # Loop over the image and save the data in a list:
        elevation_data = []
        # texture_data = []
        for h in range(rgb_elevation.height):
            elev_row = []
            for w in range(rgb_elevation.width):
                R, G, B, A = rgb_elevation.getpixel((w, h))
                height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
                elev_row.append(height)
            elevation_data.append(elev_row)
        with open(join(self.directory_prefix,'elevation.json'), 'w') as outfile:
            json.dump(elevation_data, outfile)

    """Returns the satellite image for the region passed to the constructor.  If download_tiles has not been
    called for this region, throws FileNotFoundError
    """
    def get_satellite_image(self):
        p = join(self.directory_prefix,"composite_images","satellite.png")
        if (not exists(p)):
            raise FileNotFoundError("satellite.png does not exist, try calling download_tiles first")
        return PIL.Image.open(p).convert('RGBA')

    """Returns the elevation image for the region passed to the constructor.  If download_tiles has not been
    called for this region, throws FileNotFoundError
    """
    def get_elevation_image(self):
        p = join(self.directory_prefix,"composite_images","elevation.png")
        if (not exists(p)):
            raise FileNotFoundError("elevation.png does not exist, try calling download_tiles first")
        return PIL.Image.open(p).convert('RGBA')

    """Returns the elevation data as a numpy array for the region passed to the constructor.  If download_tiles has not been
    called for this region, throws FileNotFoundError
    """
    def get_elevation_array(self):
        p = join(self.directory_prefix,"elevation.json")
        if (not exists(p)):
            raise FileNotFoundError("elevation.json does not exist, try calling download_tiles first")
        with open(p) as f:
            elevation_data = json.load(f)
            return np.array([np.array(xi) for xi in elevation_data])


if __name__ == "__main__":
    tl = (42.3586798 +.04, - 71.1000466 - .065)
    br = (42.3586798 -.02, - 71.1000466 + .065)
    m = maptileloader(tl,br,14)
    im = m.get_satellite_image()
    im.show()
    im = m.get_elevation_image()
    im.show()
    e = m.get_elevation_array()
    print(e)
