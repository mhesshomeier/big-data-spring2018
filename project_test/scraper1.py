## Set up performance data query
import jsonpickle
import pandas as pd
import requests


# Set up api for MBTA
MBTA_api = "wX9NwuHnZU2ToO7GmGR9uw"

# make sure I'm in the current directory
import os
os.chdir('project_test')

# read in the origin csv
origin_dest = pd.read_csv('data/origin_dest.csv', sep=',')
#read in origin_dest2 csv with cbd lines removed
origin_dest2 = pd.read_csv('data/origin_dest2.csv', sep=',')

#check it out
origin_dest2.head()



#check out my origin_dest2 df_columns
origin_dest2.columns

# set up a data frame to store api request addresses, created from the stops in the origin_dest2 file
#http://realtime.mbta.com/developer/api/v2.1/traveltimes?api_key=wX9NwuHnZU2ToO7GmGR9uw&format=json&from_stop=11384&to_stop=70061&from_datetime=1514419200&to_datetime=1514505600


#create the URL calling from the origin_dest2 df
def url_string(x,y):
    url = 'http://realtime.mbta.com/developer/api/v2.1/traveltimes?api_key=wX9NwuHnZU2ToO7GmGR9uw&format=json&from_stop={}&to_stop={}&from_datetime=1514419200&to_datetime=1514505600'.format(x,y)
    return url
#create input for url_string
# origin = [origin_dest2.origin_id]
# dest = [origin_dest2.dest_id]
# print(url_string(origin,dest))

# iterate through the rows in the origin_dest2 dataframe with origin_id as x and dest_id as y
# for the url_string function
for index, row in origin_dest2.iterrows():
    string = url_string(row["origin_id"], row["dest_id"])
    print(string)
#pd.DataFrame(string)

# read the urls stored in 'string' into a dataframe

print(string)
#convert the dataframe to csv
string.to_csv('data/url.csv')

# make a function that queries the mbta api
for index, row in string
    data = requests.get()
    data.json('data/data1.json')
