### Step 1

# Using the Twitter REST API, collect at least 2,000 tweets. Do not specify a search term.
# Use a lat/lng of `42.359416,-71.093993` and a radius of `5mi`. This will take 1-2 minutes
# to run.

#Import my libraries for setting up the Scraper
import jsonpickle
import tweepy
import pandas as pd

#Set up my twitter keys
import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret

#Set up my function for twitter authentication
def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)

# Set up my first Scraper
def get_tweets(
    geo,
    out_file,
    search_term = '',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        if write == True:
            with open(out_file, 'w') as f:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  return all_tweets

# set up my parser

def parse_tweet(tweet):
    p = pd.Series()
    if tweet.coordinates != None:
      p['lat'] = tweet.coordinates['coordinates'][0]
      p['lon'] = tweet.coordinates['coordinates'][1]
    else:
      p['lat'] = None
      p['lon'] = None
    p['location'] = tweet.user.location
    p['id'] = tweet.id_str
    p['content'] = tweet.text
    p['user'] = tweet.user.screen_name
    p['user_id'] = tweet.user.id_str
    p['time'] = str(tweet.created_at)
    return p

# Set variables and Run the function to scrape tweets with no search term
# Set a Lat Lon
latlng = '42.359416,-71.093993'
# Set a search distance
radius = '5mi'

geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/pset3_tweets1.json'
# set threshold number of Tweets.
t_max = 2000

tweets1 = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
  )

# Check out the tweets
print(tweets1)


### Step 2

# Clean up the data so that variations of the same user-provided location name are
# replaced with a single variation. Once you've cleaned up the locations, create a
# pie chart of user-provided locations. Your pie chart should strive for legibility!
# Let the [`matplotlib` documentation](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.pie.html)
# be your guide!


# Put my tweets in a data frame
df = pd.read_json('data/pset3_tweets1.json')

# Import data visualization Libraries
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# check out the data dtypes
tweets1.dtypes

# check out the locations that users are self reporting
tweets1['location'].unique()

# Clean up the data to make place names consistent
# Boston
bos_list = tweets1[tweets1['location'].str.contains("Boston", case = False)]['location']
tweets1['location'].replace(bos_list, 'Boston', inplace = True)
# Cambridge
camb_list = tweets1[tweets1['location'].str.contains("Cambridge", case = False)]['location']
tweets1['location'].replace(camb_list, 'Cambridge', inplace = True)
# Somerville
som_list = tweets1[tweets1['location'].str.contains("somerville", case = False)]['location']
tweets1['location'].replace(som_list, 'Somerville', inplace = True)

#check out the locations to make sure it worked correctly
tweets1['location'].unique()

# clean up anything in MA, not cambridge, boston or somerville
ma_list1 = tweets1[tweets1['location'].str.contains('ma|mass|MA|Mass', case = False)]['location']
tweets1['location'].replace(ma_list1, 'other MA', inplace = True)
print(ma_list1)
#clean up everything that isn't Boston, somerville, cambridge, other MA
not_ma1 = tweets1[~tweets1['location'].str.contains('Cambridge|Somerville|Boston|other MA', case = False)]['location']
print(not_ma1)
tweets1['location'].replace(not_ma1, 'Other, not MA', inplace = True)

#check it out
tweets1['location'].unique()

# Do I have any duplicates?
tweets1[tweets1.duplicated(subset = 'content', keep = False)]
# delete Duplicates
tweets1.drop_duplicates(subset = 'content', keep = False, inplace = True)
#make sure it worked
tweets1[tweets1.duplicated(subset = 'content', keep = False)] # woohoo!



# Make a scatterplot of the latitude and longitude of different tweets
tweets1.plot.scatter(x="lat", y="lon", color = 'orange', title = 'gps locations of scraped tweets')

### Step 3

# Create a scatterplot showing all of the tweets are that are geolocated (i.e., include
# a latitude and longitude).

# Make a scatterplot of the latitude and longitude of different tweets
tweets1.plot.scatter(x="lat", y="lon", color = 'orange', title = 'gps locations of scraped tweets')

### Step 4

# Pick a search term (e.g., "housing", "climate", "flood") and collect tweets containing
# it. Use the same lat/lon and search radius for Boston as you used above. Use a maximum
# of 2,000 tweets; depending on the search term, you may find that there are fewer than
# 2,000 tweets available.


#Set up my second scraper with a search term defined
def get_tweets2(
    geo,
    out_file,
    search_term = 'storm',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        if write == True:
            with open(out_file, 'w') as f:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  return all_tweets
## Set specifics for running the second scraper
# Set a Lat Lon
latlng = '42.359416,-71.093993'
# Set a search distance
radius = '5mi'

geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/pset3_tweets2.json'
# set threshold number of Tweets.
t_max = 2000

#Run the second parser with a new name, tweets2
tweets2 = get_tweets2(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
  )

#check it out
 print(tweets2)


### Step 5
# Clean the search term data as with the previous data.

# check out the locations that users are self reporting
tweets2['location'].unique()

# Try this to see different locations, grouped
loc_tweets = tweets2[tweets2['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets
df_count_tweets.columns
df_count_tweets.columns = ['count']
df_count_tweets

df_count_tweets.sort_index()


# Clean up the data to make place names consistent
# Boston
bos_list2 = tweets2[tweets2['location'].str.contains("Boston", case = False)]['location']
tweets2['location'].replace(bos_list2, 'Boston', inplace = True)

# Cambridge
camb_list2 = tweets2[tweets2['location'].str.contains("Cambridge", case = False)]['location']
tweets2['location'].replace(camb_list2, 'Cambridge', inplace = True)

# Somerville
som_list2 = tweets2[tweets2['location'].str.contains("somerville", case = False)]['location']
tweets2['location'].replace(som_list2, 'Somerville', inplace = True)

#check out the locations to make sure it worked correctly
tweets2['location'].unique()
# clean up anything in NY
ny_list2 = tweets2[tweets2['location'].str.contains("NY|New York|nyc|ny", case = False)]['location']
tweets2['location'].replace(ma_list2, 'NY', inplace = True)
# clean up anything in MA, not cambridge, boston or somerville
ma_list2 = tweets2[tweets2['location'].str.contains('ma|mass|MA|Mass', case = False)]['location']
tweets2['location'].replace(ma_list2, 'other MA', inplace = True)
print(ny_list2)
print(ma_list2)
#clean up everything that isn't Boston, somerville, cambridge, other MA or NY
not_ma2 = tweets2[~tweets2['location'].str.contains('Cambridge|Somerville|Boston|other MA|NY', case = False)]['location']
print(not_ma2)
tweets2['location'].replace(not_ma2, 'Other, not MA or NY', inplace = True)


df_count_tweets.sort_index()
tweets2['location'].unique()

# Do I have any duplicates?
tweets2[tweets2.duplicated(subset = 'content', keep = False)]
# delete Duplicates
tweets2.drop_duplicates(subset = 'content', keep = False, inplace = True)
#make sure it worked
tweets2[tweets2.duplicated(subset = 'content', keep = False)] # woohoo!






### Step 6

# Create a scatterplot showing all of the tweets that include your search term that
# are geolocated (i.e., include a latitude and longitude).

# Make a scatterplot of the latitude and longitude of different tweets
tweets2.plot.scatter(x="lat", y="lon", color = 'orange', title = 'gps locations of scraped tweets')

### Step 7

# Export your scraped Twitter datasets (one with a search term, one without) to two
# CSV files. We will be checking this CSV file for duplicates and for consistent location
# names, so make sure you clean carefully!

# Export the clean data to a CSV!
tweets1.to_csv('twitter_data_nosearch.csv', sep=',', encoding='utf-8')

# Export the clean search term data to a CSV!
tweets2.to_csv('twitter_data_searchterm.csv', sep=',', encoding='utf-8')
