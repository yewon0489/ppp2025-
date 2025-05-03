import requests
import os
def read_temperatures(filename):
    t_a=[]
    with open(filename, encoding="utf-8") as f:
        lines=f.readlines()[1:]
        for line in lines:
            tokens=line.strip().split(",")
            tem=float(tokens[4])
            t_a.append(tem)

    return t_a
        
def read_water(filename):
    water=[]
    with open(filename, encoding="utf-8") as f:
        lines=f.readlines()[1:]
        for line in lines:
            tokens=line.strip().split(",")
            w_all=float(tokens[9])
            if w_all>=5:
                water.append(w_all)

    return water

def read_allwater(filename):
    al_w=[]
    with open(filename, encoding="utf-8") as f:
        lines=f.readlines()[1:]
        for line in lines:
            tokens=line.strip().split(",")
            w_lines=float(tokens[9])
            al_w.append(w_lines)
 
    return(al_w)

def download_weather(station_id, year, filename):
    URL = f"https://api.taegon.kr/stations/{station_id}/?sy={year}&ey={year}&format=csv"
    with open(filename, "w", encoding="UTF-8-sig") as f:
        resp = requests.get(URL)
        resp.encoding = "utf-8"
        f.write(resp.text)
def main():
    where_ID = 146
    year = 2020
    outfile="ppp_hw12_out.txt"
    filename=f"weather_{where_ID}_{year}.csv"

    if not os.path.exists(filename):
        download_weather(where_ID, year, filename)

    year_average=read_temperatures(filename)
    up_5mm=read_water(filename)
    all_water=read_allwater(filename)

    total_temp=0
    for i in year_average:
        total_temp+=i
    tem_len=len(year_average)

    water_len=len(up_5mm)

    total_water=sum(all_water)

    answer_list=[f"{year}년 평균 기온은{(total_temp/tem_len):.2f}℃입니다.", 
                 f"{year}년 강수량이 5mm이상인 날짜는 {water_len}일 입니다.", 
                 f"{year}년 총 강수량은 {total_water}mm입니다."]

    with open(outfile,"w",encoding="utf-8") as f:
        for line in answer_list:
            f.write(line+"\n")


if __name__=="__main__":
    main()