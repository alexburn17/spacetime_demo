from setuptools import setup, find_packages

setup(
    name='spacetime',
    version='0.0.2',
    packages=find_packages('src', exclude=['test']),
    license='GNU GPLv3',
    package_dir={'': 'spacetime'},
    author='P. A. Burnham et al.',
    author_email='alexburn17@gmail.com',
    install_requires=['pandas', "numpy", "gdal", "xarray", "psutil", "plotly_express", "netCDF4"],
    description='A toolkit for working with spatiotemporal data',
    scripts=[
        "spacetime/input/readData.py",
        "spacetime/scale/rasterAlign.py",
        "spacetime/scale/rasterTrim.py",
        "spacetime/objects/fileObject.py",
        "spacetime/operations/cubeSmasher.py",
        "spacetime/operations/makeCube.py",
        "spacetime/operations/loadCube.py",
        "spacetime/graphics/dataPlot.py",
        "spacetime/operations/time.py",
        "spacetime/operations/cubeToDataframe.py",
    ]
)

