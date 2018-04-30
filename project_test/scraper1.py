## Set up performance data query
import jsonpickle
import pandas as pd
import requests
import csv

# Set up api for MBTA
MBTA_api = "wX9NwuHnZU2ToO7GmGR9uw"

# make sure I'm in the current directory
import os
os.chdir('project_test')


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
url_list = []
print(url_list)
for index, row in origin_dest2.iterrows():
    string = url_string(row["origin_id"], row["dest_id"])
    url_list.append(string)
    print(url_list)
#pd.DataFrame(string)

# type(string)
# string.count()
# n.unique(string)
# len(string)
# pd.DataFrame(string)
# read the urls stored in 'string' into a dataframe

print(url_list)
len(url_list)
#convert the dataframe to csv
# string.to_csv()


# try querying the mbta data with one link
# test = requests.get(string)
# print(test)
# test.json()

# for each item in 'string' make a request to the url and store the response as a variable
# write that variable to a json, with a name that indicates the line and stops in the url that
# we used to request the information




# make a function that queries the mbta api
namenumber = 0
for i in url_list:
    resp = requests.get(i)
    data = resp.json
    print(data)
