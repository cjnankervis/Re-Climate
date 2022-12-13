## Catalog fields

| Element         | Type          | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| type            | string        | **REQUIRED.** Set to `Catalog` if this Catalog only implements the Catalog spec. |
| stac_version    | string        | **REQUIRED.** The STAC version the Catalog implements. |
| stac_extensions | \[string]     | A list of extension identifiers the Catalog implements.                 |
| id              | string        | **REQUIRED.** Identifier for the Catalog.                    |
| title           | string        | A short descriptive one-line title for the Catalog.          |
| description     | string        | **REQUIRED.** Detailed multi-line description to fully explain the Catalog. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| links           | [[Link Object](#link-object)] | **REQUIRED.** A list of references to other documents.       |

{
"country": "uk" | "spain" | "turkey",
"latitude": {defaults to country-wide statistics},
"longitude": {defaults to country-wide statistics},
"month": {forecast valid/ release month},
"year": {forecast valid/ release year},
"lead": "1" | "2" | "3",
"extension": "asc",
"output_type": "weatherlogisticsltd" | "benchmark",
"meteorological_variable": "tmin" | "tmax" | "tmean" | "precipitation",
"percentile": "10th" | "30th" | "median" | "70th" | "90th",
"projection_year": {default is forecast release year},
"forecast_type": "monthly-centiles",
"show_metadata": ""
}

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
