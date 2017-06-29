# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:47:22 2017

An example of using the cython version of the hillshade
algorithm from LSDTopoTools/LSDRaster, compared to the pure python
module in LSDMappingTools.

(This test version dos on-the-fly-compilation to C and then a C-lib
but you could bundle a compiled c-object with the code for speed/convenience)

@author: dav
"""

import matplotlib.pyplot as plt

# For on the fly compilation - remove if you are pre-compiling the Cython-library
# This MUST come before you import the C hillshade pyx file if you are doing it
# this way.
####################
import pyximport
pyximport.install()
####################

from LSDPlottingTools import fast_hillshade as fasthill

import LSDPlottingTools.LSDMap_GDALIO as LSDMap_IO
import LSDPlottingTools.LSDMap_BasicPlotting as LSDMap_BP

#Directory = "/mnt/SCRATCH/Analyses/HydrogeomorphPaper/rainfall_maps/"
Directory = "/mnt/SCRATCH/Dev/ExampleTopoDatasets/"
BackgroundRasterName = "SanBern.bil"

raster = LSDMap_IO.ReadRasterArrayBlocks(Directory + BackgroundRasterName)

Cellsize = LSDMap_IO.GetGeoInfo(Directory + BackgroundRasterName)[3][1]
NoDataValue = LSDMap_IO.getNoDataValue(Directory + BackgroundRasterName)
print(Cellsize)

# This could be tidied up (not hard coded data res)
ncols, nrows = raster.shape
data_res = Cellsize

# LSDMappingTools hillshade
hs = LSDMap_BP.Hillshade(raster)

plt.imshow(hs, cmap="gray")
plt.show()

#LSDRaster Cythonised version pf hillshade
hs_nice = fasthill.Hillshade(raster, data_res, NoDataValue=NoDataValue)
plt.imshow(hs_nice, cmap="gray")
plt.show()
