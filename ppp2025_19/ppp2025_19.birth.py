import os.path
import requests
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib



def download_weather(station_id, s_year, e_year, filename):

    URL =f"https://api.taegon.kr/stations/{station_id}/?sy={s_year}&ey={e_year}&format=csv"
    with open(filename, "w", encoding="UTF-8") as f:
        resp = requests.get(URL)
        resp.encoding = "UTF-8"
        f.write(resp.text)


def main():
    filename = "weather(156)_2003-2024.csv"
    if not os.path.exists(filename):
        download_weather(156, 2003, 2024, filename)

    df = pd.read_csv(filename, skipinitialspace=True)
    df["date"] = pd.to_datetime(df[["year", "month", "day"]])

    df_birthday = df[(df["month"] == 11) & (df["day"] == 4)].copy()

    year = df_birthday["year"]
    temp = df_birthday["tavg"]

    fig, ax = plt.subplots()
    ax.bar(year.astype(str), temp, color="green")
    ax.set_ylim([5, 35])
    ax.set_title("내 생일(11/04) 평균기온")
    ax.set_xlabel("연도")
    ax.set_ylabel("평균 기온 (℃)")

    plt.savefig("birth_graph.png")
    plt.show()

if __name__=="__main__":
    main()


