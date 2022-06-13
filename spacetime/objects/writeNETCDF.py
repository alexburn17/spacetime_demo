import numpy as np
import netCDF4 as nc

def write_netcdf(cube, dataset, fileName, organizeFiles, organizeBands, vars=None, timeObj=None):

    ds = nc.Dataset(fileName, 'w', format='NETCDF4')

    # inmtialize vars by creating dimensions
    time = ds.createDimension('time', len(timeObj)) # no time var in this case
    lat = ds.createDimension('lat', cube.get_raster_dimensions()[1])
    lon = ds.createDimension('lon', cube.get_raster_dimensions()[0])

    # create variables in the data set
    time = ds.createVariable('time', 'float64', ('time',))
    lats = ds.createVariable('lat', 'f4', ('lat',))
    lons = ds.createVariable('lon', 'f4', ('lon',))


    #value.units = 'My Units'
    lons.units = cube.extract_units()
    lats.units = cube.extract_units()


    ds.variables['lat'][:] = cube.get_latitude()
    ds.variables['lon'][:] = cube.get_longitude()
    crs = ds.createVariable('spatial_ref', 'i4')
    crs.spatial_ref = cube.spatial_reference()

    # each file is a variable
    ############################################################################################
    if organizeFiles == "filestovar" or organizeBands=="bandstovar":

        for i in range(len(vars)):

            value = ds.createVariable(vars[i], 'f4', ('lat', 'lon', 'time',))
            value.code =  cube.extract_epsg_code()

            if cube.get_nodata_value() != None:
                value.missing = cube.get_nodata_value()
            else:
                value.missing = -9999

            # is it a list of arrays or a dictionary (XARRAY)
            if "<class 'dict'>" in str(type(dataset)):
                ds.variables[vars[i]][:] = dataset[vars[i]]
            else:
                ds.variables[vars[i]][:] = dataset[i]


        if str(type(timeObj)) == "<class 'numpy.ndarray'>":

            ds.variables['time'][:] = timeObj

        else:

            time.units = "seconds since " + str(timeObj.to_numpy()[0])
            timeObj = timeObj.to_numpy()

            timedelta = timeObj-timeObj[0]
            seconds = timedelta.astype('timedelta64[s]').astype(np.int32)
            ds.variables['time'][:] = seconds

    ############################################################################################


    # all files are times and must be stacked into one 3d cube
    ############################################################################################
    if organizeFiles == "filestotime" and organizeBands!="bandstovar":

        value = ds.createVariable('value', 'f4', ('lat', 'lon', 'time',))
        value.code =  cube.extract_epsg_code()
        if cube.get_nodata_value() != None:
            value.missing = cube.get_nodata_value()
        else:
            value.missing = -9999

        # create the main variables
        ds.variables['value'][:] = dataset

        if str(type(timeObj)) == "<class 'numpy.ndarray'>":
            ds.variables['time'][:] = timeObj
        else:
            time.units = "seconds since " + str(timeObj.to_numpy()[0])
            timeObj = timeObj.to_numpy()

            timedelta = timeObj-timeObj[0]
            seconds = timedelta.astype('timedelta64[s]').astype(np.int32)
            ds.variables['time'][:] = seconds
    ############################################################################################

    return ds

    ds.close()





