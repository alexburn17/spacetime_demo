

def load_spacetime():

    from spacetime.input.readData import read_data
    from spacetime.scale.rasterAlign import raster_align
    from spacetime.scale.rasterTrim import raster_trim
    from spacetime.objects.fileObject import file_object
    from spacetime.operations.cubeSmasher import cube_smasher
    from spacetime.operations.makeCube import make_cube
    from spacetime.operations.loadCube import load_cube
    from spacetime.graphics.dataPlot import plot_cube
    from spacetime.operations.time import cube_time, return_time, scale_time, select_time
    from spacetime.operations.cubeToDataframe import cube_to_dataframe
    from datetime import datetime, timedelta

    return(print("The spacetime library has been attached. All functions in the spacetime API are now available in your environment."))