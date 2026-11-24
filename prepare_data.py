
import pandas as pd
import numpy as np
from pathlib import Path

# 1. 서울 날씨 데이터 불러오기
df = pd.read_csv("data/seoul_weather.csv")

print("AI 학습용 데이터를 만들고 있습니다...")

# 2. 날짜순으로 정렬하기
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# 3. 내일의 평균 기온을 새로운 정답 데이터로 만들기
df["next_day_temp"] = df["mean_temp"].shift(-1)

# 4. 내일의 날짜에서 계절 정보 만들기
tomorrow = df["date"] + pd.Timedelta(days=1)

df["month"] = tomorrow.dt.month
df["day_of_year"] = tomorrow.dt.dayofyear

# 계절의 반복성을 반영하는 숫자 정보
df["day_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365.25)
df["day_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365.25)

# 5. AI가 학습할 입력 데이터 선택하기
features = [
    "mean_temp",
    "max_temp",
    "min_temp",
    "humidity",
    "precipitation",
    "max_wind_speed",
    "month",
    "day_sin",
    "day_cos"
]

target = "next_day_temp"

# 6. 빈 데이터 제거하기
training_data = df[features + [target]].dropna().copy()

# 7. 학습용 데이터 저장하기
output_path = Path("data/weather_training.csv")
training_data.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

# 8. 결과 확인하기
print("\n========== 데이터 제작 완료 ==========")
print("전체 학습 데이터 수:", len(training_data))

print("\n입력 데이터 항목:")
print(features)

print("\n예측할 정답:")
print("다음 날 평균 기온")

print("\n처음 5개 데이터:")
print(training_data.head())

print("\n저장 위치:", output_path)
print("\nAI 학습용 데이터 준비 성공!")
