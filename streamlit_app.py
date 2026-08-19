import base64
import json
import math
import pickle
import re
import html
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = ROOT / "data" / "processed"
POSITION_FILE = ROOT / "data" / "source" / "block_position_information.xlsx"
RESULT_DIR = ROOT / "Data of Ship Block Scheduling in English" / "Result"
RAW_INPUT_DIR = ROOT / "Data of Ship Block Scheduling in English" / "Raw_input_ Data"
MODEL_DIR = ROOT / "outputs" / "3_modeling"
SCHEDULE_DIR = ROOT / "outputs" / "4_scheduling_comparison"
PRECOMPUTED_DIR = ROOT / "precomputed"
PRECOMPUTED_CHART_DIR = PRECOMPUTED_DIR / "charts"
LOGO_PATH = ROOT / "Docs" / "images" / "samsung_heavy_industries_logo.png"
DATASET_STRUCTURE_IMAGE_PATH = ROOT / "Docs" / "images" / "dataset_structure_flow_infographic_v2.png"
DATASET_SELECTION_IMAGE_PATH = ROOT / "Docs" / "images" / "dataset_selection_infographic.png"
DATASET_ASSUMPTIONS_IMAGE_PATH = ROOT / "Docs" / "images" / "dataset_assumptions_infographic.png"
ANALYSIS_FLOW_IMAGE_PATH = ROOT / "Docs" / "images" / "analysis_flow_infographic.png"
TABLE_JOIN_STRATEGY_IMAGE_PATH = ROOT / "Docs" / "images" / "table_join_strategy_infographic.png"
JOIN_KEY_DISCOVERY_IMAGE_PATH = ROOT / "Docs" / "images" / "join_key_validation_infographic_gray.png"
MASTER_TABLE_ERD_PATH = ROOT / "Docs" / "images" / "1_master_table_join_erd.svg"
SHIP_BLOCK_PLAN_IMAGE_PATH = ROOT / "Docs" / "images" / "ship_block_plan_clear.png"
FEATURE_SET_EXPANSION_IMAGE_PATH = ROOT / "presentation_assets" / "feature_set_expansion_infographic.png"
DDQN_SCHEDULING_FLOW_IMAGE_PATH = ROOT / "presentation_assets" / "ddqn_scheduling_flow_infographic.png"
MODELING_SETUP_CODE_PATH = ROOT / "presentation_assets" / "modeling_setup_code.py"
REGRESSION_COMPARISON_CODE_PATH = ROOT / "presentation_assets" / "regression_comparison_code.py"
NOTEBOOK_FILES = {
    "0. Overview": ROOT / "Predicting 'Block Position Cycle'_0_overview.ipynb",
    "1. Master Table": ROOT / "Predicting 'Block Position Cycle'_1_master table.ipynb",
    "2. 전처리 및 EDA": ROOT / "Predicting 'Block Position Cycle'_2_preprocessing_eda.ipynb",
    "3. 회귀모델": ROOT / "Predicting 'Block Position Cycle'_3_modeling.ipynb",
    "4. 스케줄링 비교": ROOT / "Predicting 'Block Position Cycle'_4_scheduling_comparison.ipynb",
    "5. 최종 결론": ROOT / "Predicting 'Block Position Cycle'_5_conclusion.ipynb",
    "6. 개발 로드맵": ROOT / "Predicting 'Block Position Cycle'_6_development_roadmap.ipynb",
}
DATASET_OVERVIEW_SUBPAGE = "0.2 참고자료 및 데이터셋"
DATASET_STRUCTURE_SUBPAGE = "데이터셋 구성"
DATASET_ASSUMPTIONS_SUBPAGE = "데이터셋 전제"
RESULT_TABLE_SUBPAGE = "Result table 확인"
DATA_STRUCTURE_PAGE = "데이터 구조 확인"
PROJECT_REASON_OVERVIEW_SUBPAGE = "0.1 프로젝트를 시작한 이유"
PROJECT_TOPIC_SUBPAGE = "프로젝트 주제"
PROJECT_REASON_CHALLENGES_SUBPAGE = "건축과 조선이 공유하는 어려움"
PROJECT_REASON_SELECTION_SUBPAGE = "검토한 아이디어와 최종 선택"
ANALYSIS_FLOW_SUBPAGE = "0.5 전체 분석 흐름"
TABLE_JOIN_STRATEGY_SUBPAGE = "조인 전략과 초기 가설"
JOIN_KEY_DISCOVERY_SUBPAGE = "조인 키 탐색"
MASTER_TABLE_ERD_SUBPAGE = "테이블 연결 구조·ERD"
MASTER_TABLE_BUILD_SUBPAGE = "Master Table 생성·미리보기"
EDA_DATA_QUALITY_SUBPAGE = "데이터 품질 확인 · 종속변수"
EDA_MISSING_SUBPAGE = "결측값 해석 및 처리"
EDA_TARGET_DEFINITION_SUBPAGE = "종속변수 정의"
EDA_DERIVED_SUBPAGE = "파생변수 생성"
EDA_OUTLIER_SUBPAGE = "이상치 확인"
EDA_TARGET_DISTRIBUTION_SUBPAGE = "종속변수 분포"
EDA_NUMERIC_CORRELATION_SUBPAGE = "수치형 변수 상관관계"
EDA_CATEGORICAL_DISTRIBUTION_SUBPAGE = "범주형 변수별 Cycle 분포"
EDA_FEATURE_SET_SUBPAGE = "독립변수 세트 구성"
CYCLE_PREDICTION_PAGE = "Cycle 예측 모듈"
SCHEDULING_RESULT_PAGE = "Scheduling Result 조회 모듈"
SIMULATOR_PAGES = {CYCLE_PREDICTION_PAGE, SCHEDULING_RESULT_PAGE}
SUBMISSION_PAGE = "제출용 페이지"
SUBMISSION_COVER_SUBPAGE = "표지"
SUBMISSION_CONTENTS_SUBPAGE = "목차"
SUBMISSION_OVERVIEW_SUBPAGE = "프로젝트 개요"
SUBMISSION_PROCESS_SUBPAGE = "프로젝트 수행 절차 및 방법"
SUBMISSION_PROGRESS_SUBPAGE = "프로젝트 수행 경과"
SUBMISSION_TEAM_SUBPAGE = "프로젝트 팀 구성 및 역할"
SUBMISSION_SELF_REVIEW_SUBPAGE = "자체 평가 의견"
SUBMISSION_DEMO_VIDEO_SUBPAGE = "시연영상"
COVER_PAGE = "표지"
ANALYSIS_FLOW_PAGE = "목차"
FINAL_SUMMARY_SUBPAGE = "분석 수치 요약"
FINAL_LIMITATION_SUBPAGE = "현재 분석의 한계"
FINAL_ANALYSIS_REFRAME_SUBPAGE = "분석 구조 재정의"
FINAL_IMPLICATION_SUBPAGE = "프로젝트 시사점"
FINAL_REFERENCE_SUBPAGE = "참고문헌"
SCHEDULING_RESULT_STRUCTURE_SUBPAGE = "Result Table 구조"
SCHEDULING_RESULT_VIEWER_SUBPAGE = "Scheduling Result 조회"
SCHEDULING_POSITION_COMPARISON_SUBPAGE = "Position 배정 비교"
SCHEDULING_PUBLISHER_METRICS_SUBPAGE = "게시자 제공 지표"
SCHEDULING_MAKESPAN_SUBPAGE = "운영 성과 비교"
SCHEDULING_DELAY_SUBPAGE = "Delay 성과 비교"
SCHEDULING_CONCLUSION_SUBPAGE = "결론"
SCHEDULING_PRESENTATION_SUBPAGES = [
    SCHEDULING_RESULT_STRUCTURE_SUBPAGE,
    SCHEDULING_RESULT_VIEWER_SUBPAGE,
    SCHEDULING_POSITION_COMPARISON_SUBPAGE,
    SCHEDULING_PUBLISHER_METRICS_SUBPAGE,
    SCHEDULING_MAKESPAN_SUBPAGE,
    SCHEDULING_CONCLUSION_SUBPAGE,
]
ROADMAP_OVERVIEW_SUBPAGE = "개발 로드맵"
ROADMAP_VIEWER_SUBPAGE = "3D Scheduling Result Viewer"
ROADMAP_CALENDAR_SUBPAGE = "Calendar-it과 연계"
ROADMAP_SUBPAGES = [ROADMAP_OVERVIEW_SUBPAGE, ROADMAP_VIEWER_SUBPAGE, ROADMAP_CALENDAR_SUBPAGE]
EDA_SUBPAGES = [
    EDA_DATA_QUALITY_SUBPAGE,
    EDA_MISSING_SUBPAGE,
    EDA_DERIVED_SUBPAGE,
    EDA_OUTLIER_SUBPAGE,
    EDA_TARGET_DISTRIBUTION_SUBPAGE,
    EDA_NUMERIC_CORRELATION_SUBPAGE,
    EDA_CATEGORICAL_DISTRIBUTION_SUBPAGE,
    EDA_FEATURE_SET_SUBPAGE,
]
RAW_TABLE_SUBPAGES = {
    "Block table 확인": "block",
    "Position table 확인": "position",
    "Initial table 확인": "initial",
}
LAYOUT_SETTINGS_FILE = ROOT / "presentation_layout.json"
SLIDE_LAYOUT_DEFAULTS = {
    "problem_statement": {
        "center_x": 50,
        "content_width": 84,
        "vertical_offset": 0,
        "title_font": 30,
        "body_font": 18,
        "highlight_phrases": [
            "현장에서 실제로 사용할 수 있는 해결책",
            "경험에서 발견한 문제를 조선업과 연결",
        ],
    },
    "shared_challenges": {
        "center_x": 50,
        "content_width": 90,
        "top_space": 54,
        "title_font": 23,
        "body_font": 13,
        "image_width": 100,
    },
    "idea_selection": {
        "center_x": 50,
        "content_width": 90,
        "top_space": 54,
        "title_font": 23,
        "body_font": 13,
        "image_width": 100,
    },
}


def load_slide_layouts():
    saved = {}
    if LAYOUT_SETTINGS_FILE.exists():
        try:
            saved = json.loads(LAYOUT_SETTINGS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            saved = {}
    layouts = {}
    for slide_key, defaults in SLIDE_LAYOUT_DEFAULTS.items():
        layouts[slide_key] = {**defaults, **saved.get(slide_key, {})}
    return layouts


def save_slide_layouts(layouts):
    LAYOUT_SETTINGS_FILE.write_text(
        json.dumps(layouts, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def centered_column_ratios(center_x, content_width):
    content_width = min(float(content_width), 96.0)
    half_width = content_width / 2
    center_x = min(max(float(center_x), half_width), 100 - half_width)
    return [max(center_x - half_width, 0.01), content_width, max(100 - center_x - half_width, 0.01)]


def render_slide_layout_editor(slide_key, layouts):
    layout = layouts[slide_key]
    prefix = f"layout_{slide_key}"
    st.sidebar.markdown("---")
    st.sidebar.markdown("**현재 페이지 편집**")
    st.sidebar.caption("1200×675 고정 캔버스 · 변경 즉시 자동 저장")

    updated = dict(layout)
    updated["center_x"] = st.sidebar.slider(
        "가로 위치", 20, 80, int(layout["center_x"]), key=f"{prefix}_center_x"
    )
    updated["content_width"] = st.sidebar.slider(
        "텍스트 상자 너비", 35, 96, int(layout["content_width"]), key=f"{prefix}_content_width"
    )

    if slide_key == "problem_statement":
        updated["vertical_offset"] = st.sidebar.slider(
            "세로 위치", -180, 180, int(layout["vertical_offset"]), key=f"{prefix}_vertical_offset"
        )
    else:
        updated["top_space"] = st.sidebar.slider(
            "위쪽 여백", 0, 180, int(layout["top_space"]), key=f"{prefix}_top_space"
        )

    updated["title_font"] = st.sidebar.slider(
        "제목 폰트", 12, 56, int(layout["title_font"]), key=f"{prefix}_title_font"
    )
    updated["body_font"] = st.sidebar.slider(
        "본문 폰트", 8, 34, int(layout["body_font"]), key=f"{prefix}_body_font"
    )

    if slide_key == "problem_statement":
        phrase_text = st.sidebar.text_area(
            "강조 문구 · 한 줄에 하나",
            value="\n".join(layout["highlight_phrases"]),
            key=f"{prefix}_highlight_phrases",
        )
        updated["highlight_phrases"] = [
            phrase.strip() for phrase in phrase_text.splitlines() if phrase.strip()
        ]
    else:
        updated["image_width"] = st.sidebar.slider(
            "이미지 크기", 30, 100, int(layout["image_width"]), key=f"{prefix}_image_width"
        )

    if updated != layout:
        layouts[slide_key] = updated
        save_slide_layouts(layouts)

    if st.sidebar.button("이 페이지 기본값 복원", key=f"{prefix}_reset", width="stretch"):
        layouts[slide_key] = dict(SLIDE_LAYOUT_DEFAULTS[slide_key])
        save_slide_layouts(layouts)
        for key in list(st.session_state):
            if key.startswith(prefix):
                del st.session_state[key]
        st.rerun()

    return updated

st.set_page_config(page_title="Block Position Cycle", layout="wide")


def to_presentation_style(value):
    """슬라이드 문구를 높임말 없는 발표체로 통일한다."""
    if not isinstance(value, str):
        return value
    replacements = (
        ("가능합니다", "가능하다"),
        ("적합합니다", "적합하다"),
        ("부족합니다", "부족하다"),
        ("중요합니다", "중요하다"),
        ("동일합니다", "동일하다"),
        ("충분합니다", "충분하다"),
        ("명확합니다", "명확하다"),
        ("필요합니다", "필요하다"),
        ("보았습니다", "보았다"),
        ("했습니다", "했다"),
        ("되었습니다", "됐다"),
        ("됐습니다", "됐다"),
        ("있었습니다", "있었다"),
        ("없었습니다", "없었다"),
        ("이었습니다", "이었다"),
        ("였습니다", "였다"),
        ("있습니다", "있다"),
        ("없습니다", "없다"),
        ("보입니다", "보인다"),
        ("합니다", "한다"),
        ("됩니다", "된다"),
        ("입니다", "이다"),
        ("습니다", "다"),
    )
    for polite, declarative in replacements:
        value = value.replace(polite, declarative)
    return value


# 화면에 표시하는 설명 문구는 작성 위치와 관계없이 같은 발표체를 사용한다.
_streamlit_markdown = st.markdown
_streamlit_caption = st.caption
_streamlit_info = st.info
_streamlit_success = st.success
_streamlit_error = st.error


def _presentation_markdown(body, *args, **kwargs):
    return _streamlit_markdown(to_presentation_style(body), *args, **kwargs)


def _presentation_caption(body, *args, **kwargs):
    return _streamlit_caption(to_presentation_style(body), *args, **kwargs)


def _presentation_info(body, *args, **kwargs):
    return _streamlit_info(to_presentation_style(body), *args, **kwargs)


def _presentation_success(body, *args, **kwargs):
    return _streamlit_success(to_presentation_style(body), *args, **kwargs)


def _presentation_error(body, *args, **kwargs):
    return _streamlit_error(to_presentation_style(body), *args, **kwargs)


st.markdown = _presentation_markdown
st.caption = _presentation_caption
st.info = _presentation_info
st.success = _presentation_success
st.error = _presentation_error

# 대시보드를 1200×675 고정 16:9 캔버스로 렌더링합니다.
# 브라우저 크기에 따른 자동 축소는 사용하지 않습니다.
st.markdown(
    """
    <style>
    html, body, #root {
        min-width: 1200px;
        min-height: 675px;
        margin: 0;
        overflow: auto;
        background: #D9DEE5;
    }
    html {
        font-size: 60% !important;
    }
    #root {
        display: block;
    }
    .stApp {
        flex: 0 0 auto;
        position: relative !important;
        width: 1200px !important;
        height: 675px !important;
        min-width: 1200px !important;
        min-height: 675px !important;
        margin: 0 auto !important;
        overflow: auto;
        transform: none !important;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section[data-testid="stSidebar"] {
        height: 675px !important;
        min-height: 675px !important;
        max-height: 675px !important;
    }
    section[data-testid="stSidebar"] {
        width: 220px !important;
        min-width: 220px !important;
        max-width: 220px !important;
        flex-basis: 220px !important;
    }
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stElementContainer"]:has(> iframe[data-testid="stIFrame"]) {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DASHBOARD_PALETTE = ["#034EA2", "#3D78B8", "#78A5D1", "#425B76", "#7D8EA3", "#2D7D8C", "#A7B3C2"]
REFERENCE_COLOR = "#7D8A99"
PREDICTED_COLOR = "#034EA2"
SCHEDULING_METHODS = [
    "DDQN",
    "EDDQN",
    "Earliest Start",
    "Longest Processing",
    "Resource Utilization",
    "Response Time",
    "Shortest Processing",
]
SET_A_FEATURES = [
    "block_ship_no",
    "block_type",
    "block_length",
    "block_width",
    "block_weight",
    "block_area",
    "season",
    "block_start_window",
]
RESULT_FILES = {
    "DDQN": "DDQN scheduling.xlsx",
    "EDDQN": "EDDQN_scheduling_results.xlsx",
    "Earliest Start": "scheduling_results_heuristic_earliest_start_time_20250605_014601.xlsx",
    "Longest Processing": "scheduling_results_heuristic_longest_processing_time_20250605_014601.xlsx",
    "Resource Utilization": "scheduling_results_heuristic_resource_utilization_based_20250605_014601.xlsx",
    "Response Time": "scheduling_results_heuristic_response_time_based_20250605_014601.xlsx",
    "Shortest Processing": "scheduling_results_heuristic_shortest_processing_time_20250605_014601.xlsx",
}
METHOD_COLORS = {
    "DDQN": "#5B8FD8",
    "EDDQN": "#034EA2",
    "Earliest Start": "#7B61A8",
    "Longest Processing": "#008C95",
    "Resource Utilization": "#2E7D32",
    "Response Time": "#D18F00",
    "Shortest Processing": "#6B7280",
}
YARD_AREA_STYLES = {
    "block assembly group": ("블록 조립 구역", "#034EA2"),
    "platform 1": ("플랫폼 구역", "#2D7D8C"),
    "curved surface": ("곡면 구역", "#6B5AA6"),
}
YARD_AREA_FILLS = {
    "block assembly group": "rgba(3, 78, 162, 0.10)",
    "platform 1": "rgba(45, 125, 140, 0.10)",
    "curved surface": "rgba(107, 90, 166, 0.10)",
}
CORRELATION_CMAP = LinearSegmentedColormap.from_list(
    "gray_white_blue", ["#6F7782", "#FFFFFF", "#034EA2"]
)
AVAILABLE_MATPLOTLIB_FONTS = {font.name for font in font_manager.fontManager.ttflist}
CHART_FONT_FAMILY = next(
    (
        font_name
        for font_name in ["Malgun Gothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "NanumGothic"]
        if font_name in AVAILABLE_MATPLOTLIB_FONTS
    ),
    "DejaVu Sans",
)
sns.set_theme(style="whitegrid", palette=DASHBOARD_PALETTE)
plt.rcParams.update(
    {
        "font.family": CHART_FONT_FAMILY,
        "font.size": 10.5,
        "axes.unicode_minus": False,
        "axes.edgecolor": "#D8DEE9",
        "axes.labelcolor": "#344054",
        "axes.labelsize": 10.5,
        "axes.titlecolor": "#102A43",
        "axes.titlesize": 12.5,
        "axes.titleweight": "bold",
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "grid.color": "#E7EBF2",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)

st.markdown(
    """
    <style>
    .stApp {
        background: #FFFFFF;
        color: #1F2937;
        font-family: "Malgun Gothic", "Noto Sans KR", sans-serif;
    }
    :root {
        --primary-color: #034EA2;
    }
    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.94);
    }
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    .stApp h1 {
        color: #102A43 !important;
        font-size: 2.35rem !important;
        line-height: 1.25 !important;
        font-weight: 800 !important;
        letter-spacing: -0.035em;
    }
    .stApp h2 {
        color: #102A43 !important;
        font-size: 1.85rem !important;
        line-height: 1.35 !important;
        font-weight: 750 !important;
        letter-spacing: -0.025em;
    }
    .stApp h3 {
        color: #16324F !important;
        font-size: 1.45rem !important;
        line-height: 1.4 !important;
        font-weight: 750 !important;
        letter-spacing: -0.02em;
    }
    .stApp h4 {
        color: #263B53 !important;
        font-size: 1.15rem !important;
        line-height: 1.45 !important;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] li {
        color: #263244;
        font-size: 1rem;
        line-height: 1.78;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] li {
        margin-bottom: 0.24rem;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] th,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] td,
    [data-testid="stCaptionContainer"] {
        word-break: keep-all !important;
        overflow-wrap: normal !important;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] strong {
        color: #102A43;
        font-weight: 750;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] code {
        color: #034EA2;
        background: #EEF4FB;
        border-radius: 5px;
        padding: 0.08rem 0.28rem;
        font-size: 0.94em;
        font-weight: 650;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] table {
        width: 100% !important;
        display: table !important;
        border-collapse: collapse;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] th,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] td {
        padding: 0.65rem 0.8rem;
        white-space: normal;
        word-break: keep-all;
    }
    [data-testid="stCaptionContainer"] {
        color: #526173;
        font-size: 0.9rem;
        line-height: 1.55;
    }
[data-testid="stCode"] {
    max-height: 23rem !important;
    overflow-y: auto !important;
}
    section[data-testid="stSidebar"] {
        background: #F6F8FB;
        border-right: 1px solid #E1E7EF;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 0.65rem;
        padding-bottom: 1rem;
    }
    /* 메뉴 블록 사이 여백은 원래보다 촘촘하되, 답답하지 않게 유지한다. */
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.45rem !important;
    }
    section[data-testid="stSidebar"] [data-testid="stElementContainer"] {
        margin-bottom: 0 !important;
    }
    [data-testid="stSidebarHeader"] {
        position: absolute;
        top: auto;
        bottom: 0.8rem;
        left: 0;
        right: 0;
        width: auto;
        overflow: visible;
        z-index: 9999;
        pointer-events: none;
    }
    [data-testid="stSidebarCollapseButton"] {
        position: absolute;
        top: auto;
        bottom: 0;
        right: 1rem;
        z-index: 10000;
        pointer-events: auto;
        visibility: visible !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebarCollapseButton"] button {
        visibility: visible !important;
        opacity: 1 !important;
    }
    section[data-testid="stSidebar"] {
        color: #1F2937;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #D5DEE9;
    }
    .sidebar-page-divider {
        height: 1px;
        margin: 0.22rem 0.35rem;
        background: #D5DEE9;
    }
    section[data-testid="stSidebar"] [data-testid="stImage"] {
        background: transparent;
        border-radius: 0;
        padding: 0;
        margin-bottom: 0.45rem;
    }
    section[data-testid="stSidebar"] [data-testid="stButton"] {
        margin: 0;
    }
    section[data-testid="stSidebar"] [data-testid="stButton"] button {
        width: 100%;
        justify-content: flex-start;
        text-align: left;
        border: 0;
        border-radius: 9px;
        padding: 0.38rem 0.68rem;
        font-size: 0.94rem;
        font-weight: 650;
    }
    section[data-testid="stSidebar"] [data-testid="stButton"] button > div,
    section[data-testid="stSidebar"] [data-testid="stButton"] button span,
    section[data-testid="stSidebar"] [data-testid="stButton"] button [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] [data-testid="stButton"] button p {
        width: 100%;
        justify-content: flex-start;
        text-align: left !important;
    }
    section[data-testid="stSidebar"] [data-testid="stButton"] button p {
        font-size: 0.94rem;
        font-weight: 650;
        line-height: 1.25;
    }
    section[data-testid="stSidebar"] button[kind="secondary"] {
        background: transparent;
        color: #1F2937;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: #E9EEF5;
        color: #034EA2;
    }
    section[data-testid="stSidebar"] button[kind="primary"] {
        background: #034EA2;
        color: #FFFFFF;
        box-shadow: 0 6px 16px rgba(3, 78, 162, 0.20);
    }
    section[data-testid="stSidebar"] button[kind="primary"] * {
        color: #FFFFFF !important;
    }
    button[data-testid="stBaseButton-primaryFormSubmit"] {
        background-color: #034EA2 !important;
        border-color: #034EA2 !important;
        color: #FFFFFF !important;
    }
    button[data-testid="stBaseButton-primaryFormSubmit"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stFormSubmitButton"] button {
        background: #034EA2 !important;
        border-color: #034EA2 !important;
        color: #FFFFFF !important;
    }
    [data-testid="stFormSubmitButton"] button * {
        color: #FFFFFF !important;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        background: #023D80 !important;
        border-color: #023D80 !important;
    }
    button[data-variant="segmented_control"][data-selected="true"] {
        background-color: #EAF2FB !important;
        border-color: #034EA2 !important;
        color: #034EA2 !important;
    }
    button[data-variant="segmented_control"][data-selected="true"] * {
        color: #034EA2 !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        margin: 0.10rem 0 0.26rem 0.78rem;
        padding-left: 0.52rem;
        border-left: 2px solid rgba(3, 78, 162, 0.36);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 0.10rem 0;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] p {
        color: #3D4A5C;
        font-size: 0.84rem;
        line-height: 1.28;
    }
    label[data-testid="stRadioOption"] > div > div > div:first-child {
        background-color: #F4F4F4 !important;
        border-color: #6F7782 !important;
    }
    label[data-testid="stRadioOption"][data-selected="true"] > div > div > div:first-child {
        background-color: #111111 !important;
        border-color: #111111 !important;
    }
    [data-testid="stSlider"] > div[role="group"] > div > div:first-child {
        background-image: none !important;
        background-color: #B8D0EA !important;
    }
    [data-testid="stSlider"] > div[role="group"] > div > div:nth-child(2) {
        background-color: #034EA2 !important;
    }
    [data-testid="stSliderThumbValue"],
    [data-testid="stSliderThumbValue"] * {
        color: #034EA2 !important;
        border-color: #034EA2 !important;
    }
    input[type="range"] {
        accent-color: #034EA2;
    }
    [data-testid="stSelectbox"] [role="group"] {
        border-color: #A7B3C2 !important;
    }
    [data-testid="stSelectbox"] [role="group"][data-hovered="true"],
    [data-testid="stSelectbox"] [role="group"][data-focus-within="true"] {
        border-color: #034EA2 !important;
    }
    .sidebar-brand {
        margin-top: 0.55rem;
        padding: 1rem 0 1.4rem 0;
        border-top: 1px solid #CBD6E3;
    }
    .sidebar-brand .brand-title {
        color: #1F2937;
        font-size: 1.08rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .sidebar-brand .brand-subtitle {
        margin-top: 0.35rem;
        color: #4C5A6B;
        font-size: 0.9rem;
        line-height: 1.55;
        letter-spacing: 0;
    }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E1E7F0;
        border-top: 4px solid #034EA2;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(16, 40, 100, 0.07);
    }
    [data-testid="stMetricLabel"] p {
        color: #526173;
        font-weight: 650;
    }
    [data-testid="stMetricValue"] {
        color: #034EA2;
        font-weight: 800;
    }
    [data-testid="stDataFrame"] {
        background: #FFFFFF;
        border: 1px solid #E1E7F0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(16, 40, 100, 0.05);
    }
    [data-testid="stAlert"] {
        background: #F0F6FC;
        border-radius: 12px;
        border-left: 5px solid #034EA2;
    }
    [data-testid="stAlert"] p {
        color: #1E3A57 !important;
    }
    [data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #E1E7F0;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def load_data():
    precomputed_path = PRECOMPUTED_DIR / "app_data.pkl"
    if precomputed_path.exists():
        with open(precomputed_path, "rb") as file:
            return pickle.load(file)
    schema_version = "logic_revision_2026_08_18"
    detail = pd.read_csv(SCHEDULE_DIR / "4_schedule_detail.csv")
    for column in ["planned_start_time", "planned_finish_time", "latest_completion_time"]:
        detail[column] = pd.to_datetime(detail[column])
    with open(MODEL_DIR / "3_modeling_summary.json", encoding="utf-8") as file:
        modeling_summary = json.load(file)
    return {
        "schema_version": schema_version,
        "master": pd.read_csv(PROCESSED_DIR / "master_DDQN.csv"),
        "analysis": pd.read_csv(PROCESSED_DIR / "analysis_DDQN.csv"),
        "positions": pd.read_excel(POSITION_FILE),
        "feature_sets": pd.read_csv(MODEL_DIR / "3_feature_set_results.csv"),
        "baseline": pd.read_csv(MODEL_DIR / "3_baseline_results.csv"),
        "models": pd.read_csv(MODEL_DIR / "3_final_model_results.csv"),
        "modeling_summary": modeling_summary,
        "importance": pd.read_csv(MODEL_DIR / "3_feature_importance.csv"),
        "test": pd.read_csv(MODEL_DIR / "3_test_predictions.csv"),
        "delay": pd.read_csv(SCHEDULE_DIR / "4_delay_summary.csv"),
        "schedule": pd.read_csv(SCHEDULE_DIR / "4_schedule_summary.csv"),
        "position": pd.read_csv(SCHEDULE_DIR / "4_position_summary.csv"),
        "area_share": pd.read_csv(SCHEDULE_DIR / "4_primary_area_share.csv"),
        "match": pd.read_csv(SCHEDULE_DIR / "4_position_match_rate.csv", index_col=0),
        "detail": detail,
    }


@st.cache_resource(show_spinner=False)
def load_raw_input_tables():
    precomputed_path = PRECOMPUTED_DIR / "raw_input_tables.pkl"
    if precomputed_path.exists():
        with open(precomputed_path, "rb") as file:
            return pickle.load(file)
    return {
        "block": pd.read_excel(RAW_INPUT_DIR / "block_information_table.xlsx"),
        "position": pd.read_excel(RAW_INPUT_DIR / "block_position_information.xlsx"),
        "initial": pd.read_excel(RAW_INPUT_DIR / "initial_block_position_information.xlsx"),
    }


@st.cache_resource(show_spinner=False)
def load_scheduling_result_table(method):
    precomputed_path = PRECOMPUTED_DIR / "scheduling_results" / f"{method}.pkl"
    if precomputed_path.exists():
        return pd.read_pickle(precomputed_path)
    return pd.read_excel(RESULT_DIR / RESULT_FILES[method])


def render_precomputed_chart(filename, width="stretch"):
    """Render a build-time chart without running matplotlib during a rerun."""
    chart_path = PRECOMPUTED_CHART_DIR / filename
    if not chart_path.exists():
        raise FileNotFoundError(
            f"{chart_path} is missing. Run: python scripts/build_precomputed_results.py"
        )
    st.image(chart_path, width=width)


@st.cache_resource
def load_set_a_artifact():
    return joblib.load(MODEL_DIR / "3_final_model.joblib")


@st.cache_resource
def load_set_a_model():
    analysis = pd.read_csv(PROCESSED_DIR / "analysis_DDQN.csv")
    _, test_index = train_test_split(analysis.index, test_size=0.2, random_state=42)
    model = load_set_a_artifact()
    test = analysis.loc[test_index, ["block_index", "block_processing_cycle", *SET_A_FEATURES]].copy()
    test["predicted_cycle"] = model.predict(test[SET_A_FEATURES])
    return model, test


def observed_slider(frame, column, label, fmt, key, disabled=False):
    values = frame[column].dropna()
    options = sorted(values.astype(float).unique())
    default = min(options, key=lambda value: abs(value - float(values.median())))

    if key in st.session_state:
        return st.select_slider(
            label,
            options=options,
            format_func=lambda value: fmt % value,
            key=key,
            disabled=disabled,
        )

    return st.select_slider(
        label,
        options=options,
        value=default,
        format_func=lambda value: fmt % value,
        key=key,
        disabled=disabled,
    )


def range_slider(frame, column, label, fmt, key):
    values = frame[column].dropna().astype(float)
    minimum = float(values.min())
    maximum = float(values.max())
    default = float(values.median())
    step = 1.0 if column == "block_start_window" else 0.1

    if key in st.session_state:
        return st.slider(label, minimum, maximum, step=step, format=fmt, key=key)

    return st.slider(label, minimum, maximum, value=default, step=step, format=fmt, key=key)


def observed_select(frame, column, label, key, disabled=False):
    values = sorted(frame[column].dropna().astype(str).unique())
    default = str(frame[column].mode().iloc[0])

    if key in st.session_state:
        return st.selectbox(label, values, key=key, disabled=disabled)

    return st.selectbox(label, values, index=values.index(default), key=key, disabled=disabled)


def widget_keys(prefix):
    keys = {}

    for column in SET_A_FEATURES:
        keys[column] = f"{prefix}_{column}"

    return keys


def sync_profile(profile, catalog, keys, marker):
    if st.session_state.get(marker) == profile.name:
        return
    for column, key in keys.items():
        value = profile[column]
        st.session_state[key] = str(value) if catalog[column].dtype == "object" else float(value)
    st.session_state[marker] = profile.name


def render_block_inputs(catalog, prefix, input_mode):
    keys = widget_keys(prefix)
    inputs = {}
    is_actual = input_mode == "실제 Block 선택"
    numeric_input = observed_slider if is_actual else range_slider
    col1, col2 = st.columns(2)
    with col1:
        inputs["block_ship_no"] = observed_select(catalog, "block_ship_no", "선박번호", keys["block_ship_no"], is_actual)
        inputs["block_type"] = observed_select(catalog, "block_type", "Block 유형", keys["block_type"], is_actual)
        inputs["block_length"] = numeric_input(catalog, "block_length", "Block 길이", "%.1f", keys["block_length"], **({"disabled": True} if is_actual else {}))
        inputs["block_width"] = numeric_input(catalog, "block_width", "Block 폭", "%.1f", keys["block_width"], **({"disabled": True} if is_actual else {}))
    with col2:
        inputs["block_weight"] = numeric_input(catalog, "block_weight", "Block 중량", "%.1f", keys["block_weight"], **({"disabled": True} if is_actual else {}))
        inputs["block_area"] = numeric_input(catalog, "block_area", "Block 면적", "%.1f", keys["block_area"], **({"disabled": True} if is_actual else {}))
        inputs["season"] = observed_select(catalog, "season", "시작 계절", keys["season"], is_actual)
        inputs["block_start_window"] = numeric_input(catalog, "block_start_window", "Block 착수 가능 구간", "%.0f", keys["block_start_window"], **({"disabled": True} if is_actual else {}))
    return inputs


def build_cycle_context_chart(frame, selected_block, prediction_name, adjusted_prediction=None, show_selected_result=True):
    chart_data = frame.sort_values("block_processing_cycle").reset_index(drop=True)
    selected_rank = int(chart_data.index[chart_data["block_index"].eq(selected_block)][0])
    selected = chart_data.loc[selected_rank]
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=chart_data["block_processing_cycle"],
            mode="lines",
            name="기준 Cycle",
            line={"color": "#7D8A99", "width": 1.4},
            hovertemplate="기준 Cycle: %{y:.1f}일<extra></extra>",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=chart_data["predicted_cycle"],
            mode="lines",
            name=prediction_name,
            line={"color": "#78A5D1", "width": 1.4},
            hovertemplate="예측: %{y:.1f}일<extra></extra>",
        )
    )
    if show_selected_result:
        for label, value, color, symbol, size in [
            ("선택 기준 Cycle", selected["block_processing_cycle"], "#263244", "x", 8),
            ("선택 기존 예측", selected["predicted_cycle"], "#034EA2", "circle-open", 8),
        ]:
            figure.add_trace(
                go.Scatter(
                    x=[selected_rank],
                    y=[value],
                    mode="markers",
                    name=label,
                    marker={"color": color, "symbol": symbol, "size": size, "line": {"color": color, "width": 1}},
                    hovertemplate=f"{label}: %{{y:.1f}}일<extra>Block {int(selected_block)}</extra>",
                )
            )
        figure.add_vline(x=selected_rank, line={"color": "#A7B3C2", "width": 1, "dash": "dot"})
    if adjusted_prediction is not None:
        # 가상 Block에는 원본 행의 순위가 없으므로, 기준 Cycle 곡선과
        # 현재 입력 예측선이 만나는 위치를 보간해 표식의 x축 위치로 사용한다.
        virtual_rank = float(
            np.interp(
                adjusted_prediction,
                chart_data["block_processing_cycle"].to_numpy(),
                chart_data.index.to_numpy(),
            )
        )
        figure.add_trace(
            go.Scatter(
                x=[virtual_rank],
                y=[adjusted_prediction],
                mode="markers",
                name="가상 Block 예측",
                marker={"color": "#D18F00", "symbol": "x", "size": 9, "line": {"color": "#D18F00", "width": 1}},
                hovertemplate="가상 Block 예측: %{y:.1f}일<extra></extra>",
            )
        )
        figure.add_hline(
            y=adjusted_prediction,
            line_color="#D18F00",
            line_width=1.4,
            line_dash="dash",
            annotation_text=f"현재 입력 예측 {adjusted_prediction:.1f}일",
            annotation_position="top left",
            annotation_font_color="#9A6500",
        )
    figure.update_layout(
        height=450,
        template="plotly_white",
        margin={"l": 45, "r": 15, "t": 75, "b": 55},
        hovermode="x unified",
        legend={"orientation": "h", "x": 0, "y": 1.04, "font": {"size": 10}},
        xaxis={"title": "기준 Cycle 오름차순 Test Block", "fixedrange": True},
        yaxis={"title": "Cycle (일)", "fixedrange": True, "gridcolor": "#E7EBF2"},
        font={"family": "Malgun Gothic", "color": "#263244"},
    )
    return figure


def compact_metrics(items):
    cells = []
    for label, value, note in items:
        detail = f' <small style="color:#667085;">{note}</small>' if note else ""
        cells.append(
            f'<div style="padding:10px 16px;border-right:1px solid #E7EBF2;"><small>{label}</small><br>'
            f'<b style="font-size:1.25rem;">{value}</b>{detail}</div>'
        )
    cells = "".join(cells)
    st.markdown(
        f'<div style="display:grid;grid-template-columns:repeat({len(items)},1fr);border:1px solid #DCE3EC;'
        f'border-radius:10px;overflow:hidden;margin:0 0 .4rem;background:#FFFFFF;">{cells}</div>',
        unsafe_allow_html=True,
    )


def analysis_note(text, title="결과 해석"):
    st.markdown(
        f"""
        <div style="margin:.65rem 0 1.05rem;padding:.55rem 0 0;
        border-top:1px solid #DCE3EC;color:#425466;line-height:1.6;">
            <b style="color:#102A43;">{title}</b><span style="color:#98A2B3;"> · </span>{text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def flow_cards(items):
    columns = st.columns(len(items))
    for index, (title, body) in enumerate(items, start=1):
        with columns[index - 1]:
            st.markdown(
                f"""
                <div style="min-height:145px;padding:1rem;border:1px solid #DCE3EC;
                border-top:4px solid #034EA2;border-radius:10px;background:#FFFFFF;">
                    <small style="color:#034EA2;font-weight:700;">STEP {index:02d}</small>
                    <div style="font-size:1.05rem;font-weight:750;margin:.45rem 0;">{title}</div>
                    <div style="color:#667085;line-height:1.5;">{body}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_overview_contents():
    """Render the analysis flow as a text-first table of contents slide."""
    st.markdown(
        """
        <div style="max-width:1050px;margin:3rem auto 0;word-break:keep-all;">
            <div style="color:#102A43;font-size:2.3rem;font-weight:800;letter-spacing:-.04em;">목차</div>
            <div style="margin:.6rem 0 1.8rem;color:#667085;font-size:1.08rem;line-height:1.65;">현재 Streamlit 대시보드의 발표 페이지 순서입니다.</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;column-gap:4.2rem;border-top:2px solid #034EA2;">
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">01 · 개요</b><span style="float:right;color:#667085;">프로젝트 배경과 주제 선정</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">07 · 최종 결론</b><span style="float:right;color:#667085;">분석 결과와 시사점</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">02 · 데이터 구조 확인</b><span style="float:right;color:#667085;">데이터셋·원본 테이블</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">08 · 개발 로드맵</b><span style="float:right;color:#667085;">운영 도구 확장 방향</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">03 · 테이블 조인</b><span style="float:right;color:#667085;">연결 키와 Master Table</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">09 · Cycle 예측 모듈</b><span style="float:right;color:#667085;">Block 기준 Cycle 조회</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">04 · 전처리 및 EDA</b><span style="float:right;color:#667085;">품질·분포·변수 구성</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">10 · Scheduling Result 조회 모듈</b><span style="float:right;color:#667085;">방법별 결과 조회</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">05 · 회귀모델</b><span style="float:right;color:#667085;">Cycle 예측모델 비교</span></div>
                <div style="padding:.92rem .2rem;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">11 · 제출용 페이지</b><span style="float:right;color:#667085;">제출 항목 정리</span></div>
                <div style="padding:.92rem .2rem;"><b style="color:#034EA2;">06 · 스케줄링 비교</b><span style="float:right;color:#667085;">Position·일정·Delay 비교</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dataset_structure_infographic():
    st.markdown(
        """
        <div style="margin:.5rem 0 1rem;">
            <div style="color:#102A43;font-size:2.15rem;font-weight:800;letter-spacing:-.035em;">데이터 구조 확인</div>
            <div style="margin-top:.4rem;color:#667085;font-size:1.05rem;">세 개의 원본 테이블에 Scheduling을 적용해 Result를 만들고, README.md는 데이터 해석을 돕는 별도 안내 문서입니다.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image(DATASET_STRUCTURE_IMAGE_PATH, width="stretch")


def render_raw_table_preview(table_key):
    table_details = {
        "block": ("Block table", "Block별 생산·일정계획 속성", "block_information_table.xlsx"),
        "position": ("Position table", "작업 위치별 공간·자원 제약", "block_position_information.xlsx"),
        "initial": ("Initial table", "스케줄링 시작 시점의 초기 야드 상태", "initial_block_position_information.xlsx"),
    }
    title, description, filename = table_details[table_key]
    frame = load_raw_input_tables()[table_key]
    info_frame = pd.DataFrame(
        {
            "Column": frame.columns,
            "Non-Null": frame.notna().sum().to_numpy(),
            "Dtype": frame.dtypes.astype(str).to_numpy(),
        }
    )
    st.markdown(
        f"""
        <div style="margin:.6rem 0 1rem;">
            <div style="color:#102A43;font-size:2.15rem;font-weight:800;letter-spacing:-.035em;">{title}</div>
            <div style="margin-top:.4rem;color:#667085;font-size:1.05rem;">{description} · <code>{filename}</code></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    compact_metrics(
        [
            ("행", f"{len(frame):,}", "records"),
            ("열", f"{len(frame.columns):,}", "columns"),
            ("결측값", f"{int(frame.isna().sum().sum()):,}", "cells"),
        ]
    )
    st.markdown("#### `head()` · 처음 5개 행")
    st.dataframe(frame.head(), hide_index=True, width="stretch")
    st.markdown("#### `info()` · 컬럼 구성")
    st.dataframe(info_frame, hide_index=True, width="stretch", height=240)


def render_horizontal_scroll_dataframe(frame):
    """Keep wide source tables readable by using an explicit horizontal scrollbar."""
    table_html = frame.to_html(index=False, escape=True, border=0)
    st.markdown(
        f"""
        <style>
        .wide-source-table {{
            width:100%; overflow-x:auto; overflow-y:hidden;
            border:1px solid #DCE3EC; border-radius:9px; background:#FFFFFF;
            scrollbar-color:#98A2B3 #F3F6FA; scrollbar-width:auto;
        }}
        .wide-source-table table {{
            width:max-content; min-width:100%; margin:0; border-collapse:collapse;
            font-size:.82rem; color:#344054; white-space:nowrap;
        }}
        .wide-source-table th {{
            padding:.52rem .68rem; background:#F7F9FC; color:#667085;
            font-weight:700; text-align:left; border-bottom:1px solid #DCE3EC;
        }}
        .wide-source-table td {{
            padding:.48rem .68rem; border-bottom:1px solid #EEF2F6;
            text-align:left;
        }}
        .wide-source-table tr:last-child td {{ border-bottom:0; }}
        </style>
        <div class="wide-source-table">{table_html}</div>
        """,
        unsafe_allow_html=True,
    )


def render_scheduling_result_preview():
    st.markdown(
        """
        <div style="margin:.6rem 0 1rem;">
            <div style="color:#102A43;font-size:2.15rem;font-weight:800;letter-spacing:-.035em;">Scheduling Result</div>
            <div style="margin-top:.4rem;color:#667085;font-size:1.05rem;">동일한 Block·Position·Initial 입력에 7개 Scheduling Method를 적용한 결과 테이블입니다.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    method = st.selectbox(
        "조회할 Scheduling Method",
        SCHEDULING_METHODS,
        index=0,
        key="raw_result_method",
    )
    frame = load_scheduling_result_table(method)
    info_frame = pd.DataFrame(
        {
            "Column": frame.columns,
            "Non-Null": frame.notna().sum().to_numpy(),
            "Dtype": frame.dtypes.astype(str).to_numpy(),
        }
    )
    compact_metrics(
        [
            ("선택 방법", method, "대표: DDQN" if method == "DDQN" else "Scheduling Method"),
            ("행", f"{len(frame):,}", "Block Result"),
            ("열", f"{len(frame.columns):,}", "columns"),
        ]
    )
    st.markdown("#### `head()` · 처음 5개 행")
    st.dataframe(frame.head(), hide_index=True, width="stretch")
    st.markdown("#### `info()` · 컬럼 구성")
    st.dataframe(info_frame, hide_index=True, width="stretch", height=240)


def render_project_objectives():
    _, center_column, _ = st.columns([0.55, 4.9, 0.55])
    with center_column:
        st.markdown(
            """
            <div style="min-height:510px;display:flex;align-items:center;text-align:center;color:#102A43;">
                <div style="width:100%;">
                    <div style="color:#034EA2;font-size:14px;font-weight:800;letter-spacing:.16em;">PROJECT OBJECTIVE</div>
                    <div style="margin:.75rem 0 2.55rem;font-size:34px;font-weight:800;letter-spacing:-.04em;">프로젝트 목표</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3.1rem;text-align:left;">
                        <div style="min-height:185px;padding:1.25rem 0 0;border-top:2px solid #034EA2;">
                            <div style="display:grid;grid-template-columns:64px 1fr;gap:.95rem;align-items:start;">
                                <div style="color:#D8E6F4;font-size:48px;font-weight:800;line-height:.95;letter-spacing:-.07em;">01</div>
                                <div>
                                    <div style="color:#034EA2;font-size:12px;font-weight:800;letter-spacing:.11em;">PRE-CYCLE PREDICTION</div>
                                    <div style="margin-top:.72rem;font-size:21px;font-weight:800;line-height:1.45;letter-spacing:-.025em;">Block 고유 특성만으로<br>사전 Block Position Cycle을<br>어느 정도 예측할 수 있는가?</div>
                                </div>
                            </div>
                        </div>
                        <div style="min-height:185px;padding:1.25rem 0 0;border-top:2px solid #034EA2;">
                            <div style="display:grid;grid-template-columns:64px 1fr;gap:.95rem;align-items:start;">
                                <div style="color:#D8E6F4;font-size:48px;font-weight:800;line-height:.95;letter-spacing:-.07em;">02</div>
                                <div>
                                    <div style="color:#034EA2;font-size:12px;font-weight:800;letter-spacing:.11em;">RESULT LAYER DIAGNOSIS</div>
                                    <div style="margin-top:.72rem;font-size:21px;font-weight:800;line-height:1.45;letter-spacing:-.025em;">Position·Initial 정보가<br>추가될 때 예측 성능은<br>어떻게 변하는가?</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="margin-top:1.9rem;padding-top:.85rem;border-top:1px solid #DCE3EC;color:#667085;font-size:15px;line-height:1.65;">이 두 질문을 먼저 검증한 뒤, Scheduling 결과의 차이는 후속 단계에서 별도로 비교합니다.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_table_join_strategy():
    text_column, image_column = st.columns([0.86, 1.49], gap="large")
    with text_column:
        st.markdown(
            """
            <div style="margin:2.4rem 0 1.35rem;">
                <div style="color:#034EA2;font-size:14px;font-weight:800;letter-spacing:.16em;">INITIAL HYPOTHESIS</div>
                <div style="margin:.6rem 0;color:#102A43;font-size:30px;font-weight:800;letter-spacing:-.04em;">조인 전략과 초기 가설</div>
                <div style="color:#667085;font-size:15px;line-height:1.65;">분석을 시작할 때는 Block에 관련 테이블을 더 많이 붙일수록 예측에 쓸 수 있는 정보가 늘고, 회귀 성능도 좋아질 것이라고 기대했습니다.</div>
            </div>
            <div style="border-top:2px solid #034EA2;">
                <div style="padding:.9rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">출발점</b><br><span style="color:#475467;">Block table의 물리량을 바탕으로 회귀 분석을 진행합니다.</span></div>
                <div style="padding:.9rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">조인 후보</b><br><span style="color:#475467;">Result, Position, Initial의 운영 정보를 단계적으로 추가</span></div>
                <div style="padding:.9rem 0;"><b style="color:#034EA2;">검증 계획</b><br><span style="color:#475467;">테이블의 정보 증가가 변수 세트의 예측 성능을 실제로 개선하는지 검증</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with image_column:
        st.markdown('<div style="height:6.15rem;"></div>', unsafe_allow_html=True)
        st.image(TABLE_JOIN_STRATEGY_IMAGE_PATH, width="stretch")


def render_join_key_discovery():
    text_column, image_column = st.columns([1.05, 1.3], gap="large")
    with text_column:
        st.markdown(
            """
            <div style="margin:1.8rem 0 1.25rem;">
                <div style="color:#034EA2;font-size:14px;font-weight:800;letter-spacing:.16em;">JOIN KEY VALIDATION</div>
                <div style="margin:.6rem 0;color:#102A43;font-size:30px;font-weight:800;letter-spacing:-.04em;">조인 키 후보</div>
                <div style="color:#667085;font-size:13px;line-height:1.65;">README에 명확한 조인키가 없었다. 따라서 같은 이름의 열을 바로 연결하지 않고, <b>① 테이블 안에서 유일한 값인가 ② 양쪽 값의 집합이 같은가 ③ 조인 후 다른 식별값도 일치하는가 ④ 실제로 같은 대상을 뜻하는가</b>를 순서대로 확인했다.</div>
            </div>
            <div style="border-top:2px solid #034EA2;">
                <div style="padding:.7rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#4B5563;">01 · 제외: block no.</b><br><span style="color:#475467;">Block과 Result에 공통으로 보이지만 고유값이 97개뿐이다. 872개 Block을 하나씩 식별할 수 없어 단독 조인키로 사용할 수 없었다.</span></div>
                <div style="padding:.7rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">02 · 채택: index ↔ block sequence no.</b><br><span style="color:#475467;">양쪽 모두 872개 고유값을 가지며 값의 집합도 같다. 이 키로 결합한 뒤 양쪽 <code>block no.</code>가 100% 일치해 Block–Result 1:1 연결을 확정했다.</span></div>
                <div style="padding:.7rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">03 · 채택: block position id</b><br><span style="color:#475467;">Result의 모든 Position ID가 Position table에 존재하고, 조인 후 Position 설명도 100% 일치했다. 여러 Block이 하나의 Position을 참조하는 Result 기준 N:1 관계다.</span></div>
                <div style="padding:.7rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">04 · 선택적 연결: Position description ↔ Initial description</b><br><span style="color:#475467;">Position 66개 중 11개만 Initial 기록과 일치했다. 일치 여부는 <code>initially_occupied</code>로 만들되, Initial을 현재 Block의 직접 속성으로 해석하지 않았다.</span></div>
                <div style="padding:.7rem 0;"><b style="color:#4B5563;">05 · 제외: ship no. + block no.</b><br><span style="color:#475467;">각 테이블 내부에서는 복합키 후보였지만 Initial–Block 실제 매칭률은 0%였다. Initial은 시작 시점에 이미 작업 중인 별도 Block으로 보고 Position을 경유해 활용했다.</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with image_column:
        st.markdown('<div style="height:4rem;"></div>', unsafe_allow_html=True)
        image_left, image_center, image_right = st.columns([.165, .67, .165])
        with image_center:
            st.image(JOIN_KEY_DISCOVERY_IMAGE_PATH, width="stretch")


def render_master_table_erd():
    st.markdown(
        """
        <div style="margin:1.5rem 0 1rem;">
            <div style="color:#034EA2;font-size:14px;font-weight:800;letter-spacing:.16em;">MASTER TABLE BUILD</div>
            <div style="margin:.45rem 0;color:#102A43;font-size:2.15rem;font-weight:800;letter-spacing:-.035em;">테이블 연결 구조·ERD</div>
            <div style="color:#667085;font-size:1.05rem;">검증한 세 연결 관계와 각 키의 카디널리티를 먼저 확인한다.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    relations = pd.DataFrame(
        [
            ["Block", "DDQN Result", "index ↔ block sequence no.", "1:1"],
            ["DDQN Result", "Position", "block position id", "N:1"],
            ["Position", "Initial", "block position description", "0..1"],
        ],
        columns=["From", "To", "연결키", "관계"],
    )
    st.dataframe(relations, hide_index=True, width="stretch")
    analysis_note("Block–Result는 검증된 1:1 관계이며 Result–Position은 N:1이다. Initial은 현재 Block과 직접 연결되지 않아 Position의 초기 기록 유무로만 붙인다.")
    st.markdown("#### Master Table ERD")
    st.image(MASTER_TABLE_ERD_PATH, width="stretch")
    analysis_note("ERD는 기술적인 연결경로를 보여준다. 다만 연결 가능성은 독립변수 사용 가능성과 같지 않으며, 선택 Position은 Result 이후 정보다.", "ERD 해석")


def render_master_table_build(data):
    st.markdown(
        """
        <div style="margin:1.5rem 0 1rem;">
            <div style="color:#034EA2;font-size:14px;font-weight:800;letter-spacing:.16em;">MASTER TABLE BUILD</div>
            <div style="margin:.45rem 0;color:#102A43;font-size:2.15rem;font-weight:800;letter-spacing:-.035em;">Master Table 생성·미리보기</div>
            <div style="color:#667085;font-size:1.05rem;">검증한 연결키를 <code>validate</code> 조건과 함께 코드로 구현하고 생성 결과를 확인한다.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    code_column, preview_column = st.columns([1, 1], gap="large")
    with code_column:
        st.markdown("#### 결합 코드")
        st.code(
            """# Result에서는 Block ↔ Position 연결에 필요한 키만 추출
mapping = result_DDQN[
    ['block sequence no.', 'block position id']
].copy()

# 1. Block + DDQN Result 연결
master = block.merge(
    mapping,
    left_on='index',
    right_on='block sequence no.',
    how='left',
    validate='1:1'
)

# 2. DDQN이 선택한 Position 정보 연결
master = master.merge(
    position,
    on='block position id',
    how='left',
    suffixes=('_block', '_position'),
    validate='m:1'
)

# 3. Initial Table을 Position description 기준으로 연결
master = master.merge(
    initial,
    on='block position description',
    how='left',
    suffixes=('', '_initial')
)

print(master.shape)
master.head()""",
            language="python",
        )
    with preview_column:
        st.markdown("#### 생성 결과 · `master_DDQN.csv`")
        master = data["master"]
        st.dataframe(master.head(18), hide_index=True, width="stretch", height=430)
        compact_metrics(
            [
                ("결합 행", f"{len(master):,}", "Block 단위 유지"),
                ("결합 컬럼", f"{master.shape[1]}", "Block·Result·Position·Initial"),
            ]
        )
        analysis_note("한 행은 하나의 Block과 DDQN이 선택한 Position 결과를 나타낸다. 이 표는 탐색·결과 비교용이며 최종 Cycle 예측에는 Block 고유 특성만 사용한다.", "미리보기 해석")


def render_dataset_assumptions():
    st.markdown('<div style="height:5.5rem;"></div>', unsafe_allow_html=True)
    text_column, image_column = st.columns([0.92, 1.38], gap="large")
    with text_column:
        st.markdown(
            """
            <div style="margin:.6rem 0 1.35rem;">
                <div style="color:#102A43;font-size:2.15rem;font-weight:800;letter-spacing:-.035em;">데이터셋 전제</div>
                <div style="margin-top:.5rem;color:#667085;font-size:1.05rem;line-height:1.6;">공개 데이터셋이 조선소 Block Scheduling 문제를 단순화해 표현하기 위해 두고 있는 다섯 가지 전제입니다.</div>
            </div>
            <div style="border-top:2px solid #034EA2;">
                <div style="padding:.8rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">형상 단순화</b><br><span style="color:#475467;">Block과 Position의 평면 형상을 최소 경계 직사각형으로 봅니다.</span></div>
                <div style="padding:.8rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">동시 작업 제한</b><br><span style="color:#475467;">한 Position에는 동시에 한 Block만 배정합니다.</span></div>
                <div style="padding:.8rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">노동력 가정</b><br><span style="color:#475467;">노동력은 충분하며 결근 같은 이상 상황은 제외합니다.</span></div>
                <div style="padding:.8rem 0;border-bottom:1px solid #E7EBF2;"><b style="color:#034EA2;">적합 Position</b><br><span style="color:#475467;">각 Block은 작업 가능한 Position을 찾을 수 있다고 가정합니다.</span></div>
                <div style="padding:.8rem 0;"><b style="color:#034EA2;">작업 완료 위치</b><br><span style="color:#475467;">하나의 Block은 하나의 Position에서 작업을 끝냅니다.</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with image_column:
        st.markdown('<div style="height:2.45rem;"></div>', unsafe_allow_html=True)
        st.image(DATASET_ASSUMPTIONS_IMAGE_PATH, width="stretch")
    st.markdown(
        """
        <div style="margin:1.3rem 0 0;padding:1rem 1.25rem;border-radius:10px;
        background:#F3F7FC;border-left:4px solid #034EA2;color:#263244;line-height:1.65;">
            <b style="color:#034EA2;">해석 범위</b><br>
            이 전제는 데이터셋의 7개 Scheduling Method 결과를 같은 조건에서 비교하기 위한 공통 범위입니다.
            실제 야드의 모든 변동을 재현하는 조건이 아니라, 결과 차이를 해석하기 위한 공통 기준입니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dataset_selection_cards():
    st.markdown('<div style="height:2.1rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="margin:.4rem 0 1.1rem;">
            <div style="color:#102A43;font-size:2.15rem;font-weight:800;letter-spacing:-.035em;">데이터셋 선정</div>
            <div style="margin-top:.45rem;color:#667085;font-size:1.12rem;">분석 목적과 원본 데이터 접근성을 기준으로 세 가지 후보를 비교해 최종 데이터셋을 선택했다.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    candidate_columns = st.columns(3, gap="medium")
    with candidate_columns[0]:
        st.markdown(
            """
            <div style="height:100%;min-height:235px;padding:1.2rem;border:1px solid #E3E8EF;border-top:4px solid #98A2B3;border-radius:10px;background:#FFFFFF;box-sizing:border-box;">
                <div style="color:#667085;font-size:.82rem;font-weight:800;letter-spacing:.07em;">01 · 제외</div>
                <div style="margin:.65rem 0;color:#102A43;font-size:1.24rem;font-weight:800;">건축 공정 데이터</div>
                <div style="color:#667085;font-size:.95rem;line-height:1.65;">회귀분석 실습에는 적합하지만, 조선 Block 공정과 직접 연결성이 낮음.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with candidate_columns[1]:
        st.markdown(
            """
            <div style="height:100%;min-height:235px;padding:1.2rem;border:1px solid #E3E8EF;border-top:4px solid #98A2B3;border-radius:10px;background:#FFFFFF;box-sizing:border-box;">
                <div style="color:#667085;font-size:.82rem;font-weight:800;letter-spacing:.07em;">02 · 제외</div>
                <div style="margin:.65rem 0;color:#102A43;font-size:1.12rem;font-weight:800;line-height:1.35;">Ship-Construction<br>Resource Leveling</div>
                <div style="color:#667085;font-size:.95rem;line-height:1.65;">조선 프로젝트의 자원 평준화를 다루지만, 데이터 인코딩과 컬럼 정의가 부족함.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with candidate_columns[2]:
        st.markdown(
            """
            <div style="height:100%;min-height:235px;padding:1.2rem;border:2px solid #034EA2;border-top:5px solid #034EA2;border-radius:10px;background:#F1F6FD;box-sizing:border-box;">
                <div style="color:#034EA2;font-size:.82rem;font-weight:800;letter-spacing:.07em;">03 · 최종 선택</div>
                <div style="margin:.65rem 0;color:#102A43;font-size:1.12rem;font-weight:800;line-height:1.35;">Data of Ship Block<br>Scheduling in English</div>
                <div style="color:#475467;font-size:.95rem;line-height:1.65;">Block 특성 기반 Cycle 예측과 Scheduling Result의 Position·계획일정·Delay 비교를 하나의 흐름으로 수행할 수 있음.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(
        """
        <div style="margin:1.55rem 0 0;padding:1rem 1.2rem 1.05rem;border-top:2px solid #034EA2;background:#F8FAFD;color:#475467;font-size:.94rem;line-height:1.62;word-break:keep-all;">
            <div style="color:#102A43;font-size:1.02rem;font-weight:800;margin-bottom:.45rem;">최종 선택 데이터셋 출처 및 연구 계열</div>
            <div><b style="color:#034EA2;">SJTU (Shanghai Jiao Tong University)</b>의 선박 Block 야드 Scheduling 연구 계열로, 「带有进场时间窗的船舶分段堆场调度」(입장 시간창을 고려한 선박 Block 야드 Scheduling)와 같은 문제를 다룹니다.</div>
            <div style="margin-top:.32rem;">Block–Position 제약과 시간창을 함께 고려해 야드 배치·일정을 결정하며, 휴리스틱과 강화학습(DDQN·EDDQN)을 적용하는 흐름의 비교적 최근 연구용 데이터입니다.</div>
            <div style="margin-top:.62rem;padding-top:.55rem;border-top:1px solid #DCE3EC;">
                <b style="color:#102A43;">참고 데이터셋 원문</b>&nbsp;
                <a href="https://data.mendeley.com/datasets/2bmbmbf8hm/1?utm_source=chatgpt.com" target="_blank" style="color:#034EA2;text-decoration:none;">Data of Ship Block Scheduling in English · Mendeley Data</a>
                <span style="color:#98A2B3;">&nbsp;|&nbsp;</span>
                <a href="https://data.mendeley.com/datasets/v8y9gp3kpn/2" target="_blank" style="color:#034EA2;text-decoration:none;">A Ship-Construction Dataset for Resource Leveling Optimization · Mendeley Data</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_eda_heading(title, description):
    st.markdown(
        f"""
        <div style="margin:1.6rem 0 1.1rem;">
            <div style="color:#034EA2;font-size:.88rem;font-weight:800;letter-spacing:.11em;">PREPROCESSING · EDA</div>
            <div style="margin-top:.36rem;color:#102A43;font-size:2.25rem;font-weight:800;letter-spacing:-.04em;">{title}</div>
            <div style="margin-top:.42rem;color:#667085;font-size:1.08rem;line-height:1.6;">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_regression_heading(subpage):
    title = re.sub(r"^3(?:\.\d+)*\s*", "", subpage).strip()
    if subpage.startswith("3.4.1"):
        title = "Feature Set 비교 결과 (CDA)"
    st.markdown(
        f"""
        <div style="margin:1.1rem 0 .8rem;">
            <div style="color:#034EA2;font-size:.82rem;font-weight:800;letter-spacing:.11em;">REGRESSION MODELING</div>
            <div style="margin-top:.25rem;color:#102A43;font-size:1.85rem;font-weight:800;letter-spacing:-.035em;">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_eda_data_quality(data):
    master, analysis = data["master"], data["analysis"]
    missing = master.isna().sum().sort_values(ascending=False)
    missing = missing[missing.gt(0)].rename_axis("컬럼").reset_index(name="결측 행 수")
    render_eda_heading("데이터 품질 확인 · 종속변수", "DDQN 기준 Master Table이 Block 단위로 유지되는지와 분석 대상의 기본 무결성을 먼저 점검했다.")
    compact_metrics(
        [
            ("Master Table", f"{len(master):,}행", f"{master.shape[1]}개 컬럼"),
            ("Block index 중복", f"{master['block_index'].duplicated().sum()}건", "1 Block = 1 행"),
            ("Target 결측", f"{analysis['block_processing_cycle'].isna().sum()}건", "처리 불필요"),
            ("최종 분석 데이터", f"{analysis.shape[0]:,} × {analysis.shape[1]}", "결측 0건"),
        ]
    )
    left, right = st.columns([1.18, .82], gap="large")
    with left:
        st.markdown("#### Master Table 결측 현황")
        st.dataframe(missing, hide_index=True, width="stretch")
    with right:
        st.markdown(
            """
            <div style="margin-bottom:1rem;padding:.75rem .9rem;border:1px solid #BFD4EF;border-left:4px solid #034EA2;border-radius:8px;background:#F7FAFE;">
                <div style="color:#667085;font-size:12px;font-weight:800;letter-spacing:.06em;">종속변수</div>
                <div style="margin-top:.2rem;color:#102A43;font-size:16px;font-weight:800;"><code>block_processing_cycle</code></div>
                <div style="margin-top:.2rem;color:#667085;font-size:12px;">Block Position Cycle · 872개 Block 모두 보유</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### 점검 기준")
        checks = pd.DataFrame(
            [
                ["행 단위", "Block index", "중복 없이 872개 Block 유지"],
                ["예측 대상", "block_processing_cycle", "결측 없이 전 행 보유"],
                ["결측값", "의미·발생 구조", "일괄 대체 대신 변수별 해석"],
                ["분석용 저장", "analysis_DDQN", "최종 20개 컬럼 · 결측 0건"],
            ],
            columns=["점검", "대상", "결론"],
        )
        st.dataframe(checks, hide_index=True, width="stretch")
    analysis_note("결측이 있다는 사실보다 어떤 테이블·어떤 시점에서 생긴 정보인지가 처리 기준이다.")


def render_eda_missing_values(data):
    master = data["master"]
    render_eda_heading("결측값 해석 및 처리", "결측값을 평균이나 최빈값으로 일괄 대체하지 않고, 정보량과 데이터 생성 구조에 따라 제외·범주화·해석을 구분했다.")
    missing_count = master.isna().sum()
    handling = pd.DataFrame(
        [
            ["block_is_combined · block_combined_block", int(missing_count["block_is_combined"]), "제외", "값이 있는 Block이 2개뿐이라 일반 관계 학습이 어려움"],
            ["position_designated_block", int(missing_count["position_designated_block"]), "제외", "전 행 결측으로 정보량 없음"],
            ["position_column1", int(missing_count["position_column1"]), "제외", "값이 26개뿐이고 변수 정의가 불명확"],
            ["position_height_limit", int(missing_count["position_height_limit"]), "제외", "Primary Area와 구조적으로 중복"],
            ["position_block_type", int(missing_count["position_block_type"]), "unrestricted", "제한 없는 Position이라는 상태값으로 해석"],
            ["Initial 상태 컬럼", int(missing_count["initial_block_no"]), "사후 분석용", "초기 점유·가용성 정보로 최종 Cycle 예측에서는 제외"],
        ],
        columns=["컬럼", "결측 행 수", "처리", "해석 근거"],
    )
    st.dataframe(handling, hide_index=True, width="stretch")
    type_by_block = pd.crosstab(
        master["position_block_type"].fillna("unrestricted"),
        master["block_type"],
        margins=True,
    ).reset_index()
    height_by_area = (
        master.groupby("position_primary_area", dropna=False)["position_height_limit"]
        .agg([("전체 행 수", "size"), ("기록 행 수", "count")])
        .reset_index()
    )
    height_by_area["결측 행 수"] = height_by_area["전체 행 수"] - height_by_area["기록 행 수"]
    height_by_area = height_by_area.rename(columns={"position_primary_area": "Position Primary Area"})
    left, right = st.columns([.92, 1.08], gap="large")
    with left:
        st.markdown("#### Height Limit · Primary Area별 집계")
        st.dataframe(height_by_area, hide_index=True, width="stretch")
        analysis_note("높이 제한값은 `curved surface` 182개 행에서만 모두 기록되고, `block assembly group` 197개와 `platform 1` 493개에서는 전부 결측이다. 즉 Position의 Primary Area가 높이 제한값의 존재 여부를 완전히 결정하므로, 별도 모델 변수로 추가하지 않았다.", "구조적 중복 해석")
    with right:
        st.markdown("#### Position Block Type 교차표")
        st.dataframe(type_by_block, hide_index=True, width="stretch")
        analysis_note("`curved`·`flat` 제한 Position에는 해당 Block만 배정됐다. 결측은 오류가 아니라 제한 없는 Position이라는 구조적 상태로 해석해 `unrestricted`로 바꿨다.", "구조적 결측 해석")


def render_eda_target_definition(data):
    analysis = data["analysis"]
    target = analysis["block_processing_cycle"]
    render_eda_heading(
        "종속변수 정의",
        "무엇을 예측하는지와 언제 알 수 있는 정보인지 먼저 고정한 뒤, 이후 파생변수와 모델 입력을 구성했다.",
    )
    left, right = st.columns([1.04, .96], gap="large")
    with left:
        st.markdown("#### 예측 대상")
        target_definition = pd.DataFrame(
            [
                ["변수명", "block_processing_cycle"],
                ["의미", "스케줄링 이전 Block Table에 존재하는 기준 처리기간"],
                ["단위", "일(day)"],
                ["분석 단위", "Block 1개당 1개 값 · 872개 Block"],
                ["결측", "0건"],
            ],
            columns=["항목", "정의"],
        )
        st.dataframe(target_definition, hide_index=True, width="stretch", height=195)
    with right:
        st.markdown("#### 해석 기준")
        st.markdown(
            "`Block Position Cycle`은 실제 작업 완료 뒤에 측정된 성과지표가 아니라, "
            "**Block이 어떤 Position에 배정되기 전부터 주어진 기준 작업기간**으로 해석한다."
        )
        st.markdown(
            "따라서 이 프로젝트의 질문은 **Block 고유 특성만으로 이 기준 처리기간을 어느 정도 예측할 수 있는가**이다."
        )
        st.caption(f"현재 데이터 기준: 중앙값 {target.median():.1f}일 · 범위 {target.min():.0f}~{target.max():.0f}일")

    st.markdown("#### 데이터 생성 시점에 따른 변수 사용 원칙")
    timing = pd.DataFrame(
        [
            ["스케줄링 이전", "Block Table의 물리·일정 특성", "최종 예측 입력 (Set A)", "예측 시점에 실제로 알 수 있는 정보"],
            ["스케줄링 이후", "DDQN이 선택한 Position 특성", "사후 진단 (Set B)", "성능 변화 확인용 · 최종 입력 제외"],
            ["스케줄링 시작 시점", "Initial 점유 상태", "사후 진단 (Set C)", "결과층 정보 · 최종 입력 제외"],
        ],
        columns=["정보 시점", "사용 정보", "분석 역할", "판단 기준"],
    )
    st.dataframe(timing, hide_index=True, width="stretch", height=145)
    analysis_note(
        "Position·Initial 변수를 추가한 Set B/C는 인과효과를 검증하거나 최종 모델을 대체하기 위한 것이 아니다. "
        "데이터 생성 순서를 무시해 결과층 정보를 넣었을 때 성능과 해석이 어떻게 달라지는지 확인하는 진단 실험으로만 사용한다.",
        "종속변수·입력변수 구분",
    )


def render_eda_derived_features(data):
    render_eda_heading("파생변수 생성", "날짜·물리량·Position 상태에서 만든 변수를 사전 예측용 Block 변수와 Result 이후 진단 변수로 구분했다.")
    definitions = pd.DataFrame(
        [
            ["season", "on-position date → 계절", "Block", "Set A"],
            ["block_start_window", "latest start − earliest start", "Block", "Set A"],
            ["block_area", "length × width", "Block", "Set A"],
            ["position_area", "Position width × height", "Result 이후", "Set B"],
            ["area_margin_ratio", "(Position area − Block area) / Position area", "Result 이후", "Set B"],
            ["lifting_load_ratio", "Block weight / lifting capacity", "Result 이후", "Set B"],
            ["initially_occupied", "Initial 기록 유무", "Result 이후", "Set C"],
        ],
        columns=["파생변수", "생성 방식", "데이터 시점", "사용 세트"],
    )
    st.dataframe(definitions, hide_index=True, width="stretch")
    st.markdown("#### 파생변수 생성 코드")
    with st.container(height=280, border=False):
        st.code(
            """# ============================================================
# 1. 계절 변수 생성
# ============================================================

# on-position date를 datetime 형식으로 변환한 뒤,
# 해당 월을 기준으로 계절 범주 생성
analysis['block_on_position_date'] = pd.to_datetime(
    analysis['block_on_position_date']
)

analysis['season'] = (
    analysis['block_on_position_date']
    .dt.month
    .map({
        12: 'winter', 1: 'winter', 2: 'winter',
        3: 'spring', 4: 'spring', 5: 'spring',
        6: 'summer', 7: 'summer', 8: 'summer',
        9: 'autumn', 10: 'autumn', 11: 'autumn'
    })
)


# ============================================================
# 2. Block 작업 시작 가능 기간 생성
# ============================================================

# earliest / latest start time을 datetime 형식으로 변환한 뒤,
# 두 시점의 차이를 일(day) 단위로 계산
analysis['block_earliest_start'] = pd.to_datetime(
    analysis['block_earliest_start']
)

analysis['block_latest_start'] = pd.to_datetime(
    analysis['block_latest_start']
)

analysis['block_start_window'] = (
    analysis['block_latest_start']
    - analysis['block_earliest_start']
).dt.days


# ============================================================
# 3. 공간 여유 비율 생성
# ============================================================

# Block의 가로 × 세로를 이용해 Block 면적 계산
analysis['block_area'] = (
    analysis['block_length']
    * analysis['block_width']
)

# Position의 size 문자열을 길이와 폭으로 분리
# 예: '20*15' → position_length=20, position_width=15
analysis[['position_length', 'position_width']] = (
    analysis['position_size']
    .str.split('*', expand=True)
    .astype(float)
)

# Position의 길이 × 폭을 이용해 Position 면적 계산
analysis['position_area'] = (
    analysis['position_length']
    * analysis['position_width']
)

# Position 면적 대비 Block 배치 후 남는 면적 비율 계산
# → 값이 클수록 상대적인 공간 여유가 큼
analysis['area_margin_ratio'] = (
    analysis['position_area']
    - analysis['block_area']
) / analysis['position_area']


# ============================================================
# 4. 인양능력 사용 비율 생성
# ============================================================

# Position 인양능력 대비 Block 무게의 비율 계산
# → 값이 1에 가까울수록 인양능력을 많이 사용하는 Block
analysis['lifting_load_ratio'] = (
    analysis['block_weight']
    / analysis['position_lifting_capacity']
)


# ============================================================
# 5. 초기 점유 상태 변수 생성
# ============================================================

# Initial Table에 해당 Position의 기록이 존재하는지 여부를 이용해
# 스케줄링 시작 시점의 초기 점유 상태 생성
# 1: Initial Table에 기록된 Position
# 0: Initial Table에 기록되지 않은 Position
analysis['initially_occupied'] = (
    analysis['initial_ship_no']
    .notna()
    .astype(int)
)


# ============================================================
# 6. 생성된 파생변수 확인
# ============================================================

analysis[[
    'season',
    'block_start_window',
    'area_margin_ratio',
    'lifting_load_ratio',
    'initially_occupied'
]].head()""",
            language="python",
        )


def render_eda_outliers(data):
    analysis = data["analysis"]
    render_eda_heading("이상치 확인", "IQR 기준으로 이상치 후보를 찾되, 대형 Block·장기 작업의 실제 특성일 수 있으므로 자동 제거하지 않았다.")
    labels = {
        "block_length": "Block 길이",
        "block_width": "Block 폭",
        "block_weight": "Block 중량",
        "block_start_window": "시작 가능 구간",
        "block_area": "Block 면적",
        "area_margin_ratio": "면적 여유비율",
        "lifting_load_ratio": "인양부하비율",
        "block_processing_cycle": "Block Position Cycle",
    }
    rows = []
    for column, label in labels.items():
        q1, q3 = analysis[column].quantile([.25, .75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((analysis[column] < lower) | (analysis[column] > upper)).sum())
        rows.append([label, round(lower, 2), round(upper, 2), count, "유지"])
    outlier_table = pd.DataFrame(
        rows,
        columns=[
            "변수",
            "IQR 하한 (Q1 − 1.5×IQR)",
            "IQR 상한 (Q3 + 1.5×IQR)",
            "후보 수 (범위 밖)",
            "처리",
        ],
    )
    st.dataframe(outlier_table, hide_index=True, width="stretch")

    render_precomputed_chart("eda_outliers.png")
    st.markdown(
        """
        **소결론**

        IQR 기준으로 일부 변수에서 이상치 후보가 확인되었으나, Boxplot상 대부분 연속적인 분포의 꼬리에 위치하며 명백한 입력 오류로 판단할 만한 값은 확인되지 않았다.

        특히 Block의 크기와 Processing Cycle은 작업 대상의 특성에 따라 실제 편차가 발생할 수 있으므로, 현 단계에서는 이상치를 제거하지 않고 유지한다. 이후 모델링 과정에서 특정 관측치가 예측 오차에 과도한 영향을 미치는 경우 해당 데이터를 개별적으로 재검토한다.
        """
    )


def render_eda_target_distribution(data):
    analysis = data["analysis"]
    target = analysis["block_processing_cycle"]
    render_eda_heading("종속변수 분포", "예측 대상인 Block Position Cycle의 분포와 장기 Cycle 구간의 표본 특성을 확인했다.")
    render_precomputed_chart("eda_target_distribution.png")
    analysis_note(
        f"중앙값은 {target.median():.1f}일이며 대부분의 값은 중간 Cycle 구간에 모여 있다. "
        "50일 이상 장기 Cycle도 연속적인 꼬리로 존재한다. Block 크기·형상·작업 조건에 따른 실제 편차일 수 있으므로 이를 제거하면 장기 작업 표본이 사라져 "
        "모델이 긴 Cycle을 더 과소예측할 수 있다. 따라서 현 단계에서는 유지하고, 장기 구간의 예측오차를 별도로 점검한다.",
        "분포 해석",
    )


def render_eda_numeric_correlation(data):
    analysis = data["analysis"]
    numeric_columns = [
        "block_length", "block_width", "block_weight", "block_area", "block_start_window",
        "position_lifting_capacity", "position_area", "area_margin_ratio", "lifting_load_ratio",
        "initially_occupied", "block_processing_cycle",
    ]
    render_eda_heading("수치형 변수 상관관계", "Block 물리량·Position 특성·파생변수와 Block Position Cycle의 선형 관계를 함께 확인했다.")
    chart_col, interpretation_col = st.columns([1.22, .78], gap="large")
    with chart_col:
        render_precomputed_chart("eda_numeric_correlation.png", width="content")
    with interpretation_col:
        st.markdown("#### 상관관계 해석")
        st.markdown(
            "**1. Cycle과 직접 관련된 특성**  \\n"
            "시작 가능 구간은 Cycle과 중간 수준의 양(+)의 관계를 보이며, 길이·폭·중량·면적 같은 Block 물리 특성도 일정한 관련성을 보인다."
        )
        st.markdown(
            "**2. 단일 변수만으로는 한계**  \\n"
            "어느 한 변수도 Cycle을 충분히 설명할 만큼 강하지 않으므로, 여러 Block 고유 특성을 함께 사용해 예측한다."
        )
        st.markdown(
            "**3. 높은 변수 간 상관의 처리**  \\n"
            "중량·면적·인양부하비율은 계산 구조가 겹쳐 높은 상관이 나타난다. 예측 성능을 기준으로 비교하되, 상관계수만으로 임의 제거하지 않았다."
        )
        st.markdown(
            "**4. 사전 예측 기준**  \\n"
            "스케줄링 이후 결정되는 Position 관련 변수는 최종 사전 예측용 Set A에서 제외하고 사후 진단에만 활용한다."
        )


def render_eda_categorical_distribution(data):
    analysis = data["analysis"]
    category_columns = [
        "block_ship_no", "block_type", "season", "position_primary_area",
        "position_block_type", "position_attribute",
    ]
    labels = {
        "block_ship_no": "선체 번호", "block_type": "Block 유형", "season": "계절",
        "position_primary_area": "Position 주 구역", "position_block_type": "Position Block 유형",
        "position_attribute": "Position 속성",
    }
    render_eda_heading("범주형 변수별 Cycle 분포", "Block·Position 범주에 따라 Block Position Cycle의 중앙값과 분포 폭이 어떻게 달라지는지 비교했다.")
    render_precomputed_chart("eda_categorical_distribution.png")
    st.markdown("#### 변수별 분포 해석")
    categorical_summary = pd.DataFrame(
        [
            ["선체 번호", "두 선박의 중앙값 차이는 크지 않지만 H1088에서 장기 Cycle이 상대적으로 많다.", "선박별 표본 구성 차이를 함께 고려한다."],
            ["Block 유형", "curved의 중앙값이 다소 높지만 flat과 분포가 상당히 겹친다.", "Block Type만으로 Cycle이 뚜렷하게 구분되지는 않는다."],
            ["계절", "autumn은 상대적으로 낮고 spring은 높은 경향을 보인다.", "범주별 표본 수와 다른 변수의 영향을 함께 본다."],
            ["Position 주 구역", "curved surface에서 비교적 높은 Cycle 분포가 나타난다.", "Position은 DDQN의 선택 결과이므로 원인이 아닌 연관성으로 해석한다."],
            ["Position Block 유형", "flat·unrestricted·curved 사이의 차이가 크지 않다.", "Cycle을 직접 구분하는 효과는 제한적으로 보인다."],
            ["Position 속성", "두 범주의 중앙값과 분포는 겹치지만 general에서 장기 Cycle이 더 관찰된다.", "Boxplot만으로 관계를 확정하지 않는다."],
        ],
        columns=["변수", "관찰 결과", "해석상 주의점"],
    )
    st.dataframe(categorical_summary, hide_index=True, width="stretch", height=178)


def render_eda_feature_sets(data):
    render_eda_heading("독립변수 세트 구성", "종속변수와 Set A·B·C를 정의한 뒤, 비교에 필요한 최종 분석용 데이터를 구성했다.")
    left, right = st.columns([1.22, .78], gap="large")
    with left:
        st.markdown("#### 종속변수 및 Feature Set 정의")
        with st.container(height=760, border=False):
            st.code(
                """# ============================================================
# 종속변수 및 Feature Set 정의
# ============================================================

# 예측 대상: 스케줄링 이전 Block Table에 주어진 기준 처리기간
target_col = 'block_processing_cycle'


# ============================================================
# Set A - Block 특성
# ============================================================

# Block 자체의 물리적·일정 특성만 사용
# → 기준 처리기간이 Block 정보만으로 어느 정도 설명되는지 확인
set_a = [
    'block_ship_no',
    'block_type',
    'block_length',
    'block_width',
    'block_weight',
    'block_area',
    'season',
    'block_start_window'
]


# ============================================================
# Set B - Block + Position 특성
# ============================================================

# Set A에 스케줄링을 통해 선택된 Position의 특성을 추가
# → Position 정보가 Cycle 예측 성능에 어떤 영향을 주는지 확인
set_b = set_a + [
    'position_primary_area',
    'position_secondary_area',
    'position_lifting_capacity',
    'position_labor_team',
    'position_block_type',
    'position_attribute',
    'position_area',
    'area_margin_ratio',
    'lifting_load_ratio'
]


# ============================================================
# Set C - Block + Position + Initial 특성
# ============================================================

# Set B에 해당 Position의 스케줄링 시작 시점 초기 점유 상태를 추가
# → 초기 야드 상태 정보까지 포함했을 때의 추가 효과 확인
set_c = set_b + [
    'initially_occupied'
]


# ============================================================
# Feature Set 통합 관리
# ============================================================

# 이후 동일한 모델에 Set A / B / C를 반복 적용하기 위해 Dictionary로 정리
feature_sets = {
    'Set A - Block': set_a,
    'Set B - Block + Position': set_b,
    'Set C - Block + Position + Initial': set_c
}


# ============================================================
# Feature Set 구성 확인
# ============================================================

# Set별 변수 개수와 포함 변수 출력
for name, columns in feature_sets.items():
    print(name, ':', len(columns), 'variables')
    print(columns)
    print()""",
                language="python",
            )
    with right:
        st.markdown("#### 최종 분석용 데이터 구성")
        with st.container(height=760, border=False):
            st.code(
                """# ============================================================
# 최종 분석용 데이터 구성
# ============================================================

# Block 식별자 + Set C 전체 변수 + 종속변수만 남김
# → Set A / B / C 비교에 필요한 모든 변수를 포함한 최종 분석 데이터 생성
analysis = analysis[
    ['block_index'] + set_c + [target_col]
].copy()


# ============================================================
# 최종 분석 데이터 확인
# ============================================================

# 최종 데이터 크기와 결측값 여부 확인
print('최종 분석 데이터:', analysis.shape)
print('최종 결측값:', analysis.isna().sum().sum())

# 최종 데이터 구조 확인
analysis.head()""",
                language="python",
            )


@st.cache_data(show_spinner=False)
def build_virtual_yard_plan(position_catalog, query_position_id=None, selected_position_id=None):
    positions = position_catalog.copy()
    positions[["size_width", "size_height"]] = (
        positions["size"].astype(str).str.split("*", expand=True).astype(float)
    )
    assert len(positions) == 66, "Position Table must contain 66 positions."

    area_styles = {
        "block assembly group": ("블록 조립 구역", "#034EA2", "rgba(3,78,162,0.12)"),
        "platform 1": ("플랫폼 구역", "#2D7D8C", "rgba(45,125,140,0.12)"),
        "curved surface": ("곡면 구역", "#6B5AA6", "rgba(107,90,166,0.12)"),
    }
    area_geometry = {
        "block assembly group": (90.0, 5.0, 116.0),
        "platform 1": (150.0, 0.0, 126.0),
        "curved surface": (75.0, 4.0, 118.0),
    }
    zone_gap = 0.0
    yard_height = max(y0 + height for _, y0, height in area_geometry.values())
    x_offset = 0.0
    layout = []
    zone_bounds = []

    for area, (zone_width, zone_y0, zone_height) in area_geometry.items():
        area_positions = positions[positions["primary area"].eq(area)].copy()
        area_positions["position_area"] = area_positions["size_width"] * area_positions["size_height"]
        area_positions = area_positions.sort_values("position_area", ascending=False)
        row_count = max(1, round(math.sqrt(len(area_positions) * zone_height / zone_width)))
        remaining_area = area_positions["position_area"].sum()
        remaining_rows = row_count
        rows, current_row, current_area = [], [], 0.0
        for _, row in area_positions.iterrows():
            current_row.append(row)
            current_area += row["position_area"]
            if remaining_rows > 1 and current_area >= remaining_area / remaining_rows:
                rows.append(current_row)
                remaining_area -= current_area
                remaining_rows -= 1
                current_row, current_area = [], 0.0
        if current_row:
            rows.append(current_row)

        scale = zone_width * zone_height / area_positions["position_area"].sum()
        y_cursor = zone_y0
        zone_bounds.append((area, x_offset, x_offset + zone_width, zone_y0, zone_y0 + zone_height))
        for row_items in rows:
            row_area = sum(item["position_area"] for item in row_items)
            row_height = row_area * scale / zone_width
            x_cursor = x_offset
            for item in row_items:
                width = item["position_area"] * scale / row_height
                layout.append(
                    {
                        **item.to_dict(),
                        "x0": x_cursor,
                        "x1": x_cursor + width,
                        "y0": y_cursor,
                        "y1": y_cursor + row_height,
                    }
                )
                x_cursor += width
            y_cursor += row_height
        x_offset += zone_width + zone_gap

    total_width = x_offset - zone_gap
    figure = go.Figure()
    (_, ax0, ax1, ay0, ay1), (_, bx0, bx1, by0, by1), (_, cx0, cx1, cy0, cy1) = zone_bounds
    outline_path = (
        f"M {ax0},{ay0} L {ax1},{ay0} L {bx0},{by0} L {bx1},{by0} "
        f"L {cx0},{cy0} L {cx1},{cy0} L {cx1},{cy1} L {cx0},{cy1} "
        f"L {bx1},{by1} L {bx0},{by1} L {ax1},{ay1} L {ax0},{ay1} Z"
    )
    figure.add_shape(
        type="path",
        path=outline_path,
        fillcolor="#F8FAFC",
        line={"width": 0},
        layer="below",
    )

    for area, x0, x1, y0, y1 in zone_bounds:
        label, color, fill = area_styles[area]
        figure.add_shape(
            type="rect",
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            fillcolor=fill,
            line={"width": 0},
            layer="below",
        )
        figure.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={"size": 11, "symbol": "square", "color": color},
                name=label,
                hoverinfo="skip",
                showlegend=True,
            )
        )

    figure.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker={
                "size": 11,
                "symbol": "square",
                "color": "rgba(255,193,7,0.28)",
                "line": {"color": "#D18F00", "width": 2},
            },
            name="조회 Position",
            hoverinfo="skip",
            showlegend=True,
        )
    )
    figure.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker={
                "size": 11,
                "symbol": "square",
                "color": "rgba(3,78,162,0.16)",
                "line": {"color": "#034EA2", "width": 2},
            },
            name="선택 Position",
            hoverinfo="skip",
            showlegend=True,
        )
    )
    figure.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker={
                "size": 11,
                "symbol": "square-open",
                "color": "#263244",
                "line": {"width": 2},
            },
            name="전체 야드",
            hoverinfo="skip",
            showlegend=True,
        )
    )

    hover_x, hover_y, hover_data = [], [], []
    query_center = None
    selected_center = None
    for row in layout:
        _, color, _ = area_styles[row["primary area"]]
        is_query = str(row["block position id"]) == str(query_position_id)
        is_selected = str(row["block position id"]) == str(selected_position_id)
        figure.add_shape(
            type="rect",
            x0=row["x0"],
            x1=row["x1"],
            y0=row["y0"],
            y1=row["y1"],
            fillcolor="rgba(255,255,255,0.38)",
            line={"width": 0},
        )
        boundary = {"color": color, "width": 1.1, "dash": "dot"}
        figure.add_shape(
            type="line", x0=row["x0"], x1=row["x1"], y0=row["y0"], y1=row["y0"], line=boundary
        )
        figure.add_shape(
            type="line", x0=row["x0"], x1=row["x0"], y0=row["y0"], y1=row["y1"], line=boundary
        )
        figure.add_annotation(
            x=(row["x0"] + row["x1"]) / 2,
            y=(row["y0"] + row["y1"]) / 2,
            text=f"<b>P{int(row['index']):02d}</b>" if is_query or is_selected else f"P{int(row['index']):02d}",
            showarrow=False,
            font={"color": "#9A6500" if is_query else "#034EA2" if is_selected else "#263244", "size": 10 if is_query or is_selected else 9},
        )
        if is_query:
            query_center = ((row["x0"] + row["x1"]) / 2, (row["y0"] + row["y1"]) / 2)
            figure.add_shape(
                type="rect",
                x0=row["x0"],
                x1=row["x1"],
                y0=row["y0"],
                y1=row["y1"],
                fillcolor="rgba(255,193,7,0.28)",
                line={"color": "#D18F00", "width": 4},
                layer="above",
            )
        if is_selected:
            selected_center = ((row["x0"] + row["x1"]) / 2, (row["y0"] + row["y1"]) / 2)
            figure.add_shape(
                type="rect",
                x0=row["x0"],
                x1=row["x1"],
                y0=row["y0"],
                y1=row["y1"],
                fillcolor="rgba(3,78,162,0.16)",
                line={"color": "#034EA2", "width": 4},
                layer="above",
            )
        hover_x.append((row["x0"] + row["x1"]) / 2)
        hover_y.append((row["y0"] + row["y1"]) / 2)
        hover_data.append(
            [
                f"P{int(row['index']):02d}",
                row["block position id"],
                row["block position description"],
                row["primary area"],
                row["secondary area"],
                row["size"],
                row["lifting capacity (T)"],
                row["labor team"],
            ]
        )

    figure.add_shape(
        type="path",
        path=outline_path,
        fillcolor="rgba(0,0,0,0)",
        line={"color": "#263244", "width": 5},
        layer="above",
    )

    figure.add_trace(
        go.Scatter(
            x=hover_x,
            y=hover_y,
            mode="markers",
            marker={"size": 36, "color": "rgba(255,255,255,0.01)"},
            customdata=hover_data,
            hovertemplate=(
                "<b>%{customdata[0]} · %{customdata[1]}</b><br>"
                "%{customdata[2]}<br>구역: %{customdata[3]} / %{customdata[4]}<br>"
                "크기: %{customdata[5]} · 인양용량: %{customdata[6]}T<br>작업조: %{customdata[7]}<extra></extra>"
            ),
            showlegend=False,
        )
    )
    if query_center:
        figure.add_annotation(
            x=query_center[0],
            y=query_center[1],
            text=f"<b>조회 Position<br>{query_position_id}</b>",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-55,
            bgcolor="#FFF4CC",
            bordercolor="#D18F00",
            borderpad=5,
            font={"color": "#6B4700", "size": 11},
        )
    if selected_center and str(selected_position_id) != str(query_position_id):
        figure.add_annotation(
            x=selected_center[0],
            y=selected_center[1],
            text=f"<b>선택 Position<br>{selected_position_id}</b>",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=55,
            bgcolor="#EAF2FB",
            bordercolor="#034EA2",
            borderpad=5,
            font={"color": "#034EA2", "size": 11},
        )
    figure.update_layout(
        height=400,
        margin={"l": 15, "r": 15, "t": 46, "b": 15},
        paper_bgcolor="white",
        plot_bgcolor="white",
        clickmode="event+select",
        legend={
            "orientation": "h",
            "x": 0,
            "y": 1.08,
            "xanchor": "left",
            "yanchor": "bottom",
            "font": {"size": 12},
        },
        xaxis={"visible": False, "range": [-7, total_width + 5], "fixedrange": True},
        yaxis={"visible": False, "range": [-2, yard_height + 3], "scaleanchor": "x", "fixedrange": True},
        hoverlabel={"font": {"family": "Malgun Gothic", "size": 13}},
    )
    return figure


@st.cache_data(show_spinner=False, max_entries=32)
def build_block_3d(block):
    block_index = int(block["block_index"])
    length = float(block["block_length"])
    width = float(block["block_width"])
    weight = float(block["block_weight"])
    block_area = float(block["block_area"])
    block_type = str(block["block_type"])
    ship_no = str(block["block_ship_no"])
    shape_no = (block_index - 1) % 10 + 1
    shape_code = f"{'C' if block_type == 'curved' else 'F'}-{shape_no:02d}"
    height = max(2.5, min(7.5, weight / 40))
    ship_length, ship_width, ship_depth = (100, 34, 8) if ship_no == "H1087" else (115, 30, 7)
    block_x = min(ship_length - length - 8, ship_length * 0.42)
    block_z = 0.6

    # 실제 3D 형상 데이터가 없으므로 타입별 10개의 단순 개념 형상을 반복 배정한다.
    if block_type == "curved":
        lower_width = 0.24 + (shape_no % 5) * 0.035
        shoulder_height = 0.45 + (shape_no // 6) * 0.10
        top_width = 0.34 + ((shape_no + 2) % 5) * 0.025
        section = [
            (-width / 2, height * shoulder_height),
            (-width * lower_width, 0),
            (width * lower_width, 0),
            (width / 2, height * shoulder_height),
            (width * top_width, height),
            (-width * top_width, height),
        ]
    else:
        bottom_inset = (shape_no % 5) * 0.025
        top_inset = ((shape_no + 2) % 5) * 0.025
        side_step = 0.10 if shape_no > 5 else 0
        section = [
            (-width * (0.50 - bottom_inset), 0),
            (width * (0.50 - bottom_inset), 0),
            (width / 2, height * side_step),
            (width * (0.50 - top_inset), height),
            (-width * (0.50 - top_inset), height),
            (-width / 2, height * side_step),
        ]

    point_count = len(section)
    x = [block_x] * point_count + [block_x + length] * point_count
    y = [point[0] for point in section] * 2
    z = [point[1] + block_z for point in section] * 2
    i, j, k = [], [], []

    for index in range(point_count):
        next_index = (index + 1) % point_count
        i.extend([index, index])
        j.extend([next_index, point_count + next_index])
        k.extend([point_count + next_index, point_count + index])

    for index in range(1, point_count - 1):
        i.extend([0, point_count])
        j.extend([index, point_count + index])
        k.extend([index + 1, point_count + index + 1])

    hover = (
        f"<b>Block {block_index}</b><br>Type: {block_type}<br>"
        f"길이 {length:.1f}m · 폭 {width:.1f}m<br>중량 {weight:.1f}T · 면적 {block_area:.1f}㎡"
    )
    figure = go.Figure()
    figure.add_trace(
        go.Mesh3d(
            x=[0, 14, 14, ship_length, ship_length, 7, 14, 14, ship_length, ship_length],
            y=[0, -ship_width / 2, ship_width / 2, -ship_width / 2, ship_width / 2, 0,
               -ship_width * 0.32, ship_width * 0.32, -ship_width * 0.32, ship_width * 0.32],
            z=[0, 0, 0, 0, 0, -ship_depth, -ship_depth, -ship_depth, -ship_depth, -ship_depth],
            alphahull=0,
            color="#7D8EA3",
            opacity=0.30,
            flatshading=True,
            hoverinfo="skip",
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatter3d(
            x=[0, 14, ship_length, ship_length, 14, 0],
            y=[0, -ship_width / 2, -ship_width / 2, ship_width / 2, ship_width / 2, 0],
            z=[0.05] * 6,
            mode="lines",
            line={"color": "#425B76", "width": 5},
            hoverinfo="skip",
            showlegend=False,
        )
    )

    cabin_x0 = ship_length * 0.78 if ship_no == "H1087" else ship_length * 0.16
    cabin_x1 = cabin_x0 + ship_length * 0.12
    cabin_y0, cabin_y1 = -ship_width * 0.22, ship_width * 0.22
    cabin_z0, cabin_z1 = 0, ship_depth * 0.72
    cabin_x = [cabin_x0, cabin_x1, cabin_x1, cabin_x0, cabin_x0, cabin_x1, cabin_x1, cabin_x0]
    cabin_y = [cabin_y0, cabin_y0, cabin_y1, cabin_y1, cabin_y0, cabin_y0, cabin_y1, cabin_y1]
    cabin_z = [cabin_z0, cabin_z0, cabin_z0, cabin_z0, cabin_z1, cabin_z1, cabin_z1, cabin_z1]
    cabin_i = [0, 0, 4, 4, 0, 1, 2, 3, 0, 1, 2, 3]
    cabin_j = [1, 2, 5, 6, 1, 2, 3, 0, 4, 5, 6, 7]
    cabin_k = [2, 3, 6, 7, 5, 6, 7, 4, 5, 6, 7, 4]
    figure.add_trace(
        go.Mesh3d(
            x=cabin_x,
            y=cabin_y,
            z=cabin_z,
            i=cabin_i,
            j=cabin_j,
            k=cabin_k,
            color="#D8DEE9",
            opacity=0.92,
            flatshading=True,
            hoverinfo="skip",
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=i,
            j=j,
            k=k,
            color="#D18F00",
            opacity=0.62,
            flatshading=True,
            text=[hover] * len(x),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    frame_x, frame_y, frame_z = [], [], []
    # 하나의 Block이 여러 칸으로 보이지 않도록 양쪽 끝 윤곽만 표시한다.
    for ratio in [0, 1]:
        for point in [*section, section[0]]:
            frame_x.append(block_x + length * ratio)
            frame_y.append(point[0])
            frame_z.append(point[1] + block_z)
        frame_x.append(None)
        frame_y.append(None)
        frame_z.append(None)
    for point in section:
        frame_x.extend([block_x, block_x + length, None])
        frame_y.extend([point[0], point[0], None])
        frame_z.extend([point[1] + block_z, point[1] + block_z, None])

    figure.add_trace(
        go.Scatter3d(
            x=frame_x,
            y=frame_y,
            z=frame_z,
            mode="lines",
            line={"color": "#6B4700", "width": 4},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatter3d(
            x=[ship_length * 0.55, block_x + length / 2],
            y=[-ship_width / 2 - 3, -width / 2 - 2],
            z=[-ship_depth / 2, block_z + height / 2],
            mode="text",
            text=[f"<b>Ship {ship_no}</b>", f"<b>Block {block_index}</b>"],
            textfont={"size": 12, "color": "#102A43"},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    figure.update_layout(
        title={"text": f"Isometric Concept · Ship {ship_no} / Block {block_index}", "font": {"size": 15}},
        height=400,
        margin={"l": 0, "r": 0, "t": 70, "b": 0},
        paper_bgcolor="white",
        annotations=[
            {
                "x": 0,
                "y": 1.04,
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "xanchor": "left",
                "align": "left",
                "text": (
                    f"<b>{shape_code} · {block_type}</b> &nbsp;|&nbsp; "
                    f"L {length:.1f}m × W {width:.1f}m × H {height:.1f}m(가상) &nbsp;|&nbsp; "
                    f"{weight:.1f}T"
                ),
                "font": {"size": 11, "color": "#425B76"},
            }
        ],
        scene={
            "aspectmode": "data",
            "camera": {"eye": {"x": 1.45, "y": 1.45, "z": 1.05}},
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "zaxis": {"visible": False},
        },
        dragmode=False,
        font={"family": "Malgun Gothic", "color": "#263244"},
        showlegend=False,
    )
    return figure


@st.cache_data(show_spinner=False, max_entries=32)
def build_block_isometric(block):
    block_index = int(block["block_index"])
    length = float(block["block_length"])
    width = float(block["block_width"])
    weight = float(block["block_weight"])
    block_type = str(block["block_type"])
    ship_no = str(block["block_ship_no"])
    random_generator = np.random.default_rng(block_index)
    sections = [
        (260, 382, 542, 549), (260, 550, 542, 680), (543, 382, 786, 680),
        (787, 205, 1053, 382), (787, 383, 1053, 503), (787, 504, 1053, 680),
        (1054, 205, 1289, 382), (1054, 383, 1289, 503), (1054, 504, 1289, 680),
        (1290, 205, 1518, 320), (1290, 321, 1518, 503), (1290, 504, 1518, 680),
        (1519, 320, 1698, 503), (1519, 504, 1698, 680), (1699, 448, 1840, 680),
    ]
    figure = go.Figure()
    ship_image = Image.open(SHIP_BLOCK_PLAN_IMAGE_PATH)
    image_width, image_height = ship_image.size
    selected_section = int(random_generator.integers(0, len(sections)))
    x0, y0, x1, y1 = sections[selected_section]
    figure.add_layout_image(
        dict(source=ship_image, xref="x", yref="y", x=0, y=0, sizex=image_width, sizey=image_height, sizing="stretch", layer="below")
    )
    figure.add_shape(
        type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
        fillcolor="rgba(246, 191, 24, 0.68)", line={"color": "#D18F00", "width": 2},
    )
    figure.add_annotation(
        x=(x0 + x1) / 2,
        y=y0,
        text=f"<b>Block {block_index}</b><br>{block_type}",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#D18F00",
        bgcolor="rgba(255,255,255,0.92)",
        bordercolor="#D18F00",
        borderpad=4,
        font={"size": 11, "color": "#102A43"},
        ax=0, ay=-38,
    )
    figure.update_layout(
        title={"text": f"Ship Block Concept · Ship {ship_no} / Block {block_index}", "font": {"size": 15}},
        height=340,
        margin={"l": 0, "r": 0, "t": 58, "b": 0},
        paper_bgcolor="white",
        plot_bgcolor="white",
        annotations=[
            *figure.layout.annotations,
            {
                "x": 0,
                "y": 1.02,
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "xanchor": "left",
                "text": (
                    f"<b>{block_type}</b> &nbsp;|&nbsp; L {length:.1f}m × W {width:.1f}m &nbsp;|&nbsp; {weight:.1f}T "
                    "&nbsp;|&nbsp; 노란 영역은 Block별로 달라지는 개념 표시"
                ),
                "font": {"size": 11, "color": "#425B76"},
            },
        ],
        xaxis={"visible": False, "fixedrange": True, "range": [0, image_width]},
        yaxis={"visible": False, "fixedrange": True, "range": [image_height, 0], "scaleanchor": "x", "scaleratio": 1},
        font={"family": "Malgun Gothic", "color": "#263244"},
        showlegend=False,
    )
    return figure


@st.cache_resource(show_spinner=False)
def load_schedule_result(method):
    precomputed_path = PRECOMPUTED_DIR / "scheduling_results" / f"{method}_scheduled.pkl"
    schedule = (
        pd.read_pickle(precomputed_path)
        if precomputed_path.exists()
        else pd.read_excel(RESULT_DIR / RESULT_FILES[method], sheet_name="Scheduled Segments")
    )
    schedule["planned start time"] = pd.to_datetime(schedule["planned start time"], errors="coerce")
    schedule["planned finish time"] = pd.to_datetime(schedule["planned finish time"], errors="coerce")
    return schedule.dropna(subset=["planned start time", "planned finish time"])


@st.cache_data(show_spinner=False, max_entries=32)
def build_position_gantt(schedule, position_catalog, method, selected_block, gantt_scope="조회 Position", selected_position_id=None):
    selected_rows = schedule[schedule["block sequence no."].eq(selected_block)]
    query_position = selected_rows["block position id"].iloc[0]
    gantt_position = selected_position_id if gantt_scope == "선택 Position" and selected_position_id else query_position

    if gantt_scope in ["조회 Position", "선택 Position"]:
        schedule = schedule[schedule["block position id"].eq(gantt_position)].copy()
    elif gantt_scope != "전체 야드":
        area_by_label = {label: area for area, (label, _) in YARD_AREA_STYLES.items()}
        area_positions = position_catalog.loc[
            position_catalog["primary area"].eq(area_by_label[gantt_scope]),
            "block position id",
        ]
        schedule = schedule[schedule["block position id"].isin(area_positions)].copy()

    gantt = schedule.merge(
        position_catalog[["block position id", "primary area"]],
        on="block position id",
        how="left",
    )
    gantt["start_label"] = gantt["planned start time"].dt.strftime("%Y-%m-%d")
    gantt["finish_label"] = gantt["planned finish time"].dt.strftime("%Y-%m-%d")
    gantt["selected"] = gantt["block sequence no."].eq(selected_block)
    position_order = (
        gantt.sort_values(["primary area", "block position id"])["block position id"]
        .drop_duplicates()
        .tolist()
    )
    figure = go.Figure()

    def add_schedule_trace(rows, name, color, width):
        x, y, hover = [], [], []
        for _, row in rows.iterrows():
            text = (
                f"<b>Block {int(row['block sequence no.'])}</b><br>{row['block position id']}<br>"
                f"{row['start_label']} → {row['finish_label']}<br>Delay {int(row['delay days'])}일"
            )
            x.extend([row["planned start time"], row["planned finish time"], None])
            y.extend([row["block position id"], row["block position id"], None])
            hover.extend([text, text, None])
        figure.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line={"color": color, "width": width},
                text=hover,
                hovertemplate="%{text}<extra></extra>",
                name=name,
            )
        )

    for area, area_rows in gantt[~gantt["selected"]].groupby("primary area", sort=False):
        label, color = YARD_AREA_STYLES.get(area, (str(area), "#7D8EA3"))
        add_schedule_trace(area_rows, label, color, 5)

    selected_rows = gantt[gantt["selected"]]
    if not selected_rows.empty:
        add_schedule_trace(selected_rows, "조회 Block", "#D18F00", 10)

    # Result Table의 실제 계획일정 범위로 월 눈금을 만든다.
    schedule_start = gantt["planned start time"].min()
    schedule_finish = gantt["planned finish time"].max()
    axis_start = schedule_start.to_period("M").to_timestamp()
    axis_finish = (schedule_finish.to_period("M") + 1).to_timestamp()
    month_starts = pd.date_range(axis_start, axis_finish, freq="MS", inclusive="left")
    month_ticks = month_starts + pd.offsets.Day(14)

    figure.update_layout(
        height=max(360, min(820, len(position_order) * 12 + 150)),
        template="plotly_white",
        margin={"l": 55, "r": 20, "t": 66, "b": 20},
        showlegend=False,
        xaxis={
            "title": None,
            "type": "date",
            "side": "top",
            "range": [axis_start, axis_finish],
            "tickmode": "array",
            "tickvals": month_ticks,
            "ticktext": [f"{month:02d}" for month in month_starts.month],
            "tickangle": 0,
            "tickfont": {"size": 9, "color": "#667085"},
            "gridcolor": "#E7EBF2",
        },
        yaxis={
            "title": None,
            "categoryorder": "array",
            "categoryarray": position_order[::-1],
            "tickfont": {"size": 9},
        },
        font={"family": "Malgun Gothic", "color": "#263244"},
    )

    # 실제 일정 범위의 첫 달과 매년 1월 위에 연도를 한 번씩 표시한다.
    year_starts = [month_starts[0]]
    year_starts.extend(month_starts[month_starts.month == 1].tolist())
    for year_start in pd.DatetimeIndex(year_starts).drop_duplicates():
        figure.add_annotation(
            x=year_start + pd.offsets.Day(14),
            y=1.045,
            xref="x",
            yref="paper",
            text=f"<b>{year_start.year}</b>",
            showarrow=False,
            font={"size": 11, "color": "#425B76"},
        )
    return figure


@st.cache_resource(show_spinner=False)
def load_notebook_sections(notebook_path, split_subsections=False):
    notebook = json.loads(Path(notebook_path).read_text(encoding="utf-8"))
    markdown = "\n\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )
    lines = markdown.splitlines()
    sections = {}
    current_title = None
    current_lines = []

    for line in lines:
        if line.startswith("## "):
            if current_title:
                sections[current_title] = "\n".join(current_lines).strip()
            current_title = line[3:].strip()
            current_lines = [line]
        elif current_title:
            if line.lstrip().startswith("!["):
                continue
            if "노트북 열기" in line and ".ipynb" in line:
                continue
            current_lines.append(line)

    if current_title:
        sections[current_title] = "\n".join(current_lines).strip()

    if not split_subsections:
        return sections

    presentation_sections = {}
    for title, section_markdown in sections.items():
        section_lines = section_markdown.splitlines()
        current_title = title
        current_lines = []
        for line in section_lines[1:]:
            if line.startswith("### "):
                current_markdown = "\n".join(current_lines).strip()
                if current_markdown:
                    presentation_sections[current_title] = current_markdown
                current_title = line[4:].strip()
                current_lines = [line]
            else:
                current_lines.append(line)
        current_markdown = "\n".join(current_lines).strip()
        if current_markdown:
            presentation_sections[current_title] = current_markdown
    return presentation_sections


def display_label_without_numbers(label):
    """Keep internal navigation keys intact while hiding their leading section numbers."""
    cleaned_label = re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", str(label)).strip()
    return {
        "Overview": "개요",
        "Master Table": "테이블 조인",
        "참고자료 및 데이터셋": "데이터셋 선정",
        "개인 경험에서 출발한 문제의식": "주제 선정 배경",
        "Set A — Block 특성만 사용": "Set A 최종 후보모델 선정",
        "Feature Set 비교 결과": "Feature Set 비교 결과 (CDA)",
        "최종 변수 세트의 모델 재비교": "최종 Cycle 회귀모델 선정",
    }.get(cleaned_label, cleaned_label)


def strip_section_numbers(markdown):
    """Hide decimal section numbers from Markdown headings shown in the dashboard."""
    return re.sub(
        r"^(#{1,6}\s+)\d+(?:\.\d+)*\.?\s+",
        r"\1",
        markdown,
        flags=re.MULTILINE,
    )


def render_centered_problem_statement(markdown, layout):
    heading, _, body = markdown.partition("\n")
    title = display_label_without_numbers(heading.lstrip("# "))

    def emphasize_problem_statement(text):
        highlighted_text = html.escape(text.strip())
        highlighted_text = highlighted_text.replace("아니라, ", "아니라,<br>")
        highlighted_text = highlighted_text.replace("생각했다. ", "생각했다.<br>")
        highlighted_text = highlighted_text.replace("경험했다. ", "경험했다.<br>")
        highlighted_text = highlighted_text.replace("부족했지만, ", "부족했지만,<br>")
        for phrase in layout["highlight_phrases"]:
            if not phrase.strip():
                continue
            escaped_phrase = html.escape(phrase)
            highlighted_text = highlighted_text.replace(
                escaped_phrase,
                f'<span style="padding:.08em .24em;border-radius:.28em;background:#DCEBFA;color:#034EA2;font-weight:800;box-decoration-break:clone;-webkit-box-decoration-break:clone;">{escaped_phrase}</span>',
            )
        if title == "주제 선정 배경":
            highlighted_text = f"&ldquo;{highlighted_text}&rdquo;"
        return highlighted_text

    body_paragraphs = [paragraph for paragraph in body.split("\n\n") if paragraph.strip()]
    if title == "주제 선정 배경":
        body_paragraphs = body_paragraphs[:1]
    paragraphs = "".join(
        f"<p>{emphasize_problem_statement(paragraph)}</p>"
        for paragraph in body_paragraphs
    )
    st.markdown(
        f"""
        <style>
            .problem-statement-static .problem-statement-title {{
                font-size:40px !important;
            }}
            .problem-statement-static .problem-statement-body,
            .problem-statement-static .problem-statement-body p {{
                font-size:24px !important;
                line-height:1.55 !important;
            }}
        </style>
        <div class="problem-statement-static" style="width:100%;max-width:840px;margin:0 auto;min-height:500px;display:flex;align-items:center;text-align:center;color:#102A43;">
            <div style="width:100%;padding:1.75rem .5rem;">
                <div class="problem-statement-title" style="margin-bottom:2.35rem;font-weight:800;letter-spacing:-.04em;">{html.escape(title)}</div>
                <div class="problem-statement-body" style="color:#344054;letter-spacing:-.025em;">{paragraphs}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_centered_visual_slide(markdown, image_path, layout):
    """Center a short explanation and its visual within the fixed 16:9 canvas."""
    st.markdown(
        f"""
        <style>
        [data-testid="stMainBlockContainer"] h3 {{ font-size:{layout['title_font']}px !important; }}
        [data-testid="stMainBlockContainer"] p,
        [data-testid="stMainBlockContainer"] li {{ font-size:{layout['body_font']}px !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    _, center_column, _ = st.columns(
        centered_column_ratios(layout["center_x"], layout["content_width"])
    )
    with center_column:
        st.markdown(
            f'<div style="height:{layout["top_space"]}px;"></div>',
            unsafe_allow_html=True,
        )
        st.markdown(strip_section_numbers(markdown))
        st.image(image_path, width="stretch")


def render_selected_idea_slide(markdown, image_path, layout):
    """Show the selected smart-scheduling idea with a clear outline."""
    image_data = base64.b64encode(image_path.read_bytes()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stMainBlockContainer"] h3 {{ font-size:{layout['title_font']}px !important; }}
        [data-testid="stMainBlockContainer"] p,
        [data-testid="stMainBlockContainer"] li {{ font-size:{layout['body_font']}px !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    _, center_column, _ = st.columns(
        centered_column_ratios(layout["center_x"], layout["content_width"])
    )
    with center_column:
        st.markdown(
            f'<div style="height:{layout["top_space"]}px;"></div>',
            unsafe_allow_html=True,
        )
        st.markdown(strip_section_numbers(markdown))
        st.markdown(
            f'''<div style="position:relative;width:100%;margin-top:1rem;">
                <img src="data:image/png;base64,{image_data}" style="display:block;width:100%;border-radius:8px;">
                <div style="position:absolute;left:66.8%;top:7.6%;width:32.7%;height:84.3%;
                            border:4px solid #0067C7;border-radius:10px;box-sizing:border-box;
                            background:rgba(0,103,199,.035);box-shadow:0 0 0 4px rgba(0,103,199,.14), inset 0 0 0 1px rgba(255,255,255,.75);
                            pointer-events:none;"></div>
            </div>''',
            unsafe_allow_html=True,
        )


def build_yard_coordinates(detail):
    catalog = (
        detail[["position_id", "position_description", "position_primary_area"]]
        .drop_duplicates("position_id")
        .sort_values(["position_primary_area", "position_id"])
    )
    area_order = [area for area in YARD_AREA_STYLES if area in set(catalog["position_primary_area"])]
    area_order += sorted(set(catalog["position_primary_area"]) - set(area_order))

    records = []
    x_offset = 0
    for area in area_order:
        positions = catalog[catalog["position_primary_area"].eq(area)].reset_index(drop=True)
        columns = max(2, math.ceil(math.sqrt(len(positions) * 1.4)))
        for index, row in positions.iterrows():
            records.append(
                {
                    **row.to_dict(),
                    "yard_x": x_offset + index % columns,
                    "yard_y": index // columns,
                }
            )
        x_offset += columns + 0.3

    coordinates = pd.DataFrame(records)
    assert coordinates["position_id"].is_unique
    return coordinates


def prepare_yard_schedule(detail, method, block_limit=36):
    schedule = detail[detail["method"].eq(method)].copy()
    schedule["planned_start_time"] = pd.to_datetime(schedule["planned_start_time"], errors="coerce")
    schedule["planned_finish_time"] = pd.to_datetime(schedule["planned_finish_time"], errors="coerce")
    schedule = (
        schedule.dropna(subset=["planned_start_time", "planned_finish_time"])
        .sort_values(["planned_start_time", "block_index"])
        .head(block_limit)
    )
    schedule = schedule.merge(build_yard_coordinates(detail), on="position_id", suffixes=("", "_yard"))
    base_date = schedule["planned_start_time"].min()
    schedule["z_start"] = (schedule["planned_start_time"] - base_date).dt.days
    schedule["z_finish"] = (schedule["planned_finish_time"] - base_date).dt.days
    schedule["duration_days"] = (schedule["z_finish"] - schedule["z_start"]).clip(lower=1)
    assert schedule[["yard_x", "yard_y", "z_start", "z_finish"]].notna().all().all()
    return schedule, base_date


def cuboid_trace(row, color, area_label, show_legend):
    half_width = 0.28
    x0, x1 = row["yard_x"] - half_width, row["yard_x"] + half_width
    y0, y1 = row["yard_y"] - half_width, row["yard_y"] + half_width
    z0, z1 = row["z_start"], row["z_finish"]
    x = [x0, x1, x1, x0, x0, x1, x1, x0]
    y = [y0, y0, y1, y1, y0, y0, y1, y1]
    z = [z0, z0, z0, z0, z1, z1, z1, z1]
    i = [0, 0, 4, 4, 0, 1, 2, 3, 0, 1, 2, 3]
    j = [1, 2, 5, 6, 1, 2, 3, 0, 4, 5, 6, 7]
    k = [2, 3, 6, 7, 5, 6, 7, 4, 5, 6, 7, 4]
    hover = (
        f"<b>Block {int(row['block_index'])}</b><br>"
        f"Position: {row['position_id']}<br>"
        f"{row['position_description']}<br>"
        f"계획: {row['planned_start_time']:%Y-%m-%d} → {row['planned_finish_time']:%Y-%m-%d}<br>"
        f"기간: {int(row['duration_days'])}일 · Delay: {int(row['delay_days'])}일"
    )
    return go.Mesh3d(
        x=x,
        y=y,
        z=z,
        i=i,
        j=j,
        k=k,
        color=color,
        opacity=0.88,
        flatshading=True,
        name=area_label,
        legendgroup=row["position_primary_area"],
        showlegend=show_legend,
        text=[hover] * 8,
        hovertemplate="%{text}<extra></extra>",
    )


def yard_outline_polygon(coordinates):
    x0, x1 = coordinates["yard_x"].min() - 1.25, coordinates["yard_x"].max() + 1.25
    y0, y1 = coordinates["yard_y"].min() - 1.00, coordinates["yard_y"].max() + 1.00
    return [
        (x0 + 0.80, y0),
        (x1 - 1.35, y0),
        (x1 + 0.20, y0 + 0.65),
        (x1, y1 - 0.70),
        (x1 - 1.20, y1 + 0.25),
        (x0 + 0.80, y1 + 0.25),
        (x0 - 0.25, y1 - 0.55),
        (x0, y0 + 0.60),
    ]


def yard_area_polygon(positions, yard_y0, yard_y1):
    x0, x1 = positions["yard_x"].min() - 0.65, positions["yard_x"].max() + 0.65
    return [
        (x0 + 0.22, yard_y0),
        (x1 - 0.22, yard_y0),
        (x1, yard_y0 + 0.25),
        (x1 - 0.10, yard_y1 - 0.22),
        (x1 - 0.32, yard_y1),
        (x0 + 0.30, yard_y1),
        (x0, yard_y1 - 0.24),
        (x0, yard_y0 + 0.24),
    ]


def build_yard_figure(detail, method, block_limit=36):
    schedule, base_date = prepare_yard_schedule(detail, method, block_limit)
    coordinates = build_yard_coordinates(detail)
    figure = go.Figure()

    outline = yard_outline_polygon(coordinates)
    figure.add_trace(
        go.Mesh3d(
            x=[point[0] for point in outline],
            y=[point[1] for point in outline],
            z=[-0.22] * len(outline),
            i=[0] * (len(outline) - 2),
            j=list(range(1, len(outline) - 1)),
            k=list(range(2, len(outline))),
            color="#263244",
            opacity=0.95,
            hoverinfo="skip",
            showlegend=False,
        )
    )

    yard_y0 = coordinates["yard_y"].min() - 0.55
    yard_y1 = coordinates["yard_y"].max() + 0.55

    for area, positions in coordinates.groupby("position_primary_area", sort=False):
        area_label, color = YARD_AREA_STYLES.get(area, (area, "#7D8EA3"))
        polygon = yard_area_polygon(positions, yard_y0, yard_y1)
        figure.add_trace(
            go.Mesh3d(
                x=[point[0] for point in polygon],
                y=[point[1] for point in polygon],
                z=[0] * len(polygon),
                i=[0] * (len(polygon) - 2),
                j=list(range(1, len(polygon) - 1)),
                k=list(range(2, len(polygon))),
                color=color,
                opacity=0.18,
                hoverinfo="skip",
                showlegend=False,
            )
        )
        figure.add_trace(
            go.Scatter3d(
                x=[*[point[0] for point in polygon], polygon[0][0], None, positions["yard_x"].mean()],
                y=[*[point[1] for point in polygon], polygon[0][1], None, yard_y0 + 0.18],
                z=[*[0.02] * (len(polygon) + 1), None, 0.04],
                mode="lines+text",
                line={"color": color, "width": 3},
                text=[*[""] * (len(polygon) + 2), f"<b>{area_label}</b>"],
                textfont={"color": color, "size": 14},
                hoverinfo="skip",
                showlegend=False,
            )
        )

    figure.add_trace(
        go.Scatter3d(
            x=coordinates["yard_x"],
            y=coordinates["yard_y"],
            z=[0] * len(coordinates),
            mode="markers",
            marker={"size": 3, "color": "#788697", "opacity": 0.70},
            text=coordinates.apply(
                lambda row: f"{row['position_id']}<br>{row['position_description']}", axis=1
            ),
            hovertemplate="%{text}<extra>Position</extra>",
            name="Position",
            showlegend=False,
        )
    )

    stem_x, stem_y, stem_z = [], [], []
    for _, row in schedule.iterrows():
        stem_x.extend([row["yard_x"], row["yard_x"], None])
        stem_y.extend([row["yard_y"], row["yard_y"], None])
        stem_z.extend([0, row["z_start"], None])
    figure.add_trace(
        go.Scatter3d(
            x=stem_x,
            y=stem_y,
            z=stem_z,
            mode="lines",
            line={"color": "rgba(73, 87, 105, 0.35)", "width": 2},
            hoverinfo="skip",
            showlegend=False,
        )
    )

    seen_areas = set()
    for _, row in schedule.iterrows():
        area = row["position_primary_area"]
        area_label, color = YARD_AREA_STYLES.get(area, (area, "#7D8EA3"))
        figure.add_trace(cuboid_trace(row, color, area_label, area not in seen_areas))
        seen_areas.add(area)

    max_z = max(int(schedule["z_finish"].max()), 1)
    tick_values = [max_z * index / 5 for index in range(6)]
    tick_labels = [
        (base_date + pd.to_timedelta(int(value), unit="D")).strftime("%Y-%m")
        for value in tick_values
    ]
    figure.update_layout(
        height=620,
        margin={"l": 55, "r": 45, "t": 20, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Malgun Gothic", "size": 12, "color": "#263244"},
        legend={
            "orientation": "h",
            "y": 1.02,
            "x": 0,
            "font": {"size": 12},
            "groupclick": "togglegroup",
        },
        scene={
            "dragmode": False,
            "xaxis": {
                "title": "X (동쪽)",
                "showticklabels": False,
                "showbackground": False,
                "gridcolor": "#DDE4EC",
            },
            "yaxis": {
                "title": "Y (북쪽)",
                "showticklabels": False,
                "showbackground": False,
                "gridcolor": "#DDE4EC",
            },
            "zaxis": {
                "title": "Z (시간)",
                "tickvals": tick_values,
                "ticktext": tick_labels,
                "showbackground": False,
                "gridcolor": "#D7DEE7",
            },
            "camera": {
                "eye": {"x": -1.55, "y": -1.65, "z": 1.15},
                "projection": {"type": "orthographic"},
            },
            "aspectmode": "manual",
            "aspectratio": {"x": 2.2, "y": 1.0, "z": 1.25},
        },
    )
    return figure, schedule


def build_yard_top_view(detail, schedule):
    coordinates = build_yard_coordinates(detail)
    used_positions = set(schedule["position_id"])
    figure = go.Figure()

    outline = yard_outline_polygon(coordinates)
    figure.add_trace(
        go.Scatter(
            x=[*[point[0] for point in outline], outline[0][0]],
            y=[*[point[1] for point in outline], outline[0][1]],
            mode="lines",
            fill="toself",
            fillcolor="#E5E9EF",
            line={"color": "#263244", "width": 4},
            hoverinfo="skip",
            showlegend=False,
        )
    )

    yard_y0 = coordinates["yard_y"].min() - 0.55
    yard_y1 = coordinates["yard_y"].max() + 0.55

    for area, positions in coordinates.groupby("position_primary_area", sort=False):
        area_label, color = YARD_AREA_STYLES.get(area, (area, "#7D8EA3"))
        polygon = yard_area_polygon(positions, yard_y0, yard_y1)
        figure.add_trace(
            go.Scatter(
                x=[*[point[0] for point in polygon], polygon[0][0]],
                y=[*[point[1] for point in polygon], polygon[0][1]],
                mode="lines",
                fill="toself",
                fillcolor=YARD_AREA_FILLS.get(area, "rgba(125, 142, 163, 0.10)"),
                line={"color": color, "width": 1.5},
                hoverinfo="skip",
                showlegend=False,
            )
        )
        figure.add_annotation(
            x=positions["yard_x"].mean(),
            y=yard_y0 + 0.20,
            text=f"<b>{area_label}</b>",
            showarrow=False,
            font={"color": color, "size": 11},
        )
        figure.add_trace(
            go.Scatter(
                x=positions["yard_x"],
                y=positions["yard_y"],
                mode="markers",
                marker={
                    "symbol": "square",
                    "size": [15 if position in used_positions else 9 for position in positions["position_id"]],
                    "color": color,
                    "opacity": [0.95 if position in used_positions else 0.20 for position in positions["position_id"]],
                    "line": {"color": color, "width": 1},
                },
                text=positions.apply(
                    lambda row: (
                        f"{row['position_id']}<br>{row['position_description']}<br>"
                        f"{'선택됨' if row['position_id'] in used_positions else '미사용'}"
                    ),
                    axis=1,
                ),
                hovertemplate="%{text}<extra></extra>",
                name=area_label,
                showlegend=False,
            )
        )

    figure.update_layout(
        height=315,
        margin={"l": 10, "r": 10, "t": 25, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"visible": False, "fixedrange": True},
        yaxis={"visible": False, "fixedrange": True, "scaleanchor": "x", "scaleratio": 1},
        font={"family": "Malgun Gothic", "color": "#263244"},
    )
    return figure


def build_yard_gantt(schedule, area):
    area_schedule = (
        schedule[schedule["position_primary_area"].eq(area)]
        .sort_values(["planned_start_time", "block_index"])
        .head(12)
        .copy()
    )
    base_date = schedule["planned_start_time"].min()
    area_label, color = YARD_AREA_STYLES.get(area, (area, "#7D8EA3"))
    area_schedule["start_day"] = (area_schedule["planned_start_time"] - base_date).dt.days
    area_schedule["label"] = area_schedule.apply(
        lambda row: f"Block {int(row['block_index'])} · {row['position_id']}", axis=1
    )
    figure = go.Figure(
        go.Bar(
            x=area_schedule["duration_days"],
            y=area_schedule["label"],
            base=area_schedule["start_day"],
            orientation="h",
            marker={"color": color},
            text=area_schedule["duration_days"].map(lambda value: f"{int(value)}일"),
            textposition="inside",
            customdata=area_schedule[["planned_start_time", "planned_finish_time", "delay_days"]],
            hovertemplate=(
                "%{y}<br>%{customdata[0]|%Y-%m-%d} → %{customdata[1]|%Y-%m-%d}"
                "<br>기간 %{x}일 · Delay %{customdata[2]}일<extra></extra>"
            ),
            name=area_label,
        )
    )
    max_day = max(int(schedule["z_finish"].max()), 1)
    tick_values = [max_day * index / 4 for index in range(5)]
    tick_labels = [
        (base_date + pd.to_timedelta(int(value), unit="D")).strftime("%m/%d")
        for value in tick_values
    ]
    figure.update_layout(
        height=315,
        margin={"l": 10, "r": 10, "t": 15, "b": 35},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        bargap=0.35,
        showlegend=False,
        font={"family": "Malgun Gothic", "size": 11, "color": "#263244"},
        xaxis={
            "title": "계획 일자",
            "tickvals": tick_values,
            "ticktext": tick_labels,
            "gridcolor": "#E4E9EF",
            "fixedrange": True,
        },
        yaxis={"autorange": "reversed", "fixedrange": True},
    )
    return figure, area_schedule


def render_scheduling_presentation_page(subpage, data):
    """발표용 스케줄링 비교: 구조·조회·배정·운영 성과·결론의 5개 메시지로 재구성한다."""
    if subpage == SCHEDULING_RESULT_STRUCTURE_SUBPAGE:
        st.markdown("<div class='section-kicker'>SCHEDULING RESULT</div>", unsafe_allow_html=True)
        st.title("Result Table 구조")
        st.caption("각 방법은 동일한 Block 입력을 사용하지만, 선택 Position과 계획 일정·Delay를 서로 다르게 생성합니다.")
        structure = pd.DataFrame(
            [[method, 872, 60, "선택 Position · Planned Start/Finish · Delay"] for method in SCHEDULING_METHODS],
            columns=["Method", "Block Result", "사용 Position", "Result의 주요 정보"],
        )
        st.dataframe(structure, hide_index=True, width="stretch")
        analysis_note(
            "Result Table은 스케줄링 실행 이후 생성되는 결과층입니다. 따라서 이 페이지에서는 원본 Result의 구조를 확인하고, "
            "다음 페이지부터 방법별 Position 배정 차이를 비교합니다."
        )

    elif subpage == SCHEDULING_RESULT_VIEWER_SUBPAGE:
        render_scheduling_result_preview()

    elif subpage == SCHEDULING_POSITION_COMPARISON_SUBPAGE:
        st.markdown("<div class='section-kicker'>POSITION ASSIGNMENT</div>", unsafe_allow_html=True)
        st.title("Position 배정 비교")
        st.caption("동일한 Block도 선택 규칙에 따라 서로 다른 Position에 배정되는지 확인합니다.")
        render_precomputed_chart("scheduling_position_comparison.png")
        analysis_note(
            "대각선을 제외한 동일 Position 선택률은 대체로 약 10~13%로 낮고, 872개 중 849개 Block은 방법에 따라 Position이 달랐습니다. "
            "구역별 배정 비율도 방법마다 달라, Scheduling Method는 동일 입력에 대한 단순 계산 차이가 아니라 실제 공간 배치를 바꾸는 선택 규칙입니다."
        )

    elif subpage == SCHEDULING_PUBLISHER_METRICS_SUBPAGE:
        st.markdown("<div style='height:.15rem'></div>", unsafe_allow_html=True)
        _, publisher_table_column, _ = st.columns([.04, .92, .04])
        with publisher_table_column:
            st.image(
                ROOT / "Docs" / "images" / "publisher_algorithm_performance_existing_metrics.png",
                width="stretch",
            )
        st.caption("게시자가 제공한 기존 Scheduling 성과지표만 정리했습니다. Cycle Stability Score는 데이터 생성 시점을 혼동할 수 있어 이 표와 이후 비교에서 제외했습니다.")

    elif subpage == SCHEDULING_MAKESPAN_SUBPAGE:
        st.markdown("<div class='section-kicker'>OPERATING PERFORMANCE</div>", unsafe_allow_html=True)
        st.title("운영 성과 비교")
        st.caption("Position 선택 특성, 전체 일정 범위, 지연 성과를 같은 화면에서 비교합니다.")
        render_precomputed_chart("scheduling_operating_performance.png")
        analysis_note("면적 여유와 Initial 기록 Position 배정도 방법별로 달랐습니다. EDDQN은 가장 짧은 Makespan과 최저 Max Delay, Earliest Start는 최저 Total Delay와 Delayed Blocks를 보여, 운영 목적에 따라 우선 방법이 달라집니다.")

    else:
        st.markdown("<div class='section-kicker'>SCHEDULING CONCLUSION</div>", unsafe_allow_html=True)
        st.title("결론")
        st.markdown(
            "### 방법별 Position·일정·Delay 결과는 서로 다르며, 운영 목적에 따라 선택 기준도 달라집니다.\n\n"
            "- **Position 배정**: 동일 Block이라도 방법별 선택 Position과 구역별 배정 비율이 달랐습니다.\n"
            "- **전체 일정**: EDDQN은 가장 짧은 Makespan을 보였습니다.\n"
            "- **지연 성과**: Earliest Start는 누적지연과 지연 Block 수에서, EDDQN은 최악지연에서 강점을 보였습니다.\n\n"
            "따라서 7개 방법을 하나의 절대 순위로 정하기보다, Makespan·누적 지연·최악 지연 중 무엇을 우선할지에 따라 선택해야 합니다."
        )
        st.divider()
        st.subheader("운영 관점의 해석")
        st.markdown(
            "힘들게 테이블 조인했던 내용은 회귀분석에서는 쓰기 어렵다는 결론이 났지만, Scheduling과 엮으면 또 다른 해석을 할 수 있습니다.\n\n"
            "Delay 발생 일수나 건수에서는 EDDQN과 Earliest Start가 좋은 수치를 보여 생산관리자 입장에서는 좋은 지표로 볼 수 있습니다. "
            "하지만 작업자 입장에서 보면 이 방법들은 더 작은 Makespan을 가지고 있어, 그만큼 Block을 적치하거나 장비를 배치하고 작업을 조율하는 데는 불리할 수도 있습니다.\n\n"
            "그리고 현재 평가 지표에서 종합적으로 꼴등인 DDQN은 Scheduling, 즉 Position 배치 과정에서 Initial-recorded Position을 잘 활용하지 않았고, "
            "그래서 Delay가 많이 발생한 게 아닐까라는 가설도 세워볼 수 있습니다."
        )


def render_roadmap_presentation_page(subpage):
    if subpage == ROADMAP_OVERVIEW_SUBPAGE:
        st.markdown("<div class='section-kicker'>DEVELOPMENT ROADMAP</div>", unsafe_allow_html=True)
        st.title("개발 로드맵")
        st.caption("현재 분석 결과를 현장에서 탐색하고, 실제 실적을 반영하는 운영 지원 도구로 확장하는 단계입니다.")
        roadmap = pd.DataFrame(
            [
                [1, "완료", "Set A Cycle 예측과 7개 Result 비교 구조 확립"],
                [2, "구현 중", "7개 Scheduling Result 공간·시간 Viewer"],
                [3, "중기", "지역위험·이상배정·Position 혼잡 Analyzer"],
                [4, "장기", "실제 실적을 반영한 Cycle 재예측과 Dynamic Rescheduling"],
                [5, "구현 중", "Calendar-it을 통한 개인·팀 업무일정 연결"],
                [6, "장기", "ERP 관점의 자원·자재·원가 연결"],
                [7, "최종 확장", "MES 실적과 재예측·재스케줄링 순환구조"],
            ],
            columns=["Phase", "상태", "핵심 목표"],
        )
        st.dataframe(roadmap, hide_index=True, width="stretch")
        st.divider()
        st.subheader("향후 확장 방향")
        st.markdown(
            "**사전 Cycle 예측 → Scheduling → 실적 수집 → 잔여기간 재예측 → Rescheduling**\n\n"
            "실적 착수·완료, Man-hour, 비용과 자원정보가 확보되면 위 순환 구조를 검증할 수 있습니다. "
            "예측값과 실제 공정 진행의 차이를 지속적으로 반영하여, 일정 위험을 조기에 진단하고 재계획 후보를 제시하는 운영 지원 구조로 발전시키는 것이 최종 목표입니다."
        )
        analysis_note("실제 야드 좌표와 현장 실적이 없는 현재 단계에서 바로 가능한 다음 개발은, 기존 7개 Result를 직관적으로 탐색하는 Viewer MVP입니다.")
        return

    if subpage == ROADMAP_VIEWER_SUBPAGE:
        st.markdown("<div style='height:.15rem'></div>", unsafe_allow_html=True)
        st.title("3D Scheduling Result Viewer")
        st.caption("7개 Scheduling Method의 Position·계획일정·Delay 결과를 공간과 시간 관점에서 탐색하기 위한 UI 목업입니다.")
        roadmap_mockups = {
            "전체 야드 스케줄링 구성": "d2d9193e-3fe5-4cb9-917f-54086e6711c7.png",
            "방법 선택과 구역별 상세 활용": "fac1f1d7-707f-4161-8878-6a860b1f0eab.png",
        }
        selected_roadmap_mockup = st.radio(
            "목업 화면 선택",
            list(roadmap_mockups),
            horizontal=True,
            key="roadmap_mockup_screen",
        )
        _, roadmap_image_column, _ = st.columns([0.1, 0.8, 0.1])
        with roadmap_image_column:
            st.image(
                ROOT / "Docs" / "images" / roadmap_mockups[selected_roadmap_mockup],
                caption=selected_roadmap_mockup,
                width="stretch",
            )
        st.markdown(
            "- 7개 Scheduling Method 선택\n"
            "- Block–Position 배치 및 시간 시점·기간 조회\n"
            "- 선택 Block의 Cycle·Delay·Position 정보 확인"
        )
        analysis_note("공개 데이터에는 실제 야드 3D 좌표가 없으므로 위 이미지는 분석 결과가 아닌, 향후 Viewer의 화면 구성과 활용 방식을 설명하는 목업입니다.")
        return

    st.markdown("<div class='section-kicker'>CALENDAR-IT INTEGRATION</div>", unsafe_allow_html=True)
    st.title("Calendar-it과 연계")
    st.caption("Block 단위의 Cycle 예측과 Scheduling 결과를 개인·팀 단위의 실행 일정으로 연결하는 확장 방향입니다.")
    calendar_view = st.segmented_control(
        "Calendar-it 화면 선택",
        ["간트형 전체 일정", "주간 작업 일정"],
        default="간트형 전체 일정",
        selection_mode="single",
        key="calendar_it_view",
        label_visibility="collapsed",
    ) or "간트형 전체 일정"
    _, calendar_image_column, _ = st.columns([.04, .92, .04])
    with calendar_image_column:
        if calendar_view == "간트형 전체 일정":
            st.image(ROOT / "Docs" / "images" / "gt.png", caption="간트형 전체 일정 화면", width="stretch")
        else:
            st.image(ROOT / "Docs" / "images" / "wk.png", caption="주간 작업 일정 화면", width="stretch")
    if calendar_view == "간트형 전체 일정":
        st.markdown("**전체 일정 관점** — 공정·Block·담당 조직의 기간을 한 화면에서 확인하고, Scheduling 결과의 계획 Start/Finish를 상위 일정에 반영합니다.")
    else:
        st.markdown("**실행 일정 관점** — 확정된 Block 작업을 주간 단위의 담당자·팀 업무로 전개하고, 현장 변경 사항을 다시 일정 계획에 반영합니다.")
    st.markdown(
        "#### 연계 흐름\n"
        "Cycle 예측으로 기준 작업기간을 제시하고 → Scheduling이 Position·계획일정·Delay 후보를 계산한 뒤 → "
        "Calendar-it에서 팀별 실행 일정과 협업 작업으로 연결합니다. 이후 실제 착수·완료 정보가 확보되면 재예측·재스케줄링의 입력으로 활용할 수 있습니다."
    )
    st.markdown("Calendar-it 홈페이지: [https://dungji.cloud/](https://dungji.cloud/)")
    analysis_note("현재 이미지는 Calendar-it Pro의 일정 화면 예시이며, 본 프로젝트에서는 Scheduling 결과를 운영·협업 일정으로 확장하는 활용 방향을 제안합니다.")


def render_section_companion(page, subpage, data):
    if page == "0. Overview":
        if subpage.startswith("0.1"):
            analysis_note(
                "현장 적용 가능성과 실무 경험의 연결을 함께 만족하는 주제로 공정 작업기간 예측을 선택했습니다. "
                "개인 경험은 문제의 출발점이며, 실제 분석 질문은 공개 데이터로 검증 가능한 범위로 제한했습니다.",
                "주제 선정 결론",
            )
        elif subpage.startswith("0.2"):
            dataset_review = pd.DataFrame(
                [
                    ["건축 공기 데이터", "자료가 많고 회귀분석 가능", "조선업과의 직접 관련성이 낮음", "초기 후보"],
                    ["Ship-Construction Resource Leveling", "조선 프로젝트 일정 데이터", "인코딩·컬럼 정의 부재", "제외"],
                    ["Ship Block Scheduling in English", "Raw Table·컬럼 정의·7개 Result 제공", "실적 Cycle·실제 좌표 부재", "최종 선택"],
                ],
                columns=["후보", "장점", "제약", "판단"],
            )
            st.dataframe(dataset_review, hide_index=True, width="stretch")
            analysis_note(
                "최종 데이터셋은 Block·Position·Initial 원본과 7개 Scheduling Result를 함께 제공해 "
                "예측과 일정 결과 비교를 한 흐름에서 수행할 수 있다는 점에서 선택했습니다."
            )
        elif subpage.startswith("0.3"):
            flow_cards(
                [
                    ("사전 입력", "Block·Position 후보·Initial·기준 Cycle"),
                    ("Scheduling", "7개 방법이 Position과 계획시점을 결정"),
                    ("Result", "선택 Position·Planned Schedule·Delay 생성"),
                ]
            )
            analysis_note(
                "Cycle은 Result보다 먼저 존재하고 선택 Position은 Result에서 생성됩니다. "
                "따라서 최종 Cycle 예측은 Block 고유 특성으로 수행하고, Position은 사후 결과 비교에 사용합니다.",
                "데이터 생성 순서가 바꾼 분석 구조",
            )
        elif subpage.startswith("0.4"):
            goals = pd.DataFrame(
                [
                    ["예측", "Block 고유 특성으로 사전 Cycle 예측", "RMSE·MAE·R²"],
                    ["진단", "Set B/C 결과층 변수 추가 효과 확인", "Set A/B/C 성능 차이"],
                    ["비교", "7개 방법의 Position·시간·Delay 비교", "Makespan·Delay·배정 특성"],
                    ["확장", "실적 기반 재예측·재스케줄링 구조 제안", "개발 로드맵"],
                ],
                columns=["구분", "질문", "확인 지표"],
            )
            st.dataframe(goals, hide_index=True, width="stretch")
            analysis_note("예측모델 성능과 Scheduling 성과를 같은 점수로 합치지 않고 서로 다른 평가축으로 분리했습니다.")
        else:
            flow_cards(
                [
                    ("Master Table", "연결키와 데이터 생성 순서 검증"),
                    ("전처리·EDA", "결측·이상치·변수 세트 정의"),
                    ("회귀모델", "Set A 최종모델 구축"),
                    ("Result 비교", "Position·Makespan·Delay 비교"),
                ]
            )
            analysis_note("각 단계의 출력이 다음 단계의 입력이 되며, 최종 결론 뒤에는 동적 일정 시스템으로의 확장 방향을 제시합니다.")
        return

    if page == "1. Master Table":
        if subpage.startswith("1.1"):
            source_summary = pd.DataFrame(
                [
                    ["Block", 872, "Block 특성·기준 Cycle"],
                    ["Position", 66, "공간·인양·작업조 조건"],
                    ["Initial", 35, "시작 시점 Position 기록"],
                    ["각 Scheduling Result", 872, "선택 Position·계획일정·Delay"],
                ],
                columns=["원본", "행 수", "분석 역할"],
            )
            st.dataframe(source_summary, hide_index=True, width="stretch")
            analysis_note(
                "Block과 Position에는 배정 관계가 없으므로 Result가 중간 연결표가 됩니다. "
                "Cycle은 Block Table에, 선택 Position과 일정은 Result에 있다는 점이 핵심입니다."
            )
        elif subpage.startswith("1.2"):
            relations = pd.DataFrame(
                [
                    ["Block", "Result", "index ↔ block sequence no.", "1:1", "키 집합·block no. 일치"],
                    ["Result", "Position", "block position id", "N:1", "설명 일치율 100%"],
                    ["Position", "Initial", "block position description", "0..1", "Position 수준 간접 연결"],
                ],
                columns=["From", "To", "연결키", "관계", "검증"],
            )
            st.dataframe(relations, hide_index=True, width="stretch")
            analysis_note("Join의 정확성은 확인했지만, Join된 변수가 예측 시점에 사용 가능한지는 별도로 판단해야 합니다.")
        elif subpage.startswith("1.3"):
            analysis_note(
                "DDQN 결합표는 탐색과 Result 비교를 위한 표입니다. 선택 Position은 DDQN 실행 뒤 생긴 결과이므로 "
                "최종 Cycle 예측의 독립변수로 사용하지 않습니다.",
                "ERD 해석",
            )
        else:
            st.dataframe(data["master"].head(12), hide_index=True, width="stretch")
            analysis_note(
                "Master Table은 Block 한 행에 DDQN Result·Position·Initial 상태를 붙였습니다. "
                "분석용 저장은 가능하지만, 결과층 컬럼과 사전 입력 컬럼을 구분해 사용합니다."
            )
        return

    if page == "2. 전처리 및 EDA":
        analysis = data["analysis"]
        if subpage.startswith("2.1"):
            quality = pd.DataFrame(
                [
                    ["분석 행", f"{len(analysis):,}개", "DDQN 기준 Block 단위"],
                    ["Target 결측", f"{analysis['block_processing_cycle'].isna().sum()}개", "추가 처리 없음"],
                    ["position_block_type 결측", "unrestricted", "구조적 결측을 별도 범주화"],
                    ["IQR 이상치", "유지", "오류보다 실제 대형·장기 작업 가능성"],
                ],
                columns=["점검 항목", "처리", "판단 근거"],
            )
            st.dataframe(quality, hide_index=True, width="stretch")
            analysis_note("결측과 이상치를 일괄 삭제·대체하지 않고 변수 의미와 데이터 생성 구조를 기준으로 처리했습니다.")
        else:
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            sns.histplot(analysis["block_processing_cycle"], kde=True, color="#034EA2", ax=axes[0])
            axes[0].set_title("Block Position Cycle Distribution")
            sns.boxplot(x=analysis["block_processing_cycle"], color="#B8D0EA", ax=axes[1])
            axes[1].set_title("Block Position Cycle Boxplot")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            analysis_note(
                "대부분 15~40일에 집중된 우측 편향 분포이며 50일 이상 장기 Cycle도 연속적으로 존재합니다. "
                "명백한 입력 오류로 보기 어려워 제거하지 않고, 장기 구간의 예측오차를 모델링에서 확인합니다."
            )
        return

    if page == "3. 회귀모델":
        if subpage.startswith(("3.1", "3.2")):
            conditions = pd.DataFrame(
                [["분할", "Train 80% / Test 20% (학습 697개 / 테스트 175개)"], ["random_state", "42"], ["평가지표", "MAE·RMSE·R²"], ["전처리", "수치형 scaling·범주형 one-hot"]],
                columns=["조건", "설정"],
            )
            st.dataframe(conditions, hide_index=True, width="stretch")
            analysis_note("모든 후보모델과 변수 세트에 같은 분할·평가 조건을 적용해 성능 차이가 입력과 모델에서 오도록 통제했습니다.")
            st.markdown("#### 모델링 환경·분석 데이터 불러오기")
            with st.container(height=430, border=False):
                st.code(MODELING_SETUP_CODE_PATH.read_text(encoding="utf-8"), language="python")
        elif subpage.startswith("3.3.1"):
            baseline = data["baseline"].sort_values("RMSE")
            st.dataframe(baseline, hide_index=True, width="stretch")
            best = baseline.iloc[0]
            analysis_note(f"Set A 기준모델 중 {best['Model']}가 RMSE {best['RMSE']:.3f}, R² {best['R2']:.3f}로 가장 우수해 대표모델로 선정했습니다.")
            selection_col, exclusion_col = st.columns(2, gap="large")
            with selection_col:
                st.markdown("#### 선정 이유")
                st.markdown(
                    "- **Linear Regression** → 기본 선형 기준 모델로 변수와 Cycle의 관계 확인  \n"
                    "- **Ridge** → 다중공선성이 있는 경우 L2 규제를 통한 안정성 확인  \n"
                    "- **Decision Tree** → 선형모델이 설명하지 못하는 비선형 관계 확인  \n"
                    "- **Random Forest** → 여러 Tree를 결합해 안정적인 비선형 예측 성능 확인"
                )
            with exclusion_col:
                st.markdown("#### 제외 사유")
                st.markdown(
                    "- **Lasso / Elastic Net** → 규제모델 비교 자체가 목적이 아니므로 대표 모델인 Ridge만 사용  \n"
                    "- **Gradient Boosting** → 모델 종류를 과도하게 늘리지 않고 Feature Set 및 스케줄링 방식 비교에 집중하기 위해 제외"
                )
            st.markdown("#### Train/Test 분리·모델 비교 코드")
            with st.container(height=380, border=False):
                st.code(REGRESSION_COMPARISON_CODE_PATH.read_text(encoding="utf-8"), language="python")
        elif subpage.startswith("3.3.2"):
            candidates = data["models"].sort_values("RMSE")
            st.dataframe(candidates, hide_index=True, width="stretch")
            best = candidates.iloc[0]
            analysis_note(f"최종 후보 중 {best['Model']}가 RMSE {best['RMSE']:.3f}로 가장 낮았습니다. 비선형 모델이 Block 특성과 Cycle의 관계를 더 잘 설명했습니다.")
        elif subpage.startswith("3.4.1"):
            feature_sets = data["feature_sets"].sort_values("RMSE")
            st.markdown("**CDA · 가설 검증** · Position·Initial 정보 추가가 **RMSE**를 낮추는지 동일 조건에서 Set A/B/C로 비교")
            st.markdown('<div style="height:1.15rem;"></div>', unsafe_allow_html=True)
            _, chart_column, _ = st.columns([.12, .6, .28])
            with chart_column:
                render_precomputed_chart("regression_feature_set_rmse.png", width="content")
            st.markdown('<div style="height:.85rem;"></div>', unsafe_allow_html=True)
            st.dataframe(feature_sets, hide_index=True, width="stretch")
            analysis_note(
                "동일한 Random Forest에서 Set A가 가장 좋고 Set B/C는 오히려 낮았습니다. "
                "이 결과는 Position의 효과가 없다는 결론이 아니라, 선택 Position이 예측시점 이후의 Result라는 모델 설계 문제를 드러낸 진단입니다."
            )
            st.markdown(
                """
                <div style="margin:2.05rem auto 0;max-width:930px;padding:1rem 0;
                            border-top:1px solid #D9E2EC;border-bottom:1px solid #D9E2EC;text-align:center;
                            font-size:1.28rem;font-weight:750;line-height:1.45;color:#102A43;word-break:keep-all;">
                  <strong>Q. 정보(변수)를 더했는데,</strong>&nbsp;&nbsp;<strong>왜 성능은 오히려 낮아졌을까?</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif subpage.startswith("3.4.2"):
            # 데이터 생성 시점과 가정 수정은 본문에서 이미 한 번만 설명한다.
            pass
        elif subpage.startswith("3.4"):
            analysis_note("Feature Set 비교 결과를 바탕으로 예측시점 이후에 생성되는 Position·Initial 정보를 최종 입력에서 제외했습니다.")
        elif subpage.startswith("3.5"):
            model_comparison = data["models"].sort_values("RMSE")
            st.dataframe(
                model_comparison.style.set_properties(
                    subset=["RMSE"],
                    **{"background-color": "#EAF2FB", "color": "#034EA2", "font-weight": "700"},
                ),
                hide_index=True,
                width="stretch",
            )
            st.markdown("#### 튜닝 전후 Test 성능")
            tuning = pd.DataFrame(
                [["튜닝 전 후보", 4.489, 0.774], ["GridSearchCV 최종", 4.558, 0.767]],
                columns=["모델", "Test RMSE", "Test R²"],
            )
            st.dataframe(
                tuning.style.set_properties(
                    subset=["Test RMSE"],
                    **{"background-color": "#EAF2FB", "color": "#034EA2", "font-weight": "700"},
                ),
                hide_index=True,
                width="stretch",
            )
            analysis_note(
                "Set A를 최종 입력으로 확정한 뒤 Random Forest를 최종 후보로 유지했습니다. "
                "다만 GridSearchCV 후 별도 Test 성능은 소폭 낮아, 튜닝이 Test 향상을 자동 보장하지 않음을 함께 기록합니다."
            )
        elif subpage.startswith("3.6"):
            tuning = pd.DataFrame(
                [["튜닝 전 후보", 4.489, 0.774], ["GridSearchCV 최종", 4.558, 0.767]],
                columns=["모델", "Test RMSE", "Test R²"],
            )
            st.dataframe(tuning, hide_index=True, width="stretch")
            analysis_note("Train 기준으로 고른 튜닝 모델의 별도 Test 성능은 소폭 낮았습니다. 튜닝이 Test 향상을 자동 보장하지 않음을 함께 기록합니다.")
        elif subpage.startswith("3.7.1"):
            test = data["test"]
            metrics = data["modeling_summary"]["test_metrics"]
            compact_metrics(
                [
                    ("MAE", f"{metrics['MAE']:.3f}", "Lower is better"),
                    ("RMSE", f"{metrics['RMSE']:.3f}", "Lower is better"),
                    ("R²", f"{metrics['R2']:.3f}", "Higher is better"),
                ]
            )
            render_precomputed_chart("regression_prediction_result.png")
            analysis_note(
                "전체 중앙값 잔차는 -0.1일로 대부분의 Block에서는 예측 편향이 크지 않았습니다. "
                "그러나 기준 Cycle이 길어질수록 과소예측이 뚜렷해졌습니다. 특히 40일 이상인 "
                "14개 Block은 모두 과소예측되었으며, 평균적으로 기준 Cycle보다 약 9.8일 짧게 "
                "예측되었습니다. 이는 최종 Random Forest 모델이 중간 Cycle 구간의 일반적인 패턴은 "
                "비교적 잘 학습했지만, 표본이 적은 장기 Cycle 구간에서는 예측값이 전체 평균 방향으로 "
                "수축되는 경향이 있음을 보여줍니다."
            )
        elif subpage.startswith("3.7.2"):
            test = data["test"]
            long_cycle = test[test["reference_cycle"] >= 40]
            render_precomputed_chart("regression_residuals.png")
            analysis_note(
                f"전체 중앙값 잔차는 {test['residual'].median():.1f}일로 중앙 구간의 편향은 크지 않습니다. "
                f"반면 기준 Cycle이 40일 이상인 {len(long_cycle)}개 Block은 모두 과소예측되었고, "
                f"평균적으로 {long_cycle['residual'].mean():.1f}일 짧게 예측되었습니다. "
                "즉, 이 분석은 모델이 장기 Cycle 구간에서 일반적인 평균 패턴 쪽으로 예측값을 수축시키는 한계를 확인하는 단계입니다.",
                "잔차 분석 결과",
            )
        elif subpage.startswith("3.7.3"):
            top_n = st.slider("표시할 변수 수", 5, 20, 10, key="model_importance_top_n")
            with st.container(height=420, border=False):
                render_precomputed_chart(f"feature_importance_{top_n}.png")
        else:
            flow_cards([("최종 입력", "Set A · Block 고유 특성"), ("최종 모델", "Random Forest"), ("Test RMSE", "4.558"), ("해석 원칙", "예측 기여 ≠ 인과효과")])
            analysis_note("Set B/C는 진단 실험으로 남기고, 실제 활용 모델은 스케줄링 전에 알 수 있는 Block 특성만 사용합니다.")
        return

    if page == "4. 스케줄링 비교":
        if subpage.startswith(("4.1", "4.2")):
            structure = pd.DataFrame(
                [[method, 872, 60] for method in SCHEDULING_METHODS],
                columns=["Method", "Block Result", "사용 Position"],
            )
            st.dataframe(structure, hide_index=True, width="stretch")
            analysis_note("7개 방법은 같은 872개 Block과 Position 후보를 사용하지만, 배정 Position과 계획시점·Delay 결과가 달라집니다.")
        elif subpage.startswith("4.3"):
            fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.65))
            sns.heatmap(data["match"].astype(float), annot=True, fmt=".2f", vmin=0, vmax=1, cmap="Blues", ax=axes[0])
            axes[0].set_title("Same Position Selection Rate")
            axes[0].set_xlabel("")
            axes[0].set_ylabel("")
            sns.barplot(
                data=data["position"], x="Mean_Area_Margin_Ratio", y="Method",
                hue="Method", palette=METHOD_COLORS, legend=False, width=.5, ax=axes[1]
            )
            axes[1].set_xlim(0.40, 0.45)
            axes[1].set_title("Mean Area Margin Ratio")
            axes[1].set_ylabel("")
            sns.barplot(
                data=data["position"], x="Initially_Occupied_Assignments", y="Method",
                hue="Method", palette=METHOD_COLORS, legend=False, width=.5, ax=axes[2]
            )
            axes[2].set_title("Assignments to Initial-recorded Positions")
            axes[2].set_ylabel("")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            analysis_note(
                "대각선을 제외한 동일 Position 선택률은 대체로 약 10~13%로 낮고, 872개 중 849개 Block은 방법에 따라 Position이 달랐습니다. "
                "면적 여유비율 차이는 작지만 Initial 기록 Position 배정 건수는 방법별로 달라, 선택 규칙이 실제 배치 결과를 바꾼다는 점을 보여줍니다."
            )
            with st.expander("동일 Block의 7개 Scheduling 결과 조회", expanded=False):
                detail = data["detail"]
                block_index = st.selectbox("Block index", sorted(detail["block_index"].unique()), key="position_comparison_block_index")
                block = detail.loc[detail["block_index"].eq(block_index)].copy()
                detail_columns = [
                    "method", "position_id", "position_description", "planned_start_time",
                    "planned_finish_time", "planned_duration_days", "delay_days", "initially_occupied",
                ]
                st.dataframe(block[detail_columns].sort_values("delay_days"), hide_index=True, width="stretch")
        elif subpage.startswith("4.4"):
            best_makespan = data["schedule"].sort_values("Makespan_Days").iloc[0]
            compact_metrics([
                ("최단 Makespan", f"{best_makespan['Makespan_Days']:,.0f}일", best_makespan["Method"]),
                ("사용 Position", "60개", "모든 방법 공통"),
            ])
            st.dataframe(data["schedule"].sort_values("Makespan_Days"), hide_index=True, width="stretch")
            fig, axes = plt.subplots(1, 2, figsize=(13.5, 3.85))
            sns.barplot(
                data=data["schedule"].sort_values("Makespan_Days"), x="Makespan_Days", y="Method",
                hue="Method", palette=METHOD_COLORS, legend=False, ax=axes[0]
            )
            axes[0].set_title("Makespan")
            axes[0].set_xlabel("Days (Lower is Better)")
            axes[0].set_ylabel("")
            area_share = data["area_share"].set_index("method").loc[SCHEDULING_METHODS]
            area_share.plot(kind="barh", stacked=True, color=["#034EA2", "#6B5AA6", "#2D7D8C"], ax=axes[1])
            axes[1].set_title("Position Assignment Share by Area")
            axes[1].set_xlabel("Assignment Share")
            axes[1].set_ylabel("")
            axes[1].set_xlim(0, 1)
            axes[1].legend(["블록 조립 구역", "곡면 구역", "플랫폼 구역"], loc="lower center", bbox_to_anchor=(.5, 1), ncol=3, fontsize=8)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            analysis_note("EDDQN의 Makespan이 가장 짧고 Earliest Start가 그다음입니다. 모든 방법이 60개 Position을 써도 구역별 배정 비율과 전체 일정 범위는 달라집니다.")
        elif subpage.startswith("4.5"):
            delay_sorted = data["delay"].sort_values("Total_Delay")
            best_total_delay = delay_sorted.iloc[0]
            best_max_delay = data["delay"].sort_values("Max_Delay").iloc[0]
            compact_metrics([
                ("최저 Total Delay", f"{best_total_delay['Total_Delay']:,.0f}일", best_total_delay["Method"]),
                ("최소 Delayed Blocks", f"{data['delay'].sort_values('Delayed_Blocks').iloc[0]['Delayed_Blocks']:,.0f}개", data["delay"].sort_values("Delayed_Blocks").iloc[0]["Method"]),
                ("최저 Max Delay", f"{best_max_delay['Max_Delay']:,.0f}일", best_max_delay["Method"]),
            ])
            st.dataframe(data["delay"].sort_values("Total_Delay"), hide_index=True, width="stretch")
            fig, axes = plt.subplots(1, 2, figsize=(13.5, 3.85))
            sns.barplot(data=delay_sorted, x="Total_Delay", y="Method", hue="Method", palette=METHOD_COLORS, legend=False, ax=axes[0])
            axes[0].set_title("Total Positive Delay")
            axes[0].set_xlabel("Days (Lower is Better)")
            axes[0].set_ylabel("")
            sns.barplot(data=data["delay"].sort_values("Max_Delay"), x="Max_Delay", y="Method", hue="Method", palette=METHOD_COLORS, legend=False, ax=axes[1])
            axes[1].set_title("Maximum Delay")
            axes[1].set_xlabel("Days (Lower is Better)")
            axes[1].set_ylabel("")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            analysis_note("Earliest Start는 누적지연과 지연 Block 수, EDDQN은 최악지연에서 가장 우수합니다. 지연을 무엇으로 정의하느냐에 따라 우선 방법이 달라집니다.")
        else:
            decision = comparison[["Method", "Makespan_Days", "Total_Delay", "Delayed_Blocks", "Max_Delay"]].copy()
            st.dataframe(decision.sort_values("Makespan_Days"), hide_index=True, width="stretch")
            analysis_note("Scheduling Method는 하나의 절대점수보다 Makespan·누적지연·최악지연·Position 사용의 다기준 Trade-off로 선택해야 합니다.")
        return

    if page == "5. 최종 결론":
        flow_cards(
            [
                ("처음 질문", "Position까지 넣어 Cycle을 예측"),
                ("예상 밖 결과", "Set A가 Set B/C보다 우수"),
                ("가정 수정", "Cycle은 사전 입력·Position은 Result"),
                ("최종 구조", "Set A 예측 + 7개 Result 비교"),
            ]
        )
        analysis_note(
            "가장 중요한 결과는 특정 알고리즘의 1등보다 예측 입력과 Scheduling Result의 시간 순서를 바로잡은 것입니다. "
            "예측과 최적화 평가는 분리하되, 실제 운영에서는 순환적으로 연결할 수 있습니다.",
            "프로젝트의 핵심 메시지",
        )
        return

    if page == "6. 개발 로드맵":
        flow_cards(
            [
                ("Cycle Predictor", "Block 특성으로 사전 기준기간 추정"),
                ("Result Viewer", "7개 방법의 Position·일정·Delay 비교"),
                ("Analyzer", "군집·분류·이상징후 진단"),
                ("Dynamic Scheduling", "실적 반영 재예측·재스케줄링"),
            ]
        )
        analysis_note("현재 데이터로 구현 가능한 범위는 Result Viewer이며, 실적·자원·비용 데이터가 확보된 뒤 동적 재스케줄링으로 확장합니다.")

st.sidebar.image(LOGO_PATH, width="stretch")
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="brand-title">스마트조선소 AI 전문가 양성과정</div>
        <div class="brand-subtitle">
            Predicting Block Position Cycle Using Machine Learning<br>
            <b>김민규 · KIM MIN GYU</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
edit_mode = st.sidebar.toggle(
    "편집 모드",
    value=False,
    help="현재 슬라이드의 위치·크기·폰트·강조를 직접 조절합니다.",
)
page_names = [
    COVER_PAGE,
    ANALYSIS_FLOW_PAGE,
    "0. Overview",
    DATA_STRUCTURE_PAGE,
    *[page_name for page_name in NOTEBOOK_FILES if page_name != "0. Overview"],
    CYCLE_PREDICTION_PAGE,
    SCHEDULING_RESULT_PAGE,
    SUBMISSION_PAGE,
]
if "selected_page_index" not in st.session_state:
    requested_page = st.query_params.get("page")
    st.session_state.selected_page_index = (
        page_names.index(requested_page) if requested_page in page_names else 0
    )
page_index = min(st.session_state.selected_page_index, len(page_names) - 1)
st.session_state.selected_page_index = page_index
page = page_names[page_index]
custom_only_pages = {
    "2. 전처리 및 EDA",
    "4. 스케줄링 비교",
    "5. 최종 결론",
    "6. 개발 로드맵",
}
notebook_sections = (
    {}
    if page in {*SIMULATOR_PAGES, SUBMISSION_PAGE, COVER_PAGE, ANALYSIS_FLOW_PAGE, *custom_only_pages}
    else load_notebook_sections(
        str(NOTEBOOK_FILES["0. Overview"] if page == DATA_STRUCTURE_PAGE else NOTEBOOK_FILES[page]),
        split_subsections=page == "3. 회귀모델",
    )
)
dashboard_label = page if page in {*SIMULATOR_PAGES, SUBMISSION_PAGE, COVER_PAGE, ANALYSIS_FLOW_PAGE, "6. 개발 로드맵"} else (
    None if page in {"0. Overview", DATA_STRUCTURE_PAGE} else "주요 결과·시각화"
)
if page == COVER_PAGE:
    subpage_names = [COVER_PAGE]
elif page == ANALYSIS_FLOW_PAGE:
    subpage_names = [ANALYSIS_FLOW_PAGE]
elif page == "0. Overview":
    overview_sections = list(notebook_sections.keys())
    project_reason_index = overview_sections.index(PROJECT_REASON_OVERVIEW_SUBPAGE)
    overview_sections[project_reason_index : project_reason_index + 1] = [
        PROJECT_TOPIC_SUBPAGE,
        PROJECT_REASON_OVERVIEW_SUBPAGE,
        PROJECT_REASON_CHALLENGES_SUBPAGE,
        PROJECT_REASON_SELECTION_SUBPAGE,
    ]
    # 발표 초반에는 사후 재검토처럼 보이는 설명을 숨기고, 결론에서만 다룹니다.
    overview_sections.remove("0.3 종속변수와 데이터 생성 순서")
    overview_sections.remove("0.4 프로젝트 목표")
    overview_sections.remove(DATASET_OVERVIEW_SUBPAGE)
    overview_sections.remove(ANALYSIS_FLOW_SUBPAGE)
    subpage_names = overview_sections
elif page == DATA_STRUCTURE_PAGE:
    subpage_names = [
        DATASET_OVERVIEW_SUBPAGE,
        DATASET_ASSUMPTIONS_SUBPAGE,
        DATASET_STRUCTURE_SUBPAGE,
        *RAW_TABLE_SUBPAGES,
        RESULT_TABLE_SUBPAGE,
        "0.4 프로젝트 목표",
    ]
elif page == "2. 전처리 및 EDA":
    subpage_names = EDA_SUBPAGES
elif page == "3. 회귀모델":
    # 회귀모델의 표·그래프는 각 분석 단계에 배치한다.
    # 3.2는 3.1에, 3.3.2는 3.3.1에, 3.4 설명은 결과·설계 문제 페이지에 통합한다.
    subpage_names = [
        title for title in notebook_sections.keys()
        if not title.startswith(("3.2", "3.3.2", "3.4 탐색적", "3.4.3", "3.4.4", "3.4.5", "3.6", "3.8"))
    ]
elif page == "4. 스케줄링 비교":
    # 발표 흐름: 구조 → Position → 일정 범위 → 지연 성과 → 결론
    # 결과 저장·세부 설명은 메뉴에서 제외하고 각 비교 페이지에 필요한 내용만 배치한다.
    subpage_names = SCHEDULING_PRESENTATION_SUBPAGES
elif page == "1. Master Table":
    subpage_names = [
        TABLE_JOIN_STRATEGY_SUBPAGE,
        JOIN_KEY_DISCOVERY_SUBPAGE,
        MASTER_TABLE_ERD_SUBPAGE,
        *[
            title
            for title in notebook_sections
            if not title.startswith(("1.1", "1.2", "1.3"))
        ],
    ]
elif page == "5. 최종 결론":
    subpage_names = [
        FINAL_SUMMARY_SUBPAGE,
        FINAL_LIMITATION_SUBPAGE,
        FINAL_ANALYSIS_REFRAME_SUBPAGE,
        FINAL_IMPLICATION_SUBPAGE,
        FINAL_REFERENCE_SUBPAGE,
    ]
elif page == "6. 개발 로드맵":
    subpage_names = ROADMAP_SUBPAGES
elif page == SUBMISSION_PAGE:
    subpage_names = [
        SUBMISSION_COVER_SUBPAGE,
        SUBMISSION_CONTENTS_SUBPAGE,
        SUBMISSION_OVERVIEW_SUBPAGE,
        SUBMISSION_PROCESS_SUBPAGE,
        SUBMISSION_PROGRESS_SUBPAGE,
        SUBMISSION_TEAM_SUBPAGE,
        SUBMISSION_SELF_REVIEW_SUBPAGE,
        SUBMISSION_DEMO_VIDEO_SUBPAGE,
    ]
elif page in SIMULATOR_PAGES:
    subpage_names = [page]
else:
    subpage_names = [dashboard_label, *notebook_sections.keys()]
subpage_state_key = f"subpage_{page_index}"
requested_subpage = st.query_params.get("section")
if subpage_state_key not in st.session_state and requested_subpage in subpage_names:
    st.session_state[subpage_state_key] = requested_subpage
if st.session_state.get(subpage_state_key) not in subpage_names:
    st.session_state[subpage_state_key] = subpage_names[0]
subpage = subpage_names[0]

st.sidebar.markdown("**페이지 선택**")
for index, label in enumerate(page_names):
    if st.sidebar.button(
        display_label_without_numbers(label),
        key=f"page_button_{index}",
        type="primary" if index == page_index else "secondary",
        width="stretch",
    ):
        st.session_state.selected_page_index = index
        st.query_params["page"] = label
        st.rerun()
    if index == page_index:
        if len(subpage_names) > 1:
            subpage = st.sidebar.radio(
                "세부 페이지",
                subpage_names,
                key=f"subpage_{index}",
                format_func=display_label_without_numbers,
                label_visibility="collapsed",
            )
        if (
            st.query_params.get("page") != page
            or st.query_params.get("section") != subpage
        ):
            st.query_params["page"] = page
            st.query_params["section"] = subpage
    if index < len(page_names) - 1:
        st.sidebar.markdown('<div class="sidebar-page-divider"></div>', unsafe_allow_html=True)

data_required_pages = {
    "1. Master Table",
    "2. 전처리 및 EDA",
    "3. 회귀모델",
    "4. 스케줄링 비교",
    "5. 최종 결론",
    CYCLE_PREDICTION_PAGE,
    SCHEDULING_RESULT_PAGE,
    SUBMISSION_PAGE,
}
data = None
feature_sets = models = delay = schedule = comparison = None
if page in data_required_pages:
    try:
        data = load_data()
    except FileNotFoundError as error:
        st.error(f"필요한 사전 계산 결과를 찾지 못했습니다: {error.filename}")
        st.stop()
    feature_sets = data["feature_sets"].sort_values("RMSE")
    models = data["models"].sort_values("RMSE")
    delay = data["delay"].sort_values("Total_Delay")
    schedule = data["schedule"].sort_values("Makespan_Days")
    comparison = schedule.merge(delay, on="Method")

slide_layouts = load_slide_layouts()
editable_slide_key = None
if page == "0. Overview":
    editable_slide_key = {
        PROJECT_REASON_OVERVIEW_SUBPAGE: "problem_statement",
        PROJECT_REASON_CHALLENGES_SUBPAGE: "shared_challenges",
        PROJECT_REASON_SELECTION_SUBPAGE: "idea_selection",
    }.get(subpage)
if edit_mode:
    if editable_slide_key:
        slide_layouts[editable_slide_key] = render_slide_layout_editor(
            editable_slide_key,
            slide_layouts,
        )
    else:
        st.sidebar.info("현재 페이지는 아직 직접 편집 대상이 아닙니다.")

if page == "6. 개발 로드맵":
    st.markdown(
        """
        <style>
        [data-testid="stMainBlockContainer"] {
            max-width: 2200px !important;
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

if page == COVER_PAGE or (page == SUBMISSION_PAGE and subpage == SUBMISSION_COVER_SUBPAGE):
    st.markdown(
        """
        <div style="min-height:535px;display:flex;flex-direction:column;justify-content:center;
                    padding:1.25rem 7.5rem 2.5rem;border-top:1px solid #D7DEE8;word-break:keep-all;">
          <div style="font-size:.82rem;font-weight:800;letter-spacing:.18em;color:#034EA2;margin-bottom:1.3rem;">SMART SHIPYARD · AI PROJECT</div>
          <div style="width:58px;height:5px;background:#034EA2;margin-bottom:1.6rem;"></div>
          <div style="font-size:3.35rem;font-weight:850;line-height:1.18;letter-spacing:-.055em;color:#082B4C;">
            조선 Block Position Cycle 예측 및<br>Scheduling Method 비교
          </div>
          <div style="font-size:1.36rem;line-height:1.55;color:#52657A;margin-top:1.4rem;">
            Predicting Block Position Cycle Using Machine Learning
          </div>
          <div style="max-width:970px;font-size:1.12rem;line-height:1.75;color:#344054;margin-top:2.6rem;">
            <b>주제</b> · Block 고유 특성 기반 기준 작업기간 예측과 7개 Scheduling Result 비교
          </div>
          <div style="display:grid;grid-template-columns:1.2fr .8fr 1fr 1.5fr;gap:1.8rem;font-size:1.02rem;color:#667085;margin-top:3.1rem;">
            <span><b style="color:#034EA2;">교육과정</b><br>스마트조선소 AI 전문가 양성과정</span>
            <span><b style="color:#034EA2;">개인 수행</b><br>김민규</span>
            <span><b style="color:#034EA2;">강사</b><br>김남현 · 김주완</span>
            <span><b style="color:#034EA2;">멘토</b><br>정세민 · 이근우 · 안대영</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

if page == ANALYSIS_FLOW_PAGE or (page == SUBMISSION_PAGE and subpage == SUBMISSION_CONTENTS_SUBPAGE):
    render_overview_contents()
    st.stop()

if page == "0. Overview" and subpage == PROJECT_TOPIC_SUBPAGE:
    st.markdown(
        """
        <div style="min-height:530px;display:flex;flex-direction:column;align-items:center;justify-content:center;
                    text-align:center;padding:1.25rem 8rem;word-break:keep-all;">
          <div style="font-size:.82rem;font-weight:800;letter-spacing:.18em;color:#034EA2;margin-bottom:1.15rem;">PROJECT TOPIC</div>
          <div style="width:54px;height:4px;background:#034EA2;margin-bottom:1.65rem;"></div>
          <div style="font-size:3.05rem;font-weight:850;line-height:1.28;letter-spacing:-.06em;color:#082B4C;">
            조선 Block 고유 특성 기반<br>Block Position Cycle 예측 및<br>Scheduling Method 비교
          </div>
          <div style="max-width:930px;margin-top:2.35rem;font-size:1.25rem;line-height:1.75;color:#344054;">
            사전 입력된 Block 정보로 기준 작업기간을 예측하고,<br>
            동일한 입력 조건에서 7개 방법이 만든 Position·계획일정·Delay 결과를 비교한다.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

if page == DATA_STRUCTURE_PAGE and subpage == DATASET_OVERVIEW_SUBPAGE:
    render_dataset_selection_cards()
    st.stop()

if page == DATA_STRUCTURE_PAGE and subpage == DATASET_STRUCTURE_SUBPAGE:
    render_dataset_structure_infographic()
    st.stop()

if page == DATA_STRUCTURE_PAGE and subpage in RAW_TABLE_SUBPAGES:
    render_raw_table_preview(RAW_TABLE_SUBPAGES[subpage])
    st.stop()

if page == DATA_STRUCTURE_PAGE and subpage == RESULT_TABLE_SUBPAGE:
    render_scheduling_result_preview()
    st.stop()

if page == DATA_STRUCTURE_PAGE and subpage == DATASET_ASSUMPTIONS_SUBPAGE:
    render_dataset_assumptions()
    st.stop()

if page == DATA_STRUCTURE_PAGE and subpage == "0.4 프로젝트 목표":
    render_project_objectives()
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_DATA_QUALITY_SUBPAGE:
    render_eda_data_quality(data)
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_MISSING_SUBPAGE:
    render_eda_missing_values(data)
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_TARGET_DEFINITION_SUBPAGE:
    render_eda_target_definition(data)
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_DERIVED_SUBPAGE:
    render_eda_derived_features(data)
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_OUTLIER_SUBPAGE:
    render_eda_outliers(data)
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_TARGET_DISTRIBUTION_SUBPAGE:
    render_eda_target_distribution(data)
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_NUMERIC_CORRELATION_SUBPAGE:
    render_eda_numeric_correlation(data)
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_CATEGORICAL_DISTRIBUTION_SUBPAGE:
    render_eda_categorical_distribution(data)
    st.stop()

if page == "2. 전처리 및 EDA" and subpage == EDA_FEATURE_SET_SUBPAGE:
    render_eda_feature_sets(data)
    st.stop()

if page == "1. Master Table" and subpage == TABLE_JOIN_STRATEGY_SUBPAGE:
    render_table_join_strategy()
    st.stop()

if page == "1. Master Table" and subpage == JOIN_KEY_DISCOVERY_SUBPAGE:
    render_join_key_discovery()
    st.stop()

if page == "1. Master Table" and subpage == MASTER_TABLE_ERD_SUBPAGE:
    render_master_table_erd()
    st.stop()

if page == "1. Master Table" and subpage == MASTER_TABLE_BUILD_SUBPAGE:
    render_master_table_build(data)
    st.stop()


if page == "0. Overview" and subpage in {
    PROJECT_REASON_CHALLENGES_SUBPAGE,
    PROJECT_REASON_SELECTION_SUBPAGE,
}:
    project_reason_markdown = notebook_sections[PROJECT_REASON_OVERVIEW_SUBPAGE]
    before_ideas, ideas_heading, after_ideas = project_reason_markdown.partition(
        "### 0.1.3 검토한 아이디어와 최종 선택"
    )
    if subpage == PROJECT_REASON_CHALLENGES_SUBPAGE:
        _, challenges_heading, challenges_body = before_ideas.partition(
            "### 0.1.2 건축과 조선이 공유하는 어려움"
        )
        render_centered_visual_slide(
            f"{challenges_heading}{challenges_body}",
            ROOT / "Docs" / "images" / "shared_challenges_cards_white.png",
            slide_layouts["shared_challenges"],
        )
    else:
        ideas_markdown = f"{ideas_heading}{after_ideas}".split("\n\n이 가운데", 1)[0]
        render_selected_idea_slide(
            ideas_markdown,
            ROOT / "Docs" / "images" / "idea_selection_cards_white.png",
            slide_layouts["idea_selection"],
        )
    st.stop()


if page == "4. 스케줄링 비교" and subpage.startswith("4.1"):
    render_scheduling_result_preview()
    st.stop()

if page == "5. 최종 결론":
    if subpage == FINAL_SUMMARY_SUBPAGE:
        st.markdown("<div class='section-kicker'>ANALYSIS SUMMARY</div>", unsafe_allow_html=True)
        st.title("분석 수치 요약")
        st.caption("예측모델 성능, 변수 세트 비교, 7개 Scheduling Method의 핵심 지표를 한 페이지에서 정리합니다.")

        final_metrics = data["modeling_summary"]["test_metrics"]
        best_makespan = schedule.iloc[0]
        best_total_delay = delay.iloc[0]
        metric_1, metric_2, metric_3, metric_4 = st.columns(4)
        metric_1.metric("최종 Set A RMSE", f"{final_metrics['RMSE']:.3f}", "Random Forest · Test")
        metric_2.metric("최종 Set A R²", f"{final_metrics['R2']:.3f}", "Random Forest · Test")
        metric_3.metric("최단 Makespan", f"{best_makespan['Makespan_Days']:,.0f}일", best_makespan["Method"])
        metric_4.metric("최저 Total Delay", f"{best_total_delay['Total_Delay']:,.0f}일", best_total_delay["Method"])

        feature_column, scheduling_column = st.columns(2, gap="large")
        with feature_column:
            st.subheader("변수 세트별 예측 성능")
            feature_summary = feature_sets[["Variable Set", "Variables", "MAE", "RMSE", "R2"]].copy()
            st.dataframe(feature_summary, hide_index=True, width="stretch")
        with scheduling_column:
            st.subheader("Scheduling 핵심 지표")
            scheduling_summary = comparison[
                ["Method", "Makespan_Days", "Total_Delay", "Delayed_Blocks", "Max_Delay"]
            ].sort_values("Makespan_Days")
            st.dataframe(scheduling_summary, hide_index=True, width="stretch")

        analysis_note(
            "Cycle 예측에는 Block 고유 특성만 사용한 Set A가 가장 낮은 RMSE를 보였습니다. "
            "Scheduling 성과는 Makespan·누적지연·지연 Block 수·최악지연의 기준에 따라 우선 방법이 달라지는 다기준 결과로 해석했습니다."
        )

    elif subpage == FINAL_LIMITATION_SUBPAGE:
        st.markdown("<div class='section-kicker'>LIMITATIONS</div>", unsafe_allow_html=True)
        st.title("현재 분석의 한계")
        st.caption("공개 데이터의 범위와 해석 조건을 명확히 구분해, 결과의 적용 범위를 과도하게 확대하지 않았습니다.")
        st.markdown(
            "- 생산 후 측정된 **실제 Cycle**이 없어, 사전 Cycle 예측값이 현장 실적과 얼마나 일치하는지는 검증하지 못했습니다.\n"
            "- 공개자료에는 Cycle 산정식과 비용·작업조·이동·재취급 등의 반영 여부가 충분히 공개되지 않았습니다.\n"
            "- Initial에 기록되지 않은 Position이 실제로 모두 비어 있었는지, Position의 실제 Yard 좌표가 무엇인지는 확인할 수 없었습니다.\n"
            "- 7개 Scheduling Result는 게시자가 제공한 데이터와 실험조건에 기반하므로, 다른 조선소·기간·운영조건에서의 외부 검증이 필요합니다."
        )
        analysis_note("따라서 본 결과는 공개 데이터에서 확인한 분석 구조와 비교 기준으로 해석하며, 실제 현장 성능은 추가 운영 데이터로 검증해야 합니다.")

    elif subpage == FINAL_ANALYSIS_REFRAME_SUBPAGE:
        st.markdown("<div class='section-kicker'>ANALYSIS REFRAME</div>", unsafe_allow_html=True)
        st.title("분석 구조를 다시 정의한 과정")
        st.caption("예상 밖의 성능 결과를 단순 실패로 보지 않고, 데이터의 생성 순서와 변수의 역할을 다시 검증했습니다.")

        st.markdown(
            """
            <div style="margin:1.05rem 0 1.25rem;padding:1rem 1.05rem;border:1px solid #D9E2EC;border-radius:12px;background:#FAFCFE;">
              <div style="display:flex;align-items:stretch;gap:.5rem;">
                <div style="flex:1;padding:.72rem .8rem;border-top:4px solid #7D8A99;border-radius:7px;background:#FFF;">
                  <b style="font-size:.72rem;color:#667085;letter-spacing:.08em;">01 · 처음의 질문</b><br>
                  <span style="font-size:.92rem;line-height:1.45;color:#102A43;">Position·Initial을 더하면<br>Cycle 예측이 좋아질까?</span>
                </div>
                <div style="align-self:center;color:#98A2B3;font-size:1.35rem;">→</div>
                <div style="flex:1;padding:.72rem .8rem;border-top:4px solid #034EA2;border-radius:7px;background:#F3F8FE;">
                  <b style="font-size:.72rem;color:#034EA2;letter-spacing:.08em;">02 · 예상 밖 결과</b><br>
                  <span style="font-size:.92rem;line-height:1.45;color:#102A43;">Set A <b>4.489</b> · Set B 5.029<br>Set C 4.990</span>
                </div>
                <div style="align-self:center;color:#98A2B3;font-size:1.35rem;">→</div>
                <div style="flex:1;padding:.72rem .8rem;border-top:4px solid #008C95;border-radius:7px;background:#F2FAFA;">
                  <b style="font-size:.72rem;color:#007A82;letter-spacing:.08em;">03 · 가정 재검토</b><br>
                  <span style="font-size:.92rem;line-height:1.45;color:#102A43;">Cycle의 의미와 선택 Position의<br>생성 시점을 다시 확인</span>
                </div>
              </div>
              <div style="text-align:center;color:#98A2B3;font-size:1.25rem;line-height:1.25;">↓</div>
              <div style="display:grid;grid-template-columns:1fr 1fr 1.1fr;gap:.55rem;align-items:stretch;">
                <div style="padding:.7rem .8rem;border:1px solid #D5DEE9;border-radius:7px;background:#FFF;">
                  <b style="font-size:.78rem;color:#034EA2;">수정 ① Cycle</b><br><span style="font-size:.86rem;color:#344054;line-height:1.4;">Result가 아닌 Block Table의<br>사전 기준 처리기간</span>
                </div>
                <div style="padding:.7rem .8rem;border:1px solid #D5DEE9;border-radius:7px;background:#FFF;">
                  <b style="font-size:.78rem;color:#034EA2;">수정 ② 선택 Position</b><br><span style="font-size:.86rem;color:#344054;line-height:1.4;">입력 후보가 아닌 Scheduling이<br>만든 사후 Result</span>
                </div>
                <div style="padding:.7rem .8rem;border-top:4px solid #034EA2;border-radius:7px;background:#F3F8FE;">
                  <b style="font-size:.72rem;color:#034EA2;letter-spacing:.08em;">04 · 최종 분석 구조</b><br><span style="font-size:.92rem;color:#102A43;line-height:1.45;">Set A로 사전 Cycle 예측<br>7개 Result는 Position·일정·Delay 비교</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        question_column, revision_column = st.columns([1, 1.15], gap="large")
        with question_column:
            st.subheader("처음의 질문과 성능 결과")
            st.markdown(
                "처음에는 `Block Position Cycle`을 작업 완료 후 측정되는 실제 공기에 가깝게 이해했습니다. "
                "그래서 Block 특성에 DDQN이 선택한 Position과 Initial 상태를 더하면 예측력이 좋아질 것으로 예상했습니다.\n\n"
                "- Set A: Block\n- Set B: Block + DDQN 선택 Position\n- Set C: Block + DDQN 선택 Position + Initial\n\n"
                "그러나 Random Forest 비교에서 **Set A가 RMSE 4.489로 가장 좋았고**, Set B는 5.029, Set C는 4.990으로 낮아졌습니다. "
                "이를 단순한 변수 추가 실패로 보지 않고 두 가지 가정을 다시 검토했습니다."
            )
        with revision_column:
            st.subheader("두 차례의 가정 수정")
            st.markdown(
                "**① Cycle의 의미** — 원본 테이블과 관련자료를 다시 확인한 결과 Cycle은 Result가 아니라 Block Table에 미리 존재했습니다. "
                "따라서 Cycle을 **스케줄링 이전에 주어진 기준 처리기간**으로 다시 정의했습니다.\n\n"
                "**② 선택 Position의 역할** — DDQN Result로 Block과 선택 Position을 정확히 연결할 수는 있지만, Streamlit에서 7개 Result를 바꾸면 같은 Block도 방법에 따라 다른 Position에 배정됐습니다. "
                "즉 Position 후보 정보는 입력이지만, 특정 Block에 연결된 **선택 Position은 Scheduling Method가 만든 결과**입니다. "
                "Join 가능 여부만으로 이를 사전 Cycle 예측의 독립변수로 사용할 수는 없습니다."
            )
        analysis_note(
            "Streamlit은 완성된 결과를 보여주는 발표 화면에 그치지 않았습니다. 방법을 바꿀 때 Position과 일정이 달라지는 모습을 직접 확인하면서, 기존 분석 가정을 검증하고 시간 순서가 섞인 논리 오류를 발견한 탐색 도구로도 사용되었습니다.",
            "시각화의 역할",
        )

    elif subpage == FINAL_IMPLICATION_SUBPAGE:
        st.markdown("<div class='section-kicker'>PROJECT IMPLICATIONS</div>", unsafe_allow_html=True)
        st.title("프로젝트를 통해 얻은 시사점")
        st.caption("모델 성능 그 자체보다, 어떤 정보가 언제 생성되고 언제 사용할 수 있는지를 먼저 확인해야 한다는 점을 확인했습니다.")
        st.markdown(
            """
            <div style="margin:1.25rem 0 1.45rem;padding:1.05rem 1.2rem;
                        border-left:5px solid #98A2B3;border-radius:7px;background:#F2F4F7;
                        color:#102A43;font-size:1.24rem;font-weight:800;line-height:1.55;word-break:keep-all;">
              좋은 예측모델은 많은 변수를 사용하는 모델이 아니라,<br>
              데이터의 생성 순서와 실제 의사결정 시점을 지키는 모델이다.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "- **Join 가능 ≠ 예측에 사용 가능**: 변수의 이름보다 생성 시점과 의사결정 시점이 먼저 확인되어야 합니다.\n"
            "- 예측모델의 입력과 최적화 알고리즘의 결과를 같은 층위에서 해석하면 안 됩니다.\n"
            "- 예상과 다른 성능은 실패가 아니라 데이터 생성 순서와 가정을 재검토하는 단서가 될 수 있습니다.\n"
            "- 스케줄링은 목적함수에 따라 최적 방법이 달라지는 다기준 의사결정 문제입니다.\n"
            "- 머신러닝은 Cycle 추정과 위험 진단을 지원하고, Scheduling Engine은 실행 가능한 일정 후보를 계산하는 역할로 분리하는 편이 타당합니다."
        )

    else:
        st.markdown("<div class='section-kicker'>REFERENCES</div>", unsafe_allow_html=True)
        st.title("참고문헌")
        st.caption("분석 구조와 데이터 생성 순서, 조선 블록 Scheduling과 공정시간 해석을 검토하는 데 참고한 자료입니다.")
        reference_rows = pd.DataFrame(
            [
                ["1", "Data of Ship Block Scheduling in English.pdf", "Block·Position·Initial Table 및 7개 Scheduling Result 원천 데이터"],
                ["2", "Knowledge-Based Curved Block Construction Scheduling and Application in Shipbuilding.pdf", "블록 건조 스케줄링과 Position 제약 해석 참고"],
                ["3", "A study on the man-hour prediction system for shipbuilding.pdf", "조선 man-hour 및 공정시간 정보 해석 범위 검토"],
                ["4", "A Heuristic Algorithm for Block Storage Planning in Shipbuilding.pdf", "블록 적치 계획과 휴리스틱 Scheduling 사례 참고"],
                ["5", "조선소 블록 조립 스케줄링을 위한 자연 모사 알고리즘 비교 연구.pdf", "스케줄링 알고리즘별 성능 비교 관점 검토"],
                ["6", "조선소 선행의장 공정의 스케줄링 최적화를 위한 알고리즘 비교 분석 연구.pdf", "목적함수와 평가 기준에 따른 알고리즘 차이 검토"],
            ],
            columns=["번호", "자료", "활용 내용"],
        )
        st.dataframe(reference_rows, hide_index=True, width="stretch")
        analysis_note("원천 데이터의 Cycle 산정식과 알고리즘 내부 구현은 공개 범위에서 확인 가능한 정보만 사용했으며, 선행연구는 해석 범위를 검토하는 근거로 활용했습니다.")
    st.stop()

if page == "4. 스케줄링 비교" and subpage in SCHEDULING_PRESENTATION_SUBPAGES:
    render_scheduling_presentation_page(subpage, data)
    st.stop()

if page == "6. 개발 로드맵" and subpage in ROADMAP_SUBPAGES:
    render_roadmap_presentation_page(subpage)
    st.stop()

if page not in {*SIMULATOR_PAGES, SUBMISSION_PAGE} and subpage != dashboard_label:
    section_markdown = notebook_sections[subpage]
    section_lines = section_markdown.splitlines()
    while section_lines and not section_lines[0].strip():
        section_lines.pop(0)
    if section_lines:
        first_line = section_lines[0].lstrip()
        heading_marker = first_line.split(maxsplit=1)[0]
        if heading_marker and set(heading_marker) == {"#"}:
            section_lines.pop(0)
            while section_lines and not section_lines[0].strip():
                section_lines.pop(0)
    section_markdown = "\n".join(section_lines)
    if page == "3. 회귀모델" and subpage.startswith("3.4.2"):
        merged_sections = [
            content
            for title, content in notebook_sections.items()
            if title.startswith(("3.4.3", "3.4.4"))
        ]
        section_markdown = "\n\n".join([section_markdown, *merged_sections])
    if page == "3. 회귀모델" and subpage.startswith("3.5"):
        merged_sections = [
            content
            for title, content in notebook_sections.items()
            if title.startswith(("3.4.5", "3.6"))
        ]
        section_markdown = "\n\n".join([merged_sections[0], section_markdown, merged_sections[1]])
    if page == "3. 회귀모델" and subpage.startswith("3.9"):
        section_markdown += (
            "\n\n#### 결과 저장\n\n"
            "기준모델·변수 세트 비교, 최종 Set A 모델, Test 예측값과 변수 중요도를 저장했다. "
            "다음 스케줄링 비교 단계에서는 이 회귀모델을 점수로 사용하지 않고 Result Table을 독립적으로 비교한다."
        )
    if page == "3. 회귀모델":
        section_markdown = re.sub(r"(?<!\*)\bRMSE\b(?!\*)", "**RMSE**", section_markdown)
        render_regression_heading(subpage)
    if page == "0. Overview" and subpage == ANALYSIS_FLOW_SUBPAGE:
        render_overview_contents()
        st.stop()
    if page == "0. Overview" and subpage.startswith("0.1"):
        before_ideas, ideas_heading, after_ideas = section_markdown.partition(
            "### 0.1.3 검토한 아이디어와 최종 선택"
        )
        personal_experience, _, _ = before_ideas.partition(
            "### 0.1.2 건축과 조선이 공유하는 어려움"
        )
        render_centered_problem_statement(
            personal_experience,
            slide_layouts["problem_statement"],
        )
        st.stop()
    elif page == "3. 회귀모델" and subpage.startswith("3.4.2"):
        before_flow, flow_block, after_flow = section_markdown.partition("```text")
        if flow_block:
            _, _, after_flow = after_flow.partition("```")
        position_note, _, after_flow = after_flow.strip().partition("\n\n")
        st.markdown(strip_section_numbers(f"{before_flow}\n\n{position_note}"))
        _, flow_image_column, _ = st.columns([0.23, 0.54, 0.23])
        with flow_image_column:
            st.image(DDQN_SCHEDULING_FLOW_IMAGE_PATH, width="stretch")
        before_research, _, _ = after_flow.partition("### 3.4.4 선행연구와 Cycle 의미")
        st.markdown(strip_section_numbers(before_research))
        st.markdown(
            """
            <div style="box-sizing:border-box;height:132px;min-height:132px;max-height:132px;margin:1rem 0;padding:1rem 1.15rem;
                        border:1px solid #D0D5DD;border-left:5px solid #7D8A99;border-radius:8px;background:#F4F5F7;
                        line-height:1.75;overflow:hidden;contain:layout paint;word-break:keep-all !important;">
                <div style="margin-bottom:.5rem;color:#102A43;font-size:1.06rem;font-weight:800;white-space:nowrap;">선행연구와 Cycle 의미</div>
                <div style="color:#344054;white-space:nowrap;">블록 건조 스케줄링은 사전 계획정보와 작업장 상태를 함께 고려해 조정할 수 있으며 <i>(Jiang et al., 2022)</i>.</div>
                <div style="color:#344054;white-space:nowrap;">조선 man-hour 예측도 생산 단계별로 활용 가능한 정보를 갱신하는 구조를 제시한다 <i>(Hur et al., 2015)</i>. Cycle은 원본 Block Table에 먼저 존재한다.</div>
                <div style="margin-top:.65rem;color:#102A43;white-space:nowrap;"><b>해석 범위</b> · <code>block_processing_cycle</code> 산정식은 공개되지 않았으므로, man-hour나 스케줄링 이후의 실제 작업기간과 동일하다고 단정할 수 없다.</div>
                <div style="color:#102A43;white-space:nowrap;">따라서 본 프로젝트에서는 원본 Block Table에 먼저 존재하는 <b>기준 처리기간</b>으로만 해석한다.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(strip_section_numbers(section_markdown))

    if page == "1. Master Table" and subpage.startswith("1.3"):
        st.image(ROOT / "Docs" / "images" / "1_master_table_join_erd.svg", width="stretch")
    render_section_companion(page, subpage, data)
    st.stop()


@st.fragment
def render_cycle_simulator(data, mode):
    input_catalog = data["analysis"]
    plot_config = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]}

    if mode == CYCLE_PREDICTION_PAGE:
        set_a_model, set_a_test = load_set_a_model()
        st.subheader("스케줄링 전 Block 특성 기반 Cycle 예측")
        output = st.empty()
        input_mode = st.segmented_control(
            "Block 입력 방식",
            ["실제 Block 선택", "가상 Block 입력"],
            default="실제 Block 선택",
            selection_mode="single",
            key="pre_input_mode",
        ) or "실제 Block 선택"
        selected_block = st.select_slider(
            "테이블에서 선택할 Block" if input_mode == "실제 Block 선택" else "가상 Block 기본값 불러오기",
            options=sorted(set_a_test["block_index"].unique()),
            format_func=lambda value: f"Block {int(value)}",
            key="pre_block",
        )
        profile = set_a_test[set_a_test["block_index"].eq(selected_block)].iloc[0].copy()
        input_prefix = "pre_actual" if input_mode == "실제 Block 선택" else "pre_virtual"
        profile.name = f"{input_prefix}:{int(selected_block)}"
        sync_profile(profile, input_catalog, widget_keys(input_prefix), f"{input_prefix}_profile")

        with st.expander("Set A · Block 특성", expanded=True):
            inputs = render_block_inputs(input_catalog, input_prefix, input_mode)

        prediction = float(set_a_model.predict(pd.DataFrame([inputs], columns=SET_A_FEATURES))[0])
        original_prediction = float(profile["predicted_cycle"])
        with output.container():
            st.plotly_chart(
                build_cycle_context_chart(
                    set_a_test,
                    selected_block,
                    "Set A 예측",
                    prediction if input_mode == "가상 Block 입력" else None,
                    show_selected_result=input_mode == "실제 Block 선택",
                ),
                width="stretch",
                config=plot_config,
            )
            st.caption("Position이 정해지기 전 단계이므로 Set A의 Block 특성만 사용합니다.")
            if input_mode == "실제 Block 선택":
                compact_metrics(
                    [
                        ("선택 Block 기준 Cycle", f"{profile['block_processing_cycle']:.1f}일", "Block Table"),
                        ("선택 Block Set A 예측", f"{original_prediction:.1f}일", "동일 행의 Block 특성"),
                    ]
                )
                st.caption("선택한 Block 한 행의 특성 조합을 변경하지 않고 그대로 조회합니다.")
                prediction_gap = original_prediction - float(profile["block_processing_cycle"])
                direction = "높게" if prediction_gap > 0 else "낮게"
                analysis_note(
                    f"선택 Block의 Set A 예측은 기준 Cycle보다 {abs(prediction_gap):.1f}일 {direction} 추정됐습니다. "
                    "그래프의 전체 추세는 중간 Cycle 구간에서 비교적 잘 따라가지만 장기 Cycle 구간에서는 오차 폭이 커질 수 있음을 보여줍니다."
                )
            else:
                compact_metrics([("가상 Block Set A 예측", f"{prediction:.1f}일", "현재 입력값")])
                st.caption(
                    "주황색 선은 원본의 최소–최대 범위 안에서 만든 가상 Block의 예측입니다. 원본에 같은 조합이 "
                    "존재한다고 보장할 수 없으므로 기준 Cycle과의 절대오차는 계산하지 않습니다."
                )
                analysis_note(
                    "가상 Block에는 실제 기준 Cycle이 없으므로 입력 특성에 대한 Set A 예측값만 제시합니다. "
                    "주황색 선은 실제 작업기간이 아니라 현재 입력 조합에 대한 모델의 예측 반응입니다."
                )
        return

    result_gantt_scope_key = f"{mode}_gantt_scope"
    result_selected_position_key = f"{mode}_selected_position"
    st.subheader("기존 Scheduling Result 조회")
    yard_output = st.empty()
    with st.form("schedule_result_form", border=False):
        method_col, block_col = st.columns(2)
        with method_col:
            selected_method = st.selectbox(
                "Scheduling Result 선택",
                SCHEDULING_METHODS,
                index=1,
                key=f"{mode}_method",
            )
        method_profiles = data["detail"][data["detail"]["method"].eq(selected_method)]
        with block_col:
            selected_block = st.selectbox(
                "조회 Block",
                sorted(method_profiles["block_index"].unique()),
                format_func=lambda value: f"Block {int(value)}",
                key=f"{mode}_block",
            )
        result_submitted = st.form_submit_button("Result 불러오기", type="primary", use_container_width=True)
    result_query = (selected_method, int(selected_block))
    if result_submitted or st.session_state.get("result_query_marker") != result_query:
        st.session_state[result_gantt_scope_key] = "전체 야드"
        st.session_state[result_selected_position_key] = None
        st.session_state["result_query_marker"] = result_query
    selected_profile = method_profiles[method_profiles["block_index"].eq(selected_block)].iloc[0].copy()
    set_a_prediction = float(selected_profile["set_a_prediction"])
    compact_metrics(
        [
            ("사전 기준 Cycle", f"{selected_profile['block_processing_cycle']:.1f}일", "Block Table 입력"),
            ("Set A 예측", f"{set_a_prediction:.1f}일", "Block 특성 기반"),
            ("계획 작업기간", f"{selected_profile['planned_duration_days']:.0f}일", "Result"),
            ("Delay", f"{selected_profile['delay_days']:.0f}일", "Result"),
        ]
    )
    analysis_note(
        f"{selected_method} Result에서 Block {int(selected_block)}은 {selected_profile['position_id']}에 배정됐고, "
        f"계획 작업기간은 {selected_profile['planned_duration_days']:.0f}일, Delay는 {selected_profile['delay_days']:.0f}일입니다. "
        "사전 기준 Cycle·Set A 예측과 Result 일정은 생성 시점과 의미가 다른 값이므로 동일한 성능점수로 합치지 않습니다.",
        "조회 결과 요약",
    )
    compact_metrics(
        [
            ("조회 Block", f"Block {int(selected_block)}", str(selected_profile["block_type"])),
            ("배정 Position", str(selected_profile["position_id"]), str(selected_profile["position_primary_area"])),
            (
                "Initial 기록",
                "있음" if bool(selected_profile["initially_occupied"]) else "없음",
                "Position 수준 연결",
            ),
        ]
    )

    yard_chart_key = f"{mode}_yard_plan"
    gantt_scope_key = result_gantt_scope_key

    def select_yard_area():
        points = st.session_state.get(yard_chart_key, {}).get("selection", {}).get("points", [])
        if points and len(points[-1].get("customdata", [])) > 1:
            st.session_state[result_selected_position_key] = points[-1]["customdata"][1]
            st.session_state[gantt_scope_key] = "선택 Position"

    with yard_output.container():
        st.subheader("66개 Position으로 구성한 가상 야드 평면도")
        st.caption(
            f"{selected_method} Result가 배정한 {selected_profile['position_id']}는 조회 Position으로 강조했습니다. "
            "평면도의 다른 Position을 클릭하면 해당 Position만 선택하여 간트를 조회합니다."
        )
        yard_col, block_3d_col = st.columns([2.2, 1])
        with yard_col:
            st.plotly_chart(
                build_virtual_yard_plan(
                    data["positions"],
                    selected_profile["position_id"],
                    st.session_state.get(result_selected_position_key),
                ),
                width="stretch",
                config=plot_config,
                key=yard_chart_key,
                on_select=select_yard_area,
                selection_mode="points",
            )
        with block_3d_col:
            st.plotly_chart(
                build_block_isometric(selected_profile),
                width="stretch",
                config={"staticPlot": True, "displayModeBar": False, "displaylogo": False},
            )
            st.caption(
                "선체는 여러 Block 구획으로 나뉘며, 조회 Block에 따라 노란 영역이 달라집니다. "
                "구획 위치와 선체 형상은 이해를 돕기 위한 개념도입니다."
            )
        analysis_note(
            "평면도는 66개 Position의 규격과 구역을 개념적으로 배치한 조회 도구입니다. "
            "주황색은 Result가 배정한 조회 Position, 파란색은 사용자가 간트 확인을 위해 클릭한 선택 Position이며 실제 야드 좌표를 뜻하지 않습니다.",
            "평면도·Isometric 해석",
        )
    gantt_scope = st.segmented_control(
        "간트 조회 범위",
        ["조회 Position", "조회 구역", "선택 Position", *[label for label, _ in YARD_AREA_STYLES.values()], "전체 야드"],
        default="전체 야드",
        selection_mode="single",
        key=gantt_scope_key,
    ) or "전체 야드"
    schedule_result = load_schedule_result(selected_method)
    area_by_label = {label: area for area, (label, _) in YARD_AREA_STYLES.items()}
    query_area_label = YARD_AREA_STYLES[selected_profile["position_primary_area"]][0]
    effective_gantt_scope = query_area_label if gantt_scope == "조회 구역" else gantt_scope

    if effective_gantt_scope in area_by_label:
        area_name = area_by_label[effective_gantt_scope]
        area_positions = data["positions"][data["positions"]["primary area"].eq(area_name)].copy()
        area_sizes = area_positions["size"].astype(str).str.split("*", expand=True).astype(float)
        area_capacity = pd.to_numeric(area_positions["lifting capacity (T)"], errors="coerce")
        area_schedule = schedule_result[
            schedule_result["block position id"].isin(area_positions["block position id"])
        ]
        compact_metrics(
            [
                ("Position", f"{len(area_positions)}개", effective_gantt_scope),
                ("합산 면적", f"{area_sizes.prod(axis=1).sum():,.0f}㎡", "Position 규격 기준"),
                ("인양용량", f"{area_capacity.min():.0f}–{area_capacity.max():.0f}T", "범위"),
                ("배정 Block", f"{len(area_schedule):,}개", selected_method),
                (
                    "계획 범위",
                    f"{area_schedule['planned start time'].min():%Y-%m-%d} – "
                    f"{area_schedule['planned finish time'].max():%Y-%m-%d}",
                    "Result",
                ),
            ]
        )
    st.plotly_chart(
        build_position_gantt(
            schedule_result,
            data["positions"],
            selected_method,
            selected_block,
            effective_gantt_scope,
            st.session_state.get(result_selected_position_key),
        ),
        width="stretch",
        config=plot_config,
    )
    if gantt_scope == "전체 야드":
        st.caption("원본 Result Table의 전체 872개 Block 일정이며 조회 Block은 주황색으로 강조했습니다.")
    elif gantt_scope == "조회 Position":
        st.caption(
            f"조회 Block이 배정된 {selected_profile['position_id']}의 일정만 표시했습니다. "
            "다른 구역 또는 전체 일정은 위 범위 선택기에서 열 수 있습니다."
        )
    elif gantt_scope == "조회 구역":
        st.caption(
            f"조회 Position {selected_profile['position_id']}가 속한 {query_area_label}의 전체 일정을 표시했습니다."
        )
    elif gantt_scope == "선택 Position":
        selected_position_id = st.session_state.get(result_selected_position_key)
        if selected_position_id:
            st.caption(f"평면도에서 선택한 {selected_position_id}의 일정만 표시했습니다.")
        else:
            st.caption("평면도에서 Position을 클릭하면 해당 Position의 일정만 표시합니다.")
    else:
        st.caption(f"{gantt_scope}에 포함된 Position의 일정만 표시했습니다.")
    analysis_note(
        "간트의 막대는 원본 Result에 기록된 계획 시작·종료일입니다. 막대의 밀집과 공백은 Position별 계획 사용 패턴을 보여주지만, "
        "작업 간 선후행 제약이나 실제 현장 가동률까지 직접 증명하지는 않습니다.",
        "간트 해석",
    )


if page in SIMULATOR_PAGES:
    render_cycle_simulator(data, page)
    st.stop()

if page == SUBMISSION_PAGE:
    if subpage == SUBMISSION_OVERVIEW_SUBPAGE:
        st.markdown("<div class='section-kicker'>PROJECT OVERVIEW</div>", unsafe_allow_html=True)
        st.title("프로젝트 개요")
        st.caption("개인 프로젝트의 주제, 분석 범위, 도구와 향후 활용 방향을 제출 항목 기준으로 정리했습니다.")
        overview_rows = pd.DataFrame(
            [
                ["1. 프로젝트 주제 및 선정 배경·기획의도", "조선 블록 기준 처리기간(Block Position Cycle) 예측 및 Scheduling 결과 분석", "공정기간 예측 관심에서 출발해 조선 블록 Scheduling 데이터셋을 선정하고, 데이터 기반 생산계획 활용 가능성을 탐색"],
                ["2. 프로젝트 내용", "Block Position Cycle 회귀 예측 · 7개 Scheduling 결과 비교", "Linear·Ridge·Decision Tree·Random Forest 비교 후, DDQN·EDDQN·5개 Heuristic의 Position·일정·Delay 결과를 비교하고 Streamlit으로 시각화"],
                ["3. 활용 장비 및 재료", "Python 기반 분석 환경과 공개 조선 블록 데이터", "Python · Jupyter Notebook · pandas · NumPy · scikit-learn · Matplotlib · Streamlit / Block·Position·Initial Information 및 7개 Scheduling Result"],
                ["4. 프로젝트 구조", "데이터 이해부터 Streamlit 시각화까지 전 과정 직접 수행", "데이터 이해 → 전처리·EDA → 회귀모델 구축·평가 → 데이터 생성 구조 재검토 → 분석 구조 수정 → 7개 Scheduling 결과 비교 → Streamlit 시각화"],
                ["5. 활용방안 및 기대효과", "기준 처리기간 예측과 Scheduling 결과 비교의 기반 마련", "향후 실제 생산실적 기반 Cycle 갱신, Dynamic Scheduling, MES·ERP 연계를 통한 생산계획 의사결정 지원으로 확장 가능"],
            ],
            columns=["제출 항목", "핵심 내용", "세부 설명"],
        )
        st.dataframe(overview_rows, hide_index=True, width="stretch")
        flow_cards(
            [
                ("예측", "Block 고유 특성으로 기준 처리기간 회귀 예측"),
                ("비교", "7개 Scheduling Method의 Position·일정·Delay 비교"),
                ("확장", "실적 Cycle 갱신과 Dynamic Scheduling 의사결정 지원"),
            ]
        )

    elif subpage == SUBMISSION_PROCESS_SUBPAGE:
        st.markdown("<div class='section-kicker'>PROJECT PROCESS</div>", unsafe_allow_html=True)
        st.title("프로젝트 수행 절차 및 방법")
        st.caption("2026년 8월 13일부터 20일까지 개인 프로젝트로 수행한 분석 절차입니다.")
        process_rows = pd.DataFrame(
            [
                ["사전 기획", "8/13", "프로젝트 주제 구체화 · 데이터셋 검토 · 분석 목표 설정", "조선 Block Scheduling 데이터 선정"],
                ["데이터 이해 및 구축", "8/14~8/15", "데이터 구조 분석 · Block/Position 관계 파악 · Master Table 구축", "Scheduling Result를 Mapping으로 활용"],
                ["전처리 및 모델링", "8/15~8/16", "데이터 전처리 · EDA · Feature Engineering · 회귀모델 비교 및 평가", "Linear / Ridge / DT / RF 비교"],
                ["분석 재검토 및 확장", "8/17~8/18", "데이터 생성 시점 재검토 · Cycle 의미 재정의 · 분석 구조 수정 · 7개 Scheduling 비교", "선택 Position의 사후변수 문제 발견"],
                ["시각화 및 결과 정리", "8/18~8/20", "Scheduling 결과 시각화 · Streamlit 구현 · 결론 및 한계 정리 · 발표자료 제작", "최종 결과보고서 작성"],
                ["총 수행기간", "8/13~8/20 (8일)", "기획 → 데이터 분석 → 모델링 → 재검토 → 확장 → 시각화 및 결과 정리", "개인 프로젝트"],
            ],
            columns=["구분", "기간", "주요 활동", "비고"],
        )
        st.dataframe(process_rows, hide_index=True, width="stretch")
        flow_cards(
            [
                ("기획", "주제와 공개 데이터셋 검토"),
                ("분석", "Master Table · EDA · 회귀모델 비교"),
                ("재검토", "데이터 생성 순서를 반영해 분석 구조 수정"),
                ("정리", "Scheduling 비교 · Streamlit · 결과보고서"),
            ]
        )

    elif subpage == SUBMISSION_PROGRESS_SUBPAGE:
        st.markdown("<div class='section-kicker'>PROJECT PROGRESS</div>", unsafe_allow_html=True)
        st.title("프로젝트 수행 경과")
        st.caption("공식 요구사항이 프로젝트 분석 과정과 결과물에서 어떻게 확인되는지 정리했습니다.")
        progress_rows = pd.DataFrame(
            [
                ["1. 활용 기술·구현 방법·결과", "데이터 전처리 → 회귀모델 구축 → 모델 성능 평가 → Scheduling 결과 비교 → Streamlit 시각화"],
                ["2. 전체 프로세스", "원천 데이터 → 데이터 구조 분석 → Master Table → EDA/모델링 → 구조 재검토 → 최종 분석"],
                ["3. 피드백·보완 과정", "Cycle 의미 재해석 / 선택 Position의 생성 시점 발견 → 분석 구조 수정"],
                ["4. 결과물 증빙", "Notebook 실제 그래프 / 모델 성능 / 7개 Scheduling 비교 / Streamlit 결과 화면"],
            ],
            columns=["공식 요구사항", "프로젝트에서 보여줄 내용"],
        )
        st.dataframe(progress_rows, hide_index=True, width="stretch")
        flow_cards(
            [
                ("구현", "Python·Jupyter 기반 분석과 Streamlit 시각화"),
                ("검증", "모델 비교와 데이터 생성 구조 재검토"),
                ("증빙", "Notebook 그래프·표와 대시보드 결과 화면"),
            ]
        )

    elif subpage == SUBMISSION_TEAM_SUBPAGE:
        st.markdown("<div class='section-kicker'>PROJECT TEAM & ROLES</div>", unsafe_allow_html=True)
        st.title("프로젝트 팀 구성 및 역할")
        st.caption("개인 프로젝트 수행 범위와 교육·멘토링 지원 내용을 정리했습니다.")
        team_rows = pd.DataFrame(
            [
                ["훈련생", "김민규", "개인 수행", "주제 선정 · 데이터 조사 / 전처리 · EDA / 회귀모델 구축 · 평가 / 7개 Scheduling 분석 / Streamlit 시각화"],
                ["강사", "김남현", "교육 · 지도", "데이터 분석 및 머신러닝 교육 / 프로젝트 분석 방향 질의응답"],
                ["강사", "김주완", "교육 · 지도", "프로젝트 수행 지원 / 분석·개발 과정 질의응답"],
                ["멘토", "정세민", "프로젝트 멘토링", "프로젝트 방향성 검토 / 분석 과정 및 결과 피드백"],
                ["멘토", "이근우", "프로젝트 멘토링", "프로젝트 진행사항 검토 / 분석 방향 및 개선사항 피드백"],
                ["멘토", "안대영", "프로젝트 멘토링", "프로젝트 결과 검토 / 실무 관점의 개선 방향 자문"],
            ],
            columns=["구분", "성명", "역할", "담당 업무"],
        )
        st.dataframe(team_rows, hide_index=True, width="stretch")
        flow_cards(
            [
                ("개인 수행", "분석 설계부터 Streamlit 시각화까지 전 과정 직접 수행"),
                ("교육·지도", "데이터 분석·머신러닝 교육과 방향 질의응답"),
                ("멘토링", "분석 과정·결과 검토와 실무 관점의 개선 방향 피드백"),
            ]
        )

    elif subpage == SUBMISSION_SELF_REVIEW_SUBPAGE:
        st.markdown("<div class='section-kicker'>SELF REVIEW</div>", unsafe_allow_html=True)
        st.title("자체 평가 의견")
        st.caption("프로젝트 결과의 완성도, 배운 점과 향후 보완 방향을 정리했습니다.")
        review_rows = pd.DataFrame(
            [
                ["완성도 평가", "8 / 10", "회귀분석부터 Scheduling 비교·시각화까지 구현"],
                ["잘한 점 / 아쉬운 점", "데이터 생성 구조 재검토", "분석 구조를 수정했으며, 실제 생산실적 데이터는 부재"],
                ["추후 개선점", "실제 생산실적 기반 Cycle 예측", "Dynamic Scheduling으로 확장"],
                ["느낀 점 / 성과", "Join 가능 ≠ 예측에 사용 가능", "변수의 의미와 생성 시점을 확인하는 과정의 중요성"],
            ],
            columns=["평가 항목", "핵심 의견", "상세 내용"],
        )
        st.dataframe(review_rows, hide_index=True, width="stretch")
        flow_cards(
            [
                ("성과", "데이터 연결과 예측 변수 사용은 별개라는 점을 확인"),
                ("한계", "실제 생산실적 Cycle이 없어 외부 검증에는 한계"),
                ("확장", "실적 기반 Cycle 갱신과 Dynamic Scheduling으로 발전"),
            ]
        )

    elif subpage == SUBMISSION_DEMO_VIDEO_SUBPAGE:
        st.markdown("<div class='section-kicker'>DEMO VIDEO</div>", unsafe_allow_html=True)
        st.title("시연영상")
        st.caption("완성한 Streamlit 화면의 주요 기능을 시연하는 영상을 이 위치에 삽입합니다.")
        st.markdown(
            """
            <div style="aspect-ratio:16 / 9; max-width:1100px; margin:28px auto; border:2px solid #AAB8C8; background:#24364A; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#FFFFFF;">
                <div style="width:74px; height:74px; border:3px solid #FFFFFF; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:32px; padding-left:5px;">▶</div>
                <div style="font-size:26px; font-weight:700; margin-top:22px;">시연영상 삽입 영역</div>
                <div style="font-size:16px; color:#D5E4F5; margin-top:10px;">Streamlit 주요 기능 및 Scheduling Result 조회 화면</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.info("영상 파일이 준비되면 이 목업 자리에 `st.video()`로 교체해 삽입하면 됩니다.")
    st.stop()


if page == "0. Overview":
    st.markdown(
        """
        ### 프로젝트 요약

        공개된 조선 블록 데이터를 이용해 **Block 고유 특성으로 사전 Cycle을 예측**하고,
        7개 Scheduling Method가 만든 Position·계획일정·Delay 결과를 별도로 비교했습니다.
        """
    )
    overview_col1, overview_col2, overview_col3 = st.columns(3)
    overview_col1.metric("전체 Block", f"{len(data['master']):,}개")
    overview_col2.metric("Test Block", f"{data['detail']['block_index'].nunique():,}개")
    overview_col3.metric("Scheduling Method", f"{data['detail']['method'].nunique()}개")

    st.markdown(
        """
        ## 프로젝트를 시작한 이유

        건축 설계 실무에서 경험한 **디지털 도면과 실제 현장의 차이, 반복되는 설계변경,
        여러 조직 사이의 정보 단절**이 조선 프로젝트에서도 비슷하게 발생한다고 보았습니다.
        이를 데이터 분석 문제로 연결해 Block의 기준 작업기간을 예측하고 스케줄링 방법을 비교하는 주제를 선택했습니다.

        ## 데이터와 분석 대상

        Block·Position·Initial Table과 7개 Scheduling Result를 연결했습니다.  
        Cycle 예측의 단위는 **Block**, Scheduling 비교의 단위는 **Block별 Result**입니다.

        ## 종속변수 정의

        `Block Position Cycle`은 실제 작업 완료 후 측정된 실적 공기라기보다,
        **스케줄링 이전에 산정된 기준 처리기간**으로 해석했습니다. 정확한 산정식은 공개되지 않았으므로
        이 해석은 데이터 구조와 분석 결과에 근거한 프로젝트의 가정입니다.

        ## 분석 목표

        - Block 특성만 사용하는 Set A 최종 예측모델 구축
        - Set B·C를 통한 사후 결과층 변수 추가 실험
        - 7개 방법의 Position 선택과 Planned Schedule 비교
        - Makespan·Total Delay·Delayed Blocks·Max Delay 비교

        ## 전체 분석 흐름

        `Master Table 생성` → `전처리·EDA` → `회귀모델 비교` → `7개 Scheduling Method 비교`
        → `최종 결론` → `동적 생산일정 시스템 개발 로드맵`

        ### 핵심 결과

        - Position·Initial은 Scheduling Result이므로 최종 Cycle 예측변수에서 제외했습니다.
        - 최종 예측모델은 Block 고유 특성만 사용하는 Set A입니다.
        - EDDQN은 Makespan과 Max Delay가 가장 낮았고, Earliest Start는 Total Delay와 Delayed Blocks가 가장 낮았습니다.
        """
    )
    flow_cards(
        [
            ("데이터 연결", "Block·Result·Position·Initial의 키와 생성 순서 검증"),
            ("Cycle 예측", "스케줄링 전에 알 수 있는 Set A로 Random Forest 구축"),
            ("Result 비교", "Position·Makespan·Delay로 7개 방법 비교"),
            ("개발 확장", "실적 기반 재예측·재스케줄링 순환구조 제안"),
        ]
    )
    analysis_note(
        "이 프로젝트의 핵심은 예측과 Scheduling 평가를 분리한 것입니다. "
        "Cycle Predictor는 Block 특성으로 사전 기준기간을 추정하고, Scheduling Method는 실제 Result의 Position·시간·Delay로 평가합니다.",
        "전체 흐름 해석",
    )
    st.info("프로젝트를 시작한 배경과 개인적인 문제의식은 세부 페이지 `프로젝트를 시작한 이유`에서 확인할 수 있습니다.")

elif page == "1. Master Table":
    master = data["master"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Block", f"{len(master):,}개")
    col2.metric("컬럼", f"{master.shape[1]}개")
    col3.metric("선택 Position", f"{master['position_id'].nunique()}개")
    col4.metric("Initial 연결 Block", f"{master['initial_ship_no'].notna().sum():,}개")

    st.subheader("테이블 연결 구조")
    relations = pd.DataFrame(
        [
            ["Block", "DDQN Result", "index ↔ block sequence no.", "1:1"],
            ["DDQN Result", "Position", "block position id", "N:1"],
            ["Position", "Initial", "block position description", "0..1"],
        ],
        columns=["From", "To", "연결키", "관계"],
    )
    st.dataframe(relations, hide_index=True, width="stretch")
    analysis_note(
        "Block–Result는 검증된 1:1 관계이며 Result–Position은 N:1입니다. Initial은 현재 Block과 직접 연결되지 않아 Position의 초기 기록 여부로만 붙였습니다."
    )
    st.image(ROOT / "Docs" / "images" / "1_master_table_join_erd.svg", width="stretch")
    analysis_note(
        "ERD는 기술적인 연결경로를 보여줍니다. 다만 연결 가능성은 독립변수 사용 가능성과 같지 않으며, 선택 Position은 Result 이후 정보입니다.",
        "ERD 해석",
    )

    st.subheader("Master Table 미리보기")
    st.dataframe(master.head(20), hide_index=True, width="stretch")
    analysis_note(
        "한 행은 하나의 Block과 DDQN이 선택한 Position 결과를 나타냅니다. 이 표는 탐색·결과 비교용이며 최종 Cycle 예측에는 Block 고유 특성만 사용합니다."
    )

elif page == "2. 전처리 및 EDA":
    analysis = data["analysis"]
    derived_columns = [
        "block_area",
        "season",
        "block_start_window",
        "position_area",
        "area_margin_ratio",
        "lifting_load_ratio",
        "initially_occupied",
    ]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("분석 대상", f"{len(analysis):,}개")
    col2.metric("최종 변수", f"{analysis.shape[1]}개")
    col3.metric("파생변수", f"{len(derived_columns)}개")
    col4.metric("Target 결측", f"{analysis['block_processing_cycle'].isna().sum()}개")

    st.subheader("Block Position Cycle 분포")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(analysis["block_processing_cycle"], kde=True, ax=axes[0])
    axes[0].set_title("Block Position Cycle Distribution")
    axes[0].set_xlabel("Block Position Cycle")
    sns.boxplot(x=analysis["block_processing_cycle"], ax=axes[1])
    axes[1].set_title("Block Position Cycle Boxplot")
    axes[1].set_xlabel("Block Position Cycle")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    analysis_note(
        "Cycle은 대부분 15~40일에 모인 우측 편향 분포입니다. 50일 이상 장기값은 연속적인 꼬리로 존재해 삭제하지 않았으며, 장기 구간의 오차 확대 가능성을 모델링에서 확인합니다."
    )

    st.subheader("수치형 변수 상관관계")
    numeric_columns = [
        "block_length",
        "block_width",
        "block_weight",
        "block_area",
        "block_start_window",
        "position_lifting_capacity",
        "position_area",
        "area_margin_ratio",
        "lifting_load_ratio",
        "initially_occupied",
        "block_processing_cycle",
    ]
    fig, ax = plt.subplots(figsize=(11, 8))
    sns.heatmap(
        analysis[numeric_columns].corr(),
        annot=True,
        fmt=".2f",
        cmap=CORRELATION_CMAP,
        vmin=-1,
        vmax=1,
        ax=ax,
    )
    ax.set_title("Correlation Heatmap")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    analysis_note(
        "Block 중량–면적과 중량–인양부하비율처럼 원본 물리량과 파생변수 사이에 높은 상관이 있습니다. "
        "계산 구조에서 생긴 중복이므로 상관계수만으로 변수를 제거하지 않고 모델 성능과 함께 판단합니다."
    )

    st.subheader("범주형 변수별 Cycle 분포")
    category_columns = [
        "block_ship_no",
        "block_type",
        "season",
        "position_primary_area",
        "position_block_type",
        "position_attribute",
    ]
    category = st.selectbox("범주형 변수", category_columns)
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.boxplot(
        data=analysis,
        x=category,
        y="block_processing_cycle",
        hue=category,
        palette="Set2",
        legend=False,
        ax=ax,
    )
    ax.set_title(f"{category} vs Block Position Cycle")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    category_median = analysis.groupby(category, observed=True)["block_processing_cycle"].median().sort_values(ascending=False)
    top_category = str(category_median.index[0])
    bottom_category = str(category_median.index[-1])
    caution = (
        " Position은 DDQN의 선택 결과이므로 원인 효과가 아닌 사후 연관성으로만 해석합니다."
        if category.startswith("position_")
        else " 범주별 표본 구성과 다른 변수의 영향을 함께 고려해야 합니다."
    )
    analysis_note(
        f"중앙값은 {top_category} 범주가 가장 높고 {bottom_category} 범주가 가장 낮지만, Boxplot의 분포가 상당 부분 겹칩니다.{caution}"
    )

    with st.expander("IQR 이상치 후보 변수 Boxplot"):
        check_columns = [
            "block_length",
            "block_width",
            "block_start_window",
            "block_area",
            "block_processing_cycle",
        ]
        fig, axes = plt.subplots(2, 3, figsize=(16, 6))
        axes = axes.flatten()
        for index, column in enumerate(check_columns):
            axes[index].boxplot(analysis[column].dropna(), vert=False)
            axes[index].set_title(column)
            axes[index].set_yticks([])
        fig.delaxes(axes[-1])
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        analysis_note(
            "IQR 기준 후보는 존재하지만 대부분 분포의 연속적인 꼬리에 있습니다. 대형 Block·장기 작업일 가능성이 있어 일괄 제거하지 않았습니다."
        )

    st.subheader("독립변수 세트")
    st.dataframe(feature_sets, hide_index=True, width="stretch")
    analysis_note(
        "Set A는 최종 사전 예측용이고 Set B/C는 DDQN 결과층 정보를 붙인 진단 실험입니다. 변수 수가 늘어도 RMSE가 개선되지 않았다는 점보다 예측시점 이후 정보가 포함됐다는 점이 더 중요합니다."
    )

elif page == "3. 회귀모델":
    final_test_metrics = data["modeling_summary"]["test_metrics"]

    st.subheader("최종 Set A 모델 Test 성능")
    compact_metrics(
        [
            ("MAE", f"{final_test_metrics['MAE']:.3f}", "Lower is better"),
            ("RMSE", f"{final_test_metrics['RMSE']:.3f}", "Lower is better"),
            ("R²", f"{final_test_metrics['R2']:.3f}", "Higher is better"),
        ]
    )
    st.caption(
        "튜닝 전 Random Forest 후보의 RMSE는 4.489였고, "
        "GridSearchCV로 선택한 최종 모델은 4.558이었습니다. "
        "튜닝이 별도 Test 성능 향상을 보장하지 않는다는 점을 함께 표시합니다."
    )
    analysis_note(
        "최종 Set A 모델은 Test Cycle 변동의 약 76.7%를 설명하며 RMSE는 약 4.56일입니다. "
        "튜닝 전 후보보다 Test 성능이 소폭 낮아, GridSearchCV 결과를 과장하지 않고 그대로 기록했습니다."
    )

    st.subheader("변수 세트 비교")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(
        data=feature_sets,
        x="RMSE",
        y="Variable Set",
        hue="Variable Set",
        palette=["#034EA2", "#008C95", "#7B61A8"],
        legend=False,
        width=0.45,
        ax=ax,
    )
    ax.set_xlim(4.3, 5.2)
    ax.set_xlabel("RMSE (Lower is Better)")
    ax.set_ylabel("Variable Set")
    ax.set_title("Variable Set Comparison — Random Forest")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.dataframe(feature_sets, hide_index=True, width="stretch")
    analysis_note(
        "동일한 Random Forest에서 Set A가 가장 낮은 RMSE를 보였습니다. Set B/C의 하락은 Position이 유용하지 않다는 증거가 아니라, DDQN 실행 뒤 결정되는 결과층 정보를 예측 입력에 섞은 설계 문제를 발견한 계기입니다."
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Set A 후보모델 비교 · 튜닝 전")
        st.dataframe(models, hide_index=True, width="stretch")
        analysis_note(
            f"{models.iloc[0]['Model']}가 RMSE {models.iloc[0]['RMSE']:.3f}, R² {models.iloc[0]['R2']:.3f}로 가장 우수했습니다. "
            "선형모델보다 비선형 모델이 Block 특성과 Cycle의 관계를 더 잘 설명했습니다."
        )
    with right:
        st.subheader("주요 변수 중요도")
        top_n = st.slider("표시할 변수 수", 5, 20, 10)
        slider_progress = (top_n - 5) / (20 - 5) * 100
        st.markdown(
            f"""
            <style>
            [data-testid="stSlider"] > div[role="group"] > div > div:first-child {{
                background: linear-gradient(
                    to right,
                    #034EA2 0%,
                    #034EA2 {slider_progress:.4f}%,
                    rgba(151, 166, 195, 0.25) {slider_progress:.4f}%,
                    rgba(151, 166, 195, 0.25) 100%
                ) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        importance = data["importance"].nlargest(top_n, "importance")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=importance,
            x="importance",
            y="feature",
            order=importance["feature"],
            hue="feature",
            palette=sns.color_palette("Blues_r", n_colors=len(importance)),
            legend=False,
            ax=ax,
        )
        ax.set_title(f"Top {top_n} Feature Importance")
        ax.set_xlabel("Feature Importance")
        ax.set_ylabel("Feature")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Test 데이터 기준 Cycle과 예측 Cycle")
    model_comparison = data["test"].sort_values(
        "reference_cycle"
    ).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(
        model_comparison.index,
        model_comparison["reference_cycle"],
        color=REFERENCE_COLOR,
        linewidth=1.8,
        label="Reference Cycle",
    )
    ax.plot(
        model_comparison.index,
        model_comparison["predicted_cycle"],
        color=PREDICTED_COLOR,
        marker="o",
        markersize=3,
        linewidth=1.2,
        label="Predicted Cycle",
    )
    ax.set_xlabel("Test Blocks Sorted by Reference Cycle")
    ax.set_ylabel("Block Position Cycle")
    ax.set_title("Reference Cycle vs Predicted Cycle")
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    analysis_note(
        "전체 중앙값 잔차는 -0.1일로 대부분의 Block에서는 예측 편향이 크지 않았습니다. "
        "그러나 기준 Cycle이 길어질수록 과소예측이 뚜렷해졌습니다. 특히 40일 이상인 "
        "14개 Block은 모두 과소예측되었으며, 평균적으로 기준 Cycle보다 약 9.8일 짧게 "
        "예측되었습니다. 이는 최종 Random Forest 모델이 중간 Cycle 구간의 일반적인 패턴은 "
        "비교적 잘 학습했지만, 표본이 적은 장기 Cycle 구간에서는 예측값이 전체 평균 방향으로 "
        "수축되는 경향이 있음을 보여줍니다."
    )

    st.subheader("잔차 분석")
    residual_data = data["test"].copy()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.scatterplot(data=residual_data, x="predicted_cycle", y="residual", color="#034EA2", alpha=.7, ax=axes[0])
    axes[0].axhline(0, color="#7D8A99", linestyle="--", linewidth=1)
    axes[0].set_title("Residual vs Predicted Cycle")
    sns.histplot(residual_data["residual"], kde=True, color="#2D7D8C", ax=axes[1])
    axes[1].axvline(0, color="#7D8A99", linestyle="--", linewidth=1)
    axes[1].set_title("Residual Distribution")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    high_cycle_error = residual_data.nlargest(max(1, len(residual_data) // 5), "reference_cycle")["absolute_error"].mean()
    overall_error = residual_data["absolute_error"].mean()
    analysis_note(
        f"전체 MAE는 {overall_error:.2f}일이며 기준 Cycle 상위 20% 구간의 평균 절대오차는 {high_cycle_error:.2f}일입니다. "
        "잔차가 완전히 일정하지 않으므로 장기 Cycle을 위한 추가 데이터와 별도 검증이 필요합니다."
    )

elif page == "4. 스케줄링 비교":
    schedule_view = st.radio("분석 화면", ["방법 요약", "Block 상세조회"], horizontal=True)

    if schedule_view == "방법 요약":
        st.subheader("Scheduling Method 결과 요약")
        best_makespan = schedule.iloc[0]
        best_total_delay = delay.iloc[0]
        best_max_delay = delay.sort_values("Max_Delay").iloc[0]
        compact_metrics(
            [
                ("최단 Makespan", f"{best_makespan['Makespan_Days']:,.0f}일", best_makespan["Method"]),
                ("최저 Total Delay", f"{best_total_delay['Total_Delay']:,.0f}일", best_total_delay["Method"]),
                ("최소 Delayed Blocks", f"{delay.sort_values('Delayed_Blocks').iloc[0]['Delayed_Blocks']:,.0f}개", delay.sort_values("Delayed_Blocks").iloc[0]["Method"]),
                ("최저 Max Delay", f"{best_max_delay['Max_Delay']:,.0f}일", best_max_delay["Method"]),
            ]
        )

        fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
        sns.barplot(
            data=schedule, x="Makespan_Days", y="Method", hue="Method",
            palette=METHOD_COLORS, legend=False, ax=axes[0]
        )
        axes[0].set_title("Makespan")
        axes[0].set_xlabel("Days (Lower is Better)")
        sns.barplot(
            data=delay, x="Total_Delay", y="Method", hue="Method",
            palette=METHOD_COLORS, legend=False, ax=axes[1]
        )
        axes[1].set_title("Total Positive Delay")
        axes[1].set_ylabel("")
        sns.barplot(
            data=delay.sort_values("Max_Delay"), x="Max_Delay", y="Method", hue="Method",
            palette=METHOD_COLORS, legend=False, ax=axes[2]
        )
        axes[2].set_title("Maximum Delay")
        axes[2].set_ylabel("")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        analysis_note(
            "EDDQN은 Makespan과 Max Delay가 가장 낮고, Earliest Start는 Total Delay와 Delayed Blocks가 가장 낮습니다. "
            "세 지표의 최선이 한 방법에 모이지 않으므로 평가목적에 따라 우선순위가 달라집니다."
        )

        st.subheader("방법 간 동일 Position 선택 비율")
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.heatmap(data["match"].astype(float), annot=True, fmt=".2f", vmin=0, vmax=1, cmap="Blues", ax=ax)
        ax.set_title("Same Position Selection Rate")
        ax.set_xlabel("Scheduling Method")
        ax.set_ylabel("Scheduling Method")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        off_diagonal = data["match"].where(~np.eye(len(data["match"]), dtype=bool)).stack()
        analysis_note(
            f"서로 다른 방법의 동일 Position 선택률은 평균 {off_diagonal.mean():.1%}입니다. "
            "대부분의 Block이 방법에 따라 다른 Position에 배정되므로 Scheduling Method가 실제 공간 배치를 바꾸는 의사결정 규칙임을 확인할 수 있습니다."
        )

        st.subheader("Position 선택 특성")
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        sns.barplot(
            data=data["position"], x="Mean_Area_Margin_Ratio", y="Method",
            hue="Method", palette=METHOD_COLORS, legend=False, width=0.45, ax=axes[0]
        )
        axes[0].set_xlim(0.40, 0.45)
        axes[0].set_title("Mean Area Margin Ratio")
        sns.barplot(
            data=data["position"], x="Initially_Occupied_Assignments", y="Method",
            hue="Method", palette=METHOD_COLORS, legend=False, width=0.45, ax=axes[1]
        )
        axes[1].set_title("Assignments to Initial-recorded Positions")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        analysis_note(
            "평균 면적 여유비율의 차이는 크지 않지만 Initial 기록 Position 배정 건수는 방법마다 다릅니다. "
            "이는 선택 결과의 특성이며 사전 Cycle 변화의 원인으로 해석하지 않습니다."
        )

        st.subheader("구역별 Position 배정 비율")
        area_share = data["area_share"].set_index("method").loc[SCHEDULING_METHODS]
        fig, ax = plt.subplots(figsize=(12, 4.8))
        area_share.plot(
            kind="barh",
            stacked=True,
            color=["#034EA2", "#6B5AA6", "#2D7D8C"],
            ax=ax,
        )
        ax.set_xlabel("Assignment Share")
        ax.set_ylabel("Scheduling Method")
        ax.set_xlim(0, 1)
        ax.legend(["블록 조립 구역", "곡면 구역", "플랫폼 구역"], loc="lower center", bbox_to_anchor=(.5, 1), ncol=3)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        analysis_note(
            "모든 방법에서 플랫폼 구역의 배정 비율이 가장 높지만, 곡면·블록 조립 구역의 비중은 방법별로 달라집니다. "
            "같은 60개 Position을 사용해도 공간별 수요 분포가 동일하지 않다는 뜻입니다."
        )

        with st.expander("Position 선택 분석 전문", expanded=True):
            st.markdown(strip_section_numbers(notebook_sections["4.3 선택 Position 비교"]))
        with st.expander("Planned Schedule과 Makespan 분석 전문", expanded=True):
            st.markdown(strip_section_numbers(notebook_sections["4.4 Planned Schedule과 Makespan 비교"]))
        with st.expander("Delay 분석 전문", expanded=True):
            st.markdown(strip_section_numbers(notebook_sections["4.5 Delay 성과 비교"]))
        with st.expander("스케줄링 비교 결론 전문", expanded=True):
            st.markdown(strip_section_numbers(notebook_sections["4.7 결론"]))

    else:
        st.subheader("동일 Block의 7개 스케줄링 결과 비교")
        detail = data["detail"]
        block_index = st.selectbox("Block index", sorted(detail["block_index"].unique()))
        block = detail.loc[detail["block_index"].eq(block_index)].copy()

        col1, col2, col3 = st.columns(3)
        col1.metric("기준 Cycle", f"{block.iloc[0]['block_processing_cycle']:.0f}일")
        col2.metric("선박번호", block.iloc[0]["block_ship_no"])
        col3.metric("Block Type", block.iloc[0]["block_type"])

        columns = [
            "method",
            "position_id",
            "position_description",
            "planned_start_time",
            "planned_finish_time",
            "planned_duration_days",
            "delay_days",
            "initially_occupied",
        ]
        st.dataframe(block[columns].sort_values("delay_days"), hide_index=True, width="stretch")
        position_count = block["position_id"].nunique()
        delay_range = block["delay_days"].max() - block["delay_days"].min()
        analysis_note(
            f"같은 Block에 대해 7개 방법은 {position_count}개의 서로 다른 Position을 선택했고 Delay 범위는 {delay_range:.0f}일입니다. "
            "Cycle은 동일한 사전 입력이지만 배치와 계획 결과는 방법에 따라 달라집니다."
        )

        with st.expander("선택한 Block의 전체 데이터"):
            st.dataframe(block, hide_index=True, width="stretch")
            st.caption("Block 고유 특성은 7개 행에서 같고, method·position·planned schedule·delay가 방법별 Result로 달라집니다.")

elif page == "5. 최종 결론":
    col1, col2, col3, col4 = st.columns(4)
    final_summary = data["modeling_summary"]
    col1.metric("최종 Set A RMSE", f"{final_summary['test_metrics']['RMSE']:.2f}")
    col2.metric("최종 모델", final_summary["final_model"])
    col3.metric(f"최단 Makespan · {schedule.iloc[0]['Method']}", f"{schedule.iloc[0]['Makespan_Days']:,.0f}일")
    col4.metric(f"최저 Total Delay · {delay.iloc[0]['Method']}", f"{delay.iloc[0]['Total_Delay']:,.0f}일")

    st.subheader("프로젝트 결론")
    st.markdown(
        """
        - 선택 Position은 Block 고유 속성이 아니라 Scheduling Result라는 논리 오류를 발견했습니다.
        - 최종 Cycle 예측모델을 **Set A(Block 고유 특성)**로 수정했습니다.
        - Set B/C는 DDQN 결과층 정보를 사후에 추가한 탐색 실험으로만 유지했습니다.
        - **EDDQN**은 Makespan과 Max Delay가 가장 낮았습니다.
        - **Earliest Start**는 Total Delay와 Delayed Blocks가 가장 낮았습니다.
        - Scheduling Method는 예측 RMSE가 아니라 실제 Position·시간·Delay 결과로 비교해야 합니다.
        """
    )
    flow_cards(
        [
            ("예상 밖 결과", "Position을 추가한 Set B/C의 성능 하락"),
            ("논리 재검토", "Cycle은 사전 입력·선택 Position은 Result"),
            ("최종 예측", "Set A + Random Forest"),
            ("방법 비교", "Position·Makespan·Delay의 다기준 평가"),
        ]
    )
    analysis_note(
        "프로젝트의 가장 큰 성과는 모델 점수 자체보다 데이터 생성 순서를 재검토해 예측 입력과 Scheduling Result를 분리한 것입니다."
    )

    st.subheader("7개 방법 종합 비교")
    summary = comparison[
        ["Method", "Makespan_Days", "Total_Delay", "Delayed_Blocks", "Delay_Rate", "Max_Delay"]
    ].sort_values(["Makespan_Days", "Total_Delay"])
    st.dataframe(summary, hide_index=True, width="stretch")
    analysis_note(
        "EDDQN은 Makespan과 Max Delay, Earliest Start는 Total Delay와 Delayed Blocks에서 각각 가장 좋습니다. "
        "따라서 단일 1등보다 운영 목적에 맞는 방법을 선택하는 Trade-off 문제로 해석합니다."
    )

    st.subheader("Makespan과 Total Delay의 Trade-off")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(
        data=comparison,
        x="Makespan_Days",
        y="Total_Delay",
        hue="Method",
        palette=METHOD_COLORS,
        s=110,
        ax=ax,
    )
    for _, row in comparison.iterrows():
        ax.annotate(row["Method"], (row["Makespan_Days"], row["Total_Delay"]), xytext=(5, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Makespan (Days · Lower is Better)")
    ax.set_ylabel("Total Delay (Lower is Better)")
    ax.legend().remove()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    analysis_note(
        "왼쪽 아래일수록 두 지표가 함께 좋습니다. EDDQN과 Earliest Start가 서로 다른 축에서 강점을 보여, 목적함수와 허용 가능한 지연 위험을 함께 정해야 합니다."
    )
    st.info(
        "Cycle은 7개 방법에 공통으로 주어진 사전 입력입니다. "
        "방법 비교에는 Result에서 직접 계산한 Makespan·Delay·Position 지표만 사용합니다."
    )

    with st.expander("한계 및 향후 과제"):
        st.markdown(
            """
            - 실제 현장에서 측정된 실적 Cycle과 비용 데이터가 없습니다.
            - Initial Table에 없는 Position을 초기 비점유로 처리한 가정이 포함됩니다.
            - 실제 Yard 좌표가 없어 평면도는 개념도입니다.
            - 다른 조선소·기간·운영조건에서 외부 재현 검증이 필요합니다.
            """
        )

else:
    roadmap = pd.DataFrame(
        [
            [1, "완료", "데이터 구조·종속변수·평가지표 이해 및 7개 방법 비교"],
            [2, "다음 개발", "7개 Scheduling Result를 비교하는 3D Result Viewer MVP"],
            [3, "중기", "분류·군집·이상탐지를 추가한 Scheduling Analyzer"],
            [4, "장기", "실제 실적을 반영한 Dynamic Scheduling"],
            [5, "구현 중", "Calendar-it을 통한 개인·팀 업무일정 연결"],
            [6, "장기", "ERP 관점의 자원·자재원가 연결"],
            [7, "최종 확장", "MES 현장실적과 재예측·재스케줄링의 순환구조"],
        ],
        columns=["Phase", "상태", "핵심 목표"],
    )
    st.subheader("3D Scheduling Result Viewer · UI Mockup")
    roadmap_mockups = {
        "전체 야드 스케줄링 구성": "d2d9193e-3fe5-4cb9-917f-54086e6711c7.png",
        "방법 선택과 구역별 상세 활용": "fac1f1d7-707f-4161-8878-6a860b1f0eab.png",
    }
    selected_roadmap_mockup = st.radio(
        "목업 화면 선택",
        list(roadmap_mockups),
        horizontal=True,
        key="roadmap_mockup_screen",
    )
    _, roadmap_image_column, _ = st.columns([0.1, 0.8, 0.1])
    with roadmap_image_column:
        st.image(
            ROOT / "Docs" / "images" / roadmap_mockups[selected_roadmap_mockup],
            caption=selected_roadmap_mockup,
            width="stretch",
        )
    st.caption(
        "공개 데이터에는 실제 야드 3D 좌표가 없으므로, 위 이미지는 분석 결과가 아니라 "
        "향후 개발할 Scheduling Result Viewer의 화면 구성과 활용 방식을 설명하기 위한 목업입니다."
    )

    st.subheader("다음 단계 — 3D Scheduling Result Viewer MVP")
    st.markdown(
        """
        **MVP(Minimum Viable Product)**는 핵심 기능만 먼저 구현해 활용 가능성과 개발 방향을 확인하는 초기 버전입니다.

        이번 단계에서는 새로운 스케줄을 생성하지 않고 다음 기능에 집중합니다.

        1. 7개 Scheduling Method 선택
        2. Block–Position 배치 확인
        3. 시간 시점 또는 기간 선택
        4. 공간·시간 Scheduling View 표시
        5. 선택한 Block의 Cycle·Delay·Position 정보 확인
        """
    )

    st.subheader("단계별 개발 로드맵")
    st.dataframe(roadmap, hide_index=True, width="stretch")
    analysis_note(
        "현재 완료된 것은 데이터 해석·Cycle 예측·Result 비교입니다. 실제 좌표와 현장 실적이 없는 상태에서 바로 가능한 다음 단계는 기존 Result를 비교하는 Viewer MVP입니다."
    )
