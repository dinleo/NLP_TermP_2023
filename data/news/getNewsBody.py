import requests
from bs4 import BeautifulSoup
import csv
import time
from collections import defaultdict


def get_req(n_day, n_idx, url):
    # request
    response = requests.get(url)
    status_code = str(response.status_code)
    print("now: {}[{}] st-code: {}\nurl: {}".format(n_day, n_idx, status_code, url))
    if status_code != "200":
        exit()
    time.sleep(3)

    # soup select
    soup = BeautifulSoup(response.content, "html.parser")
    group = soup.find_all("div", {"class": "group"})

    # get_body
    txt_arr = []
    for g in group:
        tx = g.text
        if tx.startswith("Subscribe to CNBC PRO"):
            break
        txt_arr.append(g.text)
    body = " ".join(txt_arr)

    return body


def read_file(f_name, mode):
    arr = []
    with open(f_name, mode, encoding='utf-8') as f:
        reader = csv.reader(f)
        reader.__next__()
        for r in reader:
            arr.append(r)

    return arr


def write_file(f_name, mode, rows):
    with open(f_name, mode, newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def arr2dict(arr):
    dic = defaultdict(list)
    for a in arr:
        if a[1] != "":
            dic[a[0]].append(a[1])
    return dic


def dict2arr(dic):
    arr = []
    for date in dic:
        for b in dic[date]:
            arr.append([date, b])
    return arr


def handle_empty():
    link_arr = read_file(link_file_name, "r")
    link_dict = arr2dict(link_arr)
    body_arr = read_file(body_file_name, "r")
    body_dict = arr2dict(body_arr)
    new_body_dict = defaultdict(list)

    for date in body_dict:
        lb = len(body_dict[date])

        if lb == max_cnt:
            new_body_dict[date] = body_dict[date]
            continue

        lack = max_cnt - lb
        ll = len(link_dict[date])
        if ll < max_cnt + lack:
            print("{} is deleted".format(date))
            continue

        for i in range(lack):
            url = link_dict[date][max_cnt + i]
            body = get_req(date, i, url)
            if body != "":
                new_body_dict[date].append(body)

        if len(new_body_dict[date]) < max_cnt:
            print("{} is deleted".format(date))
            del new_body_dict[date]

    new_arr = dict2arr(new_body_dict)

    write_file(n_body_file_name, "w", new_arr)


def get_body_from_start(s_day, s_idx):
    link_arr = read_file(link_file_name, "r")
    link_dict = arr2dict(link_arr)

    start_flag = True
    for now_day in link_dict:
        if start_flag and now_day < s_day:
            continue
        if len(link_dict[now_day]) < min_cnt:
            continue
        for (now_idx, url) in enumerate(link_dict[now_day]):
            # start
            if start_flag:
                if now_idx < s_idx:
                    continue
                else:
                    start_flag = False

            if max_cnt <= now_idx:
                break

            # req
            body_txt = get_req(now_day, now_idx, url)

            # write
            write_file(body_file_name, "a", [[now_day, body_txt]])

            print("----------done----------")


# set param
link_file_name = "news_link/crypto_news_link.csv"
body_file_name = "news_body/crypto_news_body.csv"
n_body_file_name = "../train_data/crypto_news_body.csv"

start_day = "2022-10-28"
start_idx = 0
# minimum article count per days
min_cnt = 3
# maximum article count per days
max_cnt = 3
# idx: 0~(max_cnt-1 or 7)


# execute
# get_body_from_start(start_day, start_idx)
handle_empty()
