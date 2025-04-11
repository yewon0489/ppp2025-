def read_db(filename):
    data_list = []
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:#첫번째 행은 제외
            line = line.strip()#빈공간 제외
            token = line.split(',')#, 마다 나눠서

            temp_str = token[4].strip()#리스트 숫자 4번째거 선택
            rain_str = token[9].strip()#리시트 숫자 9번째거 선택

            avg_temp = float(temp_str)#숫자로 읽어라
            rainfall = float(rain_str)#숫자로 읽어라
            data_list.append({"avg_temp": avg_temp, "rainfall": rainfall})#avg랑 rainfall을 하나의 딕셔너리로 만들어서 리스트에 저장

    return data_list#함수를 이렇게 끝낼거고 data_list를 보여줘라


def main(): 
    weather = read_db("./weather(146)_2022-2022.csv")#이 파일 읽을게

    total_temp = 0 #처음은 0으로 시작
    total_rainfall = 0 #처음은 0으로 시작
    rain_days_over_5mm = 0 #처음은 0으로 시작

    for day in weather: #weater에서 day로 넣을건데 반복할거야
        total_temp += day["avg_temp"] # avg함수에서 day를 뽑을거고 토탈에 더할거야 그걸 반복
        total_rainfall += day["rainfall"]
        if day["rainfall"] >= 5.0:
            rain_days_over_5mm += 1
        avg_temp = total_temp / len(weather)

    print(f"연 평균 기온: {avg_temp:.5f} ℃")
    print(f"5mm 이상 강우일수: {rain_days_over_5mm} 일")
    print(f"총 강우량: {total_rainfall:.2f} mm")


if __name__ == "__main__":
    main()
