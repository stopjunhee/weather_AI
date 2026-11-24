
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from pathlib import Path

# AI 모델과 데이터 불러오기
df = pd.read_csv("data/seoul_weather.csv")
model = joblib.load("models/weather_model.joblib")
features = joblib.load("models/feature_columns.joblib")

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# 다음 날짜의 기온 예측
latest = df.iloc[-1]
tomorrow = latest["date"] + pd.Timedelta(days=1)
day_of_year = tomorrow.dayofyear

input_data = pd.DataFrame([{
    "mean_temp": latest["mean_temp"],
    "max_temp": latest["max_temp"],
    "min_temp": latest["min_temp"],
    "humidity": latest["humidity"],
    "precipitation": latest["precipitation"],
    "max_wind_speed": latest["max_wind_speed"],
    "month": tomorrow.month,
    "day_sin": np.sin(2 * np.pi * day_of_year / 365.25),
    "day_cos": np.cos(2 * np.pi * day_of_year / 365.25)
}])

prediction = model.predict(input_data[features])[0]

# 옷차림 추천
def recommend_clothes(temp):
    if temp < 5:
        return "두꺼운 패딩, 목도리, 장갑"
    elif temp < 12:
        return "코트 또는 두꺼운 재킷"
    elif temp < 20:
        return "가디건 또는 가벼운 재킷"
    elif temp < 27:
        return "긴팔 또는 반팔"
    else:
        return "얇은 반팔과 시원한 옷차림"

# 메뉴 화면
while True:
    print("\n==============================")
    print("       WEATHER AI")
    print("==============================")
    print("1. 다음 날짜 기온 예측")
    print("2. 옷차림 추천")
    print("3. 기온 그래프 보기")
    print("0. 프로그램 종료")

    choice = input("원하는 기능을 선택하세요: ")

    if choice == "1":
        print("\n예측 대상 날짜:", tomorrow.date())
        print("AI 예측 기온:", round(prediction, 1), "℃")

    elif choice == "2":
        print("\n예측 기온:", round(prediction, 1), "℃")
        print("추천 옷차림:", recommend_clothes(prediction))

    elif choice == "3":
        recent = df.tail(30)

        plt.figure(figsize=(12, 6))
        plt.plot(
            recent["date"],
            recent["mean_temp"],
            marker="o",
            label="Past Temperature"
        )
        plt.scatter(
            [tomorrow],
            [prediction],
            color="red",
            s=120,
            label="AI Prediction"
        )

        plt.title("Seoul Weather AI")
        plt.xlabel("Date")
        plt.ylabel("Temperature (Celsius)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    elif choice == "0":
        print("Weather AI를 종료합니다.")
        break

    else:
        print("잘못된 입력입니다. 다시 선택해주세요.")
