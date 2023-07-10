import csv
import time


asset_list = ['GOLD', 'NASDAQ', 'CRYPTO']

for asset in asset_list:
    filename = 'origin/' + asset + '.csv'
    new_filename = 'convert/cvt_' + asset + '.csv'
    arr = []
    with open(filename, 'r') as f:
        csv_r = csv.reader(f)
        arr = []
        for i in csv_r:
            arr.append(i)

    new_arr = [['time', 'price']]

    for i in range(1, len(arr)):
        data = arr[i]
        new_data = []
        tm = time.localtime(int(data[0]))
        if (tm.tm_year == 2022 or (tm.tm_year == 2023 and (tm.tm_mon == 1 or tm.tm_mon == 2))) and tm.tm_wday < 5:
            new_data.append(time.strftime('%Y-%m-%d', tm))
            if asset == 'CRYPTO':
                new_data.append("{0:.2f}".format(int(data[4])/1000000000))
            else:
                new_data.append(data[4])
            new_arr.append(new_data)

    with open(new_filename, 'w', newline="") as f:
        csv_w = csv.writer(f)
        csv_w.writerows(new_arr)
