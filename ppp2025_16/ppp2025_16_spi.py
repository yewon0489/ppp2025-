import requests
import os

def download_weather(station_id, year, filename):
    url = f"https://api.taegon.kr/stations/{station_id}/?sy={year}&ey={year}&format=csv"
    if not os.path.exists(filename):
        resp = requests.get(url)
        resp.encoding = "utf-8"
        with open(filename, "w", encoding="UTF-8-sig") as f:
            f.write(resp.text)

def read_column(fname, col):
    with open(fname, encoding="utf-8") as f:
        return [float(line.strip().split(",")[col]) for line in f.readlines()[1:]]

def rainfall(fname, col):
    return sum(read_column(fname, col))

def max_of_tavg(fname, col):
    return max(read_column(fname, col))

def tmax_tmin(fname, ttx, ttm):
    tmax = read_column(fname, ttx)
    tmin = read_column(fname, ttm)
    return max([tx - tm for tx, tm in zip(tmax, tmin)])

def suwon_jeonju_rain(fname_s, fname_j, col):
    rain_s = sum(read_column(fname_s, col))
    rain_j = sum(read_column(fname_j, col))
    return abs(rain_s - rain_j)

def submit_to_api(name, affiliation, student_id, a1, a2, a3, a4, verbose=False):
    url = "http://sfarm.digitalag.kr:8800/submission/create"
    params = {
        "name": name,
        "affiliation": affiliation,
        "student_id": student_id,
        "param1": a1,
        "param2": a2,
        "param3": a3,
        "param4": a4,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        if verbose:
            print("응답 코드:", response.status_code)
            print("제출 성공! 응답:", response.text)
        return True
    except requests.exceptions.RequestException as e:
        if verbose:
            print("제출 중 오류 발생:", e)
        return False

def main():
    download_weather(146, 2015, "weather_146_2015.csv")
    download_weather(146, 2022, "weather_146_2022.csv")
    download_weather(146, 2024, "weather_146_2024.csv")
    download_weather(119, 2024, "weather_119_2024.csv")


    y_rain = rainfall("weather_146_2015.csv", 9)
    tavg_2022 = max_of_tavg("weather_146_2022.csv", 4)
    tx_tm = tmax_tmin("weather_146_2024.csv", 3, 5)
    s_j_2024 = round(suwon_jeonju_rain("weather_119_2024.csv", "weather_146_2024.csv", 9), 1)


    submit_to_api("박예원", "스마트팜학과", "202210076", y_rain, tavg_2022, tx_tm, s_j_2024, verbose=True)

if __name__ == "__main__":
    main()
