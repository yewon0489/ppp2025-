import os.path
import requests
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib


def download_weather(station_id, s_year, e_year, filename):
    URL = f"https://api.taegon.kr/stations/{station_id}/?sy={s_year}&ey={e_year}&format=csv"
    with open(filename, "w", encoding="UTF-8") as f:
        resp = requests.get(URL)
        resp.encoding = "UTF-8"
        f.write(resp.text)


def main():
    filename = "weather(243)_1980-2024.csv"
    if not os.path.exists(filename):
        download_weather(156, 1980, 2024, filename)

    df = pd.read_csv(filename, skipinitialspace=True)
    df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    
    winter = df[(df["month"] == 12) | (df["month"] == 1) | (df["month"] == 2)]
    summer = df[(df["month"] >= 6) & (df["month"] <= 8)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].hist(winter["tavg"].dropna(), bins=30, color="blue", alpha=0.7)
    axes[0].set_title("겨울철 평균기온 분포 (12~2월)")
    axes[0].set_xlabel("평균기온 (℃)")
    axes[0].set_ylabel("빈도")

    axes[1].hist(summer["tavg"].dropna(), bins=30, color="red", alpha=0.7)
    axes[1].set_title("여름철 평균기온 분포 (6~8월)")
    axes[1].set_xlabel("평균기온 (℃)")
    axes[1].set_ylabel("빈도")

    plt.tight_layout()
    plt.savefig("seasonal_temp_.png")
    plt.show()


if __name__ == "__main__":
    main()