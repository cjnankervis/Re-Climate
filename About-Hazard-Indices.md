# How to interpret [seasonal climate forecast hazards](https://github.com/cjnankervis/Re-Climate#hazard-indices).

Seasonal climate forecasts provide probabilistic outlooks. These describe the prevailing weather conditions over the coming months. Understanding and quantifying their uncertainties helps guide decision making processes, with actionable information obtained by weighing up benefits against losses.

What a reliable seasonal forecast permits are good estimates of weather event likelihood, though they cannot be used to acquire time-specific knowledge and single value outcomes. For the latter the forecast must be deterministic, wrongly implying little or no uncertainty in the future.

Firstly, it is important to explain four bounds that restrict what is possible from a seasonal forecast.

•	Good reliability in a seasonal climate forecast implies that the event counts are proportional to their respective likelihoods of occurrence, which permits decision making

•	Extended precipitation forecasts should always be probabilistic in nature, since uncertainty is a natural outcome from mathematical constraints, noting Lorenz’s paper on prediction
[Edward Norton Lorenz, 1972 American Association for the Advancement of Sciences; 139th meeting](http://eapsweb.mit.edu/research/Lorenz/Butterfly_1972.pdf)

•	Collectively, ensemble members contain useful information about the chances of drier or wetter-than-average conditions, presented as statistics or summaries

•	Uncertainty or inconsistency between model simulations, and more volatile or changeable hydrological conditions both affect precipitation hazards. It is not possible to discern the difference between the two outcomes mathematically, while both increase hazard scores

## Drought Index
We can define an index to assess the driest 20% of collated model runs/ simulations (the ‘ensemble’), then compare this statistic to the lower quintile of local observations over at least 15 years of history.
We quantify the shift-of-the-tail to drier conditions, increasing the index value for each unit departure toward the lower tail of the precipitation distribution. 

## Precipitation Index
We can define another index to assess the wettest 20% of model runs (‘ensemble’), then compare this statistic to local observations over the same observational history. We can quantify the shift-of-the-tail to wetter daily conditions and increase the Precipitation Index upward for each unit departure toward the upper tail of the precipitation distribution.

## Standardized Precipitation Index (SPI)
The widely adopted standard measure of precipitation is based on extended accumulations of precipitation over the course of the forecast. To replicate a similar index system to other climate prediction companies, we define an index to assess the median (50th centile) of model simulations. Note here that these graphics provide users with no information about the statistical range in daily precipitation events; either precipitation excess or prolonged dry spells at the tails of the ensemble distribution. Overreliance on this single climate hazard metric is therefore likely to be misleading.

Note that for the SPI method, precipitation is also treated a a standardized value with reference to its climatology.
e.g., daily values are adjusted to (value - mean) / standard deviation

## [Analysis of hazards](https://github.com/cjnankervis/Re-Climate#hazard-indices).
With the two indices described above there are four possible seasonal climate hazards scenarios:

### A.	Drought Index > 6, Precipitation Index > 6

High hazard scenario with seasonal precipitation more ‘labile’ during the period e.g., extended dry conditions intermixed with extremes of heavier precipitation, or higher uncertainty and inconsistency between model simulations compared to average. This scenario implies more dry periods and daily precipitation extremes in the forecast.

### B.	Drought Index < 4, Precipitation Index < 4

Low hazard scenario with seasonal precipitation likely to be less variable (largely unchangeable) during the period e.g., consistently damp or moderately wet conditions with no extremes of heavier precipitation, or higher confidence in the model simulations centred around the climatological average. This scenario implies lower chances of extended dry periods and daily precipitation extremes.

### C.	Drought Index > 6, Precipitation Index < 4

Mixed scenario with a dry bias. Extended periods of dry weather are more likely than average, with a reduced likelihood and/ or intensity of extreme precipitation events with fewer wet ensemble members.

### D.	Drought Index < 4, Precipitation Index > 6

Mixed scenario with a wet bias. Extended dry periods are less likely than average, with a higher-than-average likelihood and/ or intensity of extreme precipitation events with more wet ensemble members.

## Graphics showing a worked example

<img src="https://re-climate.earth/wp-content/uploads/2023/01/Precip_Index.png" width="60%">
<img src="https://re-climate.earth/wp-content/uploads/2023/01/Drought_Index.png" width="60%">

<sub><b>Figure 1. Seasonal climate forecasts showing Precipitation Index (80th centile shift-of-the-tail, top) and Drought Index (20th centile shift-of-the-tail, bottom) for the same month annotated with analysis of hazards. High hazard scenario (A), Low hazard scenario (B), Mixed scenario with a dry bias (C), Mixed scenario with a wet bias (D).</b></sub>

<img src="https://re-climate.earth/wp-content/uploads/2023/01/SPI_Index.png" width="60%">

<sub><b>Figure 2. Seasonal climate forecasts showing Standardized Precipitation Index (50th centile analysis) for the same month's forecast as Figure 1. The figure indicates that in terms of total monthly accumulated precipitation the English Midlands and Northeast England are likely to be wetter-than-average.</b></sub>
