"""Build the read-only artifacts used by the presentation Streamlit app.

Run from the project root:
    python scripts/build_precomputed_results.py

The notebooks remain the source of the analysis logic.  This script packages
their saved outputs into fast-to-load pickle files and renders every chart that
does not change during the presentation.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
MODEL_DIR = ROOT / "outputs" / "3_modeling"
SCHEDULE_DIR = ROOT / "outputs" / "4_scheduling_comparison"
RAW_INPUT_DIR = ROOT / "Data of Ship Block Scheduling in English" / "Raw_input_ Data"
RESULT_DIR = ROOT / "Data of Ship Block Scheduling in English" / "Result"
PRECOMPUTED_DIR = ROOT / "precomputed"
CHART_DIR = PRECOMPUTED_DIR / "charts"
RESULT_CACHE_DIR = PRECOMPUTED_DIR / "scheduling_results"
TABLE_DIR = PRECOMPUTED_DIR / "tables"

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
    "DDQN": "#7EA6D8",
    "EDDQN": "#1E5A96",
    "Earliest Start": "#806BA6",
    "Longest Processing": "#218A8D",
    "Resource Utilization": "#3E7D3C",
    "Response Time": "#C28B12",
    "Shortest Processing": "#737780",
}
CORRELATION_CMAP = LinearSegmentedColormap.from_list(
    "presentation_correlation",
    ["#5F6873", "#F8FAFC", "#0B5AA6"],
)


def configure_plot_style() -> None:
    available = {font.name for font in font_manager.fontManager.ttflist}
    font = next(
        (
            candidate
            for candidate in ["Malgun Gothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "NanumGothic"]
            if candidate in available
        ),
        "DejaVu Sans",
    )
    plt.rcParams.update(
        {
            "font.family": font,
            "axes.unicode_minus": False,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    sns.set_theme(style="whitegrid", font=font)


def save_figure(fig: plt.Figure, name: str, dpi: int = 180) -> None:
    fig.savefig(
        CHART_DIR / name,
        dpi=dpi,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)


def portable_table_path(name: str) -> Path:
    """Use JSON-table files rather than pandas pickles for runtime portability."""
    safe_name = name.replace(" ", "_").replace("/", "_")
    return TABLE_DIR / f"{safe_name}.json"


def write_portable_table(name: str, frame: pd.DataFrame) -> None:
    """Serialize a DataFrame without binding it to a pandas/NumPy pickle ABI."""
    portable_frame = frame.rename_axis("method").reset_index() if name == "match" else frame
    portable_frame.to_json(
        portable_table_path(name),
        orient="table",
        date_format="iso",
        force_ascii=False,
        index=False,
    )


def load_app_data() -> dict:
    detail = pd.read_csv(SCHEDULE_DIR / "4_schedule_detail.csv")
    for column in ["planned_start_time", "planned_finish_time", "latest_completion_time"]:
        detail[column] = pd.to_datetime(detail[column])
    with open(MODEL_DIR / "3_modeling_summary.json", encoding="utf-8") as file:
        modeling_summary = json.load(file)
    analysis = pd.read_csv(PROCESSED_DIR / "analysis_DDQN.csv")
    model = joblib.load(MODEL_DIR / "3_final_model.joblib")
    analysis["set_a_prediction"] = model.predict(analysis[SET_A_FEATURES])
    prediction_map = analysis.set_index("block_index")["set_a_prediction"]
    detail["set_a_prediction"] = detail["block_index"].map(prediction_map)
    return {
        "schema_version": "precomputed_2026_08_19_v1",
        "master": pd.read_csv(PROCESSED_DIR / "master_DDQN.csv"),
        "analysis": analysis,
        "positions": pd.read_excel(ROOT / "data" / "source" / "block_position_information.xlsx"),
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


def build_fast_data_files(data: dict) -> None:
    # JSON table artifacts are intentionally the primary runtime format.  Pandas
    # pickles contain internal NumPy datetime objects and can fail when a cloud
    # runtime uses a different Python/NumPy build than the build machine.
    app_table_names = [
        "master", "analysis", "positions", "feature_sets", "baseline", "models",
        "importance", "test", "delay", "schedule", "position", "area_share", "match", "detail",
    ]
    for name in app_table_names:
        write_portable_table(name, data[name])
    (TABLE_DIR / "app_data_manifest.json").write_text(
        json.dumps(
            {"schema_version": data["schema_version"], "tables": app_table_names},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (PRECOMPUTED_DIR / "modeling_summary.json").write_text(
        json.dumps(data["modeling_summary"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    raw_tables = {
        "block": pd.read_excel(RAW_INPUT_DIR / "block_information_table.xlsx"),
        "position": pd.read_excel(RAW_INPUT_DIR / "block_position_information.xlsx"),
        "initial": pd.read_excel(RAW_INPUT_DIR / "initial_block_position_information.xlsx"),
    }
    raw_table_names = []
    for name, frame in raw_tables.items():
        table_name = f"raw_{name}"
        write_portable_table(table_name, frame)
        raw_table_names.append(table_name)
    (TABLE_DIR / "raw_input_manifest.json").write_text(
        json.dumps({"tables": raw_table_names}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for method, filename in RESULT_FILES.items():
        frame = pd.read_excel(RESULT_DIR / filename)
        write_portable_table(f"result_{method}", frame)
        scheduled = pd.read_excel(RESULT_DIR / filename, sheet_name="Scheduled Segments")
        write_portable_table(f"scheduled_{method}", scheduled)

    data["models"].to_csv(PRECOMPUTED_DIR / "model_metrics.csv", index=False, encoding="utf-8-sig")
    data["importance"].to_csv(PRECOMPUTED_DIR / "feature_importance.csv", index=False, encoding="utf-8-sig")
    analysis = data["analysis"]
    target = analysis["block_processing_cycle"]
    schedule = data["schedule"].sort_values("Makespan_Days")
    delay = data["delay"].sort_values("Total_Delay")
    summary = {
        "records": int(len(analysis)),
        "target_median": float(target.median()),
        "target_mean": float(target.mean()),
        "target_min": float(target.min()),
        "target_max": float(target.max()),
        "test_metrics": data["modeling_summary"]["test_metrics"],
        "best_makespan": schedule.iloc[0].to_dict(),
        "best_total_delay": delay.iloc[0].to_dict(),
        "best_max_delay": data["delay"].sort_values("Max_Delay").iloc[0].to_dict(),
    }
    (PRECOMPUTED_DIR / "summary_stats.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_eda_charts(data: dict) -> None:
    analysis = data["analysis"]
    labels = {
        "block_length": "Block 길이",
        "block_width": "Block 폭",
        "block_start_window": "시작 가능 구간",
        "block_area": "Block 면적",
        "block_processing_cycle": "Block Position Cycle",
    }
    check_columns = list(labels)
    fig, axes = plt.subplots(1, len(check_columns), figsize=(15, 3.35))
    fig.patch.set_facecolor("#FFFFFF")
    for axis, column in zip(axes, check_columns):
        sns.boxplot(
            x=analysis[column].dropna(), ax=axis, color="#8CBCE8", width=.42, linewidth=1.15,
            medianprops={"color": "#034EA2", "linewidth": 2.2},
            whiskerprops={"color": "#58738F", "linewidth": 1.15},
            capprops={"color": "#58738F", "linewidth": 1.15},
            flierprops={"marker": "o", "markersize": 4, "markerfacecolor": "#F59E0B", "markeredgecolor": "#FFFFFF", "markeredgewidth": .6, "alpha": .95},
        )
        axis.set_facecolor("#F8FAFC")
        axis.set_title(labels[column], fontsize=10.5, fontweight="bold", color="#102A43", pad=11)
        axis.set(yticks=[], ylabel="", xlabel="")
        axis.grid(axis="x", color="#DCE6F0", linestyle="--", linewidth=.8)
        axis.tick_params(axis="x", labelsize=8, colors="#52657A", length=0, pad=6)
        for spine in ["top", "right", "left"]:
            axis.spines[spine].set_visible(False)
        axis.spines["bottom"].set_color("#D6E0EA")
    fig.tight_layout()
    save_figure(fig, "eda_outliers.png")

    target = analysis["block_processing_cycle"]
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
    sns.histplot(target, kde=True, color="#034EA2", edgecolor="#FFFFFF", linewidth=.5, ax=axes[0])
    axes[0].set(title="Block Position Cycle Distribution", xlabel="Cycle (일)", ylabel="Block 수")
    axes[0].title.set_fontweight("bold")
    sns.boxplot(x=target, color="#8CBCE8", width=.42, ax=axes[1])
    axes[1].set(title="Block Position Cycle Boxplot", xlabel="Cycle (일)")
    axes[1].title.set_fontweight("bold")
    fig.tight_layout()
    save_figure(fig, "eda_target_distribution.png")

    numeric_columns = [
        "block_length", "block_width", "block_weight", "block_area", "block_start_window",
        "position_lifting_capacity", "position_area", "area_margin_ratio", "lifting_load_ratio",
        "initially_occupied", "block_processing_cycle",
    ]
    fig, ax = plt.subplots(figsize=(7.0, 5.25), dpi=220)
    heatmap = sns.heatmap(
        analysis[numeric_columns].corr(), annot=True, fmt=".2f", cmap=CORRELATION_CMAP,
        vmin=-1, vmax=1, square=True, linewidths=.35, linecolor="#FFFFFF",
        annot_kws={"size": 7.2}, cbar_kws={"shrink": .78, "aspect": 22, "pad": .035}, ax=ax,
    )
    heatmap.collections[0].colorbar.ax.tick_params(labelsize=7, length=2.2, pad=2)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right", fontsize=7)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=7)
    fig.tight_layout(pad=.8)
    save_figure(fig, "eda_numeric_correlation.png", dpi=220)

    category_columns = [
        "block_ship_no", "block_type", "season", "position_primary_area",
        "position_block_type", "position_attribute",
    ]
    category_labels = {
        "block_ship_no": "선체 번호", "block_type": "Block 유형", "season": "계절",
        "position_primary_area": "Position 주 구역", "position_block_type": "Position Block 유형",
        "position_attribute": "Position 속성",
    }
    fig, axes = plt.subplots(2, 3, figsize=(13.2, 4.15))
    for axis, column in zip(axes.flatten(), category_columns):
        sns.boxplot(data=analysis, x=column, y="block_processing_cycle", color="#8CBCE8", width=.55, fliersize=2.5, ax=axis)
        axis.set_title(category_labels[column], fontsize=10, fontweight="bold")
        axis.set_xlabel("")
        axis.set_ylabel("Cycle (일)" if column in {"block_ship_no", "position_primary_area"} else "")
        values = [str(label.get_text()) for label in axis.get_xticklabels()]
        wrapped = [" ".join(value.split()[:-1]) + "\n" + value.split()[-1] if len(value.split()) > 1 else value for value in values]
        axis.set_xticks(axis.get_xticks(), wrapped, rotation=0, ha="center", fontsize=7.2)
        axis.grid(axis="y", alpha=.2)
    fig.tight_layout(pad=.65, h_pad=.85)
    save_figure(fig, "eda_categorical_distribution.png")


def build_regression_charts(data: dict) -> None:
    feature_sets = data["feature_sets"].sort_values("RMSE")
    fig, ax = plt.subplots(figsize=(7.8, 3.55), dpi=180)
    sns.barplot(data=feature_sets, x="RMSE", y="Variable Set", hue="Variable Set", palette=["#034EA2", "#008C95", "#7B61A8"], legend=False, width=.45, ax=ax)
    ax.set_xlim(4.3, 5.2)
    ax.set_xlabel("RMSE (Lower is Better)", fontsize=8)
    ax.set_ylabel("Variable Set", fontsize=8)
    ax.tick_params(axis="both", labelsize=7.5)
    fig.tight_layout()
    save_figure(fig, "regression_feature_set_rmse.png", dpi=180)

    test = data["test"]
    comparison = test.sort_values("reference_cycle").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(14, 4.4))
    ax.plot(comparison.index, comparison["reference_cycle"], color="#7D8A99", linewidth=1.8, label="Reference Cycle")
    ax.plot(comparison.index, comparison["predicted_cycle"], color="#2D7D8C", linewidth=1.2, label="Predicted Cycle")
    ax.set_xlabel("Test Blocks Sorted by Reference Cycle")
    ax.set_ylabel("Block Position Cycle")
    ax.legend()
    fig.tight_layout()
    save_figure(fig, "regression_prediction_result.png")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
    sns.scatterplot(data=test, x="predicted_cycle", y="residual", color="#034EA2", alpha=.7, ax=axes[0])
    axes[0].axhline(0, color="#7D8A99", linestyle="--")
    axes[0].set(title="예측 Cycle별 잔차", xlabel="예측 Cycle(일)", ylabel="잔차(일)")
    sns.histplot(test["residual"], kde=True, color="#2D7D8C", ax=axes[1])
    axes[1].axvline(0, color="#7D8A99", linestyle="--")
    axes[1].set(title="잔차 분포", xlabel="잔차(일)", ylabel="Block 수")
    fig.tight_layout()
    save_figure(fig, "regression_residuals.png")

    for top_n in range(5, 21):
        importance = data["importance"].nlargest(top_n, "importance")
        fig, ax = plt.subplots(figsize=(9, max(3.7, len(importance) * .34)))
        sns.barplot(data=importance, x="importance", y="feature", color="#034EA2", ax=ax)
        ax.set(xlabel="Feature Importance", ylabel="Feature")
        fig.tight_layout()
        save_figure(fig, f"feature_importance_{top_n}.png")


def build_scheduling_charts(data: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 6.5), dpi=150, gridspec_kw={"width_ratios": [1.08, 1]})
    sns.heatmap(data["match"].astype(float), annot=True, fmt=".2f", vmin=0, vmax=1, cmap="Blues", square=True, ax=axes[0])
    axes[0].set(title="Same Position Selection Rate", xlabel="Scheduling Method", ylabel="Scheduling Method")
    area_share = data["area_share"].set_index("method").loc[SCHEDULING_METHODS]
    area_share.plot(kind="barh", stacked=True, color=["#034EA2", "#6B5AA6", "#2D7D8C"], ax=axes[1])
    axes[1].set(title="Position Assignment Share by Area", xlabel="Assignment Share", ylabel="", xlim=(0, 1))
    axes[1].legend(["블록 조립 구역", "곡면 구역", "플랫폼 구역"], loc="upper center", bbox_to_anchor=(.5, -.17), ncol=3, fontsize=8)
    fig.tight_layout()
    fig.subplots_adjust(bottom=.20)
    save_figure(fig, "scheduling_position_comparison.png", dpi=150)

    fig, axes = plt.subplots(3, 2, figsize=(14.8, 8.1), dpi=135)
    position_by_area = data["position"].sort_values("Mean_Area_Margin_Ratio")
    sns.barplot(data=position_by_area, x="Mean_Area_Margin_Ratio", y="Method", hue="Method", palette=METHOD_COLORS, legend=False, ax=axes[0, 0])
    axes[0, 0].set(xlim=(.40, .45), title="Mean Area Margin Ratio · 파생변수", ylabel="")
    initial = data["position"].sort_values("Initially_Occupied_Assignments")
    sns.barplot(data=initial, x="Initially_Occupied_Assignments", y="Method", hue="Method", palette=METHOD_COLORS, legend=False, ax=axes[0, 1])
    axes[0, 1].set(title="Assignments to Initial-recorded Positions · 파생변수", ylabel="")
    schedule = data["schedule"].sort_values("Makespan_Days")
    sns.barplot(data=schedule, x="Makespan_Days", y="Method", hue="Method", palette=METHOD_COLORS, legend=False, ax=axes[1, 0])
    axes[1, 0].set(title="Makespan", xlabel="Days (Lower is Better)", ylabel="")
    delay = data["delay"].sort_values("Total_Delay")
    sns.barplot(data=delay, x="Total_Delay", y="Method", hue="Method", palette=METHOD_COLORS, legend=False, ax=axes[1, 1])
    axes[1, 1].set(title="Total Positive Delay", xlabel="Days (Lower is Better)", ylabel="")
    max_delay = data["delay"].sort_values("Max_Delay")
    sns.barplot(data=max_delay, x="Max_Delay", y="Method", hue="Method", palette=METHOD_COLORS, legend=False, ax=axes[2, 0])
    axes[2, 0].set(title="Maximum Delay", xlabel="Days (Lower is Better)", ylabel="")
    axes[2, 1].axis("off")
    axes[2, 1].text(
        0, .98,
        "• Mean Area Margin Ratio [파생변수]\n  Position 면적 대비 Block 배치 후 남는 공간의 평균 비율\n\n"
        "• Initial-recorded Position Assignments [파생변수]\n  Initial Table에 기록된 Position으로 배정된 건수\n\n"
        "• Makespan: 전체 작업이 끝나는 데 걸린 총 기간\n"
        "• Total Positive Delay: 지연이 발생한 일수의 합계\n"
        "• Maximum Delay: 단일 Block에서 발생한 최대 지연",
        transform=axes[2, 1].transAxes, va="top", ha="left", fontsize=11, linespacing=1.62, color="#344054",
    )
    fig.tight_layout()
    save_figure(fig, "scheduling_operating_performance.png", dpi=135)


def main() -> None:
    PRECOMPUTED_DIR.mkdir(exist_ok=True)
    CHART_DIR.mkdir(exist_ok=True)
    RESULT_CACHE_DIR.mkdir(exist_ok=True)
    TABLE_DIR.mkdir(exist_ok=True)
    configure_plot_style()
    data = load_app_data()
    build_fast_data_files(data)
    build_eda_charts(data)
    build_regression_charts(data)
    build_scheduling_charts(data)
    manifest = {
        "schema_version": data["schema_version"],
        "chart_files": sorted(path.name for path in CHART_DIR.glob("*.png")),
        "scheduling_methods": SCHEDULING_METHODS,
    }
    (PRECOMPUTED_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Precomputed results created: {PRECOMPUTED_DIR}")
    print(f"Static charts: {len(manifest['chart_files'])}")


if __name__ == "__main__":
    main()
