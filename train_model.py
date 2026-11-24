
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error, r2_score

# 1. 학습 데이터 불러오기
df = pd.read_csv("data/weather_training.csv")

print("========== WEATHER AI 학습 시작 ==========")

# 2. 입력 데이터와 정답 데이터 분리
X = df.drop(columns=["next_day_temp"])
y = df["next_day_temp"]

# 3. 시간 순서를 유지해서 학습 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

print("학습 데이터:", len(X_train))
print("테스트 데이터:", len(X_test))

# 4. 세 가지 AI 모델 준비
models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}

# 5. 모델별 학습 및 평가
best_model = None
best_model_name = ""
best_mae = float("inf")

for name, model in models.items():

    print(f"\n[{name}] 학습 중...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("MAE:", round(mae, 3), "도")
    print("RMSE:", round(rmse, 3), "도")
    print("R²:", round(r2, 3))

    if mae < best_mae:
        best_mae = mae
        best_model = model
        best_model_name = name

# 6. 가장 좋은 모델 저장
model_folder = Path("models")
model_folder.mkdir(exist_ok=True)

joblib.dump(best_model, model_folder / "weather_model.joblib")

# 7. 사용한 입력 항목도 함께 저장
joblib.dump(
    X.columns.tolist(),
    model_folder / "feature_columns.joblib"
)

print("\n========== 학습 완료 ==========")
print("가장 좋은 모델:", best_model_name)
print("가장 낮은 MAE:", round(best_mae, 3), "도")
print("모델 저장 위치: models/weather_model.joblib")
