# Source: https://www.metoffice.gov.uk/hadobs/hadukgrid/data/download_2023-11.html
# Climatology: https://data.ceda.ac.uk/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.2.0.ceda/5km/tas/
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
'''4.2 Load correct visual packages'''
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
import pyproj
'''5.0 Interpolate the grid'''
import scipy
# from matplotlib.mlab import griddata as griddata_mpl
from scipy.interpolate import griddata as griddata_scipy
'''Note that Basemap version > 1.1 do not work!'''
# from mpl_toolkits.basemap import Basemap, maskoceans # conda install basemap==1.0.7
import scipy.stats as st # To calculate percentile of temperature
import xskillscore as xs # pip install xskillscore
import xarray as xr
from global_land_mask import globe # pip install global-land-mask
from mpl_toolkits.basemap import Basemap # pip install basemap

output_ext = ('COMBINED','C3S','WL') # 'COMBINED', 'C3S, 'WL' 
forecasts = (['','weatherlogisticsltd'],[''],['weatherlogisticsltd']) # '','weatherlogisticsltd'
skip_extraplots = True

use_customcolors = True; ukmo_precip = False; ed_hawkins = True; RichHildebrand = False
scale = np.array([0.85,0.85,0.85])
'''Set the analysis date'''
netcdf_file = True
'''Specify the forecast month and at what lead time'''
### LEAD 1 MONTH
years = ('2023','2023','2024','2024','2024','2024','2024','2024','2024','2024','2024'); months = ('November','December','January','February','March','April','May','June','July','August','September'); month_nos = (11,12,1,2,3,4,5,6,7,8,9); leads = (1,1,1,1,1,1,1,1,1,1,1) # Specify the forecast month and at what lead time
### LEAD 2 MONTHS
## years = ('2023','2024','2024','2024','2024','2024','2024','2024','2024','2024'); months = ('December','January','February','March','April','May','June','July','August','September'); month_nos = (12,1,2,3,4,5,6,7,8,9); leads = (2,2,2,2,2,2,2,2,2,2) # Specify the forecast month and at what lead time
### SINGLE MONTH
## years = (['2024']); months = (['September']); month_nos = ([9]); leads = ([1])
climate_end = '2020'

month_names = ('January','February','March','April',
               'May','June','July','August',
               'September','October','November','December')

if use_customcolors:
    from matplotlib.colors import LinearSegmentedColormap # To define own colour scale
    if (ed_hawkins or ukmo_precip):
        if ed_hawkins:
            custom_colors = ['#08306b', '#08519c', '#2171b5', '#4292c6',
                           '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
                           '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
                           '#ef3b2c', '#cb181d', '#a50f15', '#67000d']
        if ukmo_precip:
            custom_colors = reversed((np.array([0.2078, 0.0, 0.0039])*scale,
                            np.array([0.0471, 0.1961, 0.4118])*scale,
                            np.array([0.2314, 0.3961, 0.6118])*scale,
                            np.array([0.4275, 0.5961, 0.8118])*scale,
                            np.array([1.0, 1.0, 1.0]),
                            np.array([0.9843, 0.85, 0.8039])*scale,
                            np.array([0.9725, 0.6039, 0.35])*scale,
                            np.array([0.7647, 0.3118, 0.20])*scale,
                            np.array([0.5725, 0.1014, 0.05])*scale))
        # Create a list of normalized RGB values for your custom colors
        custom_colors_rgb = [plt.cm.colors.to_rgb(c) for c in custom_colors]
    elif RichHildebrand:
        def create_color(r, g, b):
            return [r/256, g/256, b/256]
        custom_colors_rgb = [create_color(227, 101, 33), create_color(246, 145, 53), create_color(251, 168, 74),
            create_color(218, 212, 200), create_color(141, 193, 223), create_color(114, 167, 208), 
            create_color(43, 92, 138)]
    # custom_colors = reversed(['#350001', '#0c3269', '#3b659c', '#6d98cf', '#ffffff', '#fbcccd', '#f89a9b', '#f66935', '#92080d'])
    # Define a custom colormap using `matplotlib.colors.LinearSegmentedColormap`
    colors = LinearSegmentedColormap.from_list('', custom_colors_rgb)
else:
    colors = cm.terrain_r

for model_type in range(3):

    benchmarkFCST_scipyX = np.zeros((len(month_nos),245,179))
    FCSTdata_scipyX = np.zeros((len(month_nos),245,179))
    HADUKdata_monthX = np.zeros((len(month_nos),245,179)); HADUKdata_climX = np.zeros((len(month_nos),245,179))
    for ind, month_no in enumerate(month_nos):
        print(f'{months[ind]}, {years[ind]}')   
        # Load forecast into workspace
        start_month = ((((month_nos[ind]-1)-leads[ind]) % 12) + 1)
        start_year = str(int(years[ind]) - 1) if start_month > month_nos[ind] else years[ind]
        FCST_path = 'raw_data'
        
        datapath_meds = []
        for forecast in forecasts[model_type]:
            filename_hires = f'/ReClimate_{format("%02d" % start_month)}_{start_year}_{str(leads[ind])}_Temperature-Actuals{forecast}.asc'
            datapath_meds.append(FCST_path + filename_hires)
        
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
                benchmark1 = np.copy(npa); benchmark2 = np.copy(raw_data)
            else:
                raw_data += pd.read_csv(datapath_med, header=6, delimiter=' ').values
                npa += np.asarray(aa, dtype=np.float32)
            #
        raw_data /= len(datapath_meds)
        npa /= len(datapath_meds)
        #
        benchmark_data = np.zeros((int(nrows), int(ncols)))
        data = np.zeros((int(nrows), int(ncols)))
        data[0,:] = npa; data[1:,:] = raw_data
        benchmark_data[0,:] = benchmark1; benchmark_data[1:,:] = benchmark2
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
        
        # Align forecast grid to HADUK-Grid observations
        UK_Lon = UK_Lon[2:,6:][:]; UK_Lat = UK_Lat[2:,6:][:]
        UK_Lon = UK_Lon[2:,0:((lon_dims-6-1)-6)][:]; UK_Lat = UK_Lat[2:,0:((lon_dims-6-1)-6)][:]
        UK_Lon = UK_Lon[0:((lat_dims-2-1)-1),0:][:]; UK_Lat = UK_Lat[0:((lat_dims-2-1)-1),0:][:]
        data = data[2:,6:][:]; data = data[2:,0:((lon_dims-6-1)-6)][:]; data = data[0:((lat_dims-2-1)-1),0:][:]
        benchmark_data = benchmark_data[2:,6:][:]; benchmark_data = benchmark_data[2:,0:((lon_dims-6-1)-6)][:]; benchmark_data = benchmark_data[0:((lat_dims-2-1)-1),0:][:]
        # Scale grid of Forecast data - (unchanged in this case)
        x_FCSTflat = UK_Lon.flatten(); y_FCSTflat = UK_Lat.flatten()
        z_FCSTflat = data.flatten()
        benchmark_FCSTflat = benchmark_data.flatten()
        FCSTdata_scipy = griddata_scipy((x_FCSTflat, y_FCSTflat), z_FCSTflat, (UK_Lon, UK_Lat), method='linear') # SciPy version
        benchmarkFCST_scipy = griddata_scipy((x_FCSTflat, y_FCSTflat), benchmark_FCSTflat, (UK_Lon, UK_Lat), method='linear') # SciPy version
        # remove nans and mask out sea
        FCSTdata_scipy = np.nan_to_num(FCSTdata_scipy); benchmarkFCST_scipy = np.nan_to_num(benchmarkFCST_scipy)
        FCSTdata_scipy[FCSTdata_scipy <= 0] = np.nan; benchmarkFCST_scipy[benchmarkFCST_scipy <= 0] = np.nan
        FCSTdata_scipyX[ind,:,:] = FCSTdata_scipy[:]; benchmarkFCST_scipyX[ind,:,:] = benchmarkFCST_scipy[:]
        
        # Loading ERA5 data into workspace
        if netcdf_file:
            # Read analysis month
            datapath_HADUK = f'HADUK-Grid/tas_hadukgrid_uk_5km_mon_{years[ind]}{format("%02d" % month_nos[ind])}.nc'
            ncc = Dataset(datapath_HADUK, 'r')
            lon = ncc.variables['longitude'][:]; lon = lon[::-1][:]; lon = lon[0:288-44,1:][:]
            lat = ncc.variables['latitude'][:]; lat = lat[::-1][:]; lat = lat[0:288-44,1:][:] # Degrees latitude is a regular spatial (km) grid      
            time = ncc.variables['time']
            monthly_temp = ncc.variables['tas'][:]; monthly_temp = monthly_temp[0][:]; monthly_temp = monthly_temp[::-1][:]; monthly_temp = monthly_temp[0:288-44,1:][:]
            monthly_temp[monthly_temp == monthly_temp.fill_value] = np.nan
            # Read climatology month (1991 to 2020)
            datapath_HADUK = 'HADUK-Grid/tas_hadukgrid_uk_5km_mon-30y_199101-202012.nc'
            ncc = Dataset(datapath_HADUK, 'r')
            lon = ncc.variables['longitude'][:]; lon = lon[::-1][:]; lon = lon[0:288-44,1:][:]
            lat = ncc.variables['latitude'][:]; lat = lat[::-1][:]; lat = lat[0:288-44,1:][:] # Degrees latitude is a regular spatial (km) grid      
            time = ncc.variables['time']
            monthly_clim = ncc.variables['tas'][month_no-1][:]; monthly_clim = monthly_clim[:]; monthly_clim = monthly_clim[::-1][:]; monthly_clim = monthly_clim[0:288-44,1:][:]
            monthly_clim[monthly_clim == monthly_clim.fill_value] = np.nan
    
        # mth_daysERA, dayofyearERA = mthdays(year, month[0:3])
        # Scale grid of HADUK_Grid data
        x_HADUKflat = lon.flatten(); y_HADUKflat = lat.flatten()
        z_HADUKflat = np.array(monthly_temp).flatten()
        HADUKdata_month = griddata_scipy((x_HADUKflat, y_HADUKflat), z_HADUKflat, (UK_Lon, UK_Lat), method='linear') # SciPy version
        z2_HADUKflat = np.array(monthly_clim).flatten()
        HADUKdata_clim = griddata_scipy((x_HADUKflat, y_HADUKflat), z2_HADUKflat, (UK_Lon, UK_Lat), method='linear') # SciPy version
        # remove nans
        HADUKdata_month = np.nan_to_num(HADUKdata_month); HADUKdata_clim = np.nan_to_num(HADUKdata_clim)
        HADUKdata_month[HADUKdata_month == 0] = np.nan; HADUKdata_clim[HADUKdata_clim == 0] = np.nan
        HADUKdata_monthX[ind,:,:] = HADUKdata_month[:]; HADUKdata_climX[ind,:,:] = HADUKdata_clim[:]
        
    '''Make sure that comparison arrays align perfectly'''
    mask1 = [(np.isnan(HADUKdata_monthX)) | (HADUKdata_monthX > 40) | (HADUKdata_monthX < -20)][0]
    HADUKdata_monthX = np.where(~mask1, HADUKdata_monthX, np.nan)
    mask2 = [(np.isnan(FCSTdata_scipyX)) | (FCSTdata_scipyX > 40) | (FCSTdata_scipyX < -20)][0]
    FCSTdata_scipyX = np.where(~mask2, FCSTdata_scipyX, np.nan)
    mask3 = [(np.isnan(benchmarkFCST_scipyX)) | (benchmarkFCST_scipyX > 40) | (benchmarkFCST_scipyX < -20)][0]
    benchmarkFCST_scipyX = np.where(~mask3, benchmarkFCST_scipyX, np.nan)
    
    # FIGURE A: SPEARMAN RANK
    fig = plt.figure(figsize=(8.4, 6), dpi=150, facecolor='w')
    # alternatively cmap=cm.terrain_r
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    # Hide X and Y axes tick marks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    # optional_levels = np.arange(1,20)
    optional_levels = np.arange(-1,1.1,0.1)
    a = xr.DataArray(HADUKdata_monthX[:]-HADUKdata_climX[:], dims=['time', 'x', 'y'])
    HADUKdata_climX[HADUKdata_climX > 1000] = np.nan
    clim = np.zeros((len(month_nos),245,179)); clim[0:len(month_nos),:,:] = HADUKdata_climX[:]; clim[clim > 1000] = np.nan
    b_CLIM = xr.DataArray(HADUKdata_climX[:]-HADUKdata_climX, dims=['time', 'x', 'y'])
    b = xr.DataArray(FCSTdata_scipyX[:]-HADUKdata_climX[:], dims=['time', 'x', 'y'])
    spearman_cor = xs.spearman_r(a, b, dim='time')
    # spearman_cor = scipy.stats.spearmanr(HADUKdata_monthX[:], FCSTdata_scipyX[:], alternative='greater', axis=0)
    surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(spearman_cor), rstride=0.25, cstride=0.25, cmap=colors,
                           linewidth=0, antialiased=False, vmin=-1, vmax=1, levels=optional_levels)
    # lines = ax.contour(UK_Lon, UK_Lat, np.ma.array(FCSTdata_scipy), colors=['black']*len(optional_levels), linewidths=[0.5]*len(optional_levels), alpha=0.5)
    # ax.xaxis.set_major_formatter(FormatStrFormatter('%.01f'))
    fig.colorbar(surf, aspect=8, label='Skill Score', ticks=optional_levels, format="%.02f", fraction=0.25)
    plt.title('Re-Climate Spearman Rank Corr. for \nMonthly Average of Daily Mean Temperature')
    #
    # last_digit = int(str(round(percentile))[1])
    # exts = ('st','st','nd','rd','th','th','th','th','th','th')
    # ext = exts[last_digit]
    ERA5data_month = HADUKdata_month[mask1[0]]; FCSTdata_scipy = FCSTdata_scipy[mask2[0]]
    plt.annotate(f'Valid: {months[0]} {years[0]} to {months[-1]} {years[-1]}',(-10.75,59), color='maroon')
    plt.annotate('UK-Wide Spearman Rank Corr. '+str(round(np.nanmean(spearman_cor), 2))+'\nReference: HADUK-Grid',(-10.75,59.5), color='maroon')
    # Save Plot
    plt.savefig(f'raw_data/Re-ClimateActuals_HADUK_Grid_Spearman{output_ext[model_type]}_{leads[0]}.png', dpi=150, bbox_inches='tight')
    plt.show(block=False)
    
    
    # FIGURE B: PEARSON'S
    fig = plt.figure(figsize=(8.4, 6), dpi=150, facecolor='w')
    # alternatively cmap=cm.terrain_r
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    # Hide X and Y axes tick marks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    # optional_levels = np.arange(1,20)
    optional_levels = np.arange(-1,1.1,0.1)
    a = xr.DataArray(HADUKdata_monthX[:]-HADUKdata_climX[:], dims=['time', 'x', 'y'])
    b = xr.DataArray(FCSTdata_scipyX[:]-HADUKdata_climX[:], dims=['time', 'x', 'y'])
    pearson_cor = xs.pearson_r(a, b, dim='time')
    surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(pearson_cor), rstride=0.25, cstride=0.25, cmap=colors,
                           linewidth=0, antialiased=False, vmin=-1, vmax=1, levels=optional_levels)
    # lines = ax.contour(UK_Lon, UK_Lat, np.ma.array(FCSTdata_scipy), colors=['black']*len(optional_levels), linewidths=[0.5]*len(optional_levels), alpha=0.5)
    # ax.xaxis.set_major_formatter(FormatStrFormatter('%.01f'))
    fig.colorbar(surf, aspect=8, label='Skill Score', ticks=optional_levels, format="%.02f", fraction=0.25)
    plt.title('Re-Climate Pearson Corr. for \nMonthly Average of Daily Mean Temperature')
    #
    # last_digit = int(str(round(percentile))[1])
    # exts = ('st','st','nd','rd','th','th','th','th','th','th')
    # ext = exts[last_digit]
    plt.annotate(f'Valid: {months[0]} {years[0]} to {months[-1]} {years[-1]}',(-10.75,59), color='maroon')
    plt.annotate('UK-Wide Pearson Corr. '+str(round(np.nanmean(pearson_cor), 2))+'\nReference: HADUK-Grid',(-10.75,59.5), color='maroon')
    # Save Plot
    plt.savefig(f'raw_data/Re-ClimateActuals_HADUK_Grid_Pearson{output_ext[model_type]}_{leads[0]}.png', dpi=150, bbox_inches='tight')
    plt.show(block=False)
    
    # FIGURE C: RMS ERROR
    fig = plt.figure(figsize=(8.4, 6), dpi=150, facecolor='w')
    # alternatively cmap=cm.terrain_r
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    # Hide X and Y axes tick marks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    a = xr.DataArray(HADUKdata_monthX-HADUKdata_climX, dims=['time', 'x', 'y'])
    b = xr.DataArray(FCSTdata_scipyX[:]-HADUKdata_climX[:], dims=['time', 'x', 'y'])
    optional_levels = np.arange(0,5,0.5)
    rms_error = xs.rmse(a, b, dim='time'); rms_errorCLIM = xs.rmse(a, b_CLIM, dim='time')
    surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(rms_error), rstride=0.25, cstride=0.25, cmap=colors,
                           linewidth=0, antialiased=False, vmin=0, vmax=5, levels=optional_levels)
    # lines = ax.contour(UK_Lon, UK_Lat, np.ma.array(FCSTdata_scipy), colors=['black']*len(optional_levels), linewidths=[0.5]*len(optional_levels), alpha=0.5)
    # ax.xaxis.set_major_formatter(FormatStrFormatter('%.01f'))
    fig.colorbar(surf, aspect=8, label='Root-Mean-Square Error', format="%.02f", fraction=0.25, ticks=optional_levels)
    plt.title('Re-Climate RMS Error for \nMonthly Average of Daily Mean Temperature')
    #
    # last_digit = int(str(round(percentile))[1])
    # exts = ('st','st','nd','rd','th','th','th','th','th','th')
    # ext = exts[last_digit]
    plt.annotate(f'Valid: {months[0]} {years[0]} to {months[-1]} {years[-1]}',(-10.75,59), color='maroon')
    plt.annotate('UK-Wide RMS Error '+str(round(np.nanmean(rms_error), 2))+'\nReference: HADUK-Grid',(-10.75,59.5), color='maroon')
    # Save Plot
    plt.savefig(f'raw_data/Re-ClimateActuals_HADUK_Grid_RMS{output_ext[model_type]}_{leads[0]}.png', dpi=150, bbox_inches='tight')
    plt.show(block=False)
    
    ### FIGURE Cii: RMS ERROR (Climatology)
    fig = plt.figure(figsize=(8.4, 6), dpi=150, facecolor='w')
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    optional_levels = np.arange(0,5,0.5)
    surf = ax.contourf(UK_Lon, UK_Lat, np.ma.array(rms_errorCLIM), rstride=0.25, cstride=0.25, cmap=colors,
                           linewidth=0, antialiased=False, vmin=0, vmax=5, levels=optional_levels)
    fig.colorbar(surf, aspect=8, label='Root-Mean-Square Error', format="%.02f", fraction=0.25, ticks=optional_levels)
    plt.title('Re-Climate RMS Error for \nMonthly Average of Daily Mean Temperature')
    plt.annotate(f'Valid: {months[0]} {years[0]} to {months[-1]} {years[-1]}',(-10.75,59), color='maroon')
    plt.annotate('UK-Wide RMS Error '+str(round(np.nanmean(rms_errorCLIM), 2))+'\nReference: HADUK-Grid',(-10.75,59.5), color='maroon')
    plt.savefig(f'raw_data/Re-ClimateActuals_HADUK_Grid_RMS_CLIM_{leads[0]}.png', dpi=150, bbox_inches='tight')
    plt.show(block=False)
    
    # FIGURE D: BRIER SCORE
    fig = plt.figure(figsize=(8.4, 6), dpi=150, facecolor='w')
    # alternatively cmap=cm.terrain_r
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    # Hide X and Y axes tick marks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    min_h = np.nanmin(HADUKdata_monthX, axis=0)
    forecast = FCSTdata_scipyX - HADUKdata_climX
    observation = HADUKdata_monthX - HADUKdata_climX
    mask1 = observation > 0 # 1 (Warmer than climate)
    mask2 = observation < 0 # 0 (Cooler than climate)
    observationX = np.where(mask1, observation, 1); observationX = np.where(mask2, observationX, 0)
    a = xr.DataArray(observationX[:], dims=['time', 'x', 'y'])
    mask1 = forecast > 0 # 1 (Warmer than observed)
    mask2 = forecast < 0 # 0 (Cooler than observed)
    forecastX = np.where(mask1, forecast, 1); forecastX = np.where(mask2, forecastX, 0)
    b = xr.DataArray(forecastX[:], dims=['time', 'x', 'y'])
    brier_score = xs.brier_score(a, b, np.linspace(0, 1, 21), dim='time')
    
    # Get whether the points are on land.
    z = globe.is_ocean(UK_Lat, UK_Lon)
    m = Basemap(llcrnrlon=-15, llcrnrlat=50, urcrnrlon=5, urcrnrlat=60,
                projection='merc', resolution='i')
    m.drawstates(linewidth=0.2)
    m.drawcoastlines(linewidth=0.2)
    m.drawcountries(linewidth=0.2)
    
    brier_score = np.where(z == False, brier_score, -9999)
    
    UK_LonM, UK_LatM = m(UK_Lon, UK_Lat) # Map projections
    optional_levels = np.arange(0,1.1,0.1)
    surf = m.contourf(UK_LonM, UK_LatM, brier_score, rstride=0.25, cstride=0.25, cmap=colors,
                           linewidth=0, antialiased=False, vmin=0, vmax=1, levels=optional_levels)
    # lines = ax.contour(UK_Lon, UK_Lat, np.ma.array(FCSTdata_scipy), colors=['black']*len(optional_levels), linewidths=[0.5]*len(optional_levels), alpha=0.5)
    # ax.xaxis.set_major_formatter(FormatStrFormatter('%.01f'))
    fig.colorbar(surf, aspect=8, label='Skill Score (0.0 = Perfect, 0.5 = Climatology)', ticks=optional_levels, format="%.02f", fraction=0.25)
    plt.title('Re-Climate Brier Score for \nMonthly Average of Daily Mean Temperature')
    #
    # last_digit = int(str(round(percentile))[1])
    # exts = ('st','st','nd','rd','th','th','th','th','th','th')
    # ext = exts[last_digit]
    brier_score = np.ma.masked_array(brier_score, mask=z)
    brier_score[brier_score == 0.05] = 0.0
    mean_brier = str(round(np.nanmean(brier_score), 3))
    plt.annotate('UK-Wide Brier Score '+mean_brier+',\nValid: '+months[0]+' '+years[0]+' to\n         '+months[-1]+' '+years[-1]+'\nReference: HADUK-Grid',(1000,1000), color='maroon')
    # UK-Wide Brier Score '+str(round(np.nanmean(brier_score), 2))
    # Save Plot
    plt.savefig(f'raw_data/Re-ClimateActuals_HADUK_Grid_Brier{output_ext[model_type]}_{leads[0]}.png', dpi=150, bbox_inches='tight')
    plt.show(block=False)
    
    ### ENDS
    
