
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from pathlib import Path

# 1. 날씨 데이터와 AI 모델 불러오기
df = pd.read_csv("data/seoul_weather.csv")
model = joblib.load("models/weather_model.joblib")
features = joblib.load("models/feature_columns.joblib")

# 2. 날짜순으로 정렬
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# 3. 가장 최근 날씨 데이터 선택
latest = df.iloc[-1]
tomorrow = latest["date"] + pd.Timedelta(days=1)

# 4. AI 입력 데이터 만들기
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

input_data = input_data[features]

# 5. 다음 날 평균 기온 예측
prediction = model.predict(input_data)[0]

print("AI 예측 기온:", round(prediction, 1), "℃")

# 6. 최근 30일 날씨 데이터 선택
recent = df.tail(30).copy()

# 7. 그래프 제작
plt.figure(figsize=(12, 6))

plt.plot(
    recent["date"],
    recent["mean_temp"],
    marker="o",
    label="Past Temperature"
)

# 예측 날짜 표시
plt.scatter(
    [tomorrow],
    [prediction],
    color="red",
    s=120,
    label="AI Prediction",
    zorder=5
)

plt.plot(
    [recent["date"].iloc[-1], tomorrow],
    [latest["mean_temp"], prediction],
    linestyle="--",
    color="red"
)

plt.title("Seoul Weather AI - Temperature Prediction")
plt.xlabel("Date")
plt.ylabel("Temperature (Celsius)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# 8. 그래프 이미지 저장
output_path = Path("weather_prediction.png")
plt.savefig(output_path, dpi=150)

print("그래프 저장 완료:", output_path)

# 9. 그래프 화면에 표시
plt.show()
