# 프로젝트 주제 변경·확장 과정 정리  
## `Block Position Cycle`을 '공기 예측값'으로 보던 단계에서 '사전 기준 처리기간과 스케줄링 결과의 관계 분석'으로

> 이 문서는 프로젝트 진행 중 `Block Position Cycle`의 의미를 다시 해석하면서 분석 주제가 변경·확장된 과정을 정리한 기록이다.  
> 처음에는 `Block Position Cycle`을 사실상 **블록의 공기(처리기간)** 로 보고 이를 회귀분석으로 예측하는 프로젝트로 시작했다. 그러나 EDA와 단계적 회귀분석 결과가 예상과 다르게 나타났고, 그 원인을 확인하기 위해 데이터셋 구조와 관련 선행연구를 다시 검토하면서 프로젝트의 질문 자체가 바뀌었다.

---

## 1. 최초의 프로젝트 방향 — `Block Position Cycle`을 공기로 보고 예측하기

프로젝트 시작 당시에는 `block_information_table`에 포함된 `block position cycle`을 각 Block의 작업에 필요한 **공기 또는 처리기간**으로 이해했다.

따라서 가장 처음 설정한 회귀분석의 질문은 단순했다.

> **Block의 여러 특성을 이용해 `Block Position Cycle`을 얼마나 잘 예측할 수 있는가?**

이때는 다음과 같은 단계적 분석을 구상했다.

```text
Set A : Block 정보
        ↓
Set B : Block + Position 정보
        ↓
Set C : Block + Position + Initial 정보
```

처음 생각은 비교적 자연스러웠다.

- Block의 길이, 폭, 무게, Block Type만 사용하는 것보다
- 실제 작업이 이루어질 Position의 크기, 인양능력, 작업구역, 작업조 등의 정보를 추가하고
- 여기에 스케줄링 시작 시점의 Initial 상태까지 더하면

모델이 더 많은 정보를 사용하므로 `Block Position Cycle`을 더 잘 설명할 수 있을 것이라고 예상했다.

즉 처음에는 **"정보가 많아질수록 공기 예측 성능도 좋아질 것"**이라는 관점에서 프로젝트를 진행했다.

---

## 2. 첫 번째 의문 — Position의 영향력이 예상보다 낮았다

그런데 EDA 과정에서 예상과 다른 신호가 나타났다.

Block의 물리량과 일정 관련 변수는 `Block Position Cycle`과 어느 정도 관계를 보였지만, Position 관련 변수들은 기대했던 만큼 강한 관계가 나타나지 않았다.

특히 `Block Position Cycle`을 실제로 Position에서 작업한 결과로 발생한 공기라고 생각하고 있었다면, Position의 크기·인양능력·작업구역·속성 등이 어느 정도 강한 설명력을 가질 것으로 예상할 수 있다.

하지만 실제 분석에서는 Position 정보의 영향력이 생각보다 크지 않았다.

이 시점부터 다음과 같은 의문이 생겼다.

> **정말 `Block Position Cycle`이 Position에서 작업한 결과로 생긴 실제 공기인가?**

---

## 3. 두 번째 의문 — 데이터를 추가했는데 오히려 예측력이 낮아졌다

이후 Block → Position → Initial을 차례로 연결하고, 동일한 모델과 동일한 Train/Test 조건으로 Set A, Set B, Set C를 비교했다.

그런데 기대와 달리 Position과 Initial 정보를 추가할수록 예측 성능이 좋아지지 않았고, 오히려 낮아지는 경향이 나타났다.

```text
Set A : Block
        ↓
Set B : Block + Position
        ↓
Set C : Block + Position + Initial

예상 : 정보가 추가될수록 성능 향상
실제 : 정보가 추가되어도 성능이 향상되지 않거나 오히려 저하
```

처음에는 이것을 모델링 문제로 볼 수도 있었다.

- 불필요한 변수가 추가됐는가?
- 다중공선성이 생겼는가?
- 파생변수가 과도하게 중복됐는가?
- Position 정보가 실제로 중요하지 않은가?

하지만 더 근본적인 질문이 생겼다.

> **혹시 우리가 종속변수인 `Block Position Cycle`의 의미 자체를 잘못 이해한 것은 아닐까?**

이 의문 때문에 데이터셋의 구조와 관련 조선 스케줄링·공수 산정 선행연구를 다시 확인하게 되었다.

---

# 4. 자료 재검토 — `Block Position Cycle`의 의미를 다시 찾기

## 4.1 현재 데이터셋에서 확인할 수 있는 사실

현재 사용 중인 `Data of Ship Block Scheduling in English` 데이터셋은 Block 정보, Position 정보, Initial 상태, 그리고 DQN/DDQN 및 여러 휴리스틱 스케줄링 결과로 구성되어 있다.

중요한 점은 `block position cycle`이 **Result Table에서 생성된 값이 아니라, 스케줄링 이전 입력자료인 Block Information Table에 이미 존재한다는 것**이다.

즉 데이터 흐름은 다음과 같이 보는 것이 더 자연스럽다.

```text
Block 정보
 ├─ 크기
 ├─ 무게
 ├─ Block Type
 ├─ 일정 조건
 └─ Block Position Cycle
        ↓
스케줄링 알고리즘
        ↓
Block별 Position / 일정 결정
```

따라서 `Block Position Cycle`은 **Position이 선택된 이후 실제 작업 결과로 계산된 값이라기보다, 스케줄링에 입력되는 사전 정보**에 가깝다.

현재 공개된 데이터셋 소개자료만으로는 `block position cycle`의 산정식이나 정확한 공식 정의까지 확인할 수 없다.  
따라서 아래 해석은 **관련 선행연구와 데이터 구조를 바탕으로 한 프로젝트상의 해석**이라는 점을 명확히 한다.

---

## 4.2 가장 직접적인 선행연구 — `assembly cycle`을 스케줄링 이전 입력값으로 사용

Jiang, Zhou, Tao, Li의 **Knowledge-Based Curved Block Construction Scheduling and Application in Shipbuilding**에서는 곡블록(curved block) 생산 스케줄링을 설명하면서 Block별 `assembly cycle`을 **스케줄링 이전의 Block 선별 기준**으로 사용한다.[1]

논문에서는 Block screening rule의 입력요소로 `assembly cycle` 또는 Block weight를 사용하며, 예시 규칙으로 다음과 같은 구조를 제시한다.

```text
Block의 assembly cycle
        ↓
Block screening
        ↓
Fixed-position / General-position 등의 Task Table 분류
        ↓
스케줄링 알고리즘 선택
        ↓
Position 및 일정 결정
```

즉 **Cycle이 스케줄링 결과가 아니라 스케줄링을 수행하기 전에 이미 존재하는 Block의 계획 정보**라는 구조가 확인된다.

이 점은 현재 데이터셋의 `block position cycle`이 Block Information Table에 사전에 존재한다는 구조와 매우 유사하다.

물론 두 연구의 `assembly cycle`과 현재 데이터셋의 `block position cycle`이 **완전히 동일한 변수라고 단정할 수는 없다.**

하지만 최소한 조선 블록 생산 스케줄링 분야에서 **Block별 Cycle이 사전 계획정보로 설정되고, 그 값을 이용해 이후 스케줄링이 수행되는 사례**가 존재한다는 점은 확인할 수 있다.

---

## 4.3 같은 연구에서 확인한 두 번째 핵심 — 스케줄링 후 상황은 다시 바뀔 수 있다

같은 연구에서는 실제 Block 생산이 항상 최초 스케줄링 계획대로 진행되지는 않는다고 설명한다.[1]

생산 과정에서 여러 disturbance가 발생하여 construction delay가 발생할 수 있고, 이에 따라 후속 Block의 일정에도 영향이 생기므로 실제 작업상황을 추적하면서 스케줄을 다시 조정해야 한다.

또한 Plan Adjustment Module에서는 **실제 processing 상황과 real-time position 정보를 이용해 계획을 조정하며, processing cycle도 조정될 수 있음**을 설명한다.[1]

이 구조는 본 프로젝트의 방향을 이해하는 데 매우 중요하다.

```text
사전에 설정된 Cycle
        ↓
초기 스케줄링
        ↓
Position / 작업장 / 자원 조건 결정
        ↓
실제 작업환경 및 생산상황 발생
        ↓
필요 시 Cycle / Schedule 조정
```

즉 조선 생산계획에서 Cycle은 한 번 정하면 절대 변하지 않는 '실적값'이라기보다, **스케줄링과 생산을 위해 사전에 설정하고 실제 상황에 따라 조정될 수 있는 계획 기준값**으로 이해할 여지가 있다.

---

## 4.4 Man-hour 연구 — 사전 작업량/시간은 무엇을 고려해 산정되는가?

`Block Position Cycle`의 정확한 산정식은 찾을 수 없었기 때문에, 다음으로 조선업에서 작업시간과 생산계획을 사전에 산정하는 대표 개념인 **man-hour** 관련 연구를 확인했다.

Hur et al.의 **A study on the man-hour prediction system for shipbuilding**에서는 man-hour를 작업에 필요한 **인력과 시간의 결합 단위**로 설명하며, 조선소에서 생산계획을 위해 사전에 예측해 사용한다고 설명한다.[2]

이 연구에서 특히 중요한 내용은 다음과 같다.

### ① 전문가가 사전에 예측한다

조선소의 man-hour는 작업이 끝난 뒤 단순히 측정하는 값만이 아니라, 생산계획 단계에서 전문가가 사전에 예측하여 사용한다.[2]

그리고 전문가의 예측에는 단순한 물리량만 들어가는 것이 아니라,

- 작업의 특성
- 작업 환경
- 과거 경험
- 작업 시점
- 작업 종류

등 여러 요소가 종합적으로 고려될 수 있다고 설명한다.[2]

### ② 예측 시점이 달라지면 사용하는 정보도 달라진다

이 연구는 연간 → 분기 → 월간 → 일간 계획으로 내려오면서 생산 정보가 구체화되고, 사용 가능한 변수가 늘어나는 구조를 설명한다.[2]

즉 초기에는 선박·Block과 같은 기본 사양 중심으로 계획하지만, 실제 생산 시점에 가까워질수록 공정과 작업환경 정보를 더 많이 사용할 수 있다.

### ③ 실제로 사용한 변수도 단순한 크기·무게에 한정되지 않는다

연구에서 man-hour를 예측하기 위해 사용한 변수에는 다음과 같은 항목이 포함된다.[2]

- Block type
- Process code
- Ship type
- Shop code
- Work type
- Work load
- Work organization code
- Jig code

즉 실제 조선 생산계획상의 작업시간/공수는 Block의 물리적 크기만이 아니라 **무슨 공정인지, 어디에서 작업하는지, 작업량이 얼마인지, 어떤 작업조직이 투입되는지** 같은 생산관리 요소와도 관련될 수 있다.

### ④ 숙련도 역시 영향을 줄 수 있다

해당 연구에서는 직영 작업자와 협력사 작업자의 man-hour 차이를 분석하면서 작업자의 숙련도 차이를 고려할 필요가 있다고 해석한다.[2]

또한 향후 연구에서는 작업자의 경험, 교육, 숙련도와 같은 요소를 정량화하면 더 정교한 man-hour 예측이 가능할 수 있다고 제안한다.[2]

---

## 4.5 다른 조선 연구에서 확인되는 생산시간 변동의 원인

Son, Suh, Ha의 **A Heuristic Algorithm for Block Storage Planning in Shipbuilding**에서는 선박 종류와 선박 내 위치 등에 따라 Block의 작업량과 난이도가 달라지고, 그 결과 생산시간의 편차가 발생한다고 설명한다.[3]

또한 조선 생산현장에서는

- 입고 지연
- 생산 공정 차질
- 기상 변화
- 중간 품질검사
- 공정 간 작업부하 불균형

등으로 일정이 빈번하게 달라질 수 있음을 설명한다.[3]

이 연구는 `Block Position Cycle` 자체를 정의하지는 않지만, **Block별 생산시간이 단순한 크기 하나로 결정되는 것이 아니며, 생산환경과 운영상황에 따라 실제 일정이 달라질 수 있다는 배경**을 제공한다.

---

# 5. 따라서 `Block Position Cycle`을 어떻게 해석할 것인가?

위 자료를 종합하면 현재 데이터셋의 `Block Position Cycle`에 대해 다음 세 수준을 구분하는 것이 가장 안전하다.

## 5.1 데이터에서 직접 확인되는 사실

- `Block Position Cycle`은 Block Information Table에 존재한다.
- 즉 DDQN/EDDQN/Heuristic 결과보다 먼저 주어진 값이다.
- 따라서 **스케줄링 이후 발생한 실제 실적 공기라고 보기는 어렵다.**
- 현재 공개자료에는 정확한 산정식이 없다.

## 5.2 선행연구에서 직접 확인되는 사실

- 관련 조선 Block 스케줄링 연구에서는 `assembly cycle`을 사전에 가진 상태에서 스케줄링을 수행하는 사례가 있다.[1]
- 실제 생산상황이 바뀌면 계획을 조정하며 `processing cycle` 역시 조정될 수 있는 구조가 제시되어 있다.[1]
- 조선업의 man-hour는 작업특성·환경·과거경험 등을 고려해 사전에 산정되며, 공정·작업량·작업조직·작업장 등의 요소와 관계가 있다.[2]
- Block별 작업량·난이도 및 생산환경 차이에 따라 생산시간 편차와 일정 변경이 발생할 수 있다.[3]

## 5.3 본 프로젝트에서 사용하는 해석

따라서 본 프로젝트에서는 `Block Position Cycle`을 다음과 같이 정의한다.

> **`Block Position Cycle`은 정확한 산정식은 공개되어 있지 않지만, Block의 물리적 특성과 생산계획상의 여러 조건을 바탕으로 스케줄링 이전에 설정된 Block별 기준 처리기간으로 해석한다.**

여기서 **"물리적 특성과 생산계획상의 여러 조건"**에는 선행연구에서 확인된 다음과 같은 요소들이 개념적으로 포함될 가능성이 있다.

```text
Block의 물리적 특성
 ├─ 크기
 ├─ 형상
 └─ 중량

생산계획 / 작업 특성
 ├─ 공정 종류
 ├─ 작업량
 ├─ 작업장
 ├─ 작업조직
 ├─ 작업 종류
 ├─ 작업 난이도
 ├─ 경험 / 숙련도
 └─ 생산환경
        ↓
사전 기준 작업량 / 작업기간 설정
        ↓
Block Position Cycle과 유사한 계획값
```

단, 이 부분은 반드시 다음과 같이 제한해서 사용한다.

> **현재 데이터셋의 `Block Position Cycle`이 실제로 man-hour를 이용해 계산되었다거나, 위 요소들이 모두 산식에 포함되어 있다고 확인된 것은 아니다.**  
> 관련 조선 생산계획 연구에서 이러한 방식으로 사전 작업량과 작업시간을 산정하는 사례가 확인되었기 때문에, 본 교육용 프로젝트에서는 이를 해석의 근거로 사용한다.

---

# 6. 이 해석을 하고 나니 기존 분석 결과가 오히려 자연스러워졌다

처음에는 Position 정보의 영향력이 낮고 Set B, Set C의 성능이 떨어지는 것이 문제처럼 보였다.

하지만 `Block Position Cycle`이 **스케줄링 이전에 이미 설정된 기준 처리기간**이라면 결과를 다르게 볼 수 있다.

```text
Block 특성
        ↓
사전 Cycle 설정
        ↓
스케줄링 수행
        ↓
Position 선택
```

즉 Set A의 Block 특성은 Cycle이 설정될 당시 존재하던 정보이고, Set B와 Set C에서 추가되는 Position/Initial 정보는 이후 스케줄링 과정에서 결정되거나 의미가 생기는 정보이다.

따라서 데이터가 추가됐다고 해서 반드시 사전 Cycle에 대한 예측력이 올라갈 이유는 없다.

오히려 Set A가 가장 좋은 성능을 보인다면 다음과 같은 해석이 가능하다.

> **사전에 설정된 Block Position Cycle은 Block 자체 특성 및 스케줄링 이전의 생산계획 정보와 더 강하게 연결되어 있으며, 이후 선택된 Position 정보는 이 사전 기준값을 추가적으로 설명하지 못하거나 다른 구조의 정보를 포함하고 있을 수 있다.**

따라서 **예측 성능 저하는 실패가 아니라 프로젝트 질문을 다시 정의하게 만든 분석 결과**가 되었다.

---

# 7. 프로젝트의 주제 변경·확장

## 초기 주제

> **Block의 특성을 이용한 Block Position Cycle(공기) 예측**

초기에는 `Block Position Cycle`을 실제 공기에 가까운 값으로 해석하고, 가능한 많은 정보를 넣어 예측 정확도를 높이는 것이 목표였다.

---

## 변경된 주제

데이터와 선행연구를 다시 검토한 이후에는 질문이 다음과 같이 바뀌었다.

> **스케줄링 이전에 설정된 Block Position Cycle을 Block 자체 특성이 얼마나 설명하는지 확인하고, 스케줄링으로 선택된 Position 정보를 추가했을 때 그 설명력이 어떻게 변하는지 분석한다.**

여기서 중요한 것은 **"Position을 추가하면 반드시 성능이 좋아져야 한다"는 전제를 버리는 것**이다.

성능이 올라가도 결과이고, 내려가도 결과이다.

---

## 최종 확장 방향 — 7개 스케줄링 방식 비교

현재 데이터에는 DDQN뿐 아니라 EDDQN과 5개 Heuristic 스케줄링 결과가 존재한다.

따라서 동일한 Block에 대해 각 스케줄링 방식이 선택한 Position을 연결하고, **동일한 회귀모델·동일한 Train/Test 조건을 유지한 상태에서 Position 정보만 바꾸어 비교**할 수 있다.

```text
사전 Block Position Cycle
        ↑
Block + DDQN Position
Block + EDDQN Position
Block + Heuristic 1 Position
Block + Heuristic 2 Position
...
```

이 분석의 질문은 다음과 같다.

> **각 스케줄링 방법으로 결정된 Position 정보를 사용했을 때, 사전에 설정된 Block Position Cycle의 구조를 얼마나 잘 재현할 수 있는가?**

그리고 단순히 전체 RMSE나 R²만 비교하지 않는다.

특정 스케줄링에서 오차가 커진다면,

- 장기 Cycle에서 차이가 커지는가?
- 대형/고중량 Block에서 커지는가?
- curved Block에서 커지는가?
- 특정 Position Area에서 커지는가?
- 특정 Position 제약에서 커지는가?
- 초기 점유 상태와 관계가 있는가?

등을 잔차분석으로 확인한다.

---

# 8. 이 프로젝트에서 말할 수 있는 것과 말하면 안 되는 것

## 말할 수 있는 것

> 특정 스케줄링 방식이 선택한 Position 정보가 사전 `Block Position Cycle`과 얼마나 높은 설명적 정합성을 보이는가.

> Position 정보를 추가했을 때 사전 Cycle의 재현 성능이 어떻게 달라지는가.

> 어떤 Block 특성에서 사전 Cycle과 회귀 예측값의 차이가 커지는가.

## 말하면 안 되는 것

> "스케줄링 때문에 실제 작업기간이 늘어났다."

> "이 스케줄링 방식이 실제 공기를 악화시켰다."

현재 데이터에는 **스케줄링 이후 실제 작업실적 Cycle**이 존재하지 않기 때문에 인과적으로 이렇게 말할 수 없다.

따라서 본 프로젝트는 끝까지 **사전 기준 Cycle과 스케줄링 결과의 관계 및 정합성 분석**으로 표현한다.

---

# 9. 프로젝트의 최종 서사

이 프로젝트의 가장 중요한 과정은 모델의 성능을 올린 것이 아니라 **종속변수의 의미를 다시 이해한 것**이었다.

```text
① Block Position Cycle을 공기로 해석
        ↓
② Block 특성으로 회귀예측 시작
        ↓
③ Position을 추가했지만 영향력이 낮음
        ↓
④ Initial까지 추가했지만 예측력이 오히려 저하
        ↓
⑤ "왜 데이터가 늘었는데 성능이 떨어지지?"라는 의문 발생
        ↓
⑥ 데이터 구조와 선행연구 재검토
        ↓
⑦ Cycle이 스케줄링 후 실적이 아니라 사전 기준값일 가능성 확인
        ↓
⑧ Set A/B/C의 의미를 다시 정의
        ↓
⑨ 성능 저하 자체를 분석 결과로 해석
        ↓
⑩ DDQN을 넘어 7개 스케줄링 방법의 Position 결과 비교로 확장
        ↓
⑪ 사전 Cycle과 차이가 커지는 Block의 특성을 잔차분석
```

결국 프로젝트는

> **"Block Position Cycle을 잘 예측하는 모델 만들기"**

에서

> **"사전에 설정된 Block Position Cycle과 스케줄링 이후 결정된 Position 정보 사이의 관계를 분석하고, 스케줄링 방법론별로 그 차이를 비교하는 프로젝트"**

로 변경·확장되었다.

이 과정 자체가 이번 프로젝트에서 가장 중요한 분석 결과 중 하나이다.

---

# 참고문헌

[1] Jiang, Z., Zhou, H., Tao, N., & Li, B.  
**Knowledge-Based Curved Block Construction Scheduling and Application in Shipbuilding.**  
*Journal of Shanghai Jiao Tong University (Science)*, 29(5), 759–765.  
DOI: 10.1007/s12204-022-2544-0.  
- `assembly cycle`을 Block screening의 사전 기준으로 사용하는 구조
- Block / workplace / current position status를 기반으로 스케줄링 수행
- 실제 생산 disturbance 발생 시 plan adjustment 수행
- real-time processing 상황에 따라 `processing cycle`을 조정하는 구조를 확인하는 데 사용

[2] Hur, M., Lee, S.-K., Kim, B., Cho, S., Lee, D., & Lee, D.  
**A study on the man-hour prediction system for shipbuilding.**  
*Journal of Intelligent Manufacturing*, 26(6), 1267–1279.  
- man-hour가 생산계획 단계에서 전문가에 의해 사전 예측되는 구조
- 작업 특성, 환경, 과거 경험 등을 반영한 사전 산정
- Block Type, Process Code, Shop Code, Work Type, Work Load, Work Organization Code, Jig Code 등의 변수 활용
- 작업조직 및 숙련도 차이가 man-hour 산정에 영향을 줄 수 있다는 근거
- 생산 시점이 가까워질수록 생산과정 변수를 추가해 예측을 갱신하는 구조를 확인하는 데 사용

[3] Son, J.-R., Suh, H.-W., & Ha, B.-H.  
**A Heuristic Algorithm for Block Storage Planning in Shipbuilding.**  
*Journal of the Society of Naval Architects of Korea*, 51(3), 239–245, 2014.  
- Block별 작업량과 난이도 차이에 따른 생산시간 편차
- 입고 지연, 생산 차질, 기상 변화, 품질검사 등으로 일정이 변경될 수 있는 조선 생산환경
- Block 위치·시간 제약을 함께 고려하는 스케줄링 배경을 확인하는 데 사용

[4] Chen, S.  
**Data of Ship Block Scheduling in English.**  
Mendeley Data / Shanghai Jiao Tong University, Version 1.  
- 본 프로젝트의 원 데이터셋
- Block Information, Position Information, Initial Position Information 및 DQN/DDQN/Heuristic 스케줄링 결과의 구조를 확인하는 데 사용
- 현재 공개자료만으로는 `Block Position Cycle`의 정확한 산정식과 공식 정의를 확인할 수 없음

---

## 한 문장으로 정리

> **EDA와 단계적 회귀분석에서 Position·Initial 정보를 추가할수록 예상과 달리 예측력이 개선되지 않는 현상을 출발점으로 데이터와 선행연구를 다시 검토했고, 그 결과 `Block Position Cycle`을 스케줄링 이후의 실제 공기가 아니라 스케줄링 이전에 설정된 기준 처리기간으로 재해석하면서 프로젝트를 '공기 예측'에서 '사전 Cycle과 스케줄링 결과의 관계 비교'로 변경·확장하였다.**
