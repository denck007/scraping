'''
The parse_pushshift_data script does a decent job of getting the price out, but there are a lot of 'dirty' prices.

Dirty prices are when no price, or multiple prices are found in the same post text. This script sorts them out based on this. 

The data in the 'valid_prices' csv files is still dirty, but the prices are valid. After this we need to manually go through the spreadsheets to get rid of posts that have other parts, cents listed, dubious posts, etc.

'''

import os

fnames = [x for x in os.listdir() if ".csv" in x]

for fname in fnames:

    with open(fname,'r') as f:
        data = f.readlines()

    outfile_clean = "{}_valid_prices.csv".format(fname[:-4])
    outfile_dirty = "{}_dirty_prices.csv".format(fname[:-4])

    clean_prices = []
    dirty_prices = []

    for idx,line in enumerate(data):
        price = line.split(",")[2]
        if idx==0:
            header = price
            continue

        if (price =="NONE LISTED") or (price == ""):
            continue
        elif ("-" in price) :
            dirty_prices.append(line)
        else:
            clean_prices.append(line)

    with open(outfile_clean,'w') as f:
        f.write(header)
        for line in clean_prices:
            f.write("{}".format(line))
    with open(outfile_dirty,'w') as f:
        f.write(header)
        for line in dirty_prices:
            f.write("{}".format(line))

