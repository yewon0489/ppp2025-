def maximum_temp_gap(dates, tmax, tmin):
    max_gap_date = dates[0]
    max_gap = float(tmax[0]) - float(tmin[0])

    for i in range(len(dates)):
        date = dates[i]
        tx = float(tmax[i])  
        tm = float(tmin[i])
        gap = tx - tm
        if max_gap < gap:
            max_gap = gap
            max_gap_date = date

    return max_gap_date, max_gap


def get_weather_data(filename, col_idx):
    with open(filename, encoding='utf-8') as f:
        weather_values = []
        lines = f.readlines()
        for line in lines[1:]:
            tokens = line.strip().split(',')
            weather_values.append(tokens[col_idx])
    return weather_values


def get_weather_date(fname):
    with open(fname, encoding='utf-8') as f:
        weather_dates = []
        lines = f.readlines()
        for line in lines[1:]:
            tokens = line.strip().split(',')
            weather_dates.append([int(tokens[0]), int(tokens[1]), int(tokens[2])])
    return weather_dates



def main():
    filename = "./weather(146)_2022-2022.csv"
    dates = get_weather_date(filename)
    tmax = get_weather_data(filename, 5)
    tmin = get_weather_data(filename, 7)
    max_gap_date, max_gap = maximum_temp_gap(dates, tmax, tmin)
    print(f"일교차가 가장 큰 날짜는 {max_gap_date}이고, 해당일의 일교차는 {max_gap:.1f}도입니다.")


if __name__ == "__main__":
    main()