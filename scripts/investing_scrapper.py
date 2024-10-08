import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time


## Initializing the timer
start_t = time.time()

## Creating a Fake User in order to grant access with the requests module
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

## Creating the date range of the news gathering
start = datetime.datetime.strptime("2021/09/03", "%Y/%m/%d")
end = datetime.datetime.strptime("2024/03/06", "%Y/%m/%d")
dates = [{"Date": (start + datetime.timedelta(days=x)).strftime("%Y/%m/%d"), "Titles": []} for x in range(0, (end-start).days)]

"""
Investing.com has another format for scrapping archives:
It saves all of them in pages like: https://www.investing.com/news/stock-market-news/459
The bigger the number (etc. 459) the further to the past you are.

The tricky part here is that those pages are constantly updated with new articles.
So each time I have manually to anotate two pages:
    `ending_i`   -- the page containing the newest articles I need
    `starting_i` -- the page containing the oldest articles I need

So before runing the script find the rigth pages!!!
"""

ending_i = 468    # this is the first page containing news articles for 2024/03/06
starting_i = 6591 # this is the last page containing news articles for 2021/09/03

i = 0
first = True
while (True):
    r = requests.get(f"https://www.investing.com/news/stock-market-news/{starting_i}", headers=headers)

    print(f"URL: `https://www.investing.com/news/stock-market-news/{starting_i}` | Status: `{r.status_code}`")

    ## All news article ar inside a `div` tag under the class name `textDiv` and also containing the date of the article
    soup = BeautifulSoup(r.text, "html.parser")
    divs = soup.find_all("div", "textDiv")

    ## Converting `2021/09/03` to `Sep 03, 2021`
    formated_date = str(datetime.datetime.strptime(dates[i]["Date"], "%Y/%m/%d").strftime("%b %d, %Y"))

    j = 0
    for d in divs:
        if (formated_date in str(d)):
            dates[i]["Titles"].append(str(d).split("\"")[7]) # Locating the title on the news article link
            j += 1

    ## The first page is going to contain some articles that we need
    if first:
        starting_i -= 1
        first = False
    else:
        ## Investing.com contain 17 news per page
        
        ## The quiting condition: If no articles have been found
        if (j == 0) and (starting_i <= ending_i):
            break
        
        ## The change page condition: If I have captured all the articles from one page
        elif (j == 0):
            starting_i -= 1

        ## The change condition: If I have colected all the articles for a given date, continue to the next one
        elif (j < 17):
            i += 1
        
        ## The middle condition: If a page contains articles for only one date
        elif (j == 17):
            starting_i -= 1
        
        ## If a page contains articles for dates outside our wanted range
        if (i > len(dates) - 1):
            break

## For Debugging
for d in dates:
    print(d["Date"], ": ", d["Titles"])
    print()

## Saving the results into a `csv` file
df = pd.DataFrame(dates)
df.to_csv("investing_news_titles.csv", index=False, header=True)

print((time.time() - start_t) / 60) # In minutes
