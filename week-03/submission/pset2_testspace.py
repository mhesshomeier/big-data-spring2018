

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

# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['date_new'].head

# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

#check it out
df['weekday'].head


## make my bar chart

#bar_chart = df.groupby(['date_new'])['count'].plot.bar
#print(bar_chart)

df.groupby(['date_new'])['count'].sum().plot(kind = "bar", color = 'red')


#ax = df.plot(kind='bar', title ="GPS pings",figsize=(15,10),legend=True, fontsize=12)
#ax.set_xlabel("date_new",fontsize=12)
#ax.set_ylabel("count",fontsize=12)

#df.plot(x='date_new', y='count', kind='bar')
#plt.show()
#x = df.groupby(['date_new'])
#y = df(['count'])
#plot.bar(x, y)

##df_date = df.groupby(['date_new', 'count'])
##df_date.plot(kind= 'bar')
##df[['date_new', 'count']].plot(kind = 'bar')
#    df.groupby('date_new')
