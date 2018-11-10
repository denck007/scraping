# Web scraper for r/hardwareswap using pushshift.io

The process to get data is:
1) Run 'pull_from_pushshift.py' with the 'newest_time', 'oldest_time' and 'search_term' variables updated
2) Parse out the data from pushshift using 'parse_pushshift_data.py'. Edit the 'keywords' variable to include what ever it is you are looking for. This will only search under the [H] portion of the title. Also edit the 'outfile' and 'base_file_name' variables as needed.
3) Run 'cleanup.py'. This will extract just the posts that have only 1 price in the post.
4) Manual cleanup. This is a little tedious, but doesnt actually take that long. Open the csv file in a spreadsheet editor and remove anything that does not include exactly the part you are investigating. IE if you are just looking for a processor by itself, remove all bundle and complete system builds
5) Plot it! Enter the file names  into the 'fnames' variable. Also important is the 'avg_over' variable which controls how much smoothing the script does.

## Results:
It is really interesting to see how steadily the prices are dropping. It is also very obvious when the bitcoin bubble happened in early 2018. The Ti series cards seem to be hit harder by the bubble and are dropping off in value faster than the normal series cards.

![Non-Ti Series Cards](https://github.com/denck007/scraping/blob/master/hardwareswap_scraper/imgs/Non-Ti_cards.png)

![Ti Series Cards](https://github.com/denck007/scraping/blob/master/hardwareswap_scraper/imgs/Ti_cards.png)