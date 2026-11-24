
import json
import csv
import urllib.request
import urllib.parse
from pathlib import Path

# 1. 서울의 위치 정보
latitude = 37.5665
longitude = 126.9780

# 2. 수집할 날짜
start_date = "2015-01-01"
end_date = "2025-12-31"

# 3. 수집할 날씨 항목
daily_variables = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max"
]

# 4. API 요청 주소와 설정
base_url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "daily": ",".join(daily_variables),
    "timezone": "Asia/Seoul",
    "temperature_unit": "celsius",
    "wind_speed_unit": "kmh",
    "precipitation_unit": "mm",
    "models": "era5"
}

url = base_url + "?" + urllib.parse.urlencode(params)

print("서울 날씨 데이터를 수집하고 있습니다...")
print("수집 기간:", start_date, "~", end_date)

# 5. 날씨 데이터 가져오기
try:
    with urllib.request.urlopen(url, timeout=60) as response:
        weather_data = json.loads(response.read().decode("utf-8"))

    daily_data = weather_data["daily"]

    # 6. CSV 파일 저장 위치 만들기
    data_folder = Path(__file__).parent / "data"
    data_folder.mkdir(exist_ok=True)

    file_path = data_folder / "seoul_weather.csv"

    # 7. CSV 파일로 저장하기
    headers = [
        "date",
        "mean_temp",
        "max_temp",
        "min_temp",
        "humidity",
        "precipitation",
        "max_wind_speed"
    ]

    columns = [
        "time",
        "temperature_2m_mean",
        "temperature_2m_max",
        "temperature_2m_min",
        "relative_humidity_2m_mean",
        "precipitation_sum",
        "wind_speed_10m_max"
    ]

    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for i in range(len(daily_data["time"])):
            row = [
                daily_data[column][i]
                for column in columns
            ]
            writer.writerow(row)

    print("\n데이터 수집 성공!")
    print("수집된 날짜 수:", len(daily_data["time"]))
    print("저장 위치:", file_path)

except Exception as error:
    print("\n데이터 수집 중 오류가 발생했습니다.")
    print("오류 내용:", error)
