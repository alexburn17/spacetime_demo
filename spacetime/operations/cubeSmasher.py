import numpy as np
import netCDF4 as nc
from spacetime.objects.interumCube import interum_cube

def cube_smasher(function = None, eq = None, parentCube = None, **kwarg):

    # is there a parent cube and what is the file structure?
    if parentCube != None:
        if type(parentCube.get_names()) == type(None):
            filestovar = False
        else:
            filestovar = True


    # loop through input dict to extract raster data for operations
    for key in kwarg:
        if "list" in str(type(kwarg[key])):
            for i in range(len(kwarg[key])):
                if "cube" in str(type(kwarg[key][i])):
                    kwarg[key][i] = kwarg[key][i].get_raster_data()
        else:
            if "cube" in str(type(kwarg[key])):
                kwarg[key] = kwarg[key].get_raster_data()
    # do operations as below
    if function == None:

        y = eval(eq, kwarg)

    if eq == None:

        y = function(**kwarg)

    if parentCube == None:
        out = y
    else:
        out = interum_cube(cube = parentCube, array = y, structure = filestovar)

    return out








