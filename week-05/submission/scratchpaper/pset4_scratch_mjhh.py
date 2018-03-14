## load the libraries
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

# load my dataset



#create a function to load data and return it as a float32 array, location must be the
#full file path
def tif2array(location):
    #load the data
    data = gdal.Open(location)
    # read the raster band
    band = data.GetRasterBand(1)
    #read the band as array
    array = band.ReadAsArray()
    # convert the data type to float32
    array = array.astype(np.float32)
    return(array)

red = tif2array("/Users/meganhess-homeier/Desktop/github_data/LC08_L1TP_012031_20170614_20170628_01_T1_B4.TIF")
nir = tif2array("/Users/meganhess-homeier/Desktop/github_data/LC08_L1TP_012031_20170614_20170628_01_T1_B5.TIF")
tirs = tif2array("/Users/meganhess-homeier/Desktop/github_data/LC08_L1TP_012031_20170614_20170628_01_T1_B10.TIF")

## Create a function to retrieve variables from landsat metadata, return a list of
## length 4, 'meta_text' is the location of the metadata file

def process_string (st):
    return float(st.split(' = ')[1].strip('\n'))

def retrieve_meta(meta_text):
    with open(meta_text) as f:
        meta = f.readlines()
    matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']
    matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]
    return(matching)

file = '/Users/meganhess-homeier/Desktop/github_data/LC08_L1TP_012031_20170614_20170628_01_T1_MTL.txt'
meta_list = retrieve_meta(file)
print(meta_list)

    # """
    # Calculate Top of Atmosphere Spectral Radiance
    # Note that you'll have to access the metadata variables by
    # their index number in the list, instead of naming them like we did in class.
    # """

def rad_calc(tirs, meta_list):
    rad = meta_list[0] * tirs + meta_list[1]
    plt.imshow(rad, cmap='RdYlGn')
    plt.colorbar()
    return(rad)

Rad = rad_calc(tirs, meta_list)

    # """
    # Calculate Brightness Temperature
    # Again, you'll have to access appropriate metadata variables
    # by their index number.
    #

def bt_calc(rad, meta_list):
    bt = meta_list[3] / np.log((meta_list[2]/rad) + 1) - 273.15
    plt.imshow(bt, cmap='RdYlGn')
    plt.colorbar()
    return(bt)
bt = bt_calc(Rad, meta_list)

    # """
    # Calculate Proportional Vegetation
    # """ Calculate NDVI"""
    # We're going to make a bunch of assumptions here - that NDVI < 0.2 implies unvegetated
    # terrain, that 0.2 < NDVI < 0.5 implies a mixture of vegetation and unvegetated terrain,
    # and that NDVI > 0.5 implies nearly fully vegetated land. This is a simplifying assumption
    # that probably wouldn't hold up to rigorous testing, but it's fine for our purposes.
    # NDVI_s = .2
    # ndvi_v = .5
    # """
# def pv_calc(ndvi, ndvi_s, ndvi_v):
#     #ndvi = (nir - red) / (nir + red)
#     pv = (ndvi - 0.2) / (0.5 - 0.2) ** 2
#     plt.imshow(pv, cmap='RdYlGn')
#     plt.colorbar()
def ndvi_calc(red, nir):
    return (nir - red) / (nir + red)

ndvi = ndvi_calc(red, nir)
def pv_calc(ndvi, ndvi_s, ndvi_v):
    pv = (ndvi - ndvi_s) / (ndvi_v - ndvi_s)
    plt.imshow(pv, cmap = 'RdYlGn')
    plt.colorbar()
    return(pv)

prop_veg = pv_calc(ndvi, .2, .5)

def emissivity_calc (pv, ndvi):
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest

emis = emissivity_calc(prop_veg, ndvi)

plt.imshow(emis, cmap='RdYlGn')
plt.colorbar()






    # """
    # Calculate Estimate of Land Surface Temperature.
    # Your output should
    # ---
    # Note that this should take as its input ONLY the location
    # of a directory in your file system. That means it will have
    # to call your other functions. It should:
    # 1. Define necessary constants
    # 2. Read in appropriate tifs (using tif2array)
    # 3. Retrieve needed variables from metadata (retrieve_meta)
    # 4. Calculate ndvi, rad, bt, pv, emis using appropriate functions
    # 5. Calculate land surface temperature and return it.
    # Your LST function may return strips of low-values around the raster...
    # This is a processing artifact that you're not expected to account for.
    # Nothing to worry about!
    # """
# what i need for LST:
# constants
# emissivity
    #NDVI
        # nir
        # red
    #PV
        #NDVI
        #ndvi_s = .2
        #ndvi_v = .5
# brightness temp
    #metatdata
    #metadata [2] (k1)
    # metadata [3] (k2)
    # rad calc
        # metadata [0] rad mult
        # metadata [1] rad add
#bt = k2_b10 / np.log((k1_b10/rad) + 1) - 273.15
#plt.imshow(bt, cmap='RdYlGn')
#plt.colorbar()

def lst_calc(location):
    #Define my constants
    wave = 10.8E-06
    # PLANCK'S CONSTANT
    h = 6.626e-34
    # SPEED OF LIGHT
    c = 2.998e8
    # BOLTZMANN's CONSTANT
    s = 1.38e-23
    p = h * c / s
    ndvi_s = .2
    ndvi_v = .5
    #Create my file paths
    red_path = os.path.join(location, 'LC08_L1TP_012031_20170614_20170628_01_T1_B4.TIF')
    nir_path = os.path.join(location, 'LC08_L1TP_012031_20170614_20170628_01_T1_B5.TIF')
    tir_path = os.path.join(location, 'LC08_L1TP_012031_20170614_20170628_01_T1_B10.TIF')
    meta_path = os.path.join(location, 'LC08_L1TP_012031_20170614_20170628_01_T1_MTL.txt')
    #call and organize my data using the file paths
    tirs = tif2array(tir_path)
    red = tif2array(red_path)
    nir = tif2array(nir_path)
    meta_list = retrieve_meta(meta_path)
    #Start calling my Functions
    Rad = rad_calc(tirs, meta_list)
    bt = bt_calc(Rad, meta_list)
    ndvi = ndvi_calc(red, nir)
    pv = pv_calc(ndvi, ndvi_s, ndvi_v)
    emis = emissivity_calc(pv, ndvi)
    #calculate LST
    lst = bt / (1 + (wave * bt / p) * np.log(emis))
    #plot it!
    plt.imshow(lst, cmap='RdYlGn')
    plt.colorbar()
    return(lst)


lst = lst_calc('/Users/meganhess-homeier/Desktop/github_data/')


## remove cloud coover

bqa = tif2array('/Users/meganhess-homeier/Desktop/github_data/LC08_L1TP_012031_20170614_20170628_01_T1_BQA.TIF')

def cloud_filter(array, bqa):
    array_dest = array.copy()
    array_dest[np.where((bqa != 2732) & (bqa != 2720) & (bqa != 2724) & (bqa != 2728)) ] = 'nan'
    return array_dest

## filter lst array and ndvi arrays

lst_filter = cloud_filter(lst, bqa)
ndvi_filter = cloud_filter(ndvi, bqa)

# output tifs of filtered lst array and filtered ndvi array
#define folder location
DATA = '/Users/meganhess-homeier/Desktop/github_data/'
#define array2tif using class function
def array2tif(raster_file, new_raster_file, array):
    # Invoke the GDAL Geotiff driver
    raster = gdal.Open(raster_file)

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(new_raster_file,
                        raster.RasterXSize,
                        raster.RasterYSize,
                        1,
                        gdal.GDT_Float32)
    out_raster.SetProjection(raster.GetProjection())
    # Set transformation - same logic as above.
    out_raster.SetGeoTransform(raster.GetGeoTransform())
    # Set up a new band.
    out_band = out_raster.GetRasterBand(1)
    # Set NoData Value
    out_band.SetNoDataValue(-1)
    # Write our Numpy array to the new band!
    out_band.WriteArray(array)

#output lst tif
tirs_path = os.path.join(DATA, 'LC08_L1TP_012031_20170614_20170628_01_T1_B10.TIF')
out_path = os.path.join(DATA, 'h-h_lst_20170614.tif')
array2tif(tirs_path, out_path, lst_filter)

#output ndvi tif
tirs_path = os.path.join(DATA, 'LC08_L1TP_012031_20170614_20170628_01_T1_B10.TIF')
out_path = os.path.join(DATA, 'h-h_ndvi_20170614.tif')
array2tif(tirs_path, out_path, ndvi_filter)
