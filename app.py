from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# 1. CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "seller_segments.csv"

DATA_URL = (
    "https://drive.google.com/uc"
    "?export=download&id=17v0NRoQiZxxrUPyMNq85hlK7sndQL1cG"
)

SEGMENT_NAMES = {
    0: "Established sellers",
    1: "Potential delivery-risk sellers",
    2: "Lower-volume sellers with positive observed signals",
}

SEGMENT_SHORT = {
    "Established sellers": "Established",
    "Potential delivery-risk sellers": "Delivery risk",
    "Lower-volume sellers with positive observed signals": "Lower volume",
}

SEGMENT_COLORS = {
    "Established sellers": "#3767D5",
    "Potential delivery-risk sellers": "#D97757",
    "Lower-volume sellers with positive observed signals": "#239B83",
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

    html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: #F5F7FB;
        color: #172B4D;
    }

    [data-testid="stHeader"] {
        background: rgba(245, 247, 251, 0.94);
    }

    [data-testid="stSidebar"] {
        background: #172B4D;
    }

    [data-testid="stSidebar"] * {
        color: #E7EDF8;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #B8C5D9;
    }

    [data-testid="stSidebar"] hr {
        border-color: #344968;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #172B4D !important;
        letter-spacing: -0.035em;
    }

    h1 {
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-size: 1.3rem !important;
        font-weight: 750 !important;
    }

    h3 {
        font-size: 1rem !important;
        font-weight: 700 !important;
    }

    .brand {
        color: #FFFFFF;
        font-size: 1.12rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        padding-top: 0.5rem;
    }

    .brand-subtitle {
        color: #AFC0D9;
        font-size: 0.72rem;
        margin: 0.2rem 0 1.2rem 0;
        letter-spacing: 0.08em;
    }

    .eyebrow {
        color: #64748B;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }

    .subtitle {
        color: #64748B;
        font-size: 0.9rem;
        margin-top: -0.8rem;
        margin-bottom: 1.4rem;
        line-height: 1.6;
    }

    .section-heading {
        font-size: 1.15rem;
        font-weight: 750;
        letter-spacing: -0.025em;
        color: #172B4D;
        margin-top: 1.3rem;
        margin-bottom: 0.25rem;
    }

    .section-description {
        color: #64748B;
        font-size: 0.82rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF1;
        border-radius: 13px;
        padding: 1.05rem;
        min-height: 122px;
        box-shadow: 0 2px 5px rgba(23, 43, 77, 0.025);
    }

    .kpi-label {
        color: #64748B;
        font-size: 0.75rem;
        font-weight: 650;
        margin-bottom: 0.65rem;
    }

    .kpi-value {
        color: #172B4D;
        font-size: clamp(1.25rem, 2vw, 1.8rem);
        font-weight: 800;
        letter-spacing: -0.045em;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }

    .kpi-note {
        color: #94A3B8;
        font-size: 0.71rem;
        margin-top: 0.45rem;
    }

    .panel {
        background: #FFFFFF;
        border: 1px solid #E5EAF1;
        border-radius: 13px;
        padding: 0.9rem;
        box-shadow: 0 2px 5px rgba(23, 43, 77, 0.025);
    }

    .info-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF1;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.6rem;
    }

    .info-label {
        color: #64748B;
        font-size: 0.75rem;
        font-weight: 650;
        margin-bottom: 0.35rem;
    }

    .info-value {
        color: #172B4D;
        font-size: 1.1rem;
        font-weight: 750;
    }

    .note {
        color: #64748B;
        font-size: 0.78rem;
        line-height: 1.65;
    }

    .pill {
        display: inline-block;
        background: #EAF0FF;
        color: #2D55AC;
        padding: 0.3rem 0.65rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E5EAF1;
        border-radius: 10px;
        overflow: hidden;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E5EAF1;
        border-radius: 12px;
        padding: 1rem;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
        font-size: 0.78rem;
    }

    div[data-testid="stMetricValue"] {
        color: #172B4D;
        font-weight: 750;
    }

    .stDownloadButton > button {
        border-radius: 8px;
        border: 1px solid #D6DFEC;
        background: #FFFFFF;
        color: #172B4D;
        font-weight: 650;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 650;
    }

    hr {
        border-color: #E5EAF1;
    }

    footer {
        visibility: hidden;
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


DATA_SOURCE = str(DATA_PATH) if DATA_PATH.exists() else DATA_URL

try:
    sellers = load_data(DATA_SOURCE)
except (ValueError, OSError, pd.errors.ParserError) as error:
    st.error(f"Unable to load seller data: {error}")
    st.stop()


# =========================================================
# 4. SIDEBAR NAVIGATION AND GLOBAL FILTERS
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">◈ OLIST INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="brand-subtitle">SELLER ANALYTICS PLATFORM</div>',
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


def kpi_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height: int = 320):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=20, t=45, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=MUTED, size=11),
        title=dict(
            font=dict(size=13, color=NAVY),
            x=0.02,
            xanchor="left",
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor=NAVY,
            bordercolor=NAVY,
            font=dict(color="#FFFFFF"),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        showline=False,
        zeroline=False,
        title=None,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EDF1F6",
        showline=False,
        zeroline=False,
        title=None,
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

    left, right = st.columns(2)

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
            category_orders={
                "segment_short": [
                    SEGMENT_SHORT[s]
                    for s in reversed(all_segments)
                    if s in selected_segments
                ]
            },
        )
        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            marker_line_width=0,
        )
        fig.update_xaxes(rangemode="tozero")
        fig.update_layout(title="Seller distribution")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.plotly_chart(
            style_chart(fig, max(250, 100 + len(summary) * 75)),
            use_container_width=True,
            key="seller_distribution_chart",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        fig = px.bar(
            summary,
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
            category_orders={
                "segment_short": [
                    SEGMENT_SHORT[s]
                    for s in reversed(all_segments)
                    if s in selected_segments
                ]
            },
        )
        fig.update_traces(
            texttemplate="R$ %{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            marker_line_width=0,
        )
        fig.update_xaxes(rangemode="tozero", tickprefix="R$ ")
        fig.update_layout(title="Median sales value by segment")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.plotly_chart(
            style_chart(fig, max(250, 100 + len(summary) * 75)),
            use_container_width=True,
            key="median_sales_chart",
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_operational_charts(data: pd.DataFrame) -> None:
    summary = segment_summary(data)

    left, right = st.columns(2)

    with left:
        review = summary.dropna(subset=["median_review"]).copy()

        if review.empty:
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
            fig.update_xaxes(range=[0, 5.7], dtick=1)
            fig.update_layout(title="Median customer review score")
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.plotly_chart(
                style_chart(fig, max(250, 100 + len(review) * 75)),
                use_container_width=True,
                key="review_score_chart",
            )
            st.markdown("</div>", unsafe_allow_html=True)

    with right:
        delivery = summary.dropna(subset=["median_on_time_rate"]).copy()
        delivery["on_time_pct"] = delivery["median_on_time_rate"] * 100

        if delivery.empty:
            st.info("No delivery observations are available for this selection.")
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
            fig.update_xaxes(range=[0, 112], ticksuffix="%", dtick=25)
            fig.update_layout(title="Median on-time delivery rate")
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.plotly_chart(
                style_chart(fig, max(250, 100 + len(delivery) * 75)),
                use_container_width=True,
                key="on_time_chart",
            )
            st.markdown("</div>", unsafe_allow_html=True)


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
            "average_order_value": "Average order value (R$)",
            "average_review_score": "Review score",
            "on_time_delivery_rate": "On-time delivery",
            "average_delivery_days": "Delivery days",
        }
    )

    table["Sales value (R$)"] = table["Sales value (R$)"].round(2)
    table["Average order value (R$)"] = table["Average order value (R$)"].round(2)
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
            "Average order value (R$)": st.column_config.NumberColumn(
                "Average order value (R$)", format="R$ %.2f"
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
        st.metric("Average order value", format_currency(seller["average_order_value"]))

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
    st.markdown('<div class="eyebrow">BUSINESS INTELLIGENCE / SELLERS</div>', unsafe_allow_html=True)
    st.title("Seller intelligence")
    st.markdown(
        '<div class="subtitle">'
        "A consolidated view of seller activity, commercial performance "
        "and operational signals."
        "</div>",
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
        )

    with k2:
        kpi_card(
            "SEGMENTS",
            f"{filtered['segment'].nunique():,}",
            "Represented in current view",
        )

    with k3:
        value = (
            format_number(filtered["order_count"].median())
            if not filtered.empty
            else "—"
        )
        kpi_card("MEDIAN ORDERS", value, "Orders per seller")

    with k4:
        value = (
            format_currency(filtered["total_sales_value"].median())
            if not filtered.empty
            else "—"
        )
        kpi_card("MEDIAN SALES VALUE", value, "Item prices · freight excluded")

    st.markdown(
        '<div class="note" style="margin-top:0.7rem;">'
        "Sales value is the sum of item prices attributed to a seller, "
        "excluding freight. These are historical observations, not current "
        "seller performance."
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
            "Compare customer review scores and on-time delivery rates.",
        )
        render_operational_charts(filtered)

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

                if segment == "Established sellers":
                    st.write(
                        "This group has a more established order history in "
                        "the observed dataset. It is a descriptive segment, "
                        "not a guarantee of future performance."
                    )
                elif segment == "Potential delivery-risk sellers":
                    st.write(
                        "This group showed weaker observed delivery and review "
                        "signals in the exploratory analysis. Validate order "
                        "counts and individual delivery records before drawing "
                        "conclusions about any seller."
                    )
                else:
                    st.write(
                        "This group combines lower order volumes with positive "
                        "observed signals in the analysis. Small sample sizes "
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
                - **Average order value:** Seller sales value divided by distinct
                  seller-order pairs.
                - **Review score:** Average of associated order-level reviews;
                  it is a proxy for multi-seller orders.
                - **On-time delivery:** Share of eligible delivery observations
                  that met the estimated delivery date.
                - **Delivery days:** Average duration for eligible delivered orders.
                """
            )


# =========================================================
# 9. PAGE: PROJECT GUIDE
# =========================================================

elif page == "Project Guide":
    st.markdown('<div class="eyebrow">DOCUMENTATION / ANALYTICS</div>', unsafe_allow_html=True)
    st.title("Project guide")
    st.markdown(
        '<div class="subtitle">'
        "Business context, analytical workflow, instructions, data challenges "
        "and conclusions."
        "</div>",
        unsafe_allow_html=True,
    )

    tab_overview, tab_workflow, tab_challenges, tab_usage, tab_findings = st.tabs(
        [
            "Overview",
            "Analytical approach",
            "Data challenges",
            "How to use",
            "Findings & actions",
        ]
    )

    with tab_overview:
        st.markdown("### From seller data to operational insight")

        st.markdown(
            """
            **Business problem**

            E-commerce operations teams need a consistent way to explore
            seller activity, commercial contribution and potential operational
            concerns. Raw transactional tables are not always easy for
            stakeholders to interpret directly.

            **Project objective**

            Build an interactive seller intelligence tool that turns
            transactional and operational records into seller-level metrics,
            exploratory segments and business-facing views.

            **Intended users**

            Business Operations, Analytics, Sales Operations and teams
            responsible for seller performance monitoring.

            **What this tool provides**
            - Seller segmentation using K-Means clustering.
            - Seller-level commercial and operational indicators.
            - Interactive filtering, comparisons and seller search.
            - Individual seller profiles and CSV export.
            - Documented assumptions, data-quality issues and limitations.

            **Scope**

            This is an exploratory analytics portfolio project based on
            historical public data. It is not a live CRM, a production
            monitoring system or a validated seller risk model.
            """
        )

    with tab_workflow:
        st.markdown("### Analytical workflow")

        st.markdown(
            """
            **01 — Data inspection**

            Profile the source CSV files, row counts, missing values and
            completeness of relevant fields.

            **02 — Relationship validation**

            Check key uniqueness and relationships between orders, order
            items, sellers and reviews. Investigate unmatched seller IDs
            in the separate marketing-funnel dataset.

            **03 — Seller feature engineering**

            Aggregate transactional data to seller level. Calculate order
            counts, items sold, sales value, average order value, review
            scores and delivery metrics.

            **04 — Modeling preparation**

            Apply log transformations to skewed commercial variables,
            cap extreme delivery durations at the 99th percentile for
            modeling, impute missing clustering features and standardize
            the inputs.

            **05 — Cluster evaluation**

            Compare K-Means solutions for multiple values of k using the
            silhouette score. The three-cluster solution had a silhouette
            score of 0.3088 and is used here for exploratory profiling.

            **06 — Dashboard delivery**

            Present seller metrics, segment comparisons and interactive
            records using Streamlit and Plotly.
            """
        )

        st.info(
            "The silhouette score indicates limited separation between some "
            "clusters. Segment labels should be treated as exploratory."
        )

    with tab_challenges:
        st.markdown("### Data challenges and decisions")

        st.markdown(
            """
            **Missing observations**

            Some sellers have no eligible delivery observations or no review
            score. Missing clustering features were median-imputed for the
            model, while original missing values remain missing in this report.

            **Review attribution**

            Some orders contain items from multiple sellers. An order-level
            review cannot always be interpreted as a seller-specific rating.

            **Low seller activity**

            Many sellers have only a few orders. A high or low observed rate
            can be unstable when calculated from a small number of events.

            **Outliers and skewed values**

            Commercial variables are right-skewed. Log transformations help
            reduce the influence of extreme values during clustering.
            Delivery-duration capping is applied to modeling inputs only.

            **Cluster separation**

            A silhouette score of 0.3088 suggests the groups are not cleanly
            separated. They should not be interpreted as definitive categories
            or as evidence of causality.

            **Marketing attribution**

            In a separate relationship investigation, 380 of 842 closed deals
            matched a seller ID (45.1%). This does not establish that marketing
            leads generated the sales shown in this dashboard.

            **Historical coverage**

            The data represents activity from approximately 2016–2018.
            It cannot establish a seller's current performance.
            """
        )

    with tab_usage:
        st.markdown("### How to use this tool")

        st.markdown(
            """
            **Step 1 — Choose a business question**

            Start with a question such as:
            - Which segments contain the most sellers?
            - Which group has the highest median sales value?
            - Which sellers show weak observed delivery indicators?
            - How much activity supports a seller's metrics?

            **Step 2 — Apply portfolio filters**

            Use the sidebar to select seller segments and an order-count range.
            You can also raise the minimum review score or minimum on-time
            delivery rate to narrow the portfolio. KPIs and charts update
            to reflect these filters.

            **Step 3 — Read the overview**

            Check the number of sellers in view, segments represented,
            median order count and median sales value. These are descriptive
            summaries, not changes over time.

            **Step 4 — Compare segments**

            Review the seller distribution, median sales, review score and
            delivery rate together. Segment size and typical seller sales
            answer different questions.

            **Step 5 — Explore a seller**

            Open Seller Explorer, search by seller ID, change the sorting
            criterion and select a seller to see its profile.

            **Step 6 — Export the data**

            Download the filtered records to CSV for further analysis.
            The export reflects the search and current filters.

            **Step 7 — Check the limitations**

            Before making a recommendation, consider the seller's order
            volume, missing observations, review attribution and historical
            coverage.
            """
        )

        st.markdown("### Example exploration exercises")

        with st.expander("Exercise A — Find established, high-volume sellers"):
            st.markdown(
                """
                1. Select **Established sellers** in the sidebar.
                2. Raise the minimum order count.
                3. Open Seller Explorer and sort by sales value.
                4. Inspect several sellers and compare their order counts.
                5. Export the filtered records if you need to investigate further.

                **Question:** Do the sellers with the largest sales values
                also have the largest order counts?
                """
            )

        with st.expander("Exercise B — Investigate delivery signals"):
            st.markdown(
                """
                1. Select **Potential delivery-risk sellers**.
                2. Keep the minimum review score at its lowest setting.
                3. Inspect the on-time delivery chart.
                4. Open Seller Explorer and inspect individual profiles.
                5. Check order volume before interpreting a low delivery rate.

                **Question:** Which sellers warrant further investigation,
                and how much observed activity supports that assessment?
                """
            )

        with st.expander("Exercise C — Understand low-volume uncertainty"):
            st.markdown(
                """
                1. Select **Lower-volume sellers with positive observed signals**.
                2. Keep the order-count range broad.
                3. Compare median review and delivery indicators.
                4. Increase the minimum order count and observe how the
                   population and summaries change.

                **Question:** How does the amount of observed activity affect
                your confidence in the apparent performance signals?
                """
            )

    with tab_findings:
        st.markdown("### Key findings from the current analysis")

        findings = [
            (
                "Established sellers",
                1190,
                "38.4%",
                "32",
                "R$ 4,537.94",
                "4.15",
                "93%",
                "This group has a more established order history and higher "
                "typical sales value in the observed data.",
            ),
            (
                "Potential delivery-risk sellers",
                181,
                "5.8%",
                "3",
                "R$ 397.00",
                "3.00",
                "50%",
                "Delivery and review signals warrant investigation, but most "
                "sellers in this group have very few orders.",
            ),
            (
                "Lower-volume sellers with positive observed signals",
                1724,
                "55.7%",
                "3",
                "R$ 293.10",
                "4.40",
                "100%",
                "The positive observed signals should be interpreted cautiously "
                "because many sellers have few orders.",
            ),
        ]

        for name, count, share, orders, sales, review, on_time, description in findings:
            with st.expander(f"{name} · {count:,} sellers ({share})"):
                a, b, c, d = st.columns(4)

                with a:
                    st.metric("Median orders", orders)
                with b:
                    st.metric("Median sales value", sales)
                with c:
                    st.metric("Median review score", f"{review} / 5")
                with d:
                    st.metric("Median on-time delivery", on_time)

                st.write(description)

        st.markdown("### Business implications")

        st.markdown(
            """
            - Separate portfolio size from commercial contribution.
            - Investigate low delivery signals using order-level evidence.
            - Avoid firm judgments about sellers with limited observations.
            - Add observation counts and time-based trends before building
              a production monitoring or prioritization system.
            - Validate segment stability over time before operational adoption.
            """
        )

        st.success(
            "Overall conclusion: the project demonstrates a reproducible path "
            "from raw transactional data to seller-level features, exploratory "
            "segmentation and an interactive business-facing dashboard. "
            "The next analytical step is to test segment stability and "
            "validate whether the findings lead to useful operational actions."
        )

    st.markdown("### Methodology and metric definitions")

    with st.expander("Metric definitions"):
        st.markdown(
            """
            - **Sales value:** Sum of item prices attributed to a seller;
              freight is excluded.
            - **Average order value:** Seller sales value divided by distinct
              seller-order pairs.
            - **Review score:** Average of associated order-level review scores.
              It is a proxy for some multi-seller orders.
            - **On-time delivery rate:** Share of eligible delivery observations
              delivered on or before the estimated date.
            - **Average delivery days:** Average delivery duration among eligible
              delivered orders with the required timestamps.
            - **Median:** The middle observation; it is less sensitive to extreme
              values than the mean.
            - **Silhouette score:** A clustering metric describing how well
              observations fit their assigned cluster relative to other clusters.
            """
        )

    with st.expander("Technical stack and reproducibility"):
        st.markdown(
            """
            **Current application stack**
            - Python for data preparation and application logic.
            - Pandas for data manipulation.
            - Scikit-learn for feature preparation and clustering.
            - Streamlit for the interactive application.
            - Plotly for interactive charts.

            **Reproducibility**
            The dashboard reads the generated seller segment CSV from
            `data/processed/seller_segments.csv`. The analytical scripts
            should be run before launching the app.
            """
        )


# =========================================================
# 10. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        display:flex;
        justify-content:space-between;
        gap:1rem;
        flex-wrap:wrap;
    ">
        <span style="font-size:0.75rem; color:#94A3B8;">
            OLIST SELLER INTELLIGENCE · ANALYTICS PORTFOLIO PROJECT
        </span>
        <span style="font-size:0.75rem; color:#94A3B8;">
            Historical data · Exploratory insights · Not a live CRM
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
