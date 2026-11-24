
import pandas as pd
import numpy as np
import joblib

from pathlib import Path

print("================================")
print("       WEATHER AI PREDICTION")
print("================================")

# 1. 학습된 AI 모델 불러오기
model = joblib.load("models/weather_model.joblib")

# 2. 학습에 사용한 입력 항목 불러오기
features = joblib.load("models/feature_columns.joblib")

# 3. 서울 날씨 데이터 불러오기
df = pd.read_csv("data/seoul_weather.csv")

# 4. 가장 최근 날짜의 날씨 데이터 선택
df["date"] = pd.to_datetime(df["date"])
latest = df.sort_values("date").iloc[-1]

# 5. 예측 대상 날짜 계산
tomorrow = latest["date"] + pd.Timedelta(days=1)

# 6. AI에 입력할 데이터 만들기
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

# 7. 학습 당시와 동일한 항목 순서로 정렬
input_data = input_data[features]

# 8. 기온 예측
prediction = model.predict(input_data)[0]

# 9. 결과 출력
print("\n예측 기준 날짜:", latest["date"].date())
print("예측 대상 날짜:", tomorrow.date())

print("\n========== 예측 결과 ==========")
print("예상 평균 기온:", round(prediction, 1), "℃")

# 10. 옷차림 추천
print("\n========== 옷차림 추천 ==========")

if prediction < 5:
    print("두꺼운 패딩과 목도리를 추천합니다.")
elif prediction < 12:
    print("코트나 두꺼운 재킷을 추천합니다.")
elif prediction < 20:
    print("가디건이나 가벼운 재킷을 추천합니다.")
elif prediction < 27:
    print("얇은 긴팔이나 반팔을 추천합니다.")
else:
    print("시원한 반팔과 가벼운 옷을 추천합니다.")

print("\nWEATHER AI 예측 완료!")
