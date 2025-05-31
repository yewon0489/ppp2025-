import requests
import pandas as pd
import os

def download_weather(station_id, year, filename):
    url = f"https://api.taegon.kr/stations/{station_id}/?sy={year}&ey={year}&format=csv"
    if not os.path.exists(filename):
        resp = requests.get(url)
        resp.encoding = "utf-8"
        with open(filename, "w", encoding="UTF-8-sig") as f:
            f.write(resp.text)

def rainfall(filename):
    df = pd.read_csv(filename)
    return float(f"{df['rainfall'].sum():.2f}")

def max_of_tmax(filename):
    df = pd.read_csv(filename)
    return float(f"{df['tmax'].max():.2f}")

def max_temp_diff(filename):
    df = pd.read_csv(filename)
    df["tdiff"] = df["tmax"] - df["tmin"]
    return float(f"{df['tdiff'].max():.2f}")

def rain_diff(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    return float(f"{abs(df1['rainfall'].sum() - df2['rainfall'].sum()):.2f}")

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
    download_weather(146, 2012, "weather_146_2012.csv")
    download_weather(146, 2024, "weather_146_2024.csv")
    download_weather(146, 2020, "weather_146_2020.csv")
    download_weather(119, 2019, "weather_119_2019.csv")
    download_weather(146, 2019, "weather_146_2019.csv")

    a1 = rainfall("weather_146_2012.csv")
    a2 = max_of_tmax("weather_146_2024.csv")
    a3 = max_temp_diff("weather_146_2020.csv")
    a4 = rain_diff("weather_119_2019.csv", "weather_146_2019.csv")

    submit_to_api("박예원", "스마트팜학과", "202210076", a1, a2, a3, a4, verbose=True)

if __name__ == "__main__":
    main()
