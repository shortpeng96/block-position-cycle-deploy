# Block Position Cycle 프로젝트 작업 규칙

## 먼저 읽을 파일

1. `00_먼저_읽으세요.md`
2. `Predicting 'Block Position Cycle'_0_overview.ipynb`
3. 현재 수정 대상인 `streamlit_app.py`
4. 분석 논리가 필요하면 1~6번 노트북과 `Docs/어마어마한 논리적 오류 발견.md`, `Docs/어마어마한 논리적 오류 발견 후 서사를 어떻게 할것인가에 대하여....md`

## 프로젝트의 핵심 논리

- `Block Position Cycle`은 실제 완료 후 측정한 실적 공기가 아니라 스케줄링 전에 제공된 사전 기준 처리기간으로 해석한다.
- 사전 Cycle 예측은 Position이 정해지기 전이므로 Set A의 Block 고유 특성만 사용한다.
- Position, Initial, 계획일정과 Delay는 회귀모델의 입력값이 아니라 기존 Scheduling Result에서 조회하는 결과다.
- Scheduling Result 화면은 새 스케줄을 계산하지 않는다.
- Cycle Stability와 Delay Performance는 서로 다른 평가축이며 하나의 절대점수처럼 합치지 않는다.
- 실제 야드 좌표와 실제 선체 형상은 제공되지 않았다. 야드 평면도와 Isometric 선체는 조회를 돕는 개념도임을 항상 표시한다.

## 코드 작성 수준과 스타일

- 사용자는 Python을 약 한 달 배운 수준이다. 짧고 직접적인 pandas, scikit-learn, Plotly, Streamlit 코드를 우선한다.
- 복잡한 클래스, 과도한 함수 분리, 새로운 프레임워크와 불필요한 의존성을 추가하지 않는다.
- 코드 한 줄을 지나치게 길게 쓰지 않는다.
- 기존 주석 방식, Markdown 문체, 그래프 해석 형식을 유지한다.
- 계산 로직과 기존 분석 결과는 사용자 요청 없이 변경하지 않는다.
- 사용자가 만든 파일과 원본 데이터를 삭제하거나 덮어쓰지 않는다.

## Streamlit 화면 규칙

- 기본 배경은 흰색이고 강조색은 Samsung Blue `#034EA2`를 사용한다.
- 그래프는 구분이 필요할 때 보조색을 사용할 수 있지만 다홍색 계열은 사용하지 않는다.
- 모든 표와 그래프에는 의미와 한계를 설명하는 짧은 해석을 붙인다.
- Main은 `사전 Cycle 예측`과 `기존 Scheduling Result 조회` 두 세부 페이지로 구분한다.
- 무거운 3D 렌더링 대신 정적인 2D Isometric 개념도를 사용한다.
- 반복해서 읽는 데이터와 모델은 Streamlit 캐시를 사용한다.
- 위젯 하나를 조작할 때 무거운 전체 화면이 불필요하게 다시 계산되지 않도록 form과 fragment 구조를 유지한다.

## 경로와 실행 규칙

- 모든 파일 경로는 `Path(__file__).resolve().parent`를 기준으로 한 상대경로를 유지한다.
- 특정 PC의 `N:` 드라이브나 사용자 폴더를 코드에 직접 넣지 않는다.
- 실행 명령은 `python -m streamlit run streamlit_app.py`를 기준으로 한다.

## 수정 후 최소 검증

다음 두 검증을 실행하고 오류가 없음을 확인한다.

```powershell
python -m py_compile streamlit_app.py
python -c "from streamlit.testing.v1 import AppTest; at=AppTest.from_file('streamlit_app.py'); at.run(timeout=120); print(len(at.exception))"
```

가능하면 수정한 화면을 브라우저에서 직접 확인한다. 기존 사용자 변경과 무관한 파일은 수정하지 않는다.
