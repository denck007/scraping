'''
pushshift.io has all of the reddit post history data stored in a very easy to use api.

This script allows you to search for posts with a specific title that was posted between certain dates.
The api limits the number of responses/size of json file, so this iteratively changes the dates based on the most recent data it has received until it hits the earliest time listed
'''

import json
import urllib.request
from datetime import date,datetime


newest_time = int(date(2018,11,10).strftime("%s"))
oldest_time = int(date(2015,1,1).strftime("%s"))

search_term = "subreddit=hardwareswap&title=970"
max_posts_per_file = 10000

def get_from_web(oldest,newest,count,search=""):
    if search != "":
        url = "https://api.pushshift.io/reddit/search/submission/?subreddit=hardwareswap&sort=desc&sort_type=created_utc&after={}&before={}&size={}&{}".format(oldest,newest,count,search)
        
    else:
        url = "https://api.pushshift.io/reddit/search/submission/?subreddit=hardwareswap&sort=desc&sort_type=created_utc&after={}&before={}&size={}".format(oldest,newest,count)

    contents = urllib.request.urlopen(url)
    raw_data = contents.read()
    data = json.loads(raw_data)
    if len(data["data"]) == 0:
        return data
    start = data["data"][-1]["created_utc"]
    end = data["data"][0]["created_utc"]

    if search!="":
        outfile = "{}_{}-{}.json".format(search,start,end)
    else:
        outfile = "{}-{}.json".format(start,end)
    with open(outfile,'w') as f:
        json.dump(data,f)

    return data

num_posts = 1

while num_posts > 0:
    print("Retrieving from {} to {}".format(oldest_time,newest_time))
    data = get_from_web(oldest_time,newest_time,max_posts_per_file,search_term)
    num_posts = len(data["data"])
    if num_posts == 0:
        break
    newest_time = int(data["data"][-1]["created_utc"])
