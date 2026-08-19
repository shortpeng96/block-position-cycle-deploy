# ============================================================
# 1. Train / Test 데이터 인덱스 분리
# ============================================================

# 전체 데이터의 index를 기준으로 학습용 80%, 테스트용 20%로 분리
# → Set A / B / C 모두 동일한 행을 사용하여 공정하게 비교
train_index, test_index = train_test_split(analysis.index, test_size=0.2, random_state=42)

# 종속변수도 동일한 index 기준으로 학습용 / 테스트용 분리
y_train = analysis.loc[train_index, target_col]
y_test = analysis.loc[test_index, target_col]


# ============================================================
# 2. 비교할 회귀모델 정의
# ============================================================

# 동일한 Feature Set에 여러 회귀모델을 적용하여 성능 비교
model_candidates = {
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1),

    # 'Lasso': Lasso(alpha=1.0),
    # 'Elastic Net': ElasticNet(alpha=1.0, l1_ratio=0.5),
    # 'Gradient Boosting': GradientBoostingRegressor(random_state=42)
}

# 선정 이유
# Linear Regression → 기본 선형 기준 모델로 변수와 Cycle의 관계 확인
# Ridge → 다중공선성이 있는 경우 L2 규제를 통한 안정성 확인
# Decision Tree → 선형모델이 설명하지 못하는 비선형 관계 확인
# Random Forest → 여러 Tree를 결합해 안정적인 비선형 예측 성능 확인

# 제외 사유
# Lasso / Elastic Net → 규제모델 비교 자체가 목적이 아니므로 대표 모델인 Ridge만 사용
# Gradient Boosting → 모델 종류를 과도하게 늘리지 않고 Feature Set 및 스케줄링 방식 비교에 집중하기 위해 제외


# ============================================================
# 3. 전처리 + 모델 학습 Pipeline 생성 함수
# ============================================================

def build_pipeline(feature_cols, estimator):

    # 선택한 독립변수를 수치형 / 범주형 변수로 구분
    numeric_cols = analysis[feature_cols].select_dtypes(include='number').columns.tolist()
    categorical_cols = [col for col in feature_cols if col not in numeric_cols]

    # 수치형은 표준화, 범주형은 One-Hot Encoding 적용
    preprocessor = ColumnTransformer([
        ('numeric', StandardScaler(), numeric_cols),
        ('categorical', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

    # 전처리와 회귀모델을 하나의 Pipeline으로 연결
    return Pipeline([
        ('preprocessor', preprocessor),
        ('model', clone(estimator))
    ])


# ============================================================
# 4. 회귀모델 성능 평가 함수
# ============================================================

def regression_metrics(y_true, y_pred):

    # MAE, RMSE, R²를 이용하여 예측 성능 평가
    return {
        'MAE': mean_absolute_error(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'R2': r2_score(y_true, y_pred)
    }


# ============================================================
# 5. Feature Set별 모델 비교 함수
# ============================================================

def compare_models(feature_cols, candidates):

    # 동일한 train/test index를 기준으로 Feature Set만 변경
    X_train = analysis.loc[train_index, feature_cols]
    X_test = analysis.loc[test_index, feature_cols]

    records = []
    fitted_models = {}

    # 후보 모델을 동일한 데이터에 순차적으로 학습
    for model_name, estimator in candidates.items():

        pipeline = build_pipeline(feature_cols, estimator)
        pipeline.fit(X_train, y_train)
        prediction = pipeline.predict(X_test)

        # 모델별 성능지표 저장
        records.append({
            'Model': model_name,
            **regression_metrics(y_test, prediction)
        })

        # 이후 잔차분석 등에 활용할 수 있도록 학습된 모델 저장
        fitted_models[model_name] = pipeline

    # RMSE가 낮은 모델부터 정렬
    results = pd.DataFrame(records).sort_values('RMSE').reset_index(drop=True)

    return results, fitted_models


# ============================================================
# 6. Train / Test 분리 결과 확인
# ============================================================

print('학습 데이터:', len(train_index))
print('테스트 데이터:', len(test_index))
