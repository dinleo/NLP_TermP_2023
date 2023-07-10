import time
import requests
from bs4 import BeautifulSoup
import datetime
import re
import csv

base_day = datetime.date.today().replace(2022, 10, 28)

for i in range(90):
    # date
    add_day = datetime.timedelta(days=i)
    dt = base_day + add_day
    # if 5 <= dt.weekday():
    #     continue
    day = dt.strftime("%Y/%m/%d")
    f_day = dt.strftime("%Y-%m-%d")

    # request
    url = "https://www.google.com/search?q=crypto+site%3Awww.cnbc.com/" + day + "&tbm=nws"
    response = requests.get(url)
    status_code = str(response.status_code)
    print("now: " + f_day + " st-code: " + status_code)
    if status_code != "200":
        break
    time.sleep(2)

    # soup
    soup = BeautifulSoup(response.content, "html.parser")
    link_list = soup.find_all("a")
    data_arr = []
    with open("news_link/crypto_news_link.csv", "a", newline="") as f:
        for link in link_list:
            if 8 <= len(data_arr):
                break
            href = link["href"]
            if href.startswith("/url?q=https://www.cnbc.com/" + day):
                match = re.search(r'https.*?html', href)
                if match:
                    https_html = match.group(0)
                    data = [f_day, https_html]
                    data_arr.append(data)
        csv_w = csv.writer(f)
        csv_w.writerows(data_arr)

    print("done")
