def get_weather_data(filename, col_idx):       
    weather_datas=[]
    with open(filename) as f:
        lines=f.readlines()[1:]
        for line in lines:
            tokens=line.strip().split(",")
            weather_datas.append(float(tokens[col_idx]))
    return weather_datas

#날짜
def get_weather_dates(filename):               
    weather_dates=[]
    with open(filename) as f:
        lines=f.readlines() #encoding 없어도 된다.
        for line in lines[1:]:
            tokens=line.strip().split(",")
            weather_dates.append([int(tokens[0]),int(tokens[1]),int(tokens[2])])
    return weather_dates



def gdd_year_5to9(dates, tavg):
    gdd_list=[]
    temp=5
    years=[]
    for date in dates:
        y=date[0]
        if y not in years:
            years.append(y)
            gdd_list.append(0)

    
    
    for i in range(len(tavg)):
        t = tavg[i]
        month = dates[i][1]
        year = dates[i][0]

        if month in [5,6,7,8,9]:
            if t >= temp:
                gap = t - temp
                idx = years.index(year) 
                gdd_list[idx] += gap

    return years, gdd_list



def main():
    filename="weather(146)_2001-2022.csv"
    dates=get_weather_dates(filename)
    tavg=get_weather_data(filename,4)
    years, gdd_5to9year=gdd_year_5to9(dates,tavg)
    for i in range(len(years)):
        print(f"{years[i]}년의 5월부터 9월 gdd는 {gdd_5to9year[i]:.1f}도일입니다.")

if __name__=="__main__":
    main()