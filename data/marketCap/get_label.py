import csv
import math

asset_list = ['GOLD', 'NASDAQ', 'CRYPTO']

for asset in asset_list:
    def get_score(w, b_price, p):
        return w*(math.log(p / b_price))

    filename = 'convert/cvt_' + asset + '.csv'
    new_filename = 'label/labeled_' + asset + '.csv'
    arr = []

    with open(filename, 'r') as f:
        csv_r = csv.reader(f)
        arr = []
        for i in csv_r:
            arr.append(i)

    new_arr = [['time', 'price', 'score', 'label']]
    ln = len(arr)

    weight_next_day = 0.5
    weight_next_week = 0.3
    weight_next_month = 0.2

    for i in range(1, ln):
        date = arr[i][0]
        base_price = float(arr[i][1])
        new_data = []
        if date[3] != '2':
            break
        score = get_score(weight_next_day, base_price, float(arr[i + 1][1])) \
                + get_score(weight_next_week, base_price, float(arr[i + 7][1])) \
                + get_score(weight_next_month, base_price, float(arr[i + 30][1]))
        if score < 0:
            label = asset + '_DW'
        else:
            label = asset + '_UP'
        new_data = [date, str(base_price), str(score), label]
        new_arr.append(new_data)


    with open(new_filename, 'w', newline="") as f:
        csv_w = csv.writer(f)
        csv_w.writerows(new_arr)
