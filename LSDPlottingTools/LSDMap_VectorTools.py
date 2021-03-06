## LSDMap_VectorTools.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## These functions are tools to deal with vector data using shapely
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## FJC
## 26/06/17
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from . import LSDMap_GDALIO as LSDMap_IO
from shapely.geometry import Point, Polygon

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# BASIN FUNCTIONS
# These functions do various operations on basin polygons
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
def GetBasinOutlines(DataDirectory, basins_fname):
    """
    This function takes in the raster of basins and gets a dict of basin polygons,
    where the key is the basin key and the value is a shapely polygon of the basin.

    IMPORTANT: In this case the "basin key" is usually the junction number:
        this function will use the raster values as keys and in general
        the basin rasters are output based on junction indices rather than keys

    Args:
        DataDirectory (str): the data directory with the basin raster
        basins_fname (str): the basin raster

    Returns:
        list of shapely polygons with the basins

    Author: FJC
    """
    # read in the basins raster
    this_fname = basins_fname.split('.')
    print(basins_fname)
    print(this_fname[0])
    OutputShapefile = this_fname[0]+'.shp'

    # polygonise the raster
    BasinDict = LSDMap_IO.PolygoniseRaster(DataDirectory, basins_fname, OutputShapefile)
    return BasinDict

def GetBasinCentroids(DataDirectory, basins_fname):
    """
    This function takes in the raster of basins and returns a dict where the
    key is the basin key and the value is the shapely point of the centroid

    In most cases the "basin key" is actually the junction index: it comes
    from the basins labeled within the basin raster, which is output with
    junction indices rather than junction keys

    Args:
        DataDirectory (str): the data directory with the basin raster
        fname_prefix (str): the prefix for the DEM

    Returns:
        dict of centroid points

    Author: FJC
    """
    # get the basin polygons
    BasinDict = GetBasinOutlines(DataDirectory, basins_fname)

    # get the centroids
    CentroidDict = {}
    for basin_key, basin in BasinDict.iteritems():
        CentroidDict[basin_key] = Point(basin.centroid)

    return CentroidDict

def GetPointWithinBasins(DataDirectory,basins_fname):
    """
    This function takes in the raster of basin and returns a dict where the
    key is the basin key and the value is a shapely point that is representative
    of the basin (guaranteed to be within the polygon)

    In most cases the "basin key" is actually the junction index: it comes
    from the basins labeled within the basin raster, which is output with
    junction indices rather than junction keys

    Args:
        DataDirectory (str): the data directory with the basin raster
        fname_prefix (str): the prefix for the DEM

    Returns:
        dict of representative points

    Author: FJC
    """
    # get the basin polygons
    BasinDict = GetBasinOutlines(DataDirectory, basins_fname)

    # get the centroids
    PointDict = {}
    for basin_key, basin in BasinDict.iteritems():
        PointDict[basin_key] = Point(basin.representative_point())

    return PointDict

def GetPointWithinBasinsBuffered(DataDirectory,basins_fname, basin_list = [], buffer_frac=0.1):
    """
    This function takes in the raster of basins, and buffers each basin
    (makes each one smaller). It then gets the centroid of each buffered
    basin and returns as a dict where the key is the basin key and the value
    is a shapely point that is the centroid of the buffered basin.

    In most cases the "basin key" is actually the junction index: it comes
    from the basins labeled within the basin raster, which is output with
    junction indices rather than junction keys

    This doesn't work at the moment - need to think of a way to specify the buffer
    distance appropriately.

    Args:
        DataDirectory (str): the data directory with the basin raster
        fname_prefix (str): the prefix for the DEM
        buffer_frac (float): the fraction of the basin to be removed by the
        buffer, default = 0.1

    Returns:
        dict of representative points

    Author: FJC
    """
    # get the basin polygons
    BasinDict = GetBasinOutlines(DataDirectory, basins_fname)

    # buffer and get the centre of the buffered polygons
    PointDict = {}
    for basin_key, basin in BasinDict.iteritems():
        # get the x and y lengths of the basin and append to list
        print("This basin key is: "+str(basin_key))
        lengths = []
        bounds = basin.bounds
        lengths.append(bounds[2] - bounds[0])
        lengths.append(bounds[3] - bounds[1])
        print(min(lengths))

        # buffer with a fraction of the minimum length
        new_basin = Polygon(basin.buffer(min(lengths)*buffer_frac*-1))

        # get the centroid of the buffered basin
        PointDict[basin_key] = Point(new_basin.centroid)

    return PointDict
