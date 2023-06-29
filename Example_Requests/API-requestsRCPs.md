## "Monthly Forecasts" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | <sub>**REQUIRED** geography/ mainland country area; either "uk", "spain" or "turkey"</sub> |
| instance_name    | string        | <sub>**NOT REQUIRED** necessary for tailored/ bespoke client requests only</sub> |
| latitude    | float        | <sub>**NOT REQUIRED** defaults to country-wide statistics</sub> |
| longitude    | float        | <sub>**NOT REQUIRED** defaults to country-wide statistics</sub> |
| season    | integer        | <sub>**REQUIRED** seasonal climate forecast start date/ initiation month (up to current month if after 10th day)</sub> |
| month_of_season    | integer        | <sub>**REQUIRED** seasonal climate forecast lead time of "1", "2" or "3" months (number of full months after initiation)</sub> |
| extension    | string        | <sub>**REQUIRED** "asc" for ASCII data output format</sub> |
| output_type    | string        | <sub>**REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office + ECMWF + Météo-France + NCEP + Deutscher Wetterdienst + CMCC + JMA + ECCC (Copernicus) numerical weather prediction model average |
| meteorological_variable    | string        | <sub>**REQUIRED** "tmin", "tmax", "tmean" or "precipitation" for monthly mean daily minimum, maximum and mean temperatures (degrees Celsius); or monthly accumulated precipitation (millimetres per month) respectively</sub> |
| percentile    | string        | <sub>**REQUIRED** confidence interval at either the "10th", "30th", "median", "70th" or "90th" centile</sub> |
| RCP_type    | string        | <sub>**REQUIRED**: "2.6" or "8.5", for Representative Concentration Pathways from UKCP18 models, available from July 2023 for UK only***
| projection_year    | string        | <sub>**REQUIRED** seasonal climate output is projected forward to this year. Projection years 2020 to 2030, 2030 to 2040 and 2040 to 2050 from UK Climate Projection Models 2018 available from July 2023 for the United Kingdom only</sub> |
| forecast_type    | string        | <sub>**REQUIRED** "monthly-centiles" for country-wide monthly gridded seasonal climate forecast data</sub> |
| filename    | string        | <sub>**OPTIONAL**</sub> |
| show_metadata    | string        | <sub>**OPTIONAL**</sub> | 

## "Daily Ensembles" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | <sub>**REQUIRED** geography/ mainland country area; either "uk", "spain" or "turkey" |
| instance_name    | string        | <sub>**NOT REQUIRED** necessary for tailored/ bespoke client requests only</sub> |
| latitude    | float        | <sub>**REQUIRED** latitude requirement contained within the country mainland bounding-box area, ***NOT REQUIRED FOR ZARR***</sub> |
| longitude    | float        | <sub>**REQUIRED** longitude requirement contained within the country mainland bounding-box area, ***NOT REQUIRED FOR ZARR***</sub> |
| season    | integer        | <sub>**REQUIRED** seasonal climate forecast start date/ initiation month (up to current month if after 10th day)</sub> |
| month_of_season    | integer        | <sub>**REQUIRED** "seasonal" is the only valid option which supplies 3 full months of forecasts after initiation</sub> |
| extension    | string        | <sub>**REQUIRED** "json" or "csv" for JSON/ CSV data outputs, or "zarr" for geography-wide json-style dictionary</sub> |
| output_type    | string        | <sub>**REQUIRED** "benchmark"/ "weatherlogisticsltd" options both supply statistical/ climate signal based outputs in the first 50 records, and Met Office + ECMWF + Météo-France + NCEP + Deutscher Wetterdienst + CMCC + JMA + ECCC (Copernicus) numerical weather prediction average forecasts in records 51 - 100. Additionally, a "climatology" option will supply the internal model climatology for the most recent year and season</sub> |
| meteorological_variable    | string        | <sub>**REQUIRED** "tmin", "tmax", "precipitation", "solar", "wind", "hail", "minhumidity", "maxhumidity" for daily values of: minimum and maximum temperatures (degrees Celsius), precipitation (millimetres), solar radiation (average daily W/m2), average wind speed (metres per second), hail/ precipitation intensity (millimetres per second x 1000), minimum and maximum relative humidity (%)</sub> |
| percentile    | string        | <sub>**NOT REQUIRED** entire 100 ensemble members are supplied</sub> |
| RCP_type    | string        | <sub>**REQUIRED**: "2.6" or "8.5", for Representative Concentration Pathways from UKCP18 models, available from July 2023 for UK only***
| projection_year    | string        | <sub>**REQUIRED** seasonal climate output is projected forward to this year. Projection years 2020 to 2030, 2030 to 2040 and 2040 to 2050 from UK Climate Projection Models 2018 available from July 2023 for the United Kingdom only</sub> |
| forecast_type    | string        | <sub>**REQUIRED** "ensemble" for town/ location-specific daily weather realizations at the town or city scale</sub> |
| filename    | string        | <sub>**OPTIONAL**</sub> |
| show_metadata    | string        | <sub>**OPTIONAL**</sub> | 

## "Hazard Indices" JSON request fields
See more information about the [climatological hazard reference](https://github.com/cjnankervis/Re-Climate#climatological-hazard-references)

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | <sub>**REQUIRED** Geography/ mainland country area; either "uk", "spain" or "turkey"</sub> |
| instance_name    | string        | <sub>**NOT REQUIRED** necessary for tailored/ bespoke client requests only</sub> |
| latitude    | float        | <sub>**NOT REQUIRED** defaults to country-wide statistics</sub> |
| longitude    | float        | <sub>**NOT REQUIRED** defaults to country-wide statistics</sub> |
| season    | integer        | <sub>**REQUIRED** seasonal climate forecast start date/ initiation month (up to current month if after 10th day)</sub> |
| month_of_season    | integer        | <sub>**REQUIRED** seasonal climate forecast lead time of "1" or "2" months (number of full months after initiation) or "seasonal" for average of 1 + 2 + 3 months. **Note** seasonal option is not available for wind, solar, hail and humidity variables</sub> |
| extension    | string        | <sub>**REQUIRED** "csv" for CSV/ XML type data output format or "png" or PNG for graphical download to supplied "filename"</sub> |
| output_type    | string        | <sub>**REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office + ECMWF + Météo-France + NCEP + Deutscher Wetterdienst + CMCC + JMA + ECCC (Copernicus) numerical weather prediction average</sub> |
| meteorological_variable    | string        | <sub>**REQUIRED** "hail", "solar", "wind", "aridity", "cold", "drought", "heat", "humidity", "precipitation" or "spi" for 20th/80th daily weather centile shift-of-the-tails analysis for hazards, or shift-of-the-median (50th) centile for Standard Precipitation Index (SPI) on a scale of low (1) to high (9) extreme</sub> |
| percentile    | string        | <sub>**NOT REQUIRED** shift-of-the-tail approach examines the 80th (wet or hot)/ 20th centile (dry or cold) daily ensemble </sub> |
| RCP_type    | string        | <sub>**REQUIRED**: "2.6" or "8.5", for Representative Concentration Pathways from UKCP18 models, available from July 2023 for UK only***
| projection_year    | string        | <sub>**REQUIRED** seasonal climate output is projected forward to this year. Projection years 2020 to 2030, 2030 to 2040 and 2040 to 2050 from UK Climate Projection Models 2018 available from July 2023 for the United Kingdom only</sub> |
| forecast_type    | string        | <sub>**REQUIRED** "hazard-indices" for country-wide mapped or tabular hazard indices at the town/ city level</sub> |
| filename    | string        | <sub>**OPTIONAL** optional filename for "png" extension only (default is used otherwise)</sub> |
| show_metadata    | string        | <sub>**OPTIONAL**</sub> | 

## "Daily Profiles (Deciles)" JSON request fields
See more information about the [climatological daily profile references](https://github.com/cjnankervis/Re-Climate/blob/main/README.md#daily-weather-profiles-reliability-plots)

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | <sub>**REQUIRED** Geography/ mainland country area; either "uk", "spain" or "turkey"</sub> |
| instance_name    | string        | <sub>**NOT REQUIRED** necessary for tailored/ bespoke client requests only</sub> |
| latitude    | float        | <sub>**REQUIRED** latitude requirement contained within the country mainland bounding-box area</sub> |
| longitude    | float        | <sub>**REQUIRED** longitude requirement contained within the country mainland bounding-box area</sub> |
| season    | integer        | <sub>**REQUIRED** seasonal climate forecast start date/ initiation month (up to current month if after 10th day)</sub> |
| month_of_season    | integer        | <sub>**REQUIRED** "seasonal" climate forecast provides single graphics that show data at lead times of 1, 2 and 3 months</sub> |
| extension    | string        | <sub>**REQUIRED** "png" for graphical download to supplied "filename"</sub> |
| output_type    | string        | <sub>**REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office + ECMWF + Météo-France + NCEP + Deutscher Wetterdienst + CMCC + JMA + ECCC (Copernicus) numerical weather prediction average</sub> |
| meteorological_variable    | string        | <sub>**REQUIRED** "tmin", "tmax" or "precipitation" for monthly mean daily minimum and maximum temperatures (degrees Celsius) or monthly accumulated precipitation (millimetres per month)</sub> |
| percentile    | string        | <sub>**NOT REQUIRED** all daily ensemble data is aggregated into a statistical output</sub> |
| RCP_type    | string        | <sub>**REQUIRED**: "2.6" or "8.5", for Representative Concentration Pathways from UKCP18 models, available from July 2023 for UK only***
| projection_year    | string        | <sub>**REQUIRED** seasonal climate output is projected forward to this year. Projection years 2020 to 2030, 2030 to 2040 and 2040 to 2050 from UK Climate Projection Models 2018 available from July 2023 for the United Kingdom only</sub> |
| forecast_type    | string        | <sub>**REQUIRED** "daily-profiles" for graphical plots showing deciles of daily ensemble realizations</sub> |
| filename    | string        | <sub>**OPTIONAL** optional filename for "png" extension only (default is used otherwise)</sub> |
| show_metadata    | string        | <sub>**OPTIONAL**</sub> | 

## "Graphical Summaries" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | <sub>**REQUIRED** Geography/ mainland country area; either "uk", "spain" or "turkey"</sub> |
| instance_name    | string        | <sub>**NOT REQUIRED** necessary for tailored/ bespoke client requests only</sub> |
| latitude    | float        | <sub>**REQUIRED** latitude requirement contained within the country mainland bounding-box area</sub> |
| longitude    | float        | <sub>**REQUIRED** longitude requirement contained within the country mainland bounding-box area</sub> |
| season    | integer        | <sub>**REQUIRED** seasonal climate forecast start date/ initiation month (up to current month if after 10th day)</sub> |
| month_of_season    | integer        | <sub>**REQUIRED** seasonal climate forecast start date/ initiation year (up to current year if before 11th January)</sub> |
| lead    | integer        | <sub>**REQUIRED** seasonal climate forecast lead time of "1", "2" or "3" months (number of full months after initiation) or "seasonal" for average of 1 + 2 + 3 months. **Note** that meteorological_variable "GDD" is a Seasonal only request, whereas for other meteorological variables only "1", "2" or "3" options are valid</sub> |
| extension    | string        | <sub>**REQUIRED** "png" for PNG graphical download to supplied "filename"</sub> |
| output_type    | string        | <sub>**REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office + ECMWF + Météo-France + NCEP + Deutscher Wetterdienst + CMCC + JMA + ECCC (Copernicus) numerical weather prediction average</sub> |
| meteorological_variable    | string        | <sub>**REQUIRED** "tmin", "tmax", "precipitation", "solar", "wind", "hail", "minhumidity", "maxhumidity" (or "EXCEEDANCES" or "GDD")  for daily graphical summaries of: minimum and maximum temperatures (degrees Celsius), precipitation (millimetres), solar radiation (average daily W/m2), average wind speed (metres per second), hail/ precipitation intensity (millimetres per second x 1000), minimum and maximum relative humidity (%) (or monthly profiles of precipitation return periods (frequency of occurence for millimetre per day intensities), or degree day type 7-day accumulated daily temperature (degrees Celsius)</sub> |
| percentile    | string        | <sub>**NOT REQUIRED** all daily ensemble data is aggregated into graphical plots</sub> |
| RCP_type    | string        | <sub>**REQUIRED**: "2.6" or "8.5", for Representative Concentration Pathways from UKCP18 models, available from July 2023 for UK only***
| projection_year    | string        | <sub>**REQUIRED** seasonal climate output is projected forward to this year. Projection years 2020 to 2030, 2030 to 2040 and 2040 to 2050 from UK Climate Projection Models 2018 available from July 2023 for the United Kingdom only</sub> |
| forecast_type    | string        | <sub>**REQUIRED** "graphical-summaries" for graphical summaries of daily-resolved weather ensemble data at the town/ city scale</sub> |
| filename    | string        | <sub>**OPTIONAL** user defined filename for "png" extension only (default is used otherwise)</sub> |
| show_metadata    | string        | <sub>**OPTIONAL**</sub> | 
