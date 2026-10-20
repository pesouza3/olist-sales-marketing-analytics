# Results from src/evaluate_clusters.py
K_VALUES = [2, 3, 4, 5, 6, 7, 8]
SILHOUETTE = [0.2728, 0.3088, 0.2404, 0.2635, 0.2520, 0.2571, 0.2379]
SMALLEST = [1222, 181, 145, 140, 143, 73, 73]
LARGEST = [1873, 1724, 1141, 1001, 819, 773, 716]

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# 1. CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "seller_segments.csv"

SEGMENT_NAMES = {
    0: "Higher-volume sellers",
    1: "Lower observed delivery and review signals",
    2: "Lower-volume sellers",
}

SEGMENT_SHORT = {
    "Higher-volume sellers": "Higher volume",
    "Lower observed delivery and review signals": "Lower observed signals",
    "Lower-volume sellers": "Lower volume",
}

SEGMENT_COLORS = {
    "Higher-volume sellers": "#3767D5",
    "Lower observed delivery and review signals": "#D97757",
    "Lower-volume sellers": "#239B83",
}

NAVY = "#172B4D"
BLUE = "#3767D5"
MUTED = "#64748B"

st.set_page_config(
    page_title="Olist | Seller Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. DESIGN SYSTEM
# =========================================================

st.markdown(
    """
    <style>
@import url(
 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

/* ---------------------------------------------------------
   PALETA
   --------------------------------------------------------- */

:root {
    --crm-bg: #F6F5FA;
    --crm-card: #FFFFFF;
    --crm-purple: #6537C8;
    --crm-purple-dark: #3B1C78;
    --crm-purple-mid: #522AA6;
    --crm-purple-soft: #EEE8FF;
    --crm-ink: #211A35;
    --crm-muted: #777287;
    --crm-border: #EAE7F1;
    --crm-blue: #36A9E8;
    --crm-teal: #25B891;
    --crm-coral: #E95784;
    --crm-yellow: #F0B84B;
}

/* ---------------------------------------------------------
   APLICAÇÃO
   --------------------------------------------------------- */

html,
body,
[class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        sans-serif;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background: var(--crm-bg) !important;
    color: var(--crm-ink) !important;
}

[data-testid="stHeader"] {
    background: rgba(247, 247, 252, 0.96) !important;
}

.block-container {
    max-width: 1600px !important;
    padding: 1.35rem 1.7rem 2.5rem !important;
}

/* ---------------------------------------------------------
   TIPOGRAFIA
   --------------------------------------------------------- */

h1,
h2,
h3 {
    color: var(--crm-ink) !important;
    letter-spacing: -0.04em !important;
}

h1 {
    font-size: 1.95rem !important;
    line-height: 1.2 !important;
    font-weight: 800 !important;
    margin-bottom: 0.35rem !important;
}

h2 {
    font-size: 1.15rem !important;
    font-weight: 750 !important;
}

h3 {
    font-size: 0.98rem !important;
    font-weight: 750 !important;
}

.eyebrow {
    color: var(--crm-purple) !important;
    font-size: 0.64rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.15em !important;
    margin-bottom: 0.55rem !important;
}

.subtitle {
    color: var(--crm-muted) !important;
    font-size: 0.84rem !important;
    line-height: 1.65 !important;
    margin: 0.2rem 0 1.2rem !important;
}

.snapshot-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.55rem 0.75rem;
    border: 1px solid #E2D9F7;
    border-radius: 999px;
    background: #FFFFFF;
    color: #59428C;
    font-size: 0.68rem;
    font-weight: 750;
    letter-spacing: 0.035em;
    white-space: nowrap;
    box-shadow: 0 4px 16px rgba(41, 27, 83, 0.04);
}

.snapshot-dot {
    width: 0.48rem;
    height: 0.48rem;
    border-radius: 50%;
    background: #E95784;
    box-shadow: 0 0 0 3px #FCEAF0;
}

.section-heading {
    color: var(--crm-ink) !important;
    font-size: 1.12rem !important;
    font-weight: 780 !important;
    letter-spacing: -0.035em !important;
    margin-top: 1rem !important;
    margin-bottom: 0.15rem !important;
}

.section-description {
    color: var(--crm-muted) !important;
    font-size: 0.77rem !important;
    line-height: 1.55 !important;
    margin-bottom: 0.7rem !important;
}

.note {
    color: var(--crm-muted) !important;
    font-size: 0.72rem !important;
    line-height: 1.6 !important;
}

/* ---------------------------------------------------------
   SIDEBAR — ROXO PROFUNDO, TEXTO DE ALTO CONTRASTE
   --------------------------------------------------------- */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #713BC6 0%,
        #512C9D 55%,
        #40217F 100%
    ) !important;

    border-right: 1px solid #5B32A8 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem !important;
}

/* Texto geral */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaption * {
    color: #F3F1FF !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-size: 0.78rem !important;
    line-height: 1.55 !important;
}

/* Títulos e rótulos dos controles */
[data-testid="stSidebar"] [data-testid="stRadio"] > label,
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > label,
[data-testid="stSidebar"] [data-testid="stSlider"] > label {
    color: #FFFFFF !important;
    font-size: 0.77rem !important;
    font-weight: 650 !important;
}

/* Navegação */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #F1EFFF !important;
    border-radius: 9px !important;
    padding: 0.32rem 0.4rem !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.10) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: rgba(255, 255, 255, 0.17) !important;
    color: #FFFFFF !important;
    box-shadow: inset 3px 0 0 #C8B4FF;
}

/* Divisores */
[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.23) !important;
    margin: 1rem 0 !important;
}

/* Selectbox e multiselect */
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div,
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1px solid #D8D5ED !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] input {
    color: #29264A !important;
}

/* Chips dos segmentos selecionados */
[data-testid="stSidebar"] [data-testid="stMultiSelect"]
 [data-baseweb="tag"] {
    background: #5146C7 !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}

[data-testid="stSidebar"] [data-testid="stMultiSelect"]
 [data-baseweb="tag"] * {
    color: #FFFFFF !important;
}

/* Sliders */
[data-testid="stSidebar"] [data-testid="stSlider"] {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stSlider"] p,
[data-testid="stSidebar"] [data-testid="stSlider"] label,
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stMarkdownContainer"] {
    color: #F3F1FF !important;
}

/* Botão de reset */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    background: #FFFFFF !important;
    color: #39328E !important;
    border: 1px solid #DCD8FF !important;
    border-radius: 10px !important;
    min-height: 2.45rem !important;
    font-weight: 750 !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: #EFEDFF !important;
    color: #29264A !important;
}

/* ---------------------------------------------------------
   LOGO
   --------------------------------------------------------- */

[data-testid="stSidebar"] [data-testid="stImage"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.55) !important;
    border-radius: 14px !important;
    padding: 0.65rem !important;
    margin: 0.2rem 0 0.6rem !important;
    overflow: hidden !important;
}

.brand-subtitle {
    color: #E7E4FF !important;
    font-size: 0.65rem !important;
    font-weight: 750 !important;
    letter-spacing: 0.13em !important;
    margin: 0.3rem 0 0.7rem !important;
}

/* ---------------------------------------------------------
   KPI CARDS
   --------------------------------------------------------- */

.kpi-card {
    position: relative;
    box-sizing: border-box;
    width: 100%;
    min-height: 124px;
    padding: 1rem 1rem 0.9rem;
    background: var(--crm-card);
    border: 1px solid var(--crm-border);
    border-radius: 17px;
    box-shadow: 0 7px 24px rgba(41, 27, 83, 0.055);
    overflow: hidden;
    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

.kpi-card::before {
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: var(--kpi-accent, var(--crm-purple));
    content: "";
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(41, 27, 83, 0.10);
}

.kpi-topline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
}

.kpi-label {
    color: var(--crm-muted);
    font-size: 0.66rem;
    font-weight: 800;
    letter-spacing: 0.075em;
}

.kpi-icon {
    display: grid;
    width: 2rem;
    height: 2rem;
    place-items: center;
    border-radius: 0.7rem;
    color: var(--kpi-accent, var(--crm-purple));
    background: color-mix(in srgb, var(--kpi-accent, var(--crm-purple)) 11%, white);
    font-size: 0.95rem;
}

.kpi-value {
    color: var(--crm-ink);
    font-size: clamp(1.25rem, 1.65vw, 1.75rem);
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -0.05em;
    overflow-wrap: anywhere;
}

.kpi-note {
    color: #777791;
    font-size: 0.66rem;
    line-height: 1.45;
    margin-top: 0.35rem;
}

.takeaway-label {
    color: var(--crm-muted);
    font-size: 0.68rem;
    font-weight: 650;
    margin: 0.3rem 0 0.1rem;
}

.takeaway-value {
    color: var(--crm-ink);
    font-size: clamp(1.1rem, 1.65vw, 1.5rem);
    line-height: 1.2;
    font-weight: 780;
    letter-spacing: -0.04em;
    overflow-wrap: anywhere;
}

/* ---------------------------------------------------------
   CARDS DE GRÁFICOS E CONTEÚDO
   --------------------------------------------------------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid var(--crm-border) !important;
    border-radius: 17px !important;
    box-shadow: 0 7px 24px rgba(41, 27, 83, 0.045) !important;
    padding: 0.45rem !important;
}

[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
}

.panel,
.info-card {
    background: #FFFFFF !important;
    border: 1px solid var(--crm-border) !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 16px rgba(62, 54, 137, 0.04) !important;
    padding: 1rem !important;
}

.info-card {
    min-height: 125px;
    margin-bottom: 0.5rem !important;
}

/* Tabelas */
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border: 1px solid var(--crm-border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Métricas nativas */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid var(--crm-border) !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
}

[data-testid="stMetricLabel"] {
    color: var(--crm-muted) !important;
}

/* ---------------------------------------------------------
   BOTÕES, ABAS E DIVISORES
   --------------------------------------------------------- */

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(44, 24, 94, 0.10);
}

.stDownloadButton > button {
    background: #FFFFFF !important;
    color: var(--crm-purple) !important;
    border: 1px solid #DCD9F4 !important;
}

[data-testid="stTabs"] button {
    font-weight: 650 !important;
}

hr {
    border-color: var(--crm-border) !important;
}

footer {
    visibility: hidden;
}

/* ---------------------------------------------------------
   RESPONSIVIDADE
   --------------------------------------------------------- */

@media (max-width: 1100px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

@media (max-width: 800px) {
    [data-testid="stHorizontalBlock"]:has([data-testid="stPlotlyChart"]) {
        flex-direction: column !important;
        align-items: stretch !important;
    }

    [data-testid="stHorizontalBlock"]:has([data-testid="stPlotlyChart"])
    > [data-testid="column"] {
        flex: 1 1 100% !important;
        width: 100% !important;
    }
}

@media (max-width: 700px) {
    .block-container {
        padding: 0.9rem 0.65rem 1.8rem !important;
    }

    h1 {
        font-size: 1.6rem !important;
    }

    .kpi-card {
        min-height: 100px;
    }
}
</style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. LOAD AND VALIDATE DATA
# =========================================================

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)

    required_columns = {
        "seller_id",
        "cluster",
        "order_count",
        "items_sold",
        "total_sales_value",
        "average_order_value",
        "average_review_score",
        "on_time_delivery_rate",
        "average_delivery_days",
    }

    missing = required_columns.difference(data.columns)

    if missing:
        raise ValueError(
            f"Seller data is missing required columns: {sorted(missing)}"
        )

    data["seller_id"] = data["seller_id"].astype("string")

    if data["seller_id"].isna().any() or not data["seller_id"].is_unique:
        raise ValueError("Seller IDs must be present and unique.")

    data["cluster"] = pd.to_numeric(
        data["cluster"], errors="raise"
    ).astype(int)

    data["segment"] = data["cluster"].map(SEGMENT_NAMES)

    if data["segment"].isna().any():
        raise ValueError("Unexpected cluster label found in seller data.")

    numeric_columns = [
        "order_count",
        "items_sold",
        "total_sales_value",
        "average_order_value",
        "average_review_score",
        "on_time_delivery_rate",
        "average_delivery_days",
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="raise")

    data["segment_short"] = data["segment"].map(SEGMENT_SHORT)

    return data


if not DATA_PATH.exists():
    st.error(
        f"Required dashboard data was not found at {DATA_PATH}. "
        "Restore data/processed/seller_segments.csv from the project repository."
    )
    st.stop()

try:
    sellers = load_data(str(DATA_PATH))
except (ValueError, OSError, pd.errors.ParserError) as error:
    st.error(f"Unable to load seller data: {error}")
    st.stop()


# =========================================================
# 4. SIDEBAR NAVIGATION AND GLOBAL FILTERS
# =========================================================

with st.sidebar:
    logo_path = PROJECT_ROOT / "assets" / "olist-logo.png"

    if logo_path.exists():
        st.image(str(logo_path), width=145)
    else:
        st.markdown(
            '<div class="brand">olist</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="brand-subtitle">SELLER INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("**WORKSPACE**")

    page = st.radio(
        "Navigate",
        options=[
            "Overview",
            "Segment Analysis",
            "Seller Explorer",
            "Project Guide",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**PORTFOLIO FILTERS**")
    st.caption("Filters apply across the analytical pages.")

    all_segments = list(SEGMENT_NAMES.values())

    selected_segments = st.multiselect(
        "Seller segment",
        options=all_segments,
        default=all_segments,
    )

    min_orders = int(sellers["order_count"].min())
    max_orders = int(sellers["order_count"].max())

    order_range = st.slider(
        "Orders per seller",
        min_value=min_orders,
        max_value=max_orders,
        value=(min_orders, max_orders),
    )

    min_review = st.slider(
        "Minimum review score",
        min_value=1.0,
        max_value=5.0,
        value=1.0,
        step=0.5,
        help=(
            "When raised above 1, sellers with missing review scores "
            "are excluded from the filtered results."
        ),
    )

    min_on_time_pct = st.slider(
        "Minimum on-time delivery (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        help=(
            "When raised above 0, sellers with missing delivery rates "
            "are excluded from the filtered results."
        ),
    )

    if st.button("Reset filters", use_container_width=True):
        st.session_state["reset_filters_requested"] = True
        st.rerun()

    if st.session_state.pop("reset_filters_requested", False):
        st.session_state.clear()
        st.rerun()

    st.divider()
    st.markdown("**DATASET**")
    st.caption("Olist Brazilian e-commerce")
    st.caption("Historical observations · approximately 2016–2018")
    st.caption(f"{len(sellers):,} sellers loaded")


# Apply shared filters
filtered = sellers[
    sellers["segment"].isin(selected_segments)
    & sellers["order_count"].between(order_range[0], order_range[1])
].copy()

if min_review > 1.0:
    filtered = filtered[
        filtered["average_review_score"].ge(min_review)
    ]

if min_on_time_pct > 0:
    filtered = filtered[
        filtered["on_time_delivery_rate"].ge(min_on_time_pct / 100)
    ]


# =========================================================
# 5. SHARED DISPLAY AND CHART HELPERS
# =========================================================

def section_heading(title: str, description: str) -> None:
    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="section-description">{description}</div>',
        unsafe_allow_html=True,
    )


def kpi_card(
    label: str,
    value: str,
    note: str,
    icon: str,
    accent: str,
) -> None:
    st.markdown(
        f"""
        <div class="kpi-card" style="--kpi-accent:{accent};">
            <div class="kpi-topline">
                <div class="kpi-label">{label}</div>
                <div class="kpi-icon">{icon}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def takeaway_metric(label: str, value: str) -> None:
    st.markdown(
        f'<div class="takeaway-label">{label}</div>'
        f'<div class="takeaway-value">{value}</div>',
        unsafe_allow_html=True,
    )



def style_chart(fig, height: int = 320):
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=65, t=48, b=22),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Inter, sans-serif",
            color="#85849F",
            size=11,
        ),
        title=dict(
            font=dict(size=13, color="#252443"),
            x=0.025,
            xanchor="left",
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#39328E",
            bordercolor="#39328E",
            font=dict(color="#FFFFFF"),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        showline=False,
        zeroline=False,
        title=None,
        tickangle=0,
        automargin=True,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#F0EFF8",
        showline=False,
        zeroline=False,
        title=None,
        automargin=True,
    )
    return fig


def segment_summary(data: pd.DataFrame) -> pd.DataFrame:
    # Reindexing preserves selected segments even when a filter leaves
    # a segment with zero sellers.
    summary = data.groupby("segment").agg(
        sellers=("seller_id", "size"),
        median_orders=("order_count", "median"),
        median_sales=("total_sales_value", "median"),
        median_review=("average_review_score", "median"),
        median_on_time_rate=("on_time_delivery_rate", "median"),
        median_delivery_days=("average_delivery_days", "median"),
    )

    segment_order = [
        segment for segment in all_segments if segment in selected_segments
    ]

    summary = summary.reindex(segment_order).reset_index()
    summary["segment_short"] = summary["segment"].map(SEGMENT_SHORT)
    summary["color"] = summary["segment"].map(SEGMENT_COLORS)

    return summary



def render_segment_charts(data: pd.DataFrame) -> None:
    summary = segment_summary(data)

    if summary.empty:
        st.info("Select at least one segment to display the charts.")
        return

    # Distribuição recebe aproximadamente 58% da largura.
    left, right = st.columns(2, gap="medium")

    category_order = [
        SEGMENT_SHORT[s]
        for s in reversed(all_segments)
        if s in selected_segments
    ]

    with left:
        fig = px.bar(
            summary,
            x="sellers",
            y="segment_short",
            orientation="h",
            color="segment",
            color_discrete_map=SEGMENT_COLORS,
            text="sellers",
            hover_name="segment",
            hover_data={
                "sellers": ":,",
                "segment_short": False,
                "segment": False,
            },
            category_orders={"segment_short": category_order},
        )

        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            marker_line_width=0,
        )

        max_sellers = summary["sellers"].max()
        fig.update_xaxes(
            rangemode="tozero",
            range=[0, max_sellers * 1.16]
            if pd.notna(max_sellers) and max_sellers > 0
            else None,
            dtick=1000,
            tickformat="~s",
        )
        fig.update_layout(title="Seller distribution")

        with st.container(border=True):
            st.plotly_chart(
                style_chart(fig, max(280, 115 + len(summary) * 68)),
                width="stretch",
                key="seller_distribution_chart",
            )

    with right:
        sales = summary.dropna(subset=["median_sales"]).copy()

        if sales.empty:
            st.info("No sales values are available for this selection.")
        else:
            fig = px.bar(
                sales,
                x="median_sales",
                y="segment_short",
                orientation="h",
                color="segment",
                color_discrete_map=SEGMENT_COLORS,
                text="median_sales",
                hover_name="segment",
                hover_data={
                    "median_sales": ":,.2f",
                    "segment_short": False,
                    "segment": False,
                },
                category_orders={"segment_short": category_order},
            )

            fig.update_traces(
                texttemplate="R$ %{text:,.0f}",
                textposition="outside",
                cliponaxis=False,
                marker_line_width=0,
            )

            max_sales = sales["median_sales"].max()
            fig.update_xaxes(
                rangemode="tozero",
                tickformat="~s",
                dtick=2000,
                range=[0, max_sales * 1.32]
                if pd.notna(max_sales) and max_sales > 0
                else None,
            )
            fig.update_layout(
                title="Median sales value by segment (R$)",
                margin=dict(l=10, r=88, t=48, b=22),
            )

            with st.container(border=True):
                st.plotly_chart(
                    style_chart(fig, max(280, 115 + len(summary) * 68)),
                    width="stretch",
                    key="median_sales_chart",
                )


def render_operational_charts(data: pd.DataFrame) -> None:
    summary = segment_summary(data)
    left, right = st.columns([1, 1], gap="medium")

    with left:
        review = summary.dropna(subset=["median_review"]).copy()

        if review.empty:
            with st.container(border=True):
                st.info("No review observations are available for this selection.")
        else:
            fig = px.bar(
                review,
                x="median_review",
                y="segment_short",
                orientation="h",
                color="segment",
                color_discrete_map=SEGMENT_COLORS,
                text="median_review",
                hover_name="segment",
                hover_data={
                    "median_review": ":.2f",
                    "segment_short": False,
                    "segment": False,
                },
            )

            fig.update_traces(
                texttemplate="%{text:.2f} / 5",
                textposition="outside",
                cliponaxis=False,
                marker_line_width=0,
            )
            fig.update_xaxes(range=[0, 5.8], dtick=2)
            fig.update_layout(title="Median customer review score")

            with st.container(border=True):
                st.plotly_chart(
                    style_chart(fig, max(280, 115 + len(summary) * 68)),
                    width="stretch",
                    key="review_score_chart",
                )

    with right:
        delivery = summary.dropna(subset=["median_on_time_rate"]).copy()
        delivery["on_time_pct"] = delivery["median_on_time_rate"] * 100

        if delivery.empty:
            with st.container(border=True):
                st.info(
                    "No delivery observations are available for this selection."
                )
        else:
            fig = px.bar(
                delivery,
                x="on_time_pct",
                y="segment_short",
                orientation="h",
                color="segment",
                color_discrete_map=SEGMENT_COLORS,
                text="on_time_pct",
                hover_name="segment",
                hover_data={
                    "on_time_pct": ":.1f",
                    "segment_short": False,
                    "segment": False,
                },
            )

            fig.update_traces(
                texttemplate="%{text:.0f}%",
                textposition="outside",
                cliponaxis=False,
                marker_line_width=0,
            )
            fig.update_xaxes(range=[0, 115], ticksuffix="%", dtick=50)
            fig.update_layout(title="Median on-time delivery rate")

            with st.container(border=True):
                st.plotly_chart(
                    style_chart(fig, max(280, 115 + len(summary) * 68)),
                    width="stretch",
                    key="on_time_chart",
                )


def render_executive_insights(data: pd.DataFrame) -> None:
    section_heading(
        "Executive takeaways",
        "Filter-specific comparisons to guide the next investigation.",
    )

    if data.empty:
        st.info("No insights are available for the current filters.")
        return

    summary = (
        data.groupby("segment", observed=True)
        .agg(
            sellers=("seller_id", "size"),
            median_sales=("total_sales_value", "median"),
            median_orders=("order_count", "median"),
            median_on_time=("on_time_delivery_rate", "median"),
        )
        .reset_index()
    )

    summary["share_pct"] = summary["sellers"] / len(data) * 100

    largest = summary.loc[summary["sellers"].idxmax()]
    sales_available = summary.dropna(subset=["median_sales"])

    delivery = summary.dropna(subset=["median_on_time"])
    weakest_delivery = (
        delivery.loc[delivery["median_on_time"].idxmin()]
        if not delivery.empty
        else None
    )

    largest_col, sales_col, delivery_col = st.columns(3, gap="medium")

    with largest_col:
        with st.container(border=True):
            st.caption("LARGEST SEGMENT")
            st.markdown(f"**{largest['segment']}**")
            takeaway_metric("Sellers", f"{int(largest['sellers']):,}")
            share = float(largest["share_pct"]) / 100
            st.progress(share)
            st.caption(f"{share:.1%} of the filtered portfolio")

    with sales_col:
        with st.container(border=True):
            st.caption("HIGHEST MEDIAN SALES VALUE")

            if sales_available.empty:
                st.markdown("### Not available")
                st.caption("No valid sales values for this selection.")
            else:
                highest_sales = sales_available.loc[
                    sales_available["median_sales"].idxmax()
                ]

                st.markdown(f"**{highest_sales['segment']}**")
                takeaway_metric(
                    "Median sales value",
                    f"R$ {highest_sales['median_sales']:,.2f}",
                )
                st.caption(
                    "Item prices attributed to a seller; freight excluded."
                )

    with delivery_col:
        with st.container(border=True):
            st.caption("LOWEST MEDIAN ON-TIME DELIVERY")
            if weakest_delivery is None:
                st.markdown("**Not available**")
                st.caption("No delivery observations in this selection.")
            else:
                st.markdown(f"**{weakest_delivery['segment']}**")
                takeaway_metric(
                    "Median on-time rate",
                    format_rate(weakest_delivery["median_on_time"]),
                )
                st.caption(
                    "Use as a follow-up signal; per-seller observation "
                    "counts are unavailable."
                )

    st.caption(
        "Historical descriptive analysis. Review and delivery differences "
        "do not establish causality or predict future performance; validate "
        "order volume and data coverage before interpreting individual sellers."
    )


def format_currency(value) -> str:
    if pd.isna(value):
        return "Not available"
    return f"R$ {value:,.2f}"


def format_rate(value) -> str:
    if pd.isna(value):
        return "Not available"
    return f"{value:.1%}"


def format_number(value, decimals=0) -> str:
    if pd.isna(value):
        return "Not available"
    return f"{value:,.{decimals}f}"


def render_seller_table(data: pd.DataFrame, key_prefix: str) -> None:
    search_col, sort_col = st.columns([3, 1])

    with search_col:
        query = st.text_input(
            "Search by seller ID",
            placeholder="Type part or all of a seller ID...",
            key=f"{key_prefix}_search",
        )

    with sort_col:
        sort_by = st.selectbox(
            "Sort by",
            [
                "Sales value",
                "Order count",
                "Items sold",
                "Review score",
                "On-time delivery",
            ],
            key=f"{key_prefix}_sort",
        )

    view = data.copy()

    if query.strip():
        view = view[
            view["seller_id"].str.contains(
                query.strip(), case=False, regex=False, na=False
            )
        ]

    sort_columns = {
        "Sales value": "total_sales_value",
        "Order count": "order_count",
        "Items sold": "items_sold",
        "Review score": "average_review_score",
        "On-time delivery": "on_time_delivery_rate",
    }

    view = view.sort_values(
        sort_columns[sort_by],
        ascending=False,
        na_position="last",
    )

    display_columns = [
        "seller_id",
        "segment_short",
        "order_count",
        "items_sold",
        "total_sales_value",
        "average_order_value",
        "average_review_score",
        "on_time_delivery_rate",
        "average_delivery_days",
    ]

    table = view[display_columns].rename(
        columns={
            "seller_id": "Seller ID",
            "segment_short": "Segment",
            "order_count": "Orders",
            "items_sold": "Items sold",
            "total_sales_value": "Sales value (R$)",
            "average_order_value": "Average seller sales per order (R$)",
            "average_review_score": "Review score",
            "on_time_delivery_rate": "On-time delivery",
            "average_delivery_days": "Delivery days",
        }
    )

    table["Sales value (R$)"] = table["Sales value (R$)"].round(2)
    table["Average seller sales per order (R$)"] = table[
        "Average seller sales per order (R$)"
    ].round(2)
    table["Review score"] = table["Review score"].round(2)
    table["On-time delivery"] = (table["On-time delivery"] * 100).round(1)
    table["Delivery days"] = table["Delivery days"].round(1)

    st.caption(f"{len(table):,} sellers match this search and the active filters.")

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            "Seller ID": st.column_config.TextColumn("Seller ID", width="large"),
            "Segment": st.column_config.TextColumn("Segment", width="medium"),
            "Orders": st.column_config.NumberColumn("Orders", format="%d"),
            "Items sold": st.column_config.NumberColumn("Items sold", format="%d"),
            "Sales value (R$)": st.column_config.NumberColumn(
                "Sales value (R$)", format="R$ %.2f"
            ),
            "Average seller sales per order (R$)": st.column_config.NumberColumn(
                "Average seller sales per order (R$)", format="R$ %.2f"
            ),
            "Review score": st.column_config.NumberColumn(
                "Review score", format="%.2f"
            ),
            "On-time delivery": st.column_config.NumberColumn(
                "On-time delivery (%)", format="%.1f%%"
            ),
            "Delivery days": st.column_config.NumberColumn(
                "Delivery days", format="%.1f"
            ),
        },
    )

    st.download_button(
        "Download filtered seller data ↓",
        data=table.to_csv(index=False).encode("utf-8"),
        file_name="olist_filtered_seller_segments.csv",
        mime="text/csv",
        key=f"{key_prefix}_download",
    )

    st.markdown("**Inspect an individual seller**")
    st.caption(
        "Choose a seller below to view a compact profile. "
        "The list reflects the current filters and search."
    )

    if view.empty:
        st.info("No sellers match the current search.")
        return

    selected_seller_id = st.selectbox(
        "Seller",
        options=view["seller_id"].tolist(),
        format_func=lambda seller_id: (
            f"{seller_id} · "
            f"{view.loc[view['seller_id'] == seller_id, 'segment_short'].iloc[0]}"
        ),
        key=f"{key_prefix}_seller_profile",
    )

    seller = view.loc[view["seller_id"] == selected_seller_id].iloc[0]

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### Seller profile")
    st.code(str(seller["seller_id"]), language=None)

    profile_a, profile_b, profile_c = st.columns(3)

    with profile_a:
        st.metric("Segment", seller["segment_short"])
        st.metric("Orders", format_number(seller["order_count"]))

    with profile_b:
        st.metric("Sales value", format_currency(seller["total_sales_value"]))
        st.metric(
            "Average seller sales per order",
            format_currency(seller["average_order_value"]),
        )

    with profile_c:
        st.metric("Review score", format_number(seller["average_review_score"], 2))
        st.metric("On-time delivery", format_rate(seller["on_time_delivery_rate"]))

    st.metric(
        "Average delivery duration",
        (
            f"{seller['average_delivery_days']:.1f} days"
            if pd.notna(seller["average_delivery_days"])
            else "Not available"
        ),
    )

    st.markdown(
        """
        <div class="note">
        Interpret seller metrics in context. Review scores and delivery rates
        may be based on few observations; order-level reviews are not always
        seller-specific for multi-seller orders.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 6. PAGE: OVERVIEW
# =========================================================

if page == "Overview":
    title_col, status_col = st.columns([3.6, 1], vertical_alignment="center")
    with title_col:
        st.markdown(
            '<div class="eyebrow">BUSINESS INTELLIGENCE / SELLERS</div>',
            unsafe_allow_html=True,
        )
        st.title("Seller intelligence")
        st.markdown(
            '<div class="subtitle">'
            "A consolidated view of seller activity, commercial performance "
            "and operational signals."
            "</div>",
            unsafe_allow_html=True,
        )
    with status_col:
        st.markdown(
            '<div style="text-align:right;padding-bottom:1.2rem;">'
            '<span class="snapshot-badge"><i class="snapshot-dot"></i>'
            'HISTORICAL SNAPSHOT</span></div>',
            unsafe_allow_html=True,
        )

    section_heading(
        "Portfolio overview",
        "The indicators below update when you change the sidebar filters.",
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card(
            "SELLERS IN VIEW",
            f"{len(filtered):,}",
            "Sellers matching current filters",
            "◉",
            "#6738C8",
        )

    with k2:
        kpi_card(
            "SEGMENTS",
            f"{filtered['segment'].nunique():,}",
            "Represented in current view",
            "▦",
            "#25B891",
        )

    with k3:
        value = (
            format_number(filtered["order_count"].median())
            if not filtered.empty
            else "—"
        )
        kpi_card(
            "MEDIAN ORDERS",
            value,
            "Orders per seller",
            "▤",
            "#36A9E8",
        )

    with k4:
        value = (
            format_currency(filtered["total_sales_value"].median())
            if not filtered.empty
            else "—"
        )
        kpi_card(
            "MEDIAN SALES VALUE",
            value,
            "Item prices · freight excluded",
            "↗",
            "#E95784",
        )

    st.markdown(
        '<div class="note" style="margin-top:0.7rem;">'
        "Sales value is the sum of item prices attributed to a seller, "
        "excluding freight. These are historical observations, not current "
        "seller performance. Average seller sales per order divides this "
        "value by distinct seller-order pairs."
        "</div>",
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.warning("No sellers match the active filters.")
    else:
        section_heading(
            "Segment performance",
            "Compare the number of sellers and median sales value in each group.",
        )
        render_segment_charts(filtered)

        section_heading(
            "Operational health",
            "Median review and on-time delivery signals by segment.",
        )
        render_operational_charts(filtered)
        st.caption(
            "Reviews are order-level proxies and may reflect multiple "
            "sellers. Delivery rates use delivered orders with actual "
            "and estimated dates; per-seller observation counts are not "
            "included, so treat small-sample rates cautiously."
        )

        render_executive_insights(filtered)

        with st.expander("Quick interpretation guide"):
            st.markdown(
                """
                - **Seller distribution** shows the size of each group, not its
                  contribution to total sales.
                - **Median sales value** summarizes the typical seller within
                  each segment and is less sensitive to extreme values than a mean.
                - **Review score** is an order-level review proxy for some
                  multi-seller orders.
                - **On-time delivery** is calculated from eligible delivery
                  observations; it is not a live service-level metric.
                - Always consider seller order volume before interpreting
                  a high or low operational rate.
                """
            )


# =========================================================
# 7. PAGE: SEGMENT ANALYSIS
# =========================================================

elif page == "Segment Analysis":
    st.markdown('<div class="eyebrow">PORTFOLIO / SEGMENTS</div>', unsafe_allow_html=True)
    st.title("Segment analysis")
    st.markdown(
        '<div class="subtitle">'
        "Explore the size, commercial profile and operational signals of each group."
        "</div>",
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.warning("No sellers match the active filters.")
    else:
        summary = segment_summary(filtered)

        section_heading(
            "Segment comparison",
            "All figures reflect the current portfolio filters.",
        )

        st.dataframe(
            summary.rename(
                columns={
                    "segment": "Segment",
                    "sellers": "Sellers",
                    "median_orders": "Median orders",
                    "median_sales": "Median sales value (R$)",
                    "median_review": "Median review score",
                    "median_on_time_rate": "Median on-time rate",
                    "median_delivery_days": "Median delivery days",
                }
            )[
                [
                    "Segment",
                    "Sellers",
                    "Median orders",
                    "Median sales value (R$)",
                    "Median review score",
                    "Median on-time rate",
                    "Median delivery days",
                ]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Median sales value (R$)": st.column_config.NumberColumn(
                    format="R$ %.2f"
                ),
                "Median review score": st.column_config.NumberColumn(
                    format="%.2f"
                ),
                "Median on-time rate": st.column_config.NumberColumn(
                    format="%.1%"
                ),
                "Median delivery days": st.column_config.NumberColumn(
                    format="%.1f"
                ),
            },
        )

        render_segment_charts(filtered)
        render_operational_charts(filtered)
        st.caption(
            "Review scores are order-level proxies and may reflect multiple "
            "sellers. Delivery rates use delivered orders with actual and "
            "estimated dates; per-seller observation counts are not included "
            "in this dataset, so treat small-sample rates cautiously."
        )

        st.markdown("### Segment definitions")

        for segment in selected_segments:
            with st.expander(segment):
                segment_data = filtered[filtered["segment"] == segment]

                if segment_data.empty:
                    st.info("No sellers from this segment match the active filters.")
                    continue

                st.write(f"**Sellers in view:** {len(segment_data):,}")
                st.write(
                    f"**Median orders:** "
                    f"{segment_data['order_count'].median():,.0f}"
                )
                st.write(
                    f"**Median sales value:** "
                    f"{format_currency(segment_data['total_sales_value'].median())}"
                )

                if segment == "Higher-volume sellers":
                    st.write(
                        "This group has higher observed order activity and "
                        "sales value. It is a descriptive segment, "
                        "not a guarantee of future performance."
                    )
                elif segment == "Lower observed delivery and review signals":
                    st.write(
                        "This group showed lower observed delivery and review "
                        "signals in the exploratory analysis. Validate order "
                        "counts and individual delivery records before drawing "
                        "conclusions about any seller."
                    )
                else:
                    st.write(
                        "This group combines lower order volumes and sales "
                        "value. Small sample sizes "
                        "can make these indicators unstable."
                    )


# =========================================================
# 8. PAGE: SELLER EXPLORER
# =========================================================

elif page == "Seller Explorer":
    st.markdown('<div class="eyebrow">OPERATIONS / SELLER RECORDS</div>', unsafe_allow_html=True)
    st.title("Seller explorer")
    st.markdown(
        '<div class="subtitle">'
        "Search individual sellers, compare metrics, inspect profiles "
        "and export the filtered population."
        "</div>",
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.warning("No sellers match the active filters.")
    else:
        render_seller_table(filtered, "explorer")

        with st.expander("Seller metric definitions"):
            st.markdown(
                """
                - **Orders:** Distinct seller-order pairs, not necessarily
                  unique marketplace orders across the whole dataset.
                - **Items sold:** Number of order-item rows associated with the seller.
                - **Sales value:** Sum of item prices; freight is excluded.
                - **Average seller sales per order:** Seller sales value divided
                  by distinct seller-order pairs; this is not marketplace AOV.
                - **Review score:** Average of associated order-level reviews;
                  it is a proxy for multi-seller orders.
                - **On-time delivery:** Share of eligible delivery observations
                  that met the estimated delivery date. Per-seller denominators
                  are not present in the supplied dataset.
                - **Delivery days:** Average duration for eligible delivered orders.
                """
            )


# =========================================================
# =========================================================
# 9. PAGE: PROJECT GUIDE — ANALYTICS CASE STUDY
# =========================================================

elif page == "Project Guide":
    st.markdown(
        '<div class="eyebrow">ANALYTICS / METHODOLOGY / BUSINESS IMPACT</div>',
        unsafe_allow_html=True,
    )
    st.title("Analytics case study")
    st.markdown(
        '<div class="subtitle">'
        "From transactional data to seller segmentation, analytical evidence "
        "and business recommendations."
        "</div>",
        unsafe_allow_html=True,
    )

    # Executive summary
    kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="medium")
    with kpi1:
        st.metric("Sellers analyzed", f"{len(sellers):,}")
    with kpi2:
        st.metric("Clustering features", "7")
    with kpi3:
        st.metric("Selected clusters", f"{sellers['cluster'].nunique():,}")
    with kpi4:
        st.metric("Best silhouette", "0.3088")

    st.caption(
        "Historical public dataset · Exploratory segmentation · "
        "Not a live CRM or a validated risk model"
    )

    (
        tab_business,
        tab_pipeline,
        tab_model,
        tab_insights,
        tab_actions,
        tab_stack,
    ) = st.tabs(
        [
            "Business questions",
            "Data pipeline",
            "Why K = 3?",
            "Segment insights",
            "Business actions",
            "Technical stack",
        ]
    )

    # -----------------------------------------------------
    # TAB 1 — BUSINESS QUESTIONS
    # -----------------------------------------------------
    with tab_business:
        st.markdown("### 01 · Business problem")
        st.markdown(
            """
            Marketplace teams need a structured way to compare sellers'
            commercial activity and operational signals. Transaction-level
            data is detailed, but it is difficult to use directly for
            prioritization and portfolio-level decisions.

            **Project objective:** transform historical transactions into
            seller-level metrics, exploratory groups and business-facing
            views that help analysts identify patterns worth investigating.
            """
        )

        st.markdown("### Questions driving the analysis")

        questions = [
            (
                "01",
                "How is seller activity distributed?",
                "Compare seller counts, order volumes and typical sales value "
                "across the observed segments.",
            ),
            (
                "02",
                "Which groups show different commercial profiles?",
                "Contrast order activity and median sales value, without "
                "assuming that sales value alone represents profitability.",
            ),
            (
                "03",
                "Where do operational signals deserve investigation?",
                "Explore delivery timeliness and review patterns, accounting "
                "for differences in observation volume.",
            ),
            (
                "04",
                "Does the data support three useful groups?",
                "Compare K-Means solutions across k = 2 to 8 using silhouette "
                "scores and cluster-size distributions.",
            ),
            (
                "05",
                "What actions could the business test?",
                "Translate observed patterns into hypotheses and measurable "
                "follow-up analyses, rather than treating clusters as causes.",
            ),
        ]

        for number, question, description in questions:
            with st.container(border=True):
                left, right = st.columns([0.12, 0.88])
                with left:
                    st.markdown(f"### {number}")
                with right:
                    st.markdown(f"**{question}**")
                    st.caption(description)

        st.markdown("### Analytical principle")
        st.info(
            "Separate descriptive evidence from hypotheses. A segment is "
            "a summary of observed seller characteristics, not proof that "
            "a seller will perform the same way in the future."
        )

    # -----------------------------------------------------
    # TAB 2 — DATA PIPELINE
    # -----------------------------------------------------
    with tab_pipeline:
        st.markdown("### 02 · From raw data to the dashboard")
        st.markdown(
            "The analytical workflow is organized into reproducible stages."
        )

        pipeline = [
            (
                "01",
                "Raw data",
                "Historical marketplace CSVs covering orders, order items, "
                "sellers and reviews.",
                "#EFEDFF",
            ),
            (
                "02",
                "Seller feature engineering",
                "build_seller_features.py — aggregate transactional records "
                "into seller-level commercial and operational metrics.",
                "#E9F3FF",
            ),
            (
                "03",
                "Model preparation",
                "prepare_clustering_features.py — transform skewed variables, "
                "handle missing values and standardize clustering inputs.",
                "#E5F6F1",
            ),
            (
                "04",
                "Model evaluation",
                "evaluate_clusters.py — compare K-Means solutions from "
                "k = 2 through k = 8.",
                "#FFF2E9",
            ),
            (
                "05",
                "Segment profiling",
                "profile_seller_segments.py — generate the selected "
                "three-cluster solution and seller segment profiles.",
                "#F2EDFF",
            ),
            (
                "06",
                "Interactive analytics",
                "app.py — Streamlit interface with Plotly visualizations, "
                "filters, seller exploration and CSV export.",
                "#E9F5F8",
            ),
        ]

        for number, title, description, color in pipeline:
            with st.container(border=True):
                st.markdown(
                    f'<div style="background:{color};padding:0.8rem;'
                    'border-radius:10px;">'
                    f'<span style="font-size:0.72rem;font-weight:800;">'
                    f'{number}</span> &nbsp; '
                    f'<strong>{title}</strong>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                st.write(description)

        st.markdown("### Modeling preparation")
        prep1, prep2 = st.columns(2)
        with prep1:
            st.markdown("**Transformations and quality**")
            st.write(
                "- Log transformation (`log1p`) for skewed commercial variables.\n"
                "- Delivery-duration outliers capped at the 99th percentile "
                "for modeling.\n"
                "- Missing clustering values imputed with the median."
            )
        with prep2:
            st.markdown("**Model inputs**")
            st.write(
                "- Seven clustering features.\n"
                "- Standardized features before K-Means.\n"
                "- `random_state=42` and `n_init=10` in the evaluation script."
            )

        st.info(
            "Seller features use the sellers, order items, orders, and "
            "reviews tables. Marketing funnel tables are present in the "
            "source data but are not joined into this seller segmentation."
        )

    # -----------------------------------------------------
    # TAB 3 — WHY K = 3?
    # -----------------------------------------------------
    with tab_model:
        st.markdown("### 03 · Model selection")
        st.markdown(
            f"The evaluation script tested seven candidate values of k "
            f"on {len(sellers):,} sellers and seven clustering features."
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Selected k", "3")
        col2.metric("Silhouette score", "0.3088")
        col3.metric("Candidates tested", "7")

        st.markdown("#### Silhouette score by number of clusters")

        silhouette_df = pd.DataFrame(
            {
                "k": K_VALUES,
                "Silhouette score": SILHOUETTE,
            }
        ).set_index("k")

        st.bar_chart(
            silhouette_df,
            y="Silhouette score",
            color="#5146C7",
            height=300,
        )

        st.caption(
            "Higher silhouette scores indicate better relative cohesion "
            "and separation. The metric does not prove that clusters are "
            "perfectly separated or commercially optimal."
        )

        evaluation_df = pd.DataFrame(
            {
                "k": K_VALUES,
                "Silhouette": SILHOUETTE,
                "Smallest cluster": SMALLEST,
                "Largest cluster": LARGEST,
            }
        )

        st.dataframe(
            evaluation_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "k": st.column_config.NumberColumn("k", format="%d"),
                "Silhouette": st.column_config.NumberColumn(
                    "Silhouette", format="%.4f"
                ),
                "Smallest cluster": st.column_config.NumberColumn(
                    "Smallest cluster", format="%d"
                ),
                "Largest cluster": st.column_config.NumberColumn(
                    "Largest cluster", format="%d"
                ),
            },
        )

        st.markdown("#### Why select three clusters?")
        st.markdown(
            """
            - **Highest tested score:** k = 3 achieved 0.3088, compared
              with 0.2728 for k = 2 and 0.2404 for k = 4.
            - **Interpretability:** three groups provide a manageable
              structure for exploratory seller profiling.
            - **Important limitation:** the score is moderate and the
              cluster sizes are uneven. The result supports k = 3 among
              the tested alternatives, not a claim of perfect separation.
            """
        )

        st.markdown("#### Cluster size comparison")
        size_df = pd.DataFrame(
            {
                "k": K_VALUES,
                "Smallest cluster": SMALLEST,
                "Largest cluster": LARGEST,
            }
        ).set_index("k")

        st.line_chart(
            size_df,
            height=250,
        )

        st.info(
            "The evaluation script records the smallest and largest cluster "
            "sizes. These values are not the complete cluster-size profile "
            "for every candidate k."
        )

    # -----------------------------------------------------
    # TAB 4 — SEGMENT INSIGHTS
    # -----------------------------------------------------
    with tab_insights:
        st.markdown("### 04 · What the current segments suggest")
        st.markdown(
            "The current labels describe patterns observed in the historical "
            "data. They should be interpreted as exploratory profiles."
        )

        segment_profiles = [
            {
                "cluster": 0,
                "color": "#3767D5",
                "meaning": (
                    "Higher observed order history and median sales value "
                    "in the current profile."
                ),
                "question": (
                    "Does this group also show consistent delivery and "
                    "customer experience across enough observations?"
                ),
            },
            {
                "cluster": 1,
                "color": "#D97757",
                "meaning": (
                    "A group identified through lower observed "
                    "delivery and review signals in the exploratory analysis."
                ),
                "question": (
                    "Are the signals consistent after checking order counts, "
                    "delivery records and review attribution?"
                ),
            },
            {
                "cluster": 2,
                "color": "#239B83",
                "meaning": (
                    "Lower observed sales value and activity in the current "
                    "exploratory profile."
                ),
                "question": (
                    "Which sellers have sufficient evidence and a realistic "
                    "opportunity to increase activity?"
                ),
            },
        ]

        for profile in segment_profiles:
            profile_data = sellers[sellers["cluster"] == profile["cluster"]]
            profile_name = SEGMENT_NAMES[profile["cluster"]]
            median_sales = profile_data["total_sales_value"].median()
            with st.container(border=True):
                st.markdown(
                    f'<div style="border-left:5px solid {profile["color"]};'
                    'padding:0.2rem 0 0.2rem 0.8rem;">'
                    f'<strong>{profile_name}</strong></div>',
                    unsafe_allow_html=True,
                )
                a, b = st.columns(2)
                with a:
                    st.metric("Sellers in segment", f"{len(profile_data):,}")
                with b:
                    st.metric(
                        "Median sales value",
                        format_currency(median_sales),
                    )
                st.write(profile["meaning"])
                st.caption("Question to investigate: " + profile["question"])

        st.caption(
            "Sales values are median item prices attributed to a seller, "
            "excluding freight. They are not profit, margin or current sales."
        )

        st.markdown("#### How to read these findings")
        st.markdown(
            """
            **Observed:** seller counts and median sales values differ across
            the three profiles.

            **Hypothesis:** the profiles may benefit from different operational
            or commercial approaches.

            **Not established:** that segment membership causes performance,
            predicts future outcomes, or is sufficient on its own to classify
            an individual seller as risky.
            """
        )

    # -----------------------------------------------------
    # TAB 5 — BUSINESS ACTIONS
    # -----------------------------------------------------
    with tab_actions:
        st.markdown("### 05 · From analysis to business decisions")
        st.markdown(
            "The recommendations below are hypotheses to test, not proven "
            "effects of the clustering."
        )

        actions = [
            (
                "Higher-volume sellers",
                "Retention and operational consistency",
                "Review order volume, sales value, delivery timeliness and "
                "customer feedback together. Identify practices worth "
                "investigating across comparable sellers.",
                "Repeat seller activity; on-time delivery; review score.",
            ),
            (
                "Lower observed delivery and review signals",
                "Diagnose before intervening",
                "Inspect eligible orders, estimated versus actual delivery "
                "dates, observation counts and possible logistics patterns "
                "before contacting sellers or changing service levels.",
                "On-time delivery rate; late-order share; review trend.",
            ),
            (
                "Lower-volume sellers",
                "Validate growth opportunity",
                "Separate genuinely low activity from new or sparsely observed "
                "sellers. Test targeted guidance only where the data supports "
                "a meaningful comparison.",
                "Orders per seller; sales value; repeat activity.",
            ),
        ]

        for segment, priority, action, measures in actions:
            with st.container(border=True):
                st.markdown(f"**{segment}**")
                st.markdown(f"**Priority:** {priority}")
                st.write(action)
                st.caption("Measures to monitor: " + measures)

        st.markdown("#### Suggested validation plan")
        st.write(
            "1. Establish a baseline for each proposed KPI.\n"
            "2. Define eligibility and minimum observation counts.\n"
            "3. Pilot one intervention with a comparison group where feasible.\n"
            "4. Measure changes over a defined period.\n"
            "5. Reassess segment stability before operationalizing the model."
        )

        st.warning(
            "Do not use cluster membership as the sole basis for punitive "
            "seller decisions. Validate the underlying observations and "
            "consider the potential impact on sellers."
        )

    # -----------------------------------------------------
    # TAB 6 — TECHNICAL STACK
    # -----------------------------------------------------
    with tab_stack:
        st.markdown("### 06 · Technical stack")

        tech = [
            (
                "Python",
                "Language used to build the data-processing, modeling "
                "and dashboard scripts.",
            ),
            (
                "Pandas",
                "CSV ingestion, tabular transformations, aggregations "
                "and seller-level feature preparation.",
            ),
            (
                "Scikit-learn",
                "KMeans clustering and silhouette_score evaluation.",
            ),
            (
                "Streamlit",
                "Interactive dashboard, page navigation, filters, tables "
                "and KPI presentation.",
            ),
            (
                "Plotly",
                "Interactive charts used to explore segment metrics.",
            ),
            (
                "NumPy",
                "Numerical operations where used by the project scripts.",
            ),
        ]

        for name, description in tech:
            with st.container(border=True):
                st.markdown(f"**{name}**")
                st.write(description)

        st.markdown("### Reproduce the analysis")
        st.code(
            "source .venv/bin/activate\n"
            "python src/build_seller_features.py\n"
            "python src/prepare_clustering_features.py\n"
            "python src/evaluate_clusters.py\n"
            "python src/profile_seller_segments.py\n"
            "streamlit run app.py",
            language="bash",
        )

        st.caption(
            "Run these commands from the project root with the project's "
            "dependencies installed."
        )

        st.markdown("### Key limitations")
        st.markdown(
            """
            - The data represents historical marketplace activity, not live
              seller performance.
            - A review attached to an order with multiple sellers may not
              identify which seller caused the customer experience.
            - Small observation counts can make seller-level rates unstable.
            - Silhouette score is one model-selection criterion, not a
              guarantee of business usefulness.
            - Segment labels are descriptive and should be validated before
              being used in recurring operational processes.
            """
        )

    st.divider()
    st.markdown("### Final takeaway")
    st.markdown(
        """
        The project combines seller-level feature engineering, K-Means
        clustering and interactive exploration to make historical marketplace
        data easier to investigate. The three-cluster solution is supported
        by the highest silhouette score among the tested values of k, while
        its moderate score and uneven group sizes call for careful
        interpretation and further validation.
        """
    )
