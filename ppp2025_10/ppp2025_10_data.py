def average(nums):
    return sum(nums)/len(nums)

def  get_weather_data(filename,col_idx):
    weather_datas = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines[1:]:
            tokens = line.split(',')
            #print(tokens[col_idx], type(tokens[col_idx]))
            weather_datas.append(float(tokens[col_idx]))
    return weather_datas


def  get_weather_data_int(filename,col_idx):
    weather_datas = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines[1:]:
            tokens = line.split(',')
            #print(tokens[col_idx], type(tokens[col_idx]))
            weather_datas.append(int(tokens[col_idx]))


    return weather_datas


def count_bigger_days(nums, criteria):
    cnt = 0
    for num in nums:
        if num >= criteria:
            cnt += 1
    return cnt


def get_rain_events(rainfalls):
    events =[]
    c_days = 0
    for rain in rainfalls:
        if rain > 0 :
            c_days += 1
        else:
            if c_days > 0:
                events.append(c_days)
            c_days = 0

    if c_days > 0:
        events.append(c_days)
    return events

#총 강우량(강수량) 저장하는 방법 위 함수에 이 각 값들을 더해야하는것 - 이거 숙제임 꼭 확인하기 
def get_rain_eventss(rainfalls):
    events =[]
    c_days = 0
    for rain in rainfalls:
        if rain > 0 :
            c_days += rain
        else:
            if c_days > 0:
                events.append(c_days)
            c_days = 0

    if c_days > 0:
        events.append(c_days)
    
    return events

def sumifs(rainfalls, months, selected=[6,7,8]):
    total = 0
    for i in range(len(rainfalls)):
        rain=rainfalls[i]
        month = months[i]
        if month in selected: 
            total += rain
    return total


def main(): 
    filename ="./weather(146)_2022-2022.csv"
    #tavgs = get_tavg_data(filename)
    tavgs = get_weather_data(filename, 4)
    print(f"연평균 기온(avg. of 일평균) = {average(tavgs):.2f}도")

#2. 5mm 이상인 강우일수수
    rainfalls = get_weather_data(filename, 9)
    
    count_over5_rain = count_bigger_days(rainfalls, 5)
    count_over5_rain = len([x for x in rainfalls if x >= 5])
    print(f"5mm 이상 강우일수={count_over5_rain}일")
    #3. 총 강수량은
    print(f"총 강수량은= {sum(rainfalls):,.1f}mm")
    #4. 최장연속강우일수
    print(f"최장연속강우일수={max(get_rain_events(rainfalls))}일")
    #5. 최장연속강우량량
    print(F"최장연속강우량={max(get_rain_eventss(rainfalls)):.1f}")
    #6. top3 of tmax
    #top3_tmax = sorted(get_weather_data(filename, 3), reverse=True)[:3]#sorted는 정렬하는 함수
    top3_tmax = sorted(get_weather_data(filename, 3))[-3:]#sorted는 정렬하는 함수 #[::-1]은 리스트 자체를 거꾸로 인식하게 하는 방법법
    print(f"가장 높았던 최고기온 3개는 {top3_tmax}입니다.")
    #rainfalls는 읽었음
    months = get_weather_data_int(filename, 1)
 
    print(f"여름철 강수량은 {sumifs(rainfalls, months, selected=[6,7,8]):.2f} 입니다.")
    #8. 2021년과 2022년 총 강수량을 구하시오.
    filename_20yr= "./weather(146)_2001-2022.csv"
    years = get_weather_data_int(filename_20yr, 0)
    rainfalls = get_weather_data(filename_20yr, 9)
    print(f"2021년 총 강수량은 {sumifs(rainfalls, years, selected=[2021]):.1f}입니다.")
    print(f"2022년 총 강수량은 {sumifs(rainfalls, years, selected=[2022]):.1f}입니다.")

if __name__ == "__main__":
    main()