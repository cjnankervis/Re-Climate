import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
'''4.2 Load correct visual packages'''
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
import pyproj
'''5.0 Interpolate the grid'''
# from matplotlib.mlab import griddata as griddata_mpl
from scipy.interpolate import griddata as griddata_scipy
'''Note that Basemap version > 1.1 do not work!'''
# from mpl_toolkits.basemap import Basemap, maskoceans # conda install basemap==1.0.7
import scipy.stats as st # To calculate percentile of temperature

forecasts = ['','weatherlogisticsltd']
dist = 'Gaussian' # 'Gaussian' or 'Log-Logistic' (Caution: case sensitive)
skip_extraplots = True

use_customcolors = True; ukmo_precip = True; ed_hawkins = False; RichHildebrand = False
scale = np.array([0.85,0.85,0.85])
'''Set the analysis date'''
grib_file = True; netcdf_file = False
'''Specify the forecast month and at what lead time'''
year = '2024'; month = 'October'; month_no = 10; lead = 1 # Specify the forecast month and at what lead time
'''Define end of 31-year climate (reference) period'''
climate_end = 2020 # Define end of 31-year climate time series

month_names = ('January','February','March','April',
               'May','June','July','August',
               'September','October','November','December')

if use_customcolors:
    from matplotlib.colors import LinearSegmentedColormap # To define own colour scale
    if (ed_hawkins or ukmo_precip):
        if ed_hawkins:
            custom_colors = reversed(['#08306b', '#08519c', '#2171b5', '#4292c6',
                           '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
                           '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
                           '#ef3b2c', '#cb181d', '#a50f15', '#67000d'])
        if ukmo_precip:
            custom_colors = (np.array([0.2078, 0.0, 0.0039])*scale,
                            np.array([0.0471, 0.1961, 0.4118])*scale,
                            np.array([0.2314, 0.3961, 0.6118])*scale,
                            np.array([0.4275, 0.5961, 0.8118])*scale,
                            np.array([1.0, 1.0, 1.0]),
                            np.array([0.9843, 0.85, 0.8039])*scale,
                            np.array([0.9725, 0.6039, 0.35])*scale,
                            np.array([0.7647, 0.3118, 0.20])*scale,
                            np.array([0.5725, 0.1014, 0.05])*scale)
        # Create a list of normalized RGB values for your custom colors
        custom_colors_rgb = [plt.cm.colors.to_rgb(c) for c in custom_colors]
    elif RichHildebrand:
        def create_color(r, g, b):
            return [r/256, g/256, b/256]
        custom_colors_rgb = reversed([create_color(227, 101, 33), create_color(246, 145, 53), create_color(251, 168, 74),
            create_color(218, 212, 200), create_color(141, 193, 223), create_color(114, 167, 208), 
            create_color(43, 92, 138)])
    # custom_colors = reversed(['#350001', '#0c3269', '#3b659c', '#6d98cf', '#ffffff', '#fbcccd', '#f89a9b', '#f66935', '#92080d'])
    # Define a custom colormap using `matplotlib.colors.LinearSegmentedColormap`
    colors = LinearSegmentedColormap.from_list('', custom_colors_rgb)
else:
    colors = cm.terrain

def mthdays(yyyy, mth):
    '''Assess number of days in each month'''
    yyyy = float(yyyy)
    # Feb = 29 if not yyyy % 4 else 28
    Feb = 28.25
    Jan = 31; Mar = 31; Apr = 30; May = 31; Jun = 30; Jul = 31; \
    Aug = 31; Sep = 30; Oct = 31; Nov = 30; Dec = 31
    mth_days = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
    
    mth_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', \
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    mth_ind = mth_labels.index(mth)
    '''Day of year from 1st January'''
    dayofyear = int(np.sum(mth_days[0:mth_ind]))
    '''Number of days in user specified month'''
    mth_days = int(mth_days[mth_ind])

    return mth_days, dayofyear

# Load forecast into workspace
days_in_month = mthdays(year, month[0:3])[0]
start_month = ((((month_no-1)-lead) % 12) + 1)
start_year = str(int(year) - 1) if start_month > month_no else year
FCST_path = 'raw_data'

datapath_meds = []
for forecast in forecasts:
    filename_hires = f'/ReClimate_{format("%02d" % start_month)}_{start_year}_{str(lead)}_Temperature-Actuals{forecast}.asc'
    datapath_meds.append(FCST_path + filename_hires)

if grib_file:
    import cfgrib
    import xarray as xr
    grib_data = cfgrib.open_datasets(f'./ERA5/ERA5-Land-{month[0:3]}{climate_end}_Prev30Yrs-Temperature.grib')
    grib_data = grib_data[0]['t2m']
    grib_data -= 273.15 # Convert from Kelvin to Degrees Celsius
    lon = grib_data['longitude']
    lat = grib_data['latitude']
    time = grib_data['time']

# Read / define forecast output variables
for datapath_med in datapath_meds:
    file = open(datapath_med, mode='r')
    # Read metadata line-by-line
    h1, h2 = file.readline(), file.readline()     # NCOLS 175    # NROWS 249
    h3, h4 = file.readline(), file.readline()     # XLLCENTER -225160.85671291745  # YLLCENTER 29788.11622501802
    h5 = file.readline()                          # CELLSIZE 5000.0
    h6 = file.readline()                          # NODATA_VALUE -9999
    # define META data for geolocation and grid info
    ddcols, ddrows = h1.strip().split(), h2.strip().split()
    ncols, nrows = float(ddcols[1]), float(ddrows[1])
    xcntr, ycntr = -225160.85671291745, 29788.11622501802
    cellsize     = h5.strip().split() 
    blank        = h6.strip().split()
    
    df = pd.read_csv(datapath_med, header=6, delimiter=' ')
    aa = (list(df.keys()))
    if datapath_med == datapath_meds[0]:
        raw_data = pd.read_csv(datapath_med, header=6, delimiter=' ').values
        npa = np.asarray(aa, dtype=np.float32)
    else:
        raw_data += pd.read_csv(datapath_med, header=6, delimiter=' ').values
        npa += np.asarray(aa, dtype=np.float32)
    #
raw_data /= len(datapath_meds)
npa /= len(datapath_meds)
#
data = np.zeros((int(nrows), int(ncols)))
data[0,:] = npa; data[1:,:] = raw_data
# convert BNG easting/ northing --> GPS LON / LAT
#Define easting and northing initialisation as an array
incre = float(cellsize[1])
east0, north0 = float(xcntr), float(ycntr-incre*4) # Add 25km onto latitude
east1, north1 = east0 + (incre * ncols),  north0 + (incre * nrows)
eastndarray =  np.arange(east0, east1, incre)
northndarray = np.arange(north0, north1, incre)
# convert np array of BNG easting into Lon/Lat using package
BNG = pyproj.Proj(init='epsg:27700', ellps='WGS84')  # Define conversion from WGS84 GPS to UK BNG coordinates
EEgrid, NNgrid = np.array((eastndarray, northndarray))
lon_dims = len(EEgrid); lat_dims = len(NNgrid)
UK_Lon = np.zeros((lat_dims, lon_dims)); UK_Lat = np.zeros((lat_dims, lon_dims))
for lon_ind in range(lon_dims):
    for lat_ind in range(lat_dims):
        UK_Lon[lat_dims-lat_ind-1][lon_ind], UK_Lat[lat_dims-lat_ind-1][lon_ind] = \
        BNG(EEgrid[lon_ind], NNgrid[lat_ind], inverse=True)  # Convert from ESPG:27700 to WG84 (GPS / standard coordinates)              

# Scale grid of Forecast data - (unchanged in this case)
x_FCSTflat = UK_Lon.flatten(); y_FCSTflat = UK_Lat.flatten()
z_FCSTflat = data.flatten()
FCSTdata_scipy = griddata_scipy((x_FCSTflat, y_FCSTflat), z_FCSTflat, (UK_Lon, UK_Lat), method='linear') # SciPy version
# remove nans and mask out sea
FCSTdata_scipy = np.nan_to_num(FCSTdata_scipy)
FCSTdata_scipy[FCSTdata_scipy <= 0] = np.nan

# Load ERA5 climatology reference
if netcdf_file:
    datapath_ERA5CLIM = 'ERA5/ERA5-Land-'+month[0:3]+climate_end+'_Prev30Yrs-Temperature.nc'
    ncc = Dataset(datapath_ERA5CLIM, 'r')
    lon = ncc.variables['longitude'][:]
    lat = ncc.variables['latitude'][:] # Degrees latitude is a regular spatial (km) grid      
    time = ncc.variables['time']
    temp_allyrs = ncc.variables['t2m'][:]
    temp_allyrs[temp_allyrs == temp_allyrs.fill_value] = np.nan
    temp_allyrs -= 273.15 # Convert from Kelvin to Degrees Celsius
if grib_file:
    temp_allyrs = grib_data[:]
temp_climate = np.mean(temp_allyrs, axis=0)
temp_climateSD = np.std(temp_allyrs, axis=0)

# Loading ERA5 data into workspace
if netcdf_file:
    datapath_ERA5 = 'ERA5/ERA5-Land-'+month[0:3]+year+'-Temperature.nc'
    ncc = Dataset(datapath_ERA5, 'r')
    lon = ncc.variables['longitude'][:]
    lat = ncc.variables['latitude'][:] # Degrees latitude is a regular spatial (km) grid      
    time = ncc.variables['time']
    monthly_temp = ncc.variables['t2m'][:]
    monthly_temp[monthly_temp == monthly_temp.fill_value] = np.nan
    monthly_temp -= 273.15 # Convert from Kelvin to Degrees Celsius
if grib_file:
    monthly_temp = grib_data[-1,:,:]
# mth_daysERA, dayofyearERA = mthdays(year, month[0:3])

# Scale grid of ERA5 data
lon, lat = np.meshgrid(lon, lat)
x_ERA5flat = lon.flatten(); y_ERA5flat = lat.flatten()
z_ERA5flat = np.array(monthly_temp).flatten()
ERA5data_month = griddata_scipy((x_ERA5flat, y_ERA5flat), z_ERA5flat, (UK_Lon, UK_Lat), method='linear') # SciPy version
z_ERA5CLIMflat = np.array(temp_climate).flatten()
ERA5data_climate = griddata_scipy((x_ERA5flat, y_ERA5flat), z_ERA5CLIMflat, (UK_Lon, UK_Lat), method='linear') # SciPy version
z_ERA5SDflat = np.array(temp_climateSD).flatten()
ERA5data_sd = griddata_scipy((x_ERA5flat, y_ERA5flat), z_ERA5SDflat, (UK_Lon, UK_Lat), method='linear') # SciPy version
# remove nans
ERA5data_month = np.nan_to_num(ERA5data_month); ERA5data_climate = np.nan_to_num(ERA5data_climate); ERA5data_sd = np.nan_to_num(ERA5data_sd)
ERA5data_month[ERA5data_month == 0] = np.nan; ERA5data_climate[ERA5data_climate == 0] = np.nan; ERA5data_sd[ERA5data_sd <= 0] = np.nan
'''Make sure that comparison arrays allign perfectly'''
mask = [(~np.isnan(FCSTdata_scipy)) & (~np.isnan(ERA5data_climate))]
# monthly_sds = np.nanmean((ERA5data_month - ERA5data_climate)) / np.nanmean(ERA5data_sd)
monthly_sds = np.nanmean(ERA5data_month[mask] - ERA5data_climate[mask])
# forecast_sds = np.nanmean((FCSTdata_scipy - ERA5data_climate)) / np.nanmean(ERA5data_sd)
forecast_sds = np.nanmean(FCSTdata_scipy[mask] - ERA5data_climate[mask])

if not skip_extraplots:
    # FIGURE: OBSERVATION
    fig = plt.figure(figsize=(6, 6), dpi=100, facecolor='w')
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(ERA5data_climate), rstride=0.25, cstride=0.25, cmap=cm.coolwarm_r,
                           linewidth=0, antialiased=False, vmin=25, vmax=350)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, aspect=5)
    plt.title('Observation of Mean Daily Temperature')
    plt.show(block=False)

# FIGURE: FORECAST
fig = plt.figure(figsize=(8.4, 6), dpi=150, facecolor='w')
# alternatively cmap=cm.terrain_r
ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
# Hide X and Y axes tick marks
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)
# optional_levels = np.arange(1,20)
optional_levels = np.arange(8,18,0.5)
surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(ERA5data_climate), rstride=0.25, cstride=0.25, cmap=colors,
                       linewidth=0, antialiased=False, vmin=10, vmax=18, levels=optional_levels)
# lines = ax.contour(UK_Lon, UK_Lat, np.ma.array(FCSTdata_scipy), colors=['black']*len(optional_levels), linewidths=[0.5]*len(optional_levels), alpha=0.5)
# ax.xaxis.set_major_formatter(FormatStrFormatter('%.01f'))
fig.colorbar(surf, aspect=8, label='Forecast Value (degC)', ticks=optional_levels, format="%d", fraction=0.25)
plt.title(f'Re-Climate Forecast for {month}, {year}\nMean Daily Temperature')
#
if dist == 'Log-Logistic':
    percentile = (st.fisk.cdf(np.nanmean(forecast_sds),0.835)+0.35) * 100.0
elif dist == 'Gaussian':
    percentile = st.norm.cdf(np.nanmean(forecast_sds)) * 100.0
anomaly = np.nanmean(forecast_sds)
#
# last_digit = int(str(round(percentile))[1])
# exts = ('st','st','nd','rd','th','th','th','th','th','th')
# ext = exts[last_digit]
ERA5data_month = ERA5data_month[mask]; ERA5data_climate = ERA5data_climate[mask]; FCSTdata_scipy = FCSTdata_scipy[mask]
ext = ' degC'
plt.annotate(f'Valid: 10th {month_names[start_month-1]}, {start_year}',(-10.75,59), color='maroon')
plt.annotate('UK-Wide Temperature Anomaly: '+str(round(anomaly, 2))+ext+'\nReference: ERA5-Land, 1993-2022',(-10.75,59.5), color='maroon')
print(month+' UK-Wide Temperature Anomaly: '+str(round(anomaly, 2))+ext)
print(month+' UK-Wide Temperature Climate: '+str(round(np.nanmean(ERA5data_climate), 2))+ext)
print(month+' Re-Climate forecast: '+str(round(np.nanmean(FCSTdata_scipy), 2))+ext)
# Save Plot
plt.savefig(f'raw_data/Re-ClimateActuals_{start_month}_{start_year}_{lead}.png', dpi=150, bbox_inches='tight')
plt.show(block=False)

if not skip_extraplots:
    # FIGURE: ERA5
    fig = plt.figure(figsize=(6, 6), dpi=100, facecolor='w')
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(ERA5data_month),  rstride=0.25, cstride=0.25, cmap=cm.coolwarm_r,
                           linewidth=0, antialiased=False, vmin=20, vmax=180)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, aspect=5)
    plt.title('Observed Temperature SD')
    plt.show(block=False)

    # FIGURE: STANDARD DEVIATIONS OF MONTHLY CLIMATE
    fig = plt.figure(figsize=(6, 6), dpi=100, facecolor='w')
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(monthly_sds),  rstride=0.25, cstride=0.25, cmap=cm.coolwarm_r,
                           linewidth=0, antialiased=False, vmin=-2, vmax=2)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, aspect=5)
    plt.title('Observed Temperature SDs (Z Value)')
    plt.show(block=False)
    
    # FIGURE: STANDARD DEVIATIONS OF MONTHLY CLIMATE
    fig = plt.figure(figsize=(6, 6), dpi=100, facecolor='w')
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(forecast_sds),  rstride=0.25, cstride=0.25, cmap=cm.coolwarm_r,
                           linewidth=0, antialiased=False, vmin=-2, vmax=2)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, aspect=5)
    plt.title('Forecasted Temperature SDs (Z Values)')
    percentile = st.norm.cdf(np.nanmean(forecast_sds)) * 100.0
    plt.annotate('Temp. Percentile: '+str(round(percentile))+ext+'\nReference: ERA5-Land, 1993-2022',(-12.50,50.00), color='r')
    print('Temperature Percentile: '+str(round(percentile))+ext)
    plt.show(block=False)

