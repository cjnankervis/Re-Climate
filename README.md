# WeatherLogistics® Re-Climate® API
[<img src="https://seasonalforecasts.earth/wp-content/themes/dropX/assets/images/logo.png" width="250"/>](https://seasonalforecasts.earth "Reliable Seasonal Climate Forecasts")

## About WeatherLogistics®

WeatherLogistics® is an innovative climate technology company with 10-years expertise in improving the value of seasonal climate forecasts for wider operational use.

The company’s successful projects include a European Space Agency kick-start activity. WeatherLogistics® has also undertaken data validation and meteorological product audits for the agricultural industry. Its clients include renewable energy, water management and insurance firms. Delivered through the Google Cloud Platform, its extended precipitation data offers the most detailed information available to support operations teams in Turkey and the UK impacted by drought.

Over the past 5 years WeatherLogistics' seasonal forecast codebase has been verified by the [Science & Technology Facilities Council](https://www.ukri.org/news-and-events/responding-to-climate-change/predicting-and-managing-climate-risks/flexible-and-scalable-solutions-for-climate-smart-forecasting/) and its results validated internally and by [data specialists at Agrimetrics](https://agrimetrics.co.uk/2020/06/03/seasonal-climate-forecasts-for-agriculture/). Weather Logistics also helped initiate and sponsor [Yield21 ‘Predict Our Harvest’](https://www.agritechcentres.com/news/uks-2021-wheat-yield-predicted-to-surpass-defra-estimate) and is also a [UKRI/ NERC project partner for Seasonal Weather Prediction](https://gtr.ukri.org/project/C31D56B3-9A23-4AD9-BD85-752248E3D09F).

## Requesting API Access

To get started, please request an API authentication key and user credentials from the [product owner](mailto:accounts@weatherlogistics.com). To make single requests the [API-Request.py](https://github.com/cjnankervis/Re-Climate/blob/main/API-Request.py) script should be used, while for multiple requests please see [API-Request-Multithreading.py](https://github.com/cjnankervis/Re-Climate/blob/main/API-Request-Multithreading.py). The Python code can be used to access  six main data streams, with post-processing code also supplied to calculate return periods and other statistics from daily town and city data supplied through "Daily Ensembles". For a description of all available API requests, please see [API_requests.md](https://github.com/cjnankervis/Re-Climate/blob/main/Example_Requests/API_requests.md).

## Re-Climate® Product

[<img src="https://seasonalforecasts.earth/wp-content/uploads/2022/11/Re-Climate_API-video.png" width="50%">](https://youtu.be/GkMn4gPZjts "Seasonal climate forecasts Re-Climate API YouTube Marketing Video")

The Re-Climate® API delivers the most reliable seasonal climate prediction system in Europe, with its precipitation forecasts independently assessed by the National Physical Laboratory. It achieves this by blending numerous climate datasets and weather models through its algorithms; and this helps organisations to accurately forecast extreme weather, calculate their risk exposure and build their resilience.

Modelling weather events and seasonal climate helps decision-makers communicate losses linked to floods, drought, wind damage, hail, heatwaves or freeze days to within a few kilometres.

Supplied as an 'ensemble', a collection of well-calibrated daily weather time series, Re-Climate® enables firms to better hedge or price their risk. The product also helps clients adapt to acute physical risks posed by extreme weather events such as heatwaves and floods, develop rigorous scenario plans, and protect assets from acute climate hazards on operational timescales.

### Supporting Sustainable Agriculture

WeatherLogistics has a mission to help meet UN Sustainable Development Goals (SDGs) for food, water and natural resources. Currently the firm is developing a sustainability monitoring platform to advise farmers on their present and future climate exposure and how to reduce both their agricultural inputs and reduce greenhouse gas emissions. This forms part of a 12-month project in partnership with the University of Leicester, the University of Reading and supported and funded by UKRI/ STFC.

Future farmers will be able to build smarter precision farming solutions and benchmarking platforms, integrated pest management systems, and decision-support applications to avoid food supply distribution. Growers can also optimise their operations with better timed preventative spraying, frost protection, and crop quality assurance.

# Features

Independently and impartially assessed by the [National Physical Laboratory](https://www.npl.co.uk/national-challenges), Re-Climate™ delivers forecasts of climate perils covering the next 3 months and at a 5 kilometre resolution to prepare for extended weather hazards. For more information on the seasonal climate forecast services please see [WeatherLogistics' Docs](https://re-climate.co.uk/docs).

**The Re-Climate (seasonal climate forecast) API**:

- Builds on 10-years of R&D in seasonal climate prediction science
- Combines state-of-the-art models, downscaling, statistical post-processing, chronic climate trend adjustments, and rigorous validation
- Simulates daily precipitation event generation to manage local flood/ drought
- Delivers accurate physical hazard analytics to assess intensities of daily weather events
- Extends deterministic weather predictions with a seamless 3-month probabilistic forecast extending from 2 to 15 weeks
- Provides access for historical start dates from month: '12', year: '2022'
- Supplies town or city data, reporting the closest datapoint where applicable
- Updates climate hazard information on the 14th day of each month

### Bounding Box Restrictions

- UK: 49.84° to 60.85° North, -10.7° to 2.69° East
- Spain: 35.71° to 44.17° North, -9.67° to 3.67° East
- Turkey: 35.82° to 42.14° North, 26.04° to 44.79° East

*USA is in our future development pipeline, expanding to other geographies

## Validation

WeatherLogistics completed a successful collaboration with the National Physical Laboratory (NPL) in April 2022. As part of its deliverable, NPL validated its short-term climate forecasts and provided a statistical framework for quality assessment of probabilistic weather predictions. WeatherLogistics used these techniques to ensure the reliability of its Re-Climate® product delivery.

### Direct Comparisons of Seasonal Forecasts Against Observations

NPL's validation report presents a comparison of the predicted frequencies of occurrence of daily precipitation events of different intensities against ERA5-land measurements. Covering 96 UK cities for the years 2018 to 2022, the results summarise the [late winter assessment](https://seasonalforecasts.earth/wp-content/uploads/2022/07/Late-WinterNPL_WL.pdf) from January to March period (lead times of 1 to 3 months) as they would be issued on 13th December.

Similarly, NPL’s report also provided direct comparisons for the [late summer period](https://seasonalforecasts.earth/wp-content/uploads/2022/07/Late-SummerNPL-WL.pdf) as issued on 13th June, which cover the months July to September from 2018 to 2022. For both the winter and summer the results demonstrate a good overall seasonal consistency between observations and WeatherLogistics' retrospective seasonal climate predictions  at the city scale.

## Understanding Seasonal Forecast Requests

<table>
  <tr><center><td width="50%" align="center">

|API Technical<br />Specifications | Monthly<br /> Centile | Daily<br /> Ensembles | Hazard<br /> Indices | Departures<br /> (Anomalies) | Daily<br /> Profiles | Graphical<br /> Summaries |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| <sub><b>Country-wide Forecasts<br /> (Downscaled to a 5km<br /> Regular Grid)</b></sub> | :white_check_mark: | :x: | :x: | :white_check_mark: | :x: | :x: |
| <sub><b>Town-level Modelling<br /> (Closest Location Match)</b></sub> | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub><b>Confidence Intervals (100<br /> Ensemble Members  'E' or<br /> Centile Bands 'C' or Shift-<br />of-the-Tails 'T')</b></sub> | <font size="20"><b>C</b></font> | <font size="20"><b>E</b></font> | <font size="20"><b>T</b></font> | <font size="20"><b>C</b></font> | <font size="20"><b>E</b></font> | <font size="20"><b>E</b></font> |
| <sub><b>Temporal Granularity<br /> (Seasonal 'S' or Monthly 'M'<br /> or Daily 'D')</b></sub> | <font size="20"><b>M</b></font> | <font size="20"><b>D</b></font> | <font size="20"><b>S, M</b></font> | <font size="20"><b>M</b></font> | <font size="20"><b>S, M</b></font> | <font size="20"><b>S, M</b></font> |
| <sub><b>Spatially Correlated Daily<br /> Event Generation</b></sub> | :x: | :white_check_mark: | :white_check_mark:| :x: | :white_check_mark: | :white_check_mark: |
| <sub><b>Combines NWP with<br /> Statistical Model</b></sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub><b>Validated by the National<br /> Physical Laboratory</b></sub> | :x: | :white_check_mark: | :x: | :x: | :white_check_mark: | :white_check_mark: |
| <sub><b>Weather Variability as a<br /> Function of Numerical<br /> Model Output</b></sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub><b>Forecast Trained<br /> to Local Geography</b></sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub><b>Chronic & Acute Physical<br /> Climate Change<br /> Adjustments</b></sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |

  </td></center></tr>
</table>
<sub><b>NWP = Numerical Weather Prediction</b></sub>

## Monthly Centiles
**Country-wide ASCII grid provided at a monthly granularity, useful for a big-picture seasonal overview

Monthly centile data supplies users with mapped averages of precipitation in addition to minimum, maximum and average monthly temperatures. At present these are available for the mainland geographical area of the United Kingdom, Spain and Turkey. These ASCII grids present the lower to upper thresholds in the respectively meteorological variables at the 10th, 30th, median (50th), 70th and 90th centile confidence bounds. Since the seasonal climate forecasts provide well-calibrated information, 8 in 10 months are likely to present monthly conditions between the 10th and 90th centiles at any specified geographical location.

To request this climate data on a regular 5km grid, see [monthly centile request example input](https://github.com/cjnankervis/Re-Climate/blob/main/Example_Requests/MonthlyCentiles_example.json). See further [documentation](https://re-climate.co.uk/docs/gridded-datasets/) and [ASCII formatting](https://re-climate.co.uk/docs/climate-data-outputs/). To visualise ASCII output data please see [Visualise_ASCII.py](https://github.com/cjnankervis/Re-Climate/blob/main/Visualise_ASCII.py).

## Daily Ensembles
**Unique access to 100 daily simulations at the town/ city level, ideal for those with assets at specified locations

WeatherLogistics' daily ensembles provide a Quickstart framework to calculate frequencies of occurrence, threshold or centile-based exceedance calculations, consecutive day counts or accumulations; and generate customised metrics.

Ensemble members 1 to 50 are generated using WeatherLogistics' statistical forecast system, while members 51 to 100 are generated using a multi-model average of modified Copernicus seasonal climate forecast data*. Both systems have been developed to achieve the best-on-market accuracy and reliability and have been independently and impartially reviewed by the National Physical Laboratory.

To request this climate data, see [daily ensembles example input](https://github.com/cjnankervis/Re-Climate/blob/main/Example_Requests/DailyEnsembles_example.json), and its postprocessing scripts provided for [CSV](https://github.com/cjnankervis/Re-Climate/blob/main/CSV_Postprocessing.py) and [JSON](https://github.com/cjnankervis/Re-Climate/blob/main/JSON_Postprocessing.py) inputs. See further [documentation](https://re-climate.co.uk/docs/daily-time-series/).

### Example A.
Using "JSON_Postprocessing.py" to calculate the 90th centile of ensemble members with consecutive dry days, where 24-hour accumulated precipitation is less than 1mm

<code>Mean consecutive days with an event intensity equal to or below 1.0 is 13.67, which is based on analysis of 50 ensemble members and 31 days in July</code>

### Example B.
Using "CSV_Postproccessing.py" to calculate an ensemble average of consecutive days of tropical nights (T<sub>min</sub> > 20°C), for the multi-model benchmark/ numerical weather prediction models

<code>Mean consecutive days with an event intensity equal to or above 20 is 1.0, which is based on analysis of 50 ensemble members and 31 days in July</code>

## Hazard Indices
**Mapped country-wide town/ city indices, useful for a snapshot overview of acute seasonal climate hazards

Hazard indices are based on a shift-of-the-tail approach that compares daily distribution to a baseline climatology. Climate hazards indices include precipitation, drought, SPI, hail, aridity, humidity, solar, wind, heat and cold. These are scaled from 1 - 9, with the extremes in the index indicating probability shifted by 4 deciles below or above its local climatology reference, with 5 indicating the forecast is on par with baseline climate expectations for the current forecast month or season. To request this climate data, see [hazard indices example input](https://github.com/cjnankervis/Re-Climate/blob/main/Example_Requests/HazardIndices_example.json). See further [documentation](https://re-climate.co.uk/docs/hazard-indices/).

## Departures (Anomalies)
**Country-wide ASCII grid/ town or city CSV provided at a monthly granularity; a departure forecast useful for a big-picture seasonal overview

Like the monthly centiles request, anomalies provide a country-wide mapped overview of departures from an up-to-date climatology to assess whether the seasonal forecast period is likely to be warmer/ cooler or wetter/ drier than the average monthly conditions over the most recent years. To request this climate data on a regular 5km grid, see [anomalies example input](https://github.com/cjnankervis/Re-Climate/blob/main/Example_Requests/Anomalies_example.json). See further [documentation](https://re-climate.co.uk/docs/gridded-datasets/). To visualise ASCII output data please see [Visualise_ASCII.py](https://github.com/cjnankervis/Re-Climate/blob/main/Visualise_ASCII.py).

### Example C.
November precipitation anomalies plotted using Re-Climate® data issued on 13th October 2022.

### Median
<center><img src="https://seasonalforecasts.earth/wp-content/uploads/2022/11/ASCII_Plots.png" alt="Extended precipitation forecast for November 2022" width="80%"></center>

### 90th Centile
<center><img src="https://seasonalforecasts.earth/wp-content/uploads/2022/11/ASCII_Plots_90th.png" alt="Northeast and Central Scotland flooding, 90th centile of precipitation forecast for November 2022" width="80%"></center>

## Daily Weather Profiles (Reliability Plots)
**Access to figures showing town/ city daily weather profiles as decile line plots for the upcoming season, ideal for who need a quick snapshot view

Comparisons between the seasonal profile (centile distributions) of daily temperature and precipitation plotted at each decile, compared directly to the 4.5km Europen UERRA Re-Analysis climatology from 2004 to 2018. To request this climate data for a specified town or city, see [daily profiles example input](https://github.com/cjnankervis/Re-Climate/blob/main/Example_Requests/DailyProfiles_example.json).

## Graphical Summaries
**Access to figures showing town/ city daily weather ensemble summaries as box-whisker/ violin plots for the upcoming season, ideal for who need a quick snapshot view

Comparisons between the seasonal profile (centile distributions) of multiple meteorological variables, compared against WeatherLogistics' real-time equivalent model climatology. To request this climate data for a specified town or city, see [graphical summaries example input](https://github.com/cjnankervis/Re-Climate/blob/main/Example_Requests/GraphicalSummaries_example.json).

Daily precipitation return period forecast for central London covering the mid-winter 2023 period, using the "meteorological_variable": "Exceedances" option.
<center><img src="https://seasonalforecasts.earth/wp-content/uploads/2022/12/WestminsterSeasonalforecast_MTH3_09-Late-Summer2021_2021TminLondonBoroughsForecast.png" alt="Seasonal climate forecast of minimum temperature for Westminster (London), September 2022" width="80%"></center>

[Heating Degree Days for energy utility demand management, presented as a 7-day running accumulation of daily temperatures, using the "meteorological_variable": "Gdd" option](https://seasonalforecasts.earth/wp-content/uploads/2022/12/GDD.png)

<center><img src="https://seasonalforecasts.earth/wp-content/uploads/2022/12/EXCEEDANCES.png" alt="Likelihood of exceedance for daily precipitation for Bristol, Winter 2023" width="80%"></center>

## Acknowledgements

*Contains modified Copernicus Climate Change Service information 2022. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains.

## Additional Examples

Monitoring summer temperature extremes and heatwave extremes, July forecast issued on 13th June 2022

<center><img src="https://seasonalforecasts.earth/wp-content/uploads/2022/11/TMax_System2.png" alt="July 2022 temperature extremes and heatwave conditions" width="80%"></center>

Monitoring summer precipitation deficits and drought conditions, July forecast issued on 13th June 2022

<center><img src="https://seasonalforecasts.earth/wp-content/uploads/2022/11/Precip_System2.png" alt="Summer 2022 drought management and heatwave conditions" width="80%"></center>

