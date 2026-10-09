import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales & Revenue Dashboard",page_icon="📊",layout="wide")
st.title("📊 Sales & Revenue Analysis Dashboard")
st.caption("Interactive dashboard for KPI tracking and business insights.")

@st.cache_data
def sample():
    d=pd.read_csv("data/sales_data.csv")
    d["Date"]=pd.to_datetime(d["Date"])
    return d

upload=st.sidebar.file_uploader("Upload CSV",type=["csv"])
if upload:
    df=pd.read_csv(upload)
    required={"Date","Product","Category","City","Region","Quantity","Unit_Price","Revenue"}
    missing=required-set(df.columns)
    if missing:
        st.error("Missing columns: "+", ".join(sorted(missing)))
        st.stop()
    df["Date"]=pd.to_datetime(df["Date"],errors="coerce")
else:
    df=sample()

df["Quantity"]=pd.to_numeric(df["Quantity"],errors="coerce").fillna(0)
df["Unit_Price"]=pd.to_numeric(df["Unit_Price"],errors="coerce").fillna(0)
df["Revenue"]=pd.to_numeric(df["Revenue"],errors="coerce").fillna(df["Quantity"]*df["Unit_Price"])
df=df.dropna(subset=["Date"])

st.sidebar.header("🔎 Filters")
products=sorted(df.Product.dropna().unique())
categories=sorted(df.Category.dropna().unique())
regions=sorted(df.Region.dropna().unique())
sp=st.sidebar.multiselect("Product",products,default=products)
sc=st.sidebar.multiselect("Category",categories,default=categories)
sr=st.sidebar.multiselect("Region",regions,default=regions)

f=df[df.Product.isin(sp)&df.Category.isin(sc)&df.Region.isin(sr)].copy()
if f.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

revenue=f.Revenue.sum()
units=f.Quantity.sum()
transactions=len(f)
avg=revenue/transactions if transactions else 0

a,b,c,d=st.columns(4)
a.metric("💰 Total Revenue",f"₹{revenue:,.0f}")
b.metric("📦 Units Sold",f"{units:,.0f}")
c.metric("🧾 Transactions",f"{transactions:,}")
d.metric("📈 Avg Transaction",f"₹{avg:,.0f}")

st.divider()
l,r=st.columns(2)
with l:
    st.subheader("📈 Revenue Trend")
    monthly=f.assign(Month=f.Date.dt.to_period("M").astype(str)).groupby("Month").Revenue.sum()
    st.line_chart(monthly)
with r:
    st.subheader("🏆 Top Products")
    st.bar_chart(f.groupby("Product").Revenue.sum().sort_values(ascending=False))

l,r=st.columns(2)
with l:
    st.subheader("🌍 Revenue by Region")
    st.bar_chart(f.groupby("Region").Revenue.sum().sort_values(ascending=False))
with r:
    st.subheader("🗂️ Revenue by Category")
    st.bar_chart(f.groupby("Category").Revenue.sum().sort_values(ascending=False))

st.divider()
st.subheader("📋 Sales Data")
st.dataframe(f.sort_values("Date",ascending=False),use_container_width=True)

ps=f.groupby("Product").Revenue.sum()
rs=f.groupby("Region").Revenue.sum()
cs=f.groupby("Category").Revenue.sum()
st.subheader("💡 Business Insights")
st.write(f"• **Top product:** {ps.idxmax()}")
st.write(f"• **Top region:** {rs.idxmax()}")
st.write(f"• **Top category:** {cs.idxmax()}")
st.write(f"• **Total filtered revenue:** ₹{revenue:,.0f}")
