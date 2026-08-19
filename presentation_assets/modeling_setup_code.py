# ============================================================
# 1. 라이브러리 불러오기
# ============================================================

# 파일 및 설정값 처리
import json
from pathlib import Path

# 모델 저장 및 데이터 처리
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Scikit-learn 공통 기능
from sklearn.base import clone
from sklearn.compose import ColumnTransformer

# 회귀모델
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge

# from sklearn.linear_model import Lasso, ElasticNet
# 규제모델 비교 자체가 목적이 아니므로,
# 다중공선성 완화를 대표하는 Ridge만 사용

from sklearn.tree import DecisionTreeRegressor

# from sklearn.ensemble import GradientBoostingRegressor
# 앙상블 모델 종류를 과도하게 늘리지 않고,
# Feature Set 및 스케줄링 방식 비교에 집중하기 위해 Random Forest만 사용

# 모델 평가 및 학습
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ============================================================
# 2. 분석 데이터 및 Feature Set 설정 파일 경로 지정
# ============================================================

# 전처리와 모델링 결과 저장 경로
PROCESSED_DIR = Path('data') / 'processed'
OUTPUT_DIR = Path('outputs') / '3_modeling'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 전처리가 완료된 DDQN 분석 데이터
DATA_PATH = PROCESSED_DIR / 'analysis_DDQN.csv'

# Set A / B / C 및 Target 정보가 저장된 JSON 파일
FEATURE_PATH = PROCESSED_DIR / 'feature_sets_DDQN.json'


# ============================================================
# 3. 분석 데이터 불러오기
# ============================================================

analysis = pd.read_csv(DATA_PATH)


# ============================================================
# 4. Feature Set 설정 불러오기
# ============================================================

# JSON 파일에서 Target과 Set A / B / C 변수 목록 불러오기
with open(FEATURE_PATH, encoding='utf-8') as file:
    feature_config = json.load(file)

# 종속변수 설정
target_col = feature_config['target']

# Feature Set 구성
# Set A → Block 자체 특성
# Set B → Block + DDQN이 선택한 Position 특성
# Set C → Block + Position + Initial 상태 정보
feature_sets = {
    'Set A - Block': feature_config['set_a'],
    'Set B - Block + Position': feature_config['set_b'],
    'Set C - Block + Position + Initial': feature_config['set_c']
}


# ============================================================
# 5. 분석에 필요한 컬럼 존재 여부 확인
# ============================================================

# Target과 모든 Feature Set에서 사용하는 컬럼을 하나의 집합으로 정리
required_cols = set(
    [target_col]
    + sum(feature_sets.values(), [])
)

# 필요한 컬럼 중 실제 analysis 데이터에 존재하지 않는 컬럼 확인
missing_cols = sorted(
    required_cols - set(analysis.columns)
)


# ============================================================
# 6. 데이터 및 Feature Set 기본 정보 확인
# ============================================================

print('데이터 크기:', analysis.shape)
print('전체 결측값:', analysis.isna().sum().sum())
print('누락된 필요 컬럼:', missing_cols)

print()
print('변수 세트 크기:')

for name, columns in feature_sets.items():
    print(f'- {name}: {len(columns)}개')


# ============================================================
# 7. 필수 컬럼 누락 여부 최종 검증
# ============================================================

# 필요한 컬럼이 하나라도 누락된 경우 이후 모델링을 중단
assert not missing_cols, (
    f'분석 데이터에 필요한 컬럼이 없습니다: {missing_cols}'
)
