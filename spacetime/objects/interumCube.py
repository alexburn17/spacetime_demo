import numpy as np
import netCDF4 as nc
import pandas as pd


class interum_cube(object):

    def __init__(self, cube = None, array = None, structure = None):

        # save as barracuda object
        self.cubeObj = cube.extract_original_data()
        self.array = array
        self.structure = structure

        if self.structure == True:
            self.names = np.array(array.variables)
            self.ind = self.names[0]
        if self.structure == False:
            self.ind = "value"
            self.names = None

    def extract_original_data(self):
        #print("WARNING! Original dataset is no longer of the same dimensions as your working cube. Please write your cube out using the write_cube() to store a .cd4 file of the correct dimensions!")
        out = self.cubeObj
        return out

    def extract_units(self):
        out = self.cubeObj.variables['lon'].units
        return out

    def number_of_bands(self):
        out = len(self.extract_time())
        return out

    def extract_time(self):

        a = self.array.time
        out = pd.to_datetime(a)
        return out

    def get_raster_dimensions(self):
        y = len(self.get_latitude())
        x = len(self.get_longitude())
        out = [x, y]
        return out

    def get_latitude(self):

        out = self.array.lat
        return out

    def get_longitude(self):

        out = self.array.lon
        return out

    def upper_left_corner(self):
        y = self.get_longitude()[0]
        x = self.get_latitude()[0]
        out = [x,y]
        return out
    def spatial_reference(self):
        out = self.cubeObj.variables["spatial_ref"]
        return out
    def pixel_size(self):
        long = self.get_longitude()
        pixel_size = abs(long[0]-long[1])
        return pixel_size

    def get_nodata_value(self):
        out = self.cubeObj.variables[self.ind].missing
        return out

    def extract_epsg_code(self):
        out = self.cubeObj.variables[self.ind].code
        return out

    def get_raster_data(self, variables=None):
        out = self.array
        return out

    def get_names(self):
        out = self.names
        return out
