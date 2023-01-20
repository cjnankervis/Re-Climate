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
We define an index to assess the driest 20% of collated model runs/ simulations (the ‘ensemble’), then compare this statistic to the lower quintile of local observations over at least 15 years of history.
We quantify the shift-of-the-tail to drier conditions, increasing the index value for each unit departure toward the lower tail of the precipitation distribution. Figure 3 (top) shows an example forecast for this index, noting that analyses should be combined with information from other hydrological indices.

## Precipitation Index
We define another index to assess the wettest 20% of model runs (‘ensemble’), then compare this statistic to local observations over the same observational history. We can quantify the shift-of-the-tail to wetter daily conditions and increase the Precipitation Index upward for each unit departure toward the upper tail of the precipitation distribution. Figure 3 (bottom) shows an example forecast for this index, noting that analyses should be combined with the Drought Index and Standard Precipitation Index.

## Standardized Precipitation Index (SPI)
One measure of precipitation is to accumulate precipitation over the course of the seasonal climate forecast. However, we define an SPI as the median (50th centile) of daily weather simulations. When using a median value as a measure of precipitation the shape of the distribution curve proves especially problematic. The SPI index, combined with our other hydrological indices, can be used to evaluate the predicted skewness of daily precipitation events.

With expert analysis, hazard indices can help support flood and drought operations on seasonal timescales, which is unique offering of the Re-Climate® prediction system. Figure 4 shows an example of SPI mapped onto Environment Agency rainfall gauge sites, which provides additional information to indices presented in Figure 3.

As a demonstration of skewness, Figures 1 and 2 (below) present two precipitation intensity plots from a plausible forecast compared to a daily climatology. Figure 1 shows a drier-than-average season associated with **anticyclonic conditions**. This more often results in a low SPI Index with neither precipitation extremes nor prolonged dry spells likely. However, counterintuitively, this can present itself with a negative kurtosis (broader tailed distribution). For example, **Tropical Continental Air Mass** events often lead to occasional severe supercell events; thunderstorms, hail and surface water flooding in the hottest and often driest summers.

Conversely, Figure 2 shows a negative skew (i.e., outcomes with generally more wet day extremes), commonly associated with a tendency toward a **Maritime Air Mass**. 

For more information see further parameterization and methodologies in [meteorological definitions](https://github.com/cjnankervis/Re-Climate/blob/main/Meteorological_Definitions.md#hazard-indices)

<img src="https://re-climate.earth/wp-content/uploads/2023/01/Positive_Skew.png" width="70%">

<sub><b>Figure 1. Forecasted frequency of daily precipitation plotted against their intensities (black curve) with median value (black dashed line) for a positive skew/ dry event bias. Monthly observations for the same location are shown in orange. In this example heavier precipitation events are less likely (Precipitation Index < 4), dry periods are more likely (Drought Index > 6), while the median ‘average’ of daily precipitation is less than the climatological average (SPI < 4).</b></sub>
  
<img src="https://re-climate.earth/wp-content/uploads/2023/01/Negative_Skew.png" width="70%">

<sub><b>Figure 2. As in Figure 1, but with a negative skew/ wet event bias. Heavier daily precipitation events are more likely in this example (Precipitation Index > 6), dry periods are less likely (Drought Index < 4), while the median of daily precipitation is more than the monthly climatological average at the same location (SPI > 6).</b></sub>

## [Analysis of climate hazards](https://github.com/cjnankervis/Re-Climate#hazard-indices).
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

<img src="https://re-climate.earth/wp-content/uploads/2023/01/Precip_Index.png" width="70%">
<img src="https://re-climate.earth/wp-content/uploads/2023/01/Drought_Index.png" width="70%">

<sub><b>Figure 3. Seasonal climate forecasts showing Precipitation Index (80th centile shift-of-the-tail, top) and Drought Index (20th centile shift-of-the-tail, bottom) annotated with analysis of hazards. High hazard scenario (A), Low hazard scenario (B), Mixed scenario with a dry bias (C), Mixed scenario with a wet bias (D).</b></sub>

<img src="https://re-climate.earth/wp-content/uploads/2023/01/SPI_Index.png" width="63%">

<sub><b>Figure 4. Seasonal climate forecasts showing Standardized Precipitation Index (50th centile analysis) for the same month's forecast as Figure 1. The forecast shows that in terms of the central likelihood value for daily precipitation intensity the English Midlands and Northeast England may see more rainy days than usual even though the chances of extreme downpours is reduced (see negative skew in Figure 2). Southeast England on the other hand likely to experience less rainy days and more dry days than average, though according to the Precipitation Index shows a higher-than-average chance of extreme daily precipitation events (indicated in Figure 1). For this region (marked ‘D’ in Figure 3) a positive skew is likely to increase the total accumulated precipitation toward a wetter-than-average season.</b></sub>
