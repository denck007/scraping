
'''
This was the first attempt to scrap data directly from reddit. It does not do what I want because you can only go back ~1000 posts
'''

import os
import re
import praw
from datetime import datetime
reddit = praw.Reddit("bot1",user_agent='bot1 user agent')
reddit.read_only=True

subreddit = reddit.subreddit("HardwareSwap")

keywords = ["2080","2070","1080","1070","1050","nvidia"]

found_posts = {}


def find_price(text):
    '''
    attempt to find price in post text
    '''
    price_start = text.find("$") +1 # find the first instance of a dollar sign
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


#for submission in subreddit.search("title:1080",limit=100):
idx = 0
for submission in subreddit.hot(limit=10):
    idx += 1
    #print(submission.title)
    #print(submission.score)
    #print(submission.id)
    #print(submission.url)
    #print()

    title = submission.title.lower().strip()
    title = text = re.sub("[,.]","",title) # remove all periods and commas
    location_end = title.find("]")
    location = title[1:location_end]
    have_start = title[location_end+1:].find("]")
    have_end = title.rfind("[")
    have = title[location_end+have_start+2:have_end]

    for keyword in keywords:
        if keyword in have:
            text = submission.selftext
            text = re.sub("[,.]","",text) # remove all periods and commas
            price = find_price(text)
            submission_time = submission.created_utc
            date = datetime.fromtimestamp(submission_time)
            print(submission_time)
            
            print("Number: {} Location: {} have: {} price: {}".format(idx,location,have,price))
            found_posts.update({submission.id:{"title":title,"items":have,"price":price,"year":date.year,"month":date.month,"day":date.day,"hour":date.hour,"minute":date.minute}})

            break
    
with open("ouput_data.csv",'w') as f:
    f.write("Post Id,Items for sale,Price,Year,Month,Day,Hour,Minute\n")
    for post in found_posts:
        f.write("{},{},{}".format(post,found_posts[post]["items"],found_posts[post]["price"]))

        f.write(",{},{},{},{},{}\n".format(found_posts[post]["year"],found_posts[post]["month"],found_posts[post]["day"],found_posts[post]["hour"],found_posts[post]["minute"]))

