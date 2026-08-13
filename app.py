# ===================== 第1部分：导入所需库 =====================
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# ===================== 第2部分：页面设置 =====================
st.set_page_config(
    page_title="数碳校园 - 能碳监测平台",
    page_icon="🏫",
    layout="wide"
)

# ===================== 第3部分：标题 =====================
st.title("🏫 数碳校园：高校楼宇能碳一体化监测平台")
st.markdown("---")

# ===================== 第4部分：加载数据 =====================
@st.cache_data
def load_data():
    df = pd.read_csv('building_energy.csv')
    df['日期'] = pd.to_datetime(df['日期'])
    df['人数'] = pd.to_numeric(df['人数'],errors='coerce')
    df['能耗'] = pd.to_numeric(df['能耗'],errors='coerce')
    return df

df = load_data()

# ===================== 第5部分：侧边栏筛选 =====================
st.sidebar.header("🔍 数据筛选")
building_list = ['全部'] + list(df['楼宇'].unique())
selected_building = st.sidebar.selectbox("选择楼宇", building_list)

if selected_building == '全部':
    filtered_df = df
else:
    filtered_df = df[df['楼宇'] == selected_building]

# ===================== 第6部分：核心指标卡片 =====================
col1, col2, col3 = st.columns(3)

total_energy = filtered_df['能耗'].sum()
co2_factor = 0.5777
total_co2 = total_energy * co2_factor

col1.metric("总能耗", f"{total_energy:,.0f} kWh")
col2.metric("总碳排放", f"{total_co2:,.0f} kgCO₂")
col3.metric("总人数", f"{filtered_df['人数'].sum():,.0f} 人")

st.markdown("---")

# ===================== 第7部分：选项卡 =====================
tab1, tab2, tab3 = st.tabs(["📊 能耗趋势", "📈 楼宇对比", "🤖 能耗预测"])

with tab1:
    st.subheader(f"「{selected_building}」日能耗变化趋势")
    fig_line = px.line(filtered_df, x='日期', y='能耗', title='每日能耗')
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.subheader("各楼宇总能耗与碳排放对比")
    building_summary = df.groupby('楼宇').agg({'能耗': 'sum'}).reset_index()
    building_summary['碳排放'] = building_summary['能耗'] * co2_factor
    fig_bar = px.bar(building_summary, x='楼宇', y='能耗', title='各楼宇总能耗对比', color='楼宇')
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("未来7天能耗预测")
    if len(filtered_df) < 2:
        st.warning("数据量不足，请添加更多数据。")
    else:
        filtered_df_sorted = filtered_df.sort_values('日期')
        min_date = filtered_df_sorted['日期'].min()
        filtered_df_sorted['天数'] = (filtered_df_sorted['日期'] - min_date).dt.days
        X = filtered_df_sorted[['天数']]
        y = filtered_df_sorted['能耗']
        model = LinearRegression()
        model.fit(X, y)
        last_day = filtered_df_sorted['天数'].max()
        future_days = np.array([[last_day + i] for i in range(1, 8)])
        predictions = model.predict(future_days)
        last_date = filtered_df_sorted['日期'].max()
        future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 8)]
        pred_df = pd.DataFrame({
            '日期': future_dates,
            '预测能耗 (kWh)': predictions.round(1)
        })
        st.dataframe(pred_df)
        fig_pred = px.line(pred_df, x='日期', y='预测能耗 (kWh)', title='未来7天能耗预测趋势', markers=True)
        st.plotly_chart(fig_pred, use_container_width=True)

st.markdown("---")
st.caption("数据来源：模拟校园能耗数据 | 碳排放因子：0.5777 kgCO₂/kWh")