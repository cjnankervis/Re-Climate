## "Monthly Centiles" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | **REQUIRED** geography/ mainland country area; either "uk", "spain" or "turkey" |
| instance_name    | string        | **NOT REQUIRED** necessary for tailored/ bespoke client requests only
| latitude    | float        | **NOT REQUIRED** defaults to country-wide statistics |
| longitude    | float        | **NOT REQUIRED** defaults to country-wide statistics |
| month    | integer        | **REQUIRED** seasonal climate forecast release/ initiation month (up to current month if after 13th day) |
| year    | integer        | **REQUIRED** seasonal climate forecast release/ initiation year (up to current year if before 14th January) |
| lead    | integer        | **REQUIRED** seasonal climate forecast lead time of "1", "2" or "3" months (number of full months after initiation) |
| extension    | string        | **REQUIRED** "asc" for ASCII data output format |
| output_type    | string        | **REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office + ECMWF + Météo-France multi-model average |
| meteorological_variable    | string        | **REQUIRED** "tmin", "tmax", "tmean" or "precipitation" for monthly mean daily minimum and maximum temperatures (degrees Celsius) or monthly accumulated precipitation (millimetres per month) |
| percentile    | string        | **REQUIRED** confidence interval at either the "10th", "30th", "median", "70th" or "90th" centile |
| projection_year    | string        | **NOT REQUIRED** seasonal climate output is projected forward to this year |
| forecast_type    | string        | **REQUIRED** "monthly-centiles" for country-wide monthly gridded seasonal climate forecast data |
| filename    | string        | **NOT REQUIRED** |
| show_metadata    | string        | **NOT REQUIRED** | 

## "Daily Ensembles" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | **REQUIRED** geography/ mainland country area; either "uk", "spain" or "turkey" |
| instance_name    | string        | **NOT REQUIRED** necessary for tailored/ bespoke client requests only
| latitude    | float        | **REQUIRED** latitude requirement contained within the country mainland bounding-box area |
| longitude    | float        | **REQUIRED** longitude requirement contained within the country mainland bounding-box area |
| month    | integer        | **REQUIRED** seasonal climate forecast release/ initiation month (up to current month if after 13th day) |
| year    | integer        | **REQUIRED** seasonal climate forecast release/ initiation year (up to current year if before 14th January) |
| lead    | integer        | **REQUIRED** "seasonal" is the only valid option which supplies 3 full months of forecasts after initiation |
| extension    | string        | **REQUIRED** "json" or "csv" for JSON/ CSV data outputs|
| output_type    | string        | **REQUIRED** "benchmark"/ "weatherlogisticsltd" options both supply statistical/ climate signal based outputs in the first 50 records, and Met Office + ECMWF + Météo-France multi-model average forecasts in records 51 - 100. Additionally, a "climatology" option will supply the internal model climatology for the most recent year and season |
| meteorological_variable    | string        | **REQUIRED** "tmin", "tmax", "precipitation", "solar", "wind", "hail", "minhumidity", "maxhumidity" for daily values of: minimum and maximum temperatures (degrees Celsius), precipitation (millimetres), solar radiation (average daily W/m2), average wind speed (metres per second), hail/ precipitation intensity (millimetres per second x 1000), minimum and maximum relative humidity (%) |
| percentile    | string        | **NOT REQUIRED** entire 100 ensemble members are supplied |
| projection_year    | string        | **NOT REQUIRED** seasonal climate output is projected forward to this year |
| forecast_type    | string        | **REQUIRED** "ensemble" for town/ location-specific daily weather realizations at the town or city scale |
| filename    | string        | **NOT REQUIRED** |
| show_metadata    | string        | **NOT REQUIRED** | 

## "Hazard Indices" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | **REQUIRED** Geography/ mainland country area; either "uk", "spain" or "turkey" |
| instance_name    | string        | **NOT REQUIRED** necessary for tailored/ bespoke client requests only
| latitude    | float        | **NOT REQUIRED** defaults to country-wide statistics |
| longitude    | float        | **NOT REQUIRED** defaults to country-wide statistics |
| month    | integer        | **REQUIRED** seasonal climate forecast release/ initiation month (up to current month if after 13th day) |
| year    | integer        | **REQUIRED** seasonal climate forecast release/ initiation year (up to current year if before 14th January) |
| lead    | integer        | **REQUIRED** seasonal climate forecast lead time of "1" or "2" months (number of full months after initiation) or "seasonal" for average of 1 + 2 + 3 months |
| extension    | string        | **REQUIRED** "csv" or "png" for CSV/ XML type data output format or PNG for graphical download to supplied "filename" |
| output_type    | string        | **REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office +ECMWF + Météo-France multi-model average |
| meteorological_variable    | string        | **REQUIRED** "hail", "solar", "wind", "aridity", "cold", "drought", "heat", "humidity", "precipitation" or "spi" for 20th/80th daily weather centile shift-of-the-tails analysis for hazards, or shift-of-the-median (50th) centile for Standard Precipitation Index (SPI) on a scale of low (1) to high (9) extreme |
| percentile    | string        | **REQUIRED** confidence interval at either the "10th", "30th", "median", "70th" or "90th" centile|
| projection_year    | string        | **NOT REQUIRED** seasonal climate output is projected forward to this year |
| forecast_type    | string        | **REQUIRED** "hazard-indices" for country-wide mapped or tabular hazard indices at the town/ city level |
| filename    | string        | **NOT REQUIRED** optional filename for "png" extension only (default is used otherwise) |
| show_metadata    | string        | **NOT REQUIRED** | 

## "Anomalies" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | **REQUIRED** Geography/ mainland country area; either "uk", "spain" or "turkey" |
| instance    | string        | **NOT REQUIRED** necessary for tailored/ bespoke client requests only
| latitude    | float        | **NOT REQUIRED** defaults to country-wide statistics |
| longitude    | float        | **NOT REQUIRED** defaults to country-wide statistics |
| month    | integer        | **REQUIRED** seasonal climate forecast release/ initiation month (up to current month if after 13th day) |
| year    | integer        | **REQUIRED** seasonal climate forecast release/ initiation year (up to current year if before 14th January) |
| lead    | integer        | **REQUIRED** seasonal climate forecast lead time of "1", "2" or "3" months (number of full months after initiation) |
| extension    | string        | **REQUIRED** "csv" or "asc" for CSV/ XML type data, or ascii output format |
| output_type    | string        | **REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office +ECMWF + Météo-France multi-model average |
| meteorological_variable    | string        | **REQUIRED** "Tmean" or "Precipitation" for monthly mean daily temperature average departure from model climate (degrees Celsius) or monthly accumulated daily precipitation departure (millimetres per month) |
| percentile    | string        | **REQUIRED** confidence interval at either the "10th", "30th", "median", "70th" or "90th" centile |
| projection_year    | string        | **NOT REQUIRED** seasonal climate output is projected forward to this year |
| forecast_type    | string        | **REQUIRED** "anomaly" for country-wide monthly gridded seasonal climate forecast departure map data |
| filename    | string        | **NOT REQUIRED** |
| show_metadata    | string        | **NOT REQUIRED** | 

## "Daily Profiles (Deciles)" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | **REQUIRED** Geography/ mainland country area; either "uk", "spain" or "turkey" |
| instance_name    | string        | **NOT REQUIRED** necessary for tailored/ bespoke client requests only
| latitude    | float        | **REQUIRED** latitude requirement contained within the country mainland bounding-box area |
| longitude    | float        | **REQUIRED** longitude requirement contained within the country mainland bounding-box area |
| month    | integer        | **REQUIRED** seasonal climate forecast release/ initiation month (up to current month if after 13th day) |
| year    | integer        | **REQUIRED** seasonal climate forecast release/ initiation year (up to current year if before 14th January) |
| lead    | integer        | **REQUIRED** "seasonal" climate forecast provides single graphics that show data at lead times of 1, 2 and 3 months |
| extension    | string        | **REQUIRED** "png" for graphical download to supplied "filename" |
| output_type    | string        | **REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office +ECMWF + Météo-France multi-model average |
| meteorological_variable    | string        | **REQUIRED** "tmin", "tmax" or "precipitation" for monthly mean daily minimum and maximum temperatures (degrees Celsius) or monthly accumulated precipitation (millimetres per month) |
| percentile    | string        | **NOT REQUIRED** all daily ensemble data is aggregated into a statistical output |
| projection_year    | string        | **NOT REQUIRED** seasonal climate output is projected forward to this year |
| forecast_type    | string        | **REQUIRED** "daily-profiles" for graphical plots showing deciles of daily ensemble realizations |
| filename    | string        | **NOT REQUIRED** optional filename for "png" extension only (default is used otherwise)
| show_metadata    | string        | **NOT REQUIRED** | 

## "Graphical Summaries" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | **REQUIRED** Geography/ mainland country area; either "uk", "spain" or "turkey" |
| instance_name    | string        | **NOT REQUIRED** necessary for tailored/ bespoke client requests only
| latitude    | float        | **REQUIRED** latitude requirement contained within the country mainland bounding-box area |
| longitude    | float        | **REQUIRED** longitude requirement contained within the country mainland bounding-box area |
| month    | integer        | **REQUIRED** seasonal climate forecast release/ initiation month (up to current month if after 13th day) |
| year    | integer        | **REQUIRED** seasonal climate forecast release/ initiation year (up to current year if before 14th January) |
| lead    | integer        | **REQUIRED** seasonal climate forecast lead time of "1", "2" or "3" months (number of full months after initiation) or "seasonal" for average of 1 + 2 + 3 months. **Note** that meteorological_variable "GDD" is a Seasonal only product, whereas for other meteorological variables only "1", "2" or "3" options are valid |
| extension    | string        | **REQUIRED** "png" for PNG graphical download to supplied "filename" |
| output_type    | string        | **REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office +ECMWF + Météo-France multi-model average |
| meteorological_variable    | string        | **REQUIRED** "tmin", "tmax", "precipitation", "solar", "wind", "hail", "minhumidity", "maxhumidity" (or "EXCEEDANCES" or "GDD")  for daily graphical summaries of: minimum and maximum temperatures (degrees Celsius), precipitation (millimetres), solar radiation (average daily W/m2), average wind speed (metres per second), hail/ precipitation intensity (millimetres per second x 1000), minimum and maximum relative humidity (%) (or monthly profiles of precipitation return periods (frequency of occurence for millimetre per day intensities), or degree day type 7-day accumulated daily temperature (degrees Celsius) |
| percentile    | string        | **NOT REQUIRED** all daily ensemble data is aggregated into graphical plots |
| projection_year    | string        | **NOT REQUIRED** seasonal climate output is projected forward to this year |
| forecast_type    | string        | **REQUIRED** "graphical-summaries" for graphical summaries of daily-resolved weather ensemble data at the town/ city scale |
| filename    | string        | **NOT REQUIRED** optional filename for "png" extension only (default is used otherwise)
| show_metadata    | string        | **NOT REQUIRED** | 
