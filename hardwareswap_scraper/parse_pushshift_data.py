'''
This script turns the json files from pushshift and looks for a price in the post text.
A 'price' is defined as the numbers between a '$' and the following non numeric charaters. It also matches the case where the pattern is non-numeric, then numeric price, then $

This creates raw data files. All this data needs to be reviewed and cleaned before being useful.
'''

import json
import urllib.request
from datetime import datetime

import os
import re

keywords = ["970","nvidia"]
outfile = "970.csv"
base_file_name = "subreddit=hardwareswap&title=970"


def find_price(text):
    '''
    attempt to find price in post text
    '''
    text = text.strip(" ") 
    price_start = text.find("$") +1 # find the first instance of a dollar sign
    if price_start >= len(text): # symbol could floow the price...
        price_start = text.rfind(" ") # find the price by moving to the space before 

    if price_start>0:
        while text[price_start] == " ": # remove spaces between dollar sign and price
            price_start += 1
        price_len = 0
        while text[price_start+price_len].isnumeric(): # count number of digits in price
            price_len += 1
            if len(text) == price_start + price_len: # case where last character in post is part of the price
                break

        price = text[price_start:price_start+price_len] # extract price

        if "$" in text[price_start+price_len:]: # if there is another $ recursively call find_price() on a smaller chunk
            other_price = find_price(text[price_start+price_len:])
            price = "{}-{}".format(price,other_price) # append the result

        return price
    else:
        return "NONE LISTED"



def parse_json(data):
    found_posts = {}
    idx = 0
    for submission in data["data"]:
        idx += 1
        if "selftext" not in submission.keys():
            continue

        title = submission["title"].lower().strip(" ")
        title = text = re.sub("[,.]","",title) # remove all periods and commas
        location_end = title.find("]")
        location = title[1:location_end]
        have_start = title[location_end+1:].find("]")
        have_end = title.rfind("[")
        have = title[location_end+have_start+2:have_end].strip()

        for keyword in keywords:
            if keyword in have:
                text = submission["selftext"]
                text = re.sub("[,.]","",text) # remove all periods and commas
                price = find_price(text)
                submission_time = submission["created_utc"]
                date = datetime.fromtimestamp(submission_time)
                url = submission["url"]
                
                print("Number: {} Location: {} have: {} price: {}".format(idx,location,have,price))
                found_posts.update({submission["id"]:{"title":title,"items":have,"price":price,"year":date.year,"month":date.month,"day":date.day,"hour":date.hour,"minute":date.minute,"url":url}})
                break

    return found_posts

def save_posts(posts,outfile,mode):
    with open(outfile,mode) as f:
        if mode != 'a': # if appending do not write headers
            f.write("Post Id,Items for sale,Price,URL,Year,Month,Day,Hour,Minute\n")
        for post in posts:
            f.write("{},{},{},{}".format(post,posts[post]["items"],posts[post]["price"],posts[post]["url"]))
            f.write(",{},{},{},{},{}\n".format(posts[post]["year"],posts[post]["month"],posts[post]["day"],posts[post]["hour"],posts[post]["minute"]))

fnames = [f for f in os.listdir() if base_file_name in f]

for idx,fname in enumerate(fnames):
    print(fname)
    with open(fname,'r') as f:
        raw_data = f.read()
    data = json.loads(raw_data)
    posts = parse_json(data)
    if idx == 0:
        mode = "w"
    else:
        mode = "a"
    save_posts(posts,outfile,mode)

    

