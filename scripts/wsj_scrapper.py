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
dates = [{"Date": (start + datetime.timedelta(days=x)).strftime("%Y/%m/%d"), "Titles": ""} for x in range(0, (end-start).days)]

## Iterating over all dates
for i in range(len(dates)):
    r = requests.get(f"https://www.wsj.com/news/archive/{dates[i]['Date']}", headers=headers)

    print(f"URL: `https://www.wsj.com/news/archive/{dates[i]['Date']}` | Status: `{r.status_code}`")

    ## All news titles exists inside a `span` tag inside an `a` tag, and have the same class name `WSJTheme--headlineText--He1ANr9C`
    soup = BeautifulSoup(r.text, "html.parser")
    spans = soup.find_all("span", "WSJTheme--headlineText--He1ANr9C")

    j = 2
    news_titles = []
    ## Iterating over all the pages (each page displays only 50 news articles)
    while (len(spans) != 0):
        for s in spans:
            news_titles.append(str(s)[15 + len("WSJTheme--headlineText--He1ANr9C"):-7]) # 12: `<span class=` | 2: `"` | 1: `>` | 7: `</span>`

        r = requests.get(f"https://www.wsj.com/news/archive/{dates[i]['Date']}?page={j}", headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        spans = soup.find_all("span", "WSJTheme--headlineText--He1ANr9C")
        j += 1

    dates[i]["Titles"] = news_titles

## For Debugging
for d in dates:
    print(d["Date"], ": ", d["Titles"])
    print()

## Saving the results into a `csv` file
df = pd.DataFrame(dates)
df.to_csv("wsj_news_titles.csv", index=False, header=True)

print((time.time() - start_t) / 60) # In minutes
