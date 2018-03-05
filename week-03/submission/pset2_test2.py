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

Your second task is to further clean the data. While we've successfully cleaned our data in one way
(ridding it of values that are outside the 24-hour window that correspond to a given day of the week)
it will be helpful to restructure our `hour` column in such a way that hours are listed in a more familiar 24-hour range.
To do this, you'll want to more or less copy the structure of the code we used to remove data from hours outside of a given day's
24-hour window. You'll then want to use the [DataFrame's `replace` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.replace.html).
Note that you can use lists in both `to_replace` and `value`.

After running your code, you should have either a new column in your DataFrame or new values in the 'hour' column.
These should range from 0-23. You can test this out in a couple ways; the simplest is probably to `df['hour'].unique()`;
if you're interested in seeing sums of total pings by hour, you can run `df.groupby('hour')['count'].sum()`.


for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  print(i, j)
  if (j > i):
      df['hour'].replace(range(i, i +19, 1), range(5, 24, 1), inplace = True) ## replacing the range from i to i+19 with 5 to 24
      #df['hour'].replace((i, i + 5, 2), range(0, 5, 1), inplace = True)
  #else:
     # df['hour'].replace(range(j, i + 19, 1), range(0, 24, 1), inplace = True) ## range (x, y, # by which you count)

df['hour'].unique()











 # if (j > i): ## i is the first hour of a day when a day runs from 0 to 23,
#    df.drop(df[
#    (df['weekday'] == (i/24)) &
#    (
#    ( (df['hour'] < j) & (df['hour'] > i + 18) ) |
#    ( (df['hour'] > i + 18 ) & (df['hour'] < j) )
#    )
#    ].index, inplace = True)
 # else:
'''
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    (df['hour'] < j) | (df['hour'] > i + 18 )
    )
    ].index, inplace = True)
'''
