# Plots

Collection of unrefined plots of mainly three segments of data, runs 1300-1450, runs 1700-1950, and runs 2500-2800

**Plots that demonstrate clear correlation between HV and Temperature**

2597-2615:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/2597-2615.png" width="50%" height="50%">

2612-2630:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/2612-2630.png" width="50%" height="50%">

2636-2642:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/2636-2642.png" width="50%" height="50%">

2647-2661:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/2647-2661.png" width="50%" height="50%">

2723-2741:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/2723-2741.png" width="50%" height="50%">

2742-2760:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/2742-2760.png" width="50%" height="50%">


**Plots that demonstrate questionable correlation**

1302-1326:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/1302-1326.png" width="50%" height="50%">

1357-1375:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/1357-1375.png" width="50%" height="50%">

1376-1394:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/1376-1394.png" width="50%" height="50%">

1450-1432:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/1450-1432.png" width="50%" height="50%">

1856-1763:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/1856-1763.png" width="50%" height="50%">


**Plots that demonstrate very little correlation**

1726-1744:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/1726-1744.png" width="50%" height="50%">

1745-1763:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/1745-1763.png" width="50%" height="50%">

1950-1856:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/1950-1856.png" width="50%" height="50%">


*Uninteresting plots*

2704-2722:
<img src="https://github.com/EdgarMao/DavidStuartLab/blob/master/MilliQan_Temperature-HV_Plotting/Plots/2704-2722.png" width="50%" height="50%">


**General Observations**

Runs 2500-2800 provide useful insights on the correlation between HV data and temperature data due to the frequent variation in HV settings in these runs; since the other two segments (runs 1300-1450 and runs 1700-1950) have a rather consistent HV setting, those plots might not be as useful for identifying the correlation bewteen HV data and temperature data. However, the data in runs 1300-1450 and runs 1700-1950 seem to be presenting some useful information about other potential factors that may influence the temperature of the sensor's environment by excluding the HV setting factor.

Based on the limited data in runs 2500-2800, I made a rough calulation that the change of every 200V in HV setting would lead to an estimated change of 1 degree celcius in temperature of the environment (ratio 200:1). To make inferences further than a rough estimation, I need to work on the followings:

- Obtain more refined plots of for more complete sets of data
- Get a better understanding of possible factors that may influence the temperature data, compare them with the plots at hand
- Create scatter plots with linear (possibly higher order) fits to provide a statistically vaild estiamtion of the relationship between HV and temperature data


In order to start using this data to estimate dark photon counts in MilliQan runs, my current plan is the following:

- Refine the plotting prorgam, obtain a statically valid fit of HV in relation to temperature
- Obtain data on the prepulse of different runs and establish potential correlations
- Plot dark count in relationship to HV settings and/or temperature
