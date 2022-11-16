# WeatherLogistics Re-Climate® API

The Re-Climate® product supplies reliable seasonal climate forecasts to prepare for extended weather hazards. For more information on the seasonal climate forecast services please see https://seasonalforecasts.earth/docs.

Sample seasonal climate hazard plots can be viewed at: https://github.com/cjnankervis/Re-Climate/blob/main/RE-CLIMATE_PLOTS.png

The Re-Climate (seasonal climate forecast) API:

Builds on 10-years of R&D to improve the reliability and accuracy of extended weather forecasts
Delivers the essential requirements to facilitate short-term climate action in the United Kingdom, Spain and Turkey
Combines state-of-the-art seasonal climate prediction data, downscaling, statistical post-processing, chronic climate trend adjustments, and rigorous validation methods
Supplies reliable daily precipitation event generation (ERA-5 aligned weather generator) to manage local flood/ drought risk to operations
Provides acute physical risk information to assess within-season daily intensities and likelihoods of weather events
Extends deterministic weather predictions with a seamless 3-month probabilistic forecast
Provides access for historical start dates from month: '09', year: '2022'
Supplies town or city data, reporting the closest datapoint where applicable
Updates climate hazard information on the 14th day of each month
Bounding box restrictions:

UK: 49.84° to 60.85° North, -10.7° to 2.69° East
Spain: 35.71° to 44.17° North, -9.67° to 3.67° East
Turkey: 35.82° to 42.14° North, 26.04° to 44.79° East
To get started, an API authentication key and user credentials are required to make requests using [API-Request.py]. Please contact the product owner (accounts@weatherlogistics.com). The API request scripts will provide access to four main data streams, with the opportunity for post-processing using "Daily Ensembles" data:

<table>
  <tr><center><td width="50%">

|API Technical<br />Specifications | Monthly<br /> Centile: | Daily<br /> Ensembles | Hazard<br /> Indices | Anomalies |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| <sub>Country-wide Forecasts<br /> (Downscaled to a 5km<br /> Regular Grid)</sub> | :white_check_mark: | :x: | :x: | :white_check_mark: |
| <sub>Town-level Modelling<br /> (Closest Location Match)</sub> | :x: | :white_check_mark: | :white_check_mark: | :x: |
| <sub>Confidence Intervals (100<br /> Ensemble Members  'E' or<br /> Centile Bands 'C' or Shift-<br />of-the-Tails 'T')</sub> | <font size="20"><b>C</b></font> | <font size="20"><b>E</b></font> | <font size="20"><b>T</b></font> | <font size="20"><b>C</b></font> |
| <sub>Temporal Granularity<br /> (Seasonal 'S' or Monthly 'M'<br /> or Daily 'D')</sub> | <font size="20"><b>M</b></font> | <font size="20"><b>D</b></font> | <font size="20"><b>S, M</b></font> | <font size="20"><b>M</b></font> |
| <sub>Spatially Correlated Daily<br /> Event Generation</sub> | :white_check_mark: | :x: | :x: | :white_check_mark: |
| <sub>Combines NWP with<br /> Statistical Model</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub>Validated by the National<br /> Physical Laboratory</sub> | :x: | :white_check_mark: | :x: | :x: |
| <sub>Weather Variability as a<br /> Function of Numerical<br /> Model Output</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub>Forecast Trained<br /> to Local Geography</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub>Chronic & Acute Physical<br /> Climate Change<br /> Adjustments</sub> | :white_check_mark: | :white_check_mark: | <:white_check_mark: | :white_check_mark: |

  </td></center></tr>
</table>

Monthly Centiles
**Country-wide ASCII grid provided at a monthly granularity, useful for a big-picture seasonal overview

Monthly centile data supplies users with mapped averages of precipitation in addition to minimum, maximum and average monthly temperatures. At present these are available for the United Kingdom, Spain and Turkey. They present the lower to upper thresholds in the respectively meteorological variables at the 10th, 30th, median (50th), 70th and 90th centiles. Since the seasonal climate forecasts provide well-calibrated information, 8 in 10 months are likely to present monthly conditions between the 10th and 90th centiles at any specified geographical location.

To request this climate data, see request [MonthlyCentiles_example.json]. See documentation at https://seasonalforecasts.earth/docs/gridded-datasets/.

Daily Ensembles
**Unique access to 100 daily simulations at the town/ city scale, ideal for those with assets at specified locations

WeatherLogistics' daily ensembles provide a quickstart framework to calculate frequencies of occurrence, threshold or centile-based exceedance calculations, consecutive day counts or accumulations; and generate customised metrics.

The first 50 ensemble members are generated using WeatherLogistics' statistical forecast system, and members 51 to 100 are generated using a multi-model average of modified Copernicus seasonal climate forecast data*. Both systems have been developed to achieve the best-on-market accuracy and reliability and have been independently and impartially reviewed by the National Physical Laboratory.

To request this climate data, see request [DailyEnsembles_example.json], with postprocessing scripts provided for CSV [CSV_Postprocessing.py] and JSON [JSON_Postprocessing.py]. See documentation at https://seasonalforecasts.earth/docs/daily-time-series/.

Hazard Indices
**Mapped country-wide town/ city indices, useful for a snapshot overview of acute seasonal climate hazards

Hazard indices show index values as a shift in the tail distribution from a baseline climatology. Climate hazards indices include precipitation, drought, SPI, hail, aridity, humidity, solar, wind, heat and cold. These are scaled from 0 - 10, with the extremes in the index indicating probability shifted by 4 deciles below or above its local climatatology reference, with 5 indicating the the forecast is on par with climate expectations for the current forecast month or season. To request this climate data, see request [HazardIndices_example.json]. See documentation at https://seasonalforecasts.earth/docs/hazard-indices/.

Anomalies
**Country-wide ASCII grid/ town or city CSV provided at a monthly granularity; a departure forecast useful for a big-picture seasonal overview

Similar to the monthly centiles, anomalies provide a country-wide mapped overview of departures from an up-to-date climatology to assess whether the seasonal forecast period is likely to be warmer/ cooler or wetter/ drier than the average monthly conditions over the most recent years. To request this climate data, see request [Anomalies_example.json]. See documentation at https://seasonalforecasts.earth/docs/gridded-datasets/.

*Contains modified Copernicus Climate Change Service information 2022. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains.
