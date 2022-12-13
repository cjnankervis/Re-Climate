## "Monthly Centiles" JSON request fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| country           | string        | **REQUIRED** Geography/ mainland country area; either "uk", "spain" or "turkey" |
| latitude    | float        | **NOT REQUIRED** |
| longitude    | float        | **NOT REQUIRED** |
| month    | integer        | **REQUIRED** seasonal climate forecast release/ initiation month (up to current month if after 13th day)|
| year    | integer        | **REQUIRED** seasonal climate forecast release/ initiation year (up to current year if before 14th January)|
| lead    | integer        | **REQUIRED** seasonal climate forecast lead time in months (number of full months after initiation)|
| extension    | string        | **REQUIRED** "asc" for ASCII data output format|
| output_type    | string        | **REQUIRED** "weatherlogisticsltd" for statistical/ climate signal based output; or "benchmark" for Met Office/ ECMWF/ Météo-France multi-model average|
| percentile    | string        | **REQUIRED** confidence interval at either the "10th", "30th", "median", "70th" or "90th" centile|
| projection_year    | string        | **NOT REQUIRED** seasonal climate output is projected forward to this year|
| forecast_type    | string        | **REQUIRED** "monthly-centiles" for country-wide monthly gridded data |
| show_metadata    | string        | **NOT REQUIRED** | 

Daily Ensembles
- JSON keywords

{
"country": "uk" | "spain" | "turkey",
"latitude": {latitude within country bounding box},
"longitude": {longitude within country bounding box},
"month": {forecast valid/ release month},
"year": {forecast valid/ release year},
"lead": "seasonal",
"extension": "json" | "csv",
"output_type": "weatherlogisticsltd" | "benchmark",
"meteorological_variable": "tmin" | "tmax" | "precipitation" | "solar" | "wind" | "hail" | "minhumidity" | "maxhumidity",
"percentile": {no percentile is required},
"projection_year": {default is forecast release year},
"forecast_type": "ensemble",
"show_metadata": ""
}

Hazard Indices
- JSON keywords

{
"country": "uk" | "spain" | "turkey",
"latitude": {defaults to country-wide statistics},
"longitude": {defaults to country-wide statistics},
"month": {forecast valid/ release month},
"year": {forecast valid/ release year},
"lead": "1" | "2" | "seasonal",
"extension": "csv" | "png",
"output_type": "weatherlogisticsltd" | "benchmark",
"meteorological_variable": "Hail" | "Solar" | "Wind" | "Aridity" | "Cold" | "Drought" | "Heat" | "Humidity" | "Precipitation" | "Spi"
"percentile": {no percentile is required},
"projection_year": {default is forecast release year},
"forecast_type": "hazard-indices",
"show_metadata": ""
"filename": "{output filename}.png"
}

Anomalies
- JSON keywords

{
"country": "uk" | "spain" | "turkey",
"latitude": {defaults to country-wide statistics},
"longitude": {defaults to country-wide statistics},
"month": {forecast valid/ release month},
"year": {forecast valid/ release year},
"lead": "1" | "2" | "3",
"extension": "asc" | "csv",
"output_type": "weatherlogisticsltd" | "benchmark",
"meteorological_variable": "Tmean | "Precipitation",
"percentile": "10th" | "30th" | "median" | "70th" | "90th",
"projection_year": {default is forecast release year},
"forecast_type": "anomaly",
"show_metadata": ""
}

Daily Profiles (Deciles)
- JSON keywords

{
"country": "uk" | "spain" | "turkey",
"latitude": {latitude within country bounding box},
"longitude": {longitude within country bounding box},
"month": {forecast valid/ release month},
"year": {forecast valid/ release year},
"lead": "seasonal",
"extension": "png",
"output_type": "weatherlogisticsltd" | "benchmark",
"meteorological_variable": "tmin" | "tmax" | "precipitation",
"percentile": {no percentile is required},
"projection_year": {default is forecast release year},
"forecast_type": "daily-profiles",
"filename": "{output filename}.png"
}

Graphical Summaries
- JSON keywords

{
"country": "uk" | "spain" | "turkey",
"latitude": {latitude within country bounding box},
"longitude": {longitude within country bounding box},
"month": {forecast valid/ release month},
"year": {forecast valid/ release year},
"lead": "1" | "2" | "3" | "seasonal", {*NOTE* GDD is a Seasonal only product, whereas for other meteorological variables lead 1, 2 or 3 are valid}
"extension": "png",
"output_type": {not required since output includes both weatherlogisticsltd and benchmark),
"meteorological_variable": "tmin" | "tmax" | "precipitation" | "solar" | "wind" | "hail" | "minhumidity" | "maxhumidity" | "EXCEEDANCES" | "GDD",
"percentile": {no percentile is required},
"projection_year": {default is forecast release year},
"forecast_type": "graphical-summaries",
"filename": "{output filename}.png"
}
