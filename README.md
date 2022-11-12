# WeatherLogistics Re-Climate® API

The Re-Climate® product supplies reliable seasonal climate forecasts to prepare for extended weather hazards. For more information on the seasonal climate forecast services please see https://seasonalforecasts.earth/docs.

Sample seasonal climate hazard plots can be viewed at: https://github.com/cjnankervis/Re-Climate/blob/main/RE-CLIMATE_PLOTS.png

The Re-Climate (seasonal climate forecast) API:
- Combines state-of-the-art seasonal climate prediction data, statistical post-processing and chronic climate change science
- Supply reliable daily precipitation probablistic event generation to manage local flood/ drought risk to operations
- Provide acute physical risk information to assess within-season daily intensities and likelihoods of weather events
- Extend weather predictions with three month probabilistic forecasts
- Provide access for historical start dates from month: '09', year: '2022'
- Supply town or city data, reporting the closest datapoint where applicable
- Are available for the United Kingdom, Spain and Turkey and are udated on 14th day of each month

Bounding box restrictions:
UK: 49.84° to 60.85° North, 10.7° to 2.69° East
Spain: 35.71° to 44.17° North, -9.67° to 3.67° East
Turkey: 35.82° to 42.14° North, 26.04° to 44.79° East

Firstly, an API authentication key and user credentials are required to make requests using [API-Request.py]. The API provides access to four main data streams, with the opportunity for post-processing using Daily Ensembles:

1.	Monthly Centiles

**Country-wide ASCII grid provided at a monthly granularity, useful for a big-picture seasonal overview

Monthly centile data supplies users with mapped averages of precipitation in addition to minimum, maximum and average monthly temperatures. At present these are available for the United Kingdom, Spain and Turkey. They present the lower to upper thresholds in the respectively meteorological variables at the 10th, 30th, median (50th), 70th and 90th centiles. Since the seasonal climate forecasts provide well-calibrated information, 8 in 10 months are likely to present monthly conditions between the 10th and 90th centiles at any specified geographical location.

To request this climate data, see request [MonthlyCentiles_example.json]. See documentation at https://seasonalforecasts.earth/docs/gridded-datasets/.

2.	Daily Ensembles

**Unique access to 100 daily simulations at the town/ city scale, ideal for those with assets at specified locations

WeatherLogistics' daily ensembles provide a quickstart framework to calculate frequencies of occurrence, threshold or centile-based exceedance calculations, consecutive day counts or accumulations; and generate customised metrics.

The first 50 ensemble members are generated using WeatherLogistics' statistical forecast system, and members 51 to 100 are generated using a multi-model average of modified Copernicus seasonal climate forecast data*. Both systems have been developed to achieve the best-on-market accuracy and reliability and have been independently and impartially reviewed by the National Physical Laboratory.

To request this climate data, see request [DailyEnsembles_example.json], with postprocessing scripts provided for CSV [CSV_Postprocessing.py] and JSON [JSON_Postprocessing.py]. See documentation at https://seasonalforecasts.earth/climate-api-overview//hazard-indices/.

3.	Hazard Indices

**Mapped country-wide town/ city indices, useful for a snapshot overview of acute seasonal climate hazards

Hazard indices show index values as a shift in the tail distribution from a baseline climatology. Climate hazards indices include precipitation, drought, SPI, hail, aridity, humidity, solar, wind, heat and cold. These are scaled from 0 - 10, with the extremes in the index indicating probability shifted by 4 deciles below or above its local climatatology reference, with 5 indicating the the forecast is on par with climate expectations for the current forecast month or season.
To request this climate data, see request [HazardIndices_example.json]. See documentation at https://seasonalforecasts.earth/docs/hazard-indices/.

4.	Anomalies

**Country-wide ASCII grid/ town or city CSV provided at a monthly granularity; a departure forecast useful for a big-picture seasonal overview

Similar to the monthly centiles, anomalies provide a country-wide mapped overview of departures from an up-to-date climatology to assess whether the seasonal forecast period is likely to be warmer/ cooler or wetter/ drier than the average monthly conditions over the most recent years.
To request this climate data, see request [Anomalies_example.json]

*Contains modified Copernicus Climate Change Service information 2022. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains. See documentation at https://seasonalforecasts.earth/docs/gridded-datasets/.
