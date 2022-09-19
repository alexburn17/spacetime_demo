import numpy as np
import netCDF4 as nc
from osgeo import gdal
from spacetime.objects.cubeMeta import cube_meta
from spacetime.objects.writeNETCDF import write_netcdf
from spacetime.objects.cubeObject import cube
from itertools import accumulate
import string

# todo: pass timeObj down to netcdf maker for if state
def make_cube(data = None, fileName = None, organizeFiles="filestotime", organizeBands="bandstotime", varNames=None, timeObj=None):

    if "file_object" in str(type(data)):

        # merge gdal datasets to one interum gdal cube
        dataList = []
        tempMat = []
        numBands = []
        time =  timeObj

        # deal with no user defined time vector with both file structures
        if type(timeObj) == type(None):

            # set up time dimension
            if organizeFiles == "filestotime" and organizeBands == "bandstotime":
                time = np.arange(len(data.extract_time()[0]) * len(data.extract_time()))
            if organizeFiles == "filestotime" and organizeBands == "bandstovar":
                time = np.arange(len(data.extract_time()))
            if organizeFiles == "filestovar" and organizeBands == "bandstotime":
                time = np.arange(len(data.extract_time()[0]))

        for i in range(len(data.extract_time())):

            tempArray = data.get_raster_data()[i]
            obj = data.extract_original_data()[i]
            bandNum = data.number_of_bands()[i]

            tempMat.append(tempArray)
            numBands.append(bandNum)

            for j in range(bandNum):
                # build vrt object
                dataList.append(gdal.BuildVRT("", obj, bandList = [j+1]))


        # split meta data cube and data by number of bands
        metaDataSplit = split_list(input = dataList, index = numBands)
        dataSplit = split_list(input = tempMat, index = numBands)

        # if files are one variable to stack
        if organizeFiles == "filestotime" and organizeBands == "bandstotime":

            outMat = np.dstack(tempMat) # stack data arrays
            fullCube = gdal.BuildVRT("", dataList, separate=True) # make a virtual cube for vrt layers
            gdalCube = cube_meta(fullCube) # make gdal cube to query data and metadata
            preCube = write_netcdf(cube=gdalCube, dataset=outMat, fileName=fileName, organizeFiles = "filestotime", organizeBands = "bandstotime", timeObj = time) # make netcdf4 cube
            cubeObj = cube(preCube, fileStruc = "filestotime", timeObj=time) # make a cube object

        if organizeFiles == "filestotime" and organizeBands == "bandstovar":

            # merge data and metadata
            metaDataMerge = merge_layers(metaDataSplit, raster=True)
            dataMerge = merge_layers(tempMat, raster=False)

            # take each vrt object and make cube meta object
            gdalCube = []
            for i in range(len(metaDataMerge)):
                gdalCube.append(cube_meta(metaDataMerge[i]))

            # if no var names given generate numbers
            if varNames == None:
                names = list(range(numBands[0]))
                varNames = list(map(str, names))

            # stack the arrays
            stacked = np.stack(dataMerge)

            # change indexes
            # Var, Lat, Lon, Time -> Time, Lat, Lon, Var
            arranged = np.moveaxis(stacked, [3,0], [0,3])

            #split into a list of arrays for each variable instead of for time
            dataOut = split_list(arranged, [1]*len(varNames), squeeze = True)

            preCube = write_netcdf(cube=gdalCube[0], dataset=dataOut, fileName=fileName, organizeFiles = "filestovar", organizeBands="bandstotime", vars=varNames, timeObj = time) # make netcdf4 cube
            cubeObj = cube(preCube, fileStruc = "filestovar", names=varNames, timeObj=time)


        # if files are each one variable
        if organizeFiles == "filestovar" and organizeBands == "bandstotime":

            # merge data and metadata
            metaDataMerge = merge_layers(metaDataSplit, raster=True)

            dataMerge = merge_layers(tempMat, raster=False)

            # take each vrt object and make cube meta object
            gdalCube = []
            for i in range(len(metaDataMerge)):
                gdalCube.append(cube_meta(metaDataMerge[i]))

            # if no var names given generate numbers
            if varNames == None:
                names = list(range(len(gdalCube)))
                varNames = list(map(str, names))


            preCube = write_netcdf(cube=gdalCube[0], dataset=dataMerge, fileName=fileName, organizeFiles = "filestovar", organizeBands="bandstotime", vars=varNames, timeObj = time) # make netcdf4 cube
            cubeObj = cube(preCube, fileStruc = "filestovar", names=varNames, timeObj=time)

    # if the object is already a cube and needs to be written back out
    else:

        time = data.extract_time()
        lat = data.get_latitude()
        lon = data.get_longitude()
        array = data.get_raster_data()
        varNames = data.get_names()

        if type(varNames) != type(None):
            preCube = write_netcdf(cube=data, dataset=array, fileName=fileName, organizeFiles = "filestovar",organizeBands="bandstotime", vars=varNames, timeObj = time) # make netcdf4 cube
            cubeObj = cube(preCube, fileStruc = "filestovar", names=varNames, timeObj=time)

        else:
            preCube = write_netcdf(cube=data, dataset=array, fileName=fileName, organizeFiles = "filestotime", organizeBands="bandstotime" ,timeObj = time) # make netcdf4 cube
            cubeObj = cube(preCube, fileStruc = "filestotime", timeObj=time)


    return cubeObj





#################################################
# helper function to split list by band numbers
def split_list(input, index, squeeze=False):

    if squeeze == False:
        out = [input[x - y: x] for x, y in zip(
            accumulate(index), index)]
    else:
        out = [np.squeeze(input[x - y: x]) for x, y in zip(
            accumulate(index), index)]



    return out
#################################################



#################################################
# helper function to merge virtual and data layers into a cube
def merge_layers(data, raster=False):

    subCubeList = []
    for i in range(len(data)): # nt len of data but time or vars?

        if raster == False:

            subCube = np.dstack(data[i]) # these indexes are reversed between the two data sets
            subCube = np.moveaxis(subCube, 2, 0)

        if raster == True:

            subCube = gdal.BuildVRT("", data[i], separate=True)

        subCubeList.append(subCube)

    return subCubeList
#################################################

