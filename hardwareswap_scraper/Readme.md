# Web scraper for r/hardwareswap using pushshift.io

I was curious what the historical prices were for various nvidia gpus, specificially the 970,980,1070,1080,2070,2080 cards. The code is broken up into a bunch of serial manual commands. As I figured out each major step, I just created a new script.

## Results:
It is really interesting to see how steadily the prices are dropping. It is also very obvious when the bitcoin bubble happened in early 2018. The Ti series cards seem to be hit harder by the bubble and are dropping off in value faster than the normal series cards.

![Non-Ti Series Cards](https://github.com/denck007/scraping/blob/master/hardwareswap_scraper/imgs/Non-Ti_cards.png)

![Ti Series Cards](https://github.com/denck007/scraping/blob/master/hardwareswap_scraper/imgs/Ti_cards.png)