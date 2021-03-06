from osgeo import gdal
from osgeo import osr
import numpy as np
import pandas as pd
import netCDF4 as nc
import re
from spacetime.operations.time import cube_time, return_time
import xarray as xr


class cube(object):

    def __init__(self, inputCube, fileStruc, timeObj, names=None):

        # save as barracuda object
        self.cubeObj = inputCube
        self.fileStruc = fileStruc
        self.names = names
        self.timeObj = timeObj

        if self.fileStruc == "filestovar":
            self.ind = self.names[0]
        else:
            self.ind = "value"
            self.names = None

        if str(type(self.timeObj)) == "<class 'numpy.ndarray'>":
            self.noTime = True
        else:
            self.noTime = False

    def extract_original_data(self):
        return self.cubeObj

    def extract_units(self):
        out = self.cubeObj.variables['lon'].units
        return out

    def number_of_bands(self):
        out = self.cubeObj.variables["time"].shape[0]
        return out

    def extract_time(self):

        if self.noTime == True:
            out = self.cubeObj.variables["time"][:]

        else:
            a = self.cubeObj.variables["time"]
            a = return_time(a)
            out = pd.to_datetime(a)

        return out

    def get_raster_dimensions(self):
        y = len(self.cubeObj.variables["lat"][:])
        x = len(self.cubeObj.variables["lon"][:])
        out = [x, y]
        return out

    def get_latitude(self):
        out = self.cubeObj.variables["lat"][:]
        return out

    def get_longitude(self):
        out = self.cubeObj.variables["lon"][:]
        return out

    def upper_left_corner(self):
        y = self.get_longitude()[0]
        x = self.get_latitude()[0]
        out = [x,y]
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

    def get_names(self):
        out = self.names
        return out

    def spatial_reference(self):
        out = self.cubeObj.variables["spatial_ref"]
        return out
    def get_raster_data(self, variables=None):

        if self.fileStruc == "filestotime":
            out = self.cubeObj.variables[self.ind][:]

            outMat = xr.DataArray(data=out, dims=["lat", "lon", "time"], coords=dict(
               lon=(["lon"], self.get_longitude()),
               lat=(["lat"], self.get_latitude()),
               time=self.extract_time()))

        if self.fileStruc == "filestovar":

            outList = []
            for i in range(len(self.names)):
                outList.append(self.cubeObj.variables[self.names[i]][:])

            intDS = np.array(outList)

            out = xr.DataArray(data=intDS, dims=["variables" ,"lat", "lon", "time"], coords=dict(
                  variables = (["variables"], self.names),
                  lon=(["lon"], self.get_longitude()),
                  lat=(["lat"], self.get_latitude()),
                  time=self.extract_time()))

            # allow selecting of vars
            if variables == None:
                outMat = out
            else:
                index = [self.names.index(x) for x in variables]
                outMat = out[index,:,:,:]


        return outMat
