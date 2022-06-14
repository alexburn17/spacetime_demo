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

        for i in range(len(data.extract_original_data())):

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

            outMat = np.dstack(dataSplit[0]) # stack data arrays
            fullCube = gdal.BuildVRT("", dataList, separate=True) # make a virtual cube for vrt layers
            gdalCube = cube_meta(fullCube) # make gdal cube to query data and metadata
            preCube = write_netcdf(cube=gdalCube, dataset=outMat, fileName=fileName, organizeFiles = "filestotime", organizeBands = "bandstotime", timeObj = time) # make netcdf4 cube
            cubeObj = cube(preCube, fileStruc = "filestotime", timeObj=time) # make a cube object

        # if files are multi variable to stack
        if organizeFiles == "filestotime" and organizeBands == "bandstovar":

            outMat = np.dstack(dataSplit[0]) # stack data arrays
            numBands = int(outMat.shape[2]/len(time))

            # if no var names given generate letters A-Z
            if varNames == None:
                varNames = list(string.ascii_uppercase[0:numBands])

            # create sub cubes for vrrt and array for each band variable
            arrayCube = []
            gdalCube = []
            for i in range(numBands):
                arrayCube.append(outMat[:, :, 0::numBands])
                gdalCube.append(dataList[0::numBands])

            metaDataMerge = merge_layers(gdalCube, raster=True)
            dataMerge = merge_layers(arrayCube, raster=False)

            metaCube = []
            for i in range(len(metaDataMerge)):
                metaCube.append(cube_meta(metaDataMerge[i]))

            preCube = write_netcdf(cube=metaCube[0], dataset=dataMerge, fileName=fileName, organizeFiles = "filestotime", organizeBands="bandstovar", vars=varNames, timeObj = time) # make netcdf4 cube
            cubeObj = cube(preCube, fileStruc = "filestovar", names=varNames, timeObj=time)

        # if files are each one variable
        if organizeFiles == "filestovar" and organizeBands == "bandstotime":

            # merge data and metadata
            metaDataMerge = merge_layers(metaDataSplit, raster=True)
            dataMerge = merge_layers(dataSplit, raster=False)

            # take each vrt object and make cube meta object
            gdalCube = []
            for i in range(len(metaDataMerge)):
                gdalCube.append(cube_meta(metaDataMerge[i]))

            # if no var names given generate letters A-Z
            if varNames == None:
                varNames = list(string.ascii_uppercase[0:len(gdalCube)])

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
def split_list(input, index):

    # split lists
    out = [input[x - y: x] for x, y in zip(
        accumulate(index), index)]

    return out
#################################################



#################################################
# helper function to merge virtual and data layers into a cube
def merge_layers(data, raster=False):

    subCubeList = []
    for i in range(len(data)):

        if raster == False:

            subCube = np.dstack(data[0][i])
            subCube = np.moveaxis(subCube, 2, 0)

        if raster == True:

            subCube = gdal.BuildVRT("", data[i], separate=True)

        subCubeList.append(subCube)

    return subCubeList
#################################################
