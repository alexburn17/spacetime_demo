# import matplotlib.pyplot as plt
# import glob
# from osgeo import gdal
# import numpy as np
# import pandas as pd
# import netCDF4 as nc
# import os
# import subprocess
# from on_load import load_spacetime
#
# # load spacetime
# load_spacetime()

#from spacetime import spacetime as st


# read in data set
########################################################################################################################
# a list of paths to raster files
#file1 = "/Users/pburnham/Documents/geospatialData/Carya_ovata/Carya_ovata_sim_disc_1km.tif"
#file2 = "/Users/pburnham/Documents/geospatialData/Carya_ovata/Carya_ovata_sim_disc_10km.tif"


#data = [file2, file2]

# read data from list of files and make a spaceTime file object
#ds = st.read_data(data)
# ##########################################################################
#
# # align the rasters to the same epsg codes and grid size
# newObj = raster_align(data=ds)
#
# # trim the rasters to the same greatest common bounding box
# trimmed = raster_trim(newObj)
#
# # create spacetime time object
# yearObj = cube_time(start="2000-12-31", length=101, scale = "month")
#
#
# # make the alinged file object into a cube with a time element (writes the new file to disk)
# ds = make_cube(data = trimmed, fileName = "test.nc4", organizeFiles = "filestovar", organizeBands = "bandstotime", timeObj = yearObj) #varNames=names


# sub = select_time(cube=ds, range=['2000-12-31', '2010-12-31'])
#
# test = make_cube(data = sub, fileName = "testCube.nc4")
#
# newtest = load_cube(file = "testCube.nc4")
#
# print(newtest.get_raster_data())



# #answer = cube_smasher(function=np.max, parentCube = ds, a=[ds,ds],axis=0)
# answer = cube_smasher(eq = "a * c", a = ds, c = 5, parentCube = ds)
#
# print(answer.get_raster_data())

# # scale time does basic temporal summary (here we are doing monthly means)
# x = scale_time(cube=ds, scale="month", method="mean")
#
# # selects ranges of time and/or slices at different scales
# # here we extract aprils between '2000-02-29' and '2000-04-30'
# y = select_time(cube=x, range=['2000-02-29', '2000-04-30'], scale = "month", element=4)
#
# # cube smasher does mathmatical/function operations on a cube or cubes (times 5)
# answer = cube_smasher(eq = "a * c", a = y, c = 5, parentCube = y)
#
# # plot the cube and output the data set in dataframe format that made the plot
#plot_cube(cube=ds, variable="1", type="time_series", summary = "max", showPlot = True)

# # convert a cube into a dataframe
# df = cube_to_dataframe(cube=ds)
# print(df)
#
# # write out our final cube as a .cd4 file
# #ds = make_cube(data = x, fileName = "testCube.nc4")
#
# # pull in the file name of our newly created cube
# #newCube = "/Users/pburnham/Documents/GitHub/barra_python/testCube.nc4"
#
# # load the cube object back in
# #ds = load_cube(file = newCube)




































# read in data set
########################################################################################################################
# a list of paths to raster files
# path1 = "/Users/pburnham/Documents/geospatialData/Carya_ovata/Carya_ovata_sim_disc_1km.tif"
# path2 = "/Users/pburnham/Documents/geospatialData/Carya_ovata/Carya_ovata_sim_disc_10km.tif"


#data = glob.glob('/Users/pburnham/Documents/geospatialData/kestrel/*.tif')
#data.sort(key=lambda f: int(re.sub('\D', '', f)))
#
#
# path1 = "/Users/pburnham/Documents/geospatialData/Carya_ovata/N0.tif"
# path2 = "/Users/pburnham/Documents/geospatialData/Carya_ovata/Kts.tif"
# data = [path2, path2]
#
#
# # read data from list of files and make a spaceTime file object
# ds = read_data(data)
#
#
# ########################################################################################################################
# # align the rasters to the same epsg codes and grid size
# newObj = raster_align(data=ds)
#
# print(newObj.get_raster_data()[0].shape)

# trim the rasters to the same greatest common bounding box
#trimmed = raster_trim(newObj)

# create spacetime time object
#yearObj = cube_time(start="1980", length=28, scale = "year", skips = 1)

# make the aligned file object into a cube with a time element (writes the new file to disk)
#ds = make_cube(data = trimmed, fileName = "kestrel.nc4", organizeFiles = "stack", timeObj = yearObj)

#print(ds.get_raster_data())

#newCube = "/Users/pburnham/Documents/GitHub/barra_python/kestrel.nc4"
#ds = load_cube(file = newCube)


#
# # scale time does basic temporal summary (here we are doing monthly means)
# x = scale_time(cube=ds, scale="month", method="mean")
#
# # select time selects ranges of time and/or slices at different scales (here we extract aprils between '2000-02-29' and '2000-04-30')
# y = select_time(cube=x, range=['2000-02-29', '2000-04-30'], scale = "month", element=4)
#
# # cube smasher does mathmatical/function operations on a cube or cubes (multiply all values by a scalar value, 5)
# answer = cube_smasher(eq = "a * c", a = y, c = 5, parentCube = y)
#
# # plot the cube and output the data set in dataframe format that made the plot
#t=plot_cube(cube=ds, type="space", summary = "mean", showPlot = False) # variable="B"


#
# # convert a cube into a dataframe
# df = cube_to_dataframe(cube=x)
#
# # write out our final cube as a .cd4 file
# ds = make_cube(data = x, fileName = "testCube.nc4")
#
# # pull in the file name of our newly created cube
# newCube = "/Users/pburnham/Documents/GitHub/barraz_python/testCube.nc4"
#
# # load the cube object back in
# ds = load_cube(file = newCube)


# data = ["demoData/LULC_1995.tif", "demoData/India_cropped-area_1km_2016.tif"]
#
# fo = read_data(data)
# alignedFO = raster_align(data=fo, resolution=0.08, SRS=4326, noneVal=127)
# trimmedFO = raster_trim(alignedFO, method = "intersection")
#
# yearObj = cube_time(start="1995", length=2, scale = "year", skips = 21)
# # set files as the variables and bands within each file as time variables
# cube = make_cube(data = trimmedFO, fileName = "indiaCube.nc4", organizeFiles = "filestotime", organizeBands="bandstotime", timeObj = yearObj)
#
# plot_cube(cube=cube, type="time_series", showPlot=True)



