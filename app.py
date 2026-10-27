import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RFM by Sayan | Customer Intelligence",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DARK NEON DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 5%, #15285b 0%, transparent 35%),
        radial-gradient(ellipse at 90% 20%, #24134c 0%, transparent 35%),
        #071126;
    color: #edf3ff;
}

header[data-testid="stHeader"] {
    background: rgba(7, 17, 38, 0.9);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1734, #091126);
    border-right: 1px solid #243b70;
}

section[data-testid="stSidebar"] * {
    color: #edf3ff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1600px;
}

h1, h2, h3 {
    color: #f5f7ff !important;
    font-weight: 750 !important;
}

p, label {
    color: #bdcbed;
}

.hero {
    padding: 30px 32px;
    margin-bottom: 25px;
    border-radius: 22px;
    border: 1px solid #294b92;
    background:
        radial-gradient(ellipse at 80% 0%, #233e83 0%, transparent 45%),
        linear-gradient(120deg, #101c42, #10102d);
    box-shadow: 0 0 35px rgba(50, 100, 255, 0.13);
}

.hero-tag {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 30px;
    color: #c5a7ff;
    background: #251858;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.hero h1 {
    font-size: clamp(28px, 3vw, 43px);
    line-height: 1.25;
    margin: 16px 0 10px;
}

.gradient-text {
    background: linear-gradient(90deg, #48c8ff, #b58aff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #b9c9ed;
    margin-bottom: 0;
}

.brand {
    font-size: 27px;
    font-weight: 800;
    margin: 10px 0 4px;
}

.brand span {
    color: #a98aff;
}

.sub-brand {
    color: #91a5ce;
    font-size: 12px;
    letter-spacing: 1.5px;
}

.kpi {
    position: relative;
    min-height: 150px;
    padding: 22px 20px;
    margin-bottom: 14px;
    overflow: hidden;
    border-radius: 18px;
    background: linear-gradient(145deg, #121f40, #0c1630);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi:hover {
    transform: translateY(-4px);
}

.kpi-purple {
    border: 1px solid #8b45ff;
    box-shadow: 0 0 12px #7629d866, 0 0 28px #7629d822,
                inset 0 0 16px #7629d822;
}

.kpi-green {
    border: 1px solid #00e6ad;
    box-shadow: 0 0 12px #00e6ad55, 0 0 28px #00e6ad22,
                inset 0 0 16px #00e6ad18;
}

.kpi-blue {
    border: 1px solid #16aaff;
    box-shadow: 0 0 12px #168aff66, 0 0 28px #168aff22,
                inset 0 0 16px #168aff18;
}

.kpi-gold {
    border: 1px solid #ffba45;
    box-shadow: 0 0 12px #ffba4555, 0 0 28px #ffba4522,
                inset 0 0 16px #ffba4518;
}

.kpi-label {
    color: #c1cdec;
    font-size: 13px;
    font-weight: 600;
}

.kpi-value {
    font-size: clamp(16px, 1.4vw, 25px);
    font-weight: 800;
    margin: 15px 0 9px;
    color: #ffffff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.kpi-note {
    font-size: 11px;
    color: #8fa9d7;
}

.panel {
    padding: 22px;
    border: 1px solid #263f78;
    border-radius: 18px;
    background: linear-gradient(145deg, #101c39, #0b1530);
    box-shadow: 0 0 20px #193f8014;
    margin-bottom: 20px;
}

.section-caption {
    color: #90a6d1;
    font-size: 13px;
    margin-top: -8px;
    margin-bottom: 18px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #263f78;
    border-radius: 12px;
}

.stButton button, .stDownloadButton button {
    border-radius: 10px;
    border: 1px solid #7656e9;
    background: linear-gradient(100deg, #4524a5, #284ac2);
    color: white;
    font-weight: 600;
}

hr {
    border-color: #26395f;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATASET
# =========================================================

DATA_PATH = Path("data") / "sales_data.csv"

st.sidebar.markdown(
    '<div class="brand">📈 RFM <span>by Sayan</span></div>'
    '<div class="sub-brand">CUSTOMER INTELLIGENCE WORKSPACE</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Explore your data")

uploaded_file = st.sidebar.file_uploader(
    "Upload sales CSV (optional)",
    type=["csv"]
)

try:
    if uploaded_file is not None:
        sales_data = pd.read_csv(
            uploaded_file,
            dtype={"_CustomerID": str}
        )
    elif DATA_PATH.exists():
        sales_data = pd.read_csv(
            DATA_PATH,
            dtype={"_CustomerID": str}
        )
    else:
        st.title("📊 RFM by Sayan")
        st.error(
            "Dataset not found. Place sales_data.csv inside the data "
            "folder, or upload it using the sidebar."
        )
        st.code(
            "RFM_project/\n"
            "├── app.py\n"
            "└── data/\n"
            "    └── sales_data.csv"
        )
        st.stop()

except Exception as e:
    st.error(f"Unable to load the dataset: {e}")
    st.stop()


# =========================================================
# VALIDATE AND PREPARE DATA
# =========================================================

required_columns = [
    "OrderNumber",
    "_CustomerID",
    "OrderDate",
    "Unit Price",
    "Discount Applied",
    "Order Quantity"
]

missing_columns = [
    col for col in required_columns
    if col not in sales_data.columns
]

if missing_columns:
    st.error(
        "Your dataset is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

df = sales_data.copy()

df["_CustomerID"] = df["_CustomerID"].astype("string").str.strip()

df["OrderDate"] = pd.to_datetime(
    df["OrderDate"], errors="coerce"
)

for col in [
    "Unit Price",
    "Discount Applied",
    "Order Quantity"
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(
    subset=[
        "_CustomerID",
        "OrderNumber",
        "OrderDate",
        "Unit Price",
        "Discount Applied",
        "Order Quantity"
    ]
)

df = df[df["_CustomerID"] != ""]

if df.empty:
    st.error("No valid sales records were found in your dataset.")
    st.stop()

# Handle discounts represented either as 0.10 or 10.
discount = df["Discount Applied"].copy()

if not discount.empty and discount.abs().max() > 1:
    discount = discount / 100

discount = discount.clip(0, 1)

# Net sales revenue after discounts.
df["Revenue"] = (
    df["Unit Price"] * (1 - discount)
    * df["Order Quantity"]
)

# Profit is calculated separately when unit cost exists.
if "Unit Cost" in df.columns:
    df["Unit Cost"] = pd.to_numeric(
        df["Unit Cost"], errors="coerce"
    )
    df["Profit"] = (
        df["Unit Price"] * (1 - discount)
        - df["Unit Cost"]
    ) * df["Order Quantity"]
else:
    df["Profit"] = np.nan

latest_order = df["OrderDate"].max()

# Match the date convention in your original RFM analysis.
today_date = max(
    pd.Timestamp("2021-01-01"),
    latest_order.normalize() + pd.Timedelta(days=1)
)

rfm = df.groupby("_CustomerID").agg(
    recency=(
        "OrderDate",
        lambda x: (today_date - x.max().normalize()).days
    ),
    frequency=("OrderNumber", "count"),
    monetary=("Revenue", "sum"),
    last_order=("OrderDate", "max")
)

rfm["R"] = (
    pd.qcut(
        rfm["recency"].rank(method="first"),
        5,
        labels=[5, 4, 3, 2, 1]
    ).astype(int)
)

rfm["F"] = (
    pd.qcut(
        rfm["frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)
)

rfm["M"] = (
    pd.qcut(
        rfm["monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)
)

rfm["rfm_score_total"] = rfm[["R", "F", "M"]].sum(axis=1)

rfm["RFM Score"] = (
    rfm["R"].astype(str)
    + rfm["F"].astype(str)
    + rfm["M"].astype(str)
)

# =========================================================
# CUSTOMER SEGMENTS
# =========================================================

def customer_segment(row):
    r, f, m = row["R"], row["F"], row["M"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    if r >= 3 and f >= 4:
        return "Loyal Customers"

    if r >= 4 and f >= 2:
        return "Potential Loyalists"

    if r >= 4 and f <= 2:
        return "Recent Customers"

    if r <= 2 and f >= 3 and m >= 3:
        return "At Risk"

    if r <= 2 and f <= 2:
        return "Hibernating"

    return "Needs Attention"


rfm["Segment"] = rfm.apply(customer_segment, axis=1)
rfm.index.name = "_CustomerID"

segment_order = [
    "Champions",
    "Loyal Customers",
    "Potential Loyalists",
    "Recent Customers",
    "Needs Attention",
    "At Risk",
    "Hibernating"
]

segment_colors = {
    "Champions": "#9255ff",
    "Loyal Customers": "#287bff",
    "Potential Loyalists": "#20d49a",
    "Recent Customers": "#ffb52e",
    "Needs Attention": "#e34bbd",
    "At Risk": "#ff5267",
    "Hibernating": "#25c6cf"
}

currency_symbol = "$"

def money(value):
    return f"{currency_symbol}{value:,.0f}"


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Filters")

available_segments = [
    segment for segment in segment_order
    if segment in rfm["Segment"].unique()
]

selected_segments = st.sidebar.multiselect(
    "Customer segments",
    options=available_segments,
    default=available_segments
)

minimum_score = int(rfm["rfm_score_total"].min())
maximum_score = int(rfm["rfm_score_total"].max())

score_range = st.sidebar.slider(
    "Total RFM score",
    min_value=minimum_score,
    max_value=maximum_score,
    value=(minimum_score, maximum_score)
)

filtered = rfm[
    rfm["Segment"].isin(selected_segments)
    & rfm["rfm_score_total"].between(
        score_range[0], score_range[1]
    )
].copy()

st.sidebar.markdown("---")
st.sidebar.metric("Total customers", f"{len(rfm):,}")
st.sidebar.metric("Sales records", f"{len(df):,}")

st.sidebar.caption(
    "RFM by Sayan • Customer analytics"
)

if filtered.empty:
    st.warning(
        "No customers match the selected filters. "
        "Please select more segments or widen the RFM score range."
    )
    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <span class="hero-tag">RFM ANALYSIS</span>
    <h1>Know your customers.<br>
    Grow your <span class="gradient-text">business.</span></h1>
    <p>Understand customer behaviour, discover valuable segments,
    and make better data-driven decisions.</p>
</div>
""", unsafe_allow_html=True)

st.caption(
    f"Dataset period: {df['OrderDate'].min():%d %b %Y} — "
    f"{df['OrderDate'].max():%d %b %Y}"
)


# =========================================================
# KPI CARDS
# =========================================================

customer_count = len(filtered)

customer_ids = filtered.index

matching_orders = df[
    df["_CustomerID"].isin(customer_ids)
]

total_revenue = matching_orders["Revenue"].sum()

average_customer_value = (
    filtered["monetary"].mean()
    if customer_count else 0
)

average_rfm_score = filtered["rfm_score_total"].mean()
total_orders = matching_orders["OrderNumber"].nunique()  #Calculate Unique Orders
k1, k2, k3, k4, k5 = st.columns(5)

kpi_data = [
    (
        k1, "kpi-purple", "👥 CUSTOMERS IN VIEW",
        f"{customer_count:,}",
        "Unique customers after filters"
    ),
    (
        k2, "kpi-green", "💰 NET SALES REVENUE",
        money(total_revenue),
        "Revenue after discounts"
    ),
    (
        k3, "kpi-blue", "🎯 AVG. CUSTOMER VALUE",
        money(average_customer_value),
        "Average revenue per customer"
    ),
    (
        k4, "kpi-gold", "⭐ AVG. RFM SCORE",
        f"{average_rfm_score:.2f} / 15",
        "Recency + Frequency + Monetary"
    ),
    (
    k5, "kpi-purple", "🛒 TOTAL ORDERS",
    f"{total_orders:,}",
    "Unique orders in the dataset"
    )
]

for col, style, label, value, note in kpi_data:
    with col:
        st.markdown(
            f"""
            <div class="kpi {style}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CUSTOMER SEGMENTATION AND REVENUE CHARTS
# =========================================================

st.markdown("## 📊 Customer Intelligence")
st.markdown(
    '<div class="section-caption">'
    'Explore your customer segments and their business contribution.'
    '</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

segment_counts = (
    filtered["Segment"]
    .value_counts()
    .reindex(segment_order, fill_value=0)
)

segment_counts = segment_counts[segment_counts > 0]

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🍩 Customer Segmentation")

    fig = go.Figure(
        go.Pie(
            labels=segment_counts.index,
            values=segment_counts.values,
            hole=0.65,
            marker=dict(
                colors=[
                    segment_colors[s]
                    for s in segment_counts.index
                ],
                line=dict(color="#0b1530", width=3)
            ),
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Customers: %{value}<br>"
                "Share: %{percent}<extra></extra>"
            )
        )
    )

    fig.add_annotation(
        text=f"<b>{customer_count}</b><br>Customers",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=19, color="white")
    )

    fig.update_layout(
        height=360,
        margin=dict(t=15, b=15, l=5, r=5),
        showlegend=True,
        legend=dict(
            font=dict(color="#dce7ff", size=10),
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            x=0
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce7ff")
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("💵 Revenue by Segment")

    revenue_by_segment = (
        matching_orders.merge(
            filtered[["Segment"]],
            left_on="_CustomerID",
            right_index=True,
            how="inner"
        )
        .groupby("Segment")["Revenue"]
        .sum()
        .reindex(segment_order)
        .dropna()
        .sort_values()
    )

    if not revenue_by_segment.empty:
        revenue_fig = px.bar(
            x=revenue_by_segment.values,
            y=revenue_by_segment.index,
            orientation="h",
            text=[
                f"${value / 1_000_000:.2f}M"
                for value in revenue_by_segment.values
            ],
            color=revenue_by_segment.index,
            color_discrete_map=segment_colors
        )

        revenue_fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "%{y}<br>Revenue: $%{x:,.2f}<extra></extra>"
            )
        )

        revenue_fig.update_layout(
            height=360,
            showlegend=False,
            margin=dict(t=15, b=15, l=5, r=55),
            xaxis=dict(
                title="Revenue ($)",
                gridcolor="#203357",
                zeroline=False
            ),
            yaxis=dict(title="", gridcolor="rgba(0,0,0,0)"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dce7ff")
        )

        st.plotly_chart(
            revenue_fig, use_container_width=True
        )
    else:
        st.info("No revenue data available.")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# CUSTOMER BEHAVIOUR AND RFM DISTRIBUTION
# =========================================================

left, right = st.columns(2)

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🔵 Customer Behaviour")

    behaviour_fig = px.scatter(
        filtered.reset_index(),
        x="recency",
        y="frequency",
        size="monetary",
        color="Segment",
        hover_name="_CustomerID",
        hover_data={
            "recency": True,
            "frequency": True,
            "monetary": ":,.2f",
            "rfm_score_total": True,
            "Segment": True
        },
        color_discrete_map=segment_colors,
        size_max=27
    )

    behaviour_fig.update_layout(
        height=370,
        margin=dict(t=15, b=15, l=5, r=5),
        xaxis=dict(
            title="Recency (days)",
            gridcolor="#203357"
        ),
        yaxis=dict(
            title="Order Frequency",
            gridcolor="#203357"
        ),
        legend=dict(font=dict(color="#dce7ff", size=10)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce7ff")
    )

    st.plotly_chart(
        behaviour_fig, use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📈 RFM Score Distribution")

    score_counts = (
        filtered["rfm_score_total"]
        .value_counts()
        .sort_index()
    )

    score_fig = px.bar(
        x=score_counts.index,
        y=score_counts.values,
        text=score_counts.values
    )

    score_fig.update_traces(
        marker=dict(
            color=score_counts.values,
            colorscale=[
                [0, "#3436a5"],
                [0.5, "#7445ed"],
                [1, "#c17bff"]
            ],
            line=dict(color="#b18cff", width=1)
        ),
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "RFM Score: %{x}<br>"
            "Customers: %{y}<extra></extra>"
        )
    )

    score_fig.update_layout(
        height=370,
        margin=dict(t=20, b=15, l=5, r=15),
        xaxis=dict(
            title="Total RFM Score",
            dtick=1,
            gridcolor="#203357"
        ),
        yaxis=dict(
            title="Number of Customers",
            gridcolor="#203357"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce7ff")
    )

    st.plotly_chart(score_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# CUSTOMER EXPLORER
# =========================================================

st.markdown("---")
st.markdown("## 🔍 Customer Explorer")
st.markdown(
    '<div class="section-caption">'
    'Search, sort, inspect, and export your customer-level RFM analysis.'
    '</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search by Customer ID or segment",
    placeholder="For example: 1001 or Champions"
)

explorer = filtered.reset_index()

if search.strip():
    mask = (
        explorer["_CustomerID"].str.contains(
            search.strip(), case=False, na=False
        )
        | explorer["Segment"].str.contains(
            search.strip(), case=False, na=False
        )
    )
    explorer = explorer[mask]

sort_column = st.selectbox(
    "Sort customers by",
    options=[
        "rfm_score_total",
        "monetary",
        "frequency",
        "recency",
        "_CustomerID"
    ],
    format_func=lambda x: {
        "rfm_score_total": "Total RFM Score",
        "monetary": "Customer Revenue",
        "frequency": "Order Frequency",
        "recency": "Recency (days)",
        "_CustomerID": "Customer ID"
    }[x]
)

ascending = sort_column in ["recency", "_CustomerID"]

explorer = explorer.sort_values(
    sort_column, ascending=ascending
)

display_columns = [
    "_CustomerID",
    "recency",
    "frequency",
    "monetary",
    "R",
    "F",
    "M",
    "RFM Score",
    "rfm_score_total",
    "Segment"
]

display_names = {
    "_CustomerID": "Customer ID",
    "recency": "Recency (Days)",
    "frequency": "Frequency",
    "monetary": "Monetary Value ($)",
    "R": "R Score",
    "F": "F Score",
    "M": "M Score",
    "RFM Score": "RFM Code",
    "rfm_score_total": "Total RFM Score",
    "Segment": "Customer Segment"
}

table = explorer[display_columns].rename(
    columns=display_names
)

st.caption(f"Showing {len(table):,} customers")

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
    height=400
)

csv_data = table.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 Download Customer Analysis (CSV)",
    data=csv_data,
    file_name="rfm_by_sayan_customer_analysis.csv",
    mime="text/csv"
)


# =========================================================
# CUSTOMER DETAILS
# =========================================================

st.markdown("### 👤 Individual Customer Details")

customer_options = explorer["_CustomerID"].astype(str).tolist()

if customer_options:
    chosen_customer = st.selectbox(
        "Select a customer",
        options=customer_options
    )

    details = explorer[
        explorer["_CustomerID"].astype(str) == chosen_customer
    ].iloc[0]

    a, b, c, d = st.columns(4)

    a.metric("Recency", f"{int(details['recency'])} days")
    b.metric("Frequency", f"{int(details['frequency'])} orders")
    c.metric("Monetary Value", money(details["monetary"]))
    d.metric(
        "RFM Score",
        f"{int(details['rfm_score_total'])} / 15"
    )

    st.info(
        f"Customer segment: **{details['Segment']}** "
        f"| RFM code: **{details['RFM Score']}**"
    )
# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.markdown("---")
st.markdown("## 💡 Business Insights")
st.caption("Turn customer data into actionable business decisions.")

if not explorer.empty:

    # Count customers in each segment
    segment_counts = explorer["Segment"].value_counts()

    champions = int(segment_counts.get("Champions", 0))
    loyal = int(segment_counts.get("Loyal Customers", 0))
    at_risk = int(segment_counts.get("At Risk", 0))
    hibernating = int(segment_counts.get("Hibernating", 0))

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏆 Champions", champions)
    col2.metric("💙 Loyal Customers", loyal)
    col3.metric("⚠️ At-Risk Customers", at_risk)
    col4.metric("😴 Hibernating", hibernating)

    st.markdown("### 🎯 Recommended Business Actions")

    if champions > 0:
        st.success(
            f"🏆 **Reward Champions:** Offer exclusive rewards "
            f"to retain your {champions} valuable customers."
        )

    if loyal > 0:
        st.info(
            f"💙 **Strengthen Loyalty:** Introduce loyalty benefits "
            f"and personalised offers for {loyal} loyal customers."
        )

    if at_risk > 0:
        st.warning(
            f"⚠️ **Win Back At-Risk Customers:** Send targeted offers "
            f"to encourage {at_risk} customers to purchase again."
        )

    if hibernating > 0:
        st.info(
            f"😴 **Reactivate Hibernating Customers:** Use re-engagement "
            f"campaigns to reconnect with {hibernating} inactive customers."
        )

else:
    st.info("No customers are available for business insights.")


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:20px 0; color:#8399c4;">
        <strong style="color:#b59aff;">RFM by Sayan</strong><br>
        Customer Intelligence • RFM Analysis • Data-Driven Decisions
    </div>
    """,
    unsafe_allow_html=True
)