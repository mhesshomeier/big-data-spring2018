# Problem Set 2: Intro to Pandas

Building off the in-class workshop, this problem set will require you to use some of Python's data wrangling functions and produce a few simple plots with Matplotlib. These plots will help us begin to think about how the aggregated GPS data works, how it might be useful, and how it might fall short.

## What to Submit

Create a duplicate of this file (`PSet2_pandas_intro.md`) in the provided 'submission' folder; your solutions to each problem should be included in the `python` code block sections beneath the 'Solution' heading in each problem section.

Be careful! We have to be able to run your code. This means that if you, for example, change a variable name and neglect to change every appearance of that name in your code, we're going to run into problems.

## Graphic Presentation

Make sure to label all the axes and add legends and units (where appropriate).

## Code Quality

While code performance and optimization won't count, all the code should be highly readable, and reusable. Where possible, create functions, build helper functions where needed, and make sure the code is self-explanatory.

## Preparing the Data

You'll want to make sure that your data is prepared using the procedure we followed in class. The code is reproduced below; you should simply be able to run the code and reproduce the dataset with well-formatted datetime dates and no erroneous hour values.

```python
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# This line lets us plot on our ipython notebook
%matplotlib inline

# Read in the data

df = pd.read_csv('data/skyhook_2017-07.csv', sep=',')

# check it output
df.head
## check out the data types
df.dtypes
## check out the shape
df.shape
# columns
df.columns
type(df.columns)


bastille = df[df['date'] == '2017-07-14']
bastille.head


# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['date_new'].head

# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

#check it out
df['weekday'].head

# range
range(0,10,1)


# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.
# df[df['date'] == '2017-07-10'].groupby('hour')['count'].sum()
for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    ( (df['hour'] < j) & (df['hour'] > i + 18) ) |
    ( (df['hour'] > i + 18 ) & (df['hour'] < j) )
    )
    ].index, inplace = True)
  else:
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    (df['hour'] < j) | (df['hour'] > i + 18 )
    )
    ].index, inplace = True)

```
## when i = 0, J is 163,
## go through and write out values while constructing the iterator
## range (163,167,1)? with what? 19,24,1?



## Problem 1: Create a Bar Chart of Total Pings by Date

Your first task is to create a bar chart (not a line chart!) of the total count of GPS pings, collapsed by date.
You'll have to use `.groupby` to collapse your table on the grouping variable and choose how to aggregate the `count` column.
Your code should specify a color for the bar chart and your plot should have a title.
Check out the [Pandas Visualization documentation](https://pandas.pydata.org/pandas-docs/stable/visualization.html) for some guidance regarding what parameters you can customize and what they do.

### Solution

#df.plot for the plot, kind = bar to make it a bar chart (?), group count by date

```python

df.groupby(['date_new'])['count'].sum().plot(kind = "bar", color = 'red', title = 'gps pings by date')


# problem 6
# This bar chart of GPS pings by date makes it clear that on 7-24-17 utilization of the skyhook service declined dramatically, unfortunately,
# even though the visulaization makes this trend clear, there's nothing in the data that might explain this precipitous drop. This lack of information
# highlights a shortcoming in the data in that we don't have full information about the dataset that might explain this drop in skyhook gps utilization.
# Metadata for the dataset might help explain the drop as would a better understanding of skyhook and why people use it. This chart might help identify
# climate change vulnerabilities by showing us how many people (at least, how many people using GPS) are in Boston on certain days, which could help
# planners understand how many people are in the city during disaster events.
```




```

## Problem 2: Modify the Hours Column

Your second task is to further clean the data. While we've successfully cleaned our data in one way
(ridding it of values that are outside the 24-hour window that correspond to a given day of the week)
it will be helpful to restructure our `hour` column in such a way that hours are listed in a more familiar 24-hour range.
To do this, you'll want to more or less copy the structure of the code we used to remove data from hours outside of a given day's
24-hour window. You'll then want to use the [DataFrame's `replace` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.replace.html).
Note that you can use lists in both `to_replace` and `value`.

After running your code, you should have either a new column in your DataFrame or new values in the 'hour' column.
These should range from 0-23. You can test this out in a couple ways; the simplest is probably to `df['hour'].unique()`;
if you're interested in seeing sums of total pings by hour, you can run `df.groupby('hour')['count'].sum()`.

### Solution

```python

for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df['hour'].replace(range(j, j + 5, 1), range(-5, 0, 1), inplace=True)
    df['hour'].replace(range(i, i + 19, 1), range(0, 19, 1), inplace=True)
  else:
    df['hour'].replace(range(j, j + 24, 1), range(-5, 19, 1), inplace=True)

```

## Problem 3: Create a Timestamp Column

Now that you have both a date and a time (stored in a more familiar 24-hour range),
you can combine them to make a single timestamp. Because the columns in a `pandas` DataFrames are vectorized,
this is a relatively simple matter of addition, with a single catch:
you'll need to use `pd.to_timedelta` to convert your hours columns to a duration.

### Solution

```python
df['timestamp'] = df['date_new'] + pd.to_timedelta(df['hour'], unit = 'h')
df.head()
```

## Problem 4: Create Two Line Charts of Activity by Hour

Create two more graphs. The first should be a **line plot** of **total activity** by your new `timestamp` field
---in other words a line graph that displays the total number of GPS pings in each hour over the course of the week.
The second should be a **bar chart** of **summed counts** by hours of the day---in other words,
a bar chart displaying the sum of GPS pings occurring across locations for each of the day's 24 hours.

### Solution

```python
df.groupby(['timestamp'])['count'].sum().plot(color = "purple", title = 'GPS pings by timestamp')
df.groupby(['hour'])['count'].sum().plot(kind = 'bar', color = "green", title = 'gps pings by hour of the day')
```
# problem 6
# The chart of GPS pings by hour of the day shows that hours -1 through 5, have precipitously fewer gps pings, possibly indicating that
# people are less likely to travel (and therefore use GPS) during those hours. Though, as with the gps pings by date bar chart, the lack of
# metadata explaining this info and what it represents significantly limits our understanding of what the decrease in pings means. Certainly
# people are much less likely to use the GPS service between -1 through 5. If the data does indicate times when people are more or less
# likely to be traveling then it might help climate planners understand when people are out of the houses, on the roads and sidewalks.
# This could help planners know when weather events might be riskier for travelers or when transit agencies can implement climate change ready
# infrastructure.


## Problem 5: Create a Scatter Plot of Shaded by Activity

Pick three times (or time ranges) and use the latitude and longitude to produce scatterplots of each.
In each of these scatterplots, the size of the dot should correspond to the number of GPS pings.
Find the [Scatterplot documentation here]
(http://pandas.pydata.org/pandas-docs/version/0.19.1/visualization.html
#scatter-plot). You may also want to look into how to specify a pandas Timestamp (e.g., pd.Timestamp)
#so that you can write a mask that will filter your DataFrame appropriately.
#Start with the [Timestamp documentation](https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timestamps-vs-time-spans)!

```python
time1 = df[df['timestamp'] == '2017-07-01 09:00:00']
time1.head()
time1.plot.scatter(x="lat", y="lon", color = 'orange', title = 'gps locations at 9:00 on july 1', s=time1['count']*0.5)


time2 = df[df['timestamp'] == '2017-07-01 10:00:00']
time2.head()
time2.plot.scatter(x="lat", y="lon", color = 'purple', title = 'gps locations at 10:00 on july 1', s=time1['count']*0.5)

time3 = df[df['timestamp'] == '2017-07-01 11:00:00']
time3.head()
time3.plot.scatter(x="lat", y="lon", color = 'black', title = 'gps locations at 11:00 on july 1', s=time1['count']*0.5)
```
# problem 6
# These scatter plots of latitude and longitude data together show that pings across the
# city decrease as the night goes on, with the smallest concentration of pings at 10:00 on the 1st. A
# weakness of the data is that it doesn't have a basemap (though that's more of a weakness of my own skills rather than the
# completeness of the data) so it's hard to place the gps pings in a way that's understandable. This location data could be
# incredibly useful for climate change planners in understanding where people are at different times of day (or different days throughout the year)
# and like the previous visualizations that would help planners understand where people might be during adverse weather events.




## Problem 6: Analyze Your (Very) Preliminary Findings

For three of the visualizations you produced above, write a one or two paragraph analysis that identifies:

1. A phenomenon that the data make visible (for example, how location services are utilized over the course of a day and why this might by).

2. A shortcoming in the completeness of the data that becomes obvious when it is visualized.

3. How this data could help us identify vulnerabilities related to climate change in the greater Boston area.
