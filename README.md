
# Weather AI - 서울 날씨 및 기온 예측 프로그램

## 1. 프로젝트 소개
서울의 과거 날씨 데이터를 활용하여 머신러닝 모델을 학습하고,
다음 날짜의 평균 기온을 예측하는 프로그램입니다.

## 2. 주요 기능
- 서울 과거 날씨 데이터 수집
- 날씨 데이터 전처리
- 머신러닝 모델 학습 및 성능 비교
- 다음 날짜 평균 기온 예측
- 기온에 따른 옷차림 추천
- 과거 기온 및 예측 기온 그래프 시각화

## 3. 사용 기술
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Joblib

## 4. 실행 방법

필요한 라이브러리 설치:

```bash
pip install -r requirements.txt
```

프로그램 실행:

```bash
python main.py
```

## 5. 프로젝트 파일 구성

- data/: 날씨 데이터 및 학습 데이터
- models/: 학습된 AI 모델
- collect_weather.py: 날씨 데이터 수집
- prepare_data.py: 데이터 전처리
- train_model.py: AI 모델 학습
- predict.py: 기온 예측
- visualize.py: 그래프 시각화
- main.py: 통합 프로그램 실행

## 6. 데이터 안내
서울의 과거 날씨 데이터를 사용합니다.
현재 모델의 예측 대상은 데이터의 마지막 날짜 다음 날입니다.
실시간 일기예보가 아닌 과거 데이터 기반의 머신러닝 예측입니다.
