
import pandas as pd

# 서울 날씨 데이터 불러오기
df = pd.read_csv("data/seoul_weather.csv")

print("========== 데이터 확인 ==========")

# 데이터 크기 확인
print("\n1. 데이터 크기")
print(df.shape)

# 데이터 항목 확인
print("\n2. 데이터 항목")
print(df.columns.tolist())

# 처음 5개 데이터 확인
print("\n3. 처음 5개 데이터")
print(df.head())

# 빈 데이터 확인
print("\n4. 항목별 빈 데이터 개수")
print(df.isnull().sum())

# 전체 데이터 요약
print("\n5. 기온 데이터 통계")
print(df[["mean_temp", "max_temp", "min_temp"]].describe())

print("\n데이터 검사 완료!")
