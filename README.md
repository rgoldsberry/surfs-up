# surfs-up
Data Analysis Bootcamp - Week 9

## Overview

The purpose of this project was to analyze weather data collected at 9 different observatories over the island of Oahu to determine if the island would be a suitable location for a "Surf and Shake" shop selling shakes and surfboards. 

During the lesson we created a few figures to look at the amount of rainfall throughout the year, high and low temperatures, and built a simple site using Flask for people to pull the data and look at it themselves.

For the challenge we had two deliverables to create:
> - The descriptive statistics of all data points collected in the month of June
> - The descriptive statistics of all data points collected in the month of December


## Resources

- Data Source: [hawaii.sqlite](hawaii.sqlite)

- Software: Python 3.7.13, Jupyter Notebook 6.4.8

## Results

### Provide a bulleted list with three major points from the two analysis deliverables:

1. Assuming June and December are near the extremes for temperature conditions in Hawaii, Oahu seems to have a narrow band of temperatures. June has an average temp of 74.94 degF and a standard deviation of 3.26 degF, while December has an average temp of 71.04 degF and a standard deviation of 3.75 degF. This sort of stable predictability should be a plus for an outdoors-y store.

2. After looking at the mean and standard deviation it's natural to consider what the median is saying. The median temperature in December is 71 degF and the median in June is 75 degF. Both being so close to the mean of their respective months means there probably aren't a lot of outliers dragging those means away and tell the same story of pretty stable comfortable weather. And again, both being in the 70s should mean there are plenty of "outdoor" days in those months where people will be out and about and able to walk into the store.

3. If the investors are worried seeing the low temp of 56 in December, we can point to the 25th percentile temperature of 69 degrees and reassure them that in an average December we could expect 75% of days to come in at or above ~70 degrees so don't fear for more than a week or so of "cold" days.


## Summary

### Provide a high-level summary of the results:

As stated above, Oahu seems to have a pretty stable, narrow temperature range that it stays in, and it should be fairly conducive to a Surf and Shake shop.

### Provide two additional queries that you would perform to gather more weather data for June and December:

1. I'd create the same two dataframes but with precipitation totals to see if there is a concern about rain during these months. The following queries accomplish that:

        june_prcp = session.query(Measurement.prcp).\
        where(extract('month', Measurement.date) == 6).all()

        dec_prcp = session.query(Measurement.prcp).\
        where(extract('month', Measurement.date) == 12).all()

2. I'd go the extra step and create a summary dataframe that shows the min/avg/max temps for all twelve months instead of just June and December. Since we're just showing min/mean/max it would be a good supplement to the more detailed June and December summaries. The following code accomplishes that:

        # specify columns and run query
        cols = [extract('month', Measurement.date), func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs), 1), func.max(Measurement.tobs)]

        results = session.query(*cols)\
            .group_by(extract('month', Measurement.date)).all()

        # convert to dataframe, change month numbers to names, display
        temps_by_month = pd.DataFrame(results, columns=['Month', 'Min Temp', 'Avg Temp', 'Max Temp'])

        temps_by_month['Month'] = [datetime.datetime.strptime(str(month), "%m").strftime("%B") for month in temps_by_month['Month']]

        temps_by_month.set_index('Month', inplace=True)

        temps_by_month
