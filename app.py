# ===================== 第1部分：导入所需库 =====================
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import io
import base64

# ===================== 第2部分：页面设置 =====================
st.set_page_config(
    page_title="数碳校园 - 能碳监测平台",
    page_icon="🏛️",
    layout="wide"
)

# ===================== 第3部分：自定义CSS样式 =====================
st.markdown("""
<style>
    /* 整个页面背景 */
    .stApp {
        background: linear-gradient(145deg, #0b1120 0%, #141b33 60%, #0b1120 100%);
    }
    
    /* 主标题 */
    .main-title {
        color: #ffffff;
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #60b0ff, #00d4ff, #60b0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        padding-top: 10px;
    }
    .sub-title {
        color: #6688aa;
        text-align: center;
        font-size: 15px;
        letter-spacing: 6px;
        margin-top: -5px;
    }
    
    /* 发光分割线 */
    .glow-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,180,255,0.3), transparent);
        margin: 20px 0 30px 0;
    }
    
    /* ===== 指标卡片 ===== */
    .metric-card {
        background: rgba(16, 28, 58, 0.85);
        border: 1px solid rgba(60, 160, 255, 0.15);
        border-radius: 16px;
        padding: 24px 20px 20px 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        height: 100%;
    }
    .metric-card:hover {
        border-color: rgba(60, 160, 255, 0.4);
        box-shadow: 0 8px 40px rgba(0, 100, 255, 0.08);
        transform: translateY(-2px);
    }
    .metric-label {
        color: #7a9bcb;
        font-size: 13px;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .metric-number {
        color: #e8f0ff;
        font-size: 40px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .metric-number .highlight-blue {
        color: #5bb8ff;
    }
    .metric-number .highlight-green {
        color: #4cd9a0;
    }
    .metric-number .highlight-gold {
        color: #f0c040;
    }
    .metric-unit {
        color: #5a7a9a;
        font-size: 14px;
        font-weight: 400;
        margin-left: 6px;
    }
    .metric-footer {
        color: #4a6a8a;
        font-size: 12px;
        margin-top: 6px;
        border-top: 1px solid rgba(60, 160, 255, 0.06);
        padding-top: 8px;
    }
    
    /* ===== 图表容器 ===== */
    .chart-container {
        background: rgba(12, 22, 48, 0.7);
        border: 1px solid rgba(60, 160, 255, 0.08);
        border-radius: 16px;
        padding: 20px 20px 10px 20px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    .chart-title {
        color: #8ab4e8;
        font-size: 15px;
        font-weight: 500;
        letter-spacing: 1px;
        margin-bottom: 10px;
        padding-left: 4px;
    }
    .chart-title .emoji {
        margin-right: 8px;
    }
    
    /* ===== 排行榜卡片 ===== */
    .rank-card {
        background: rgba(12, 22, 48, 0.5);
        border: 1px solid rgba(60, 160, 255, 0.08);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .rank-number {
        color: #5a7a9a;
        font-size: 14px;
        font-weight: 600;
        width: 30px;
    }
    .rank-name {
        color: #c0d8f0;
        font-size: 14px;
        flex: 1;
        margin-left: 10px;
    }
    .rank-value {
        color: #5bb8ff;
        font-size: 14px;
        font-weight: 500;
    }
    .rank-bar-bg {
        background: rgba(60, 160, 255, 0.1);
        border-radius: 4px;
        height: 6px;
        width: 100px;
        overflow: hidden;
        margin-left: 10px;
    }
    .rank-bar-fill {
        background: linear-gradient(90deg, #5bb8ff, #4cd9a0);
        height: 100%;
        border-radius: 4px;
    }
    .rank-medal {
        font-size: 18px;
        margin-right: 6px;
    }
    
    /* ===== 环保换算卡片 ===== */
    .eco-card {
        background: rgba(12, 22, 48, 0.5);
        border: 1px solid rgba(60, 160, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .eco-card:hover {
        border-color: rgba(60, 160, 255, 0.2);
    }
    .eco-icon {
        font-size: 28px;
        margin-bottom: 4px;
    }
    .eco-number {
        color: #4cd9a0;
        font-size: 22px;
        font-weight: 700;
    }
    .eco-label {
        color: #5a7a9a;
        font-size: 12px;
        letter-spacing: 1px;
    }
    
    /* ===== 侧边栏 ===== */
    [data-testid="stSidebar"] {
        background: rgba(8, 16, 35, 0.95) !important;
        border-right: 1px solid rgba(60, 160, 255, 0.08) !important;
        padding-top: 10px;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #7a9bcb !important;
        font-size: 13px !important;
        letter-spacing: 1px !important;
    }
    [data-testid="stSidebar"] .stSelectbox div div {
        background: rgba(20, 40, 80, 0.6) !important;
        color: #c0d8f0 !important;
        border-color: rgba(60, 160, 255, 0.15) !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] .stDateInput label {
        color: #7a9bcb !important;
        font-size: 13px !important;
        letter-spacing: 1px !important;
    }
    .sidebar-header {
        color: #60b0ff;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        letter-spacing: 2px;
        padding: 8px 0;
        border-bottom: 1px solid rgba(60,160,255,0.08);
        margin-bottom: 20px;
    }
    .sidebar-stat {
        color: #5a7a9a;
        font-size: 12px;
        letter-spacing: 0.5px;
        padding: 6px 0;
        border-bottom: 1px solid rgba(60,160,255,0.04);
    }
    .sidebar-stat span {
        color: #8ab4e8;
        float: right;
    }
    
    /* ===== 上传区域 ===== */
    .upload-area {
        background: rgba(12, 22, 48, 0.5);
        border: 1.5px dashed rgba(60, 160, 255, 0.2);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 20px;
    }
    .upload-success {
        color: #4cd9a0;
        font-size: 13px;
    }
    .upload-hint {
        color: #5a7a9a;
        font-size: 13px;
    }
    .upload-hint strong {
        color: #8ab4e8;
        font-weight: 400;
    }
    
    /* ===== Tabs ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(12, 22, 48, 0.5);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(60,160,255,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        color: #5a7a9a;
        border-radius: 8px;
        padding: 8px 24px;
        font-size: 14px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(60, 160, 255, 0.12);
        color: #7ab8ff;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #9ac8ff;
        background: rgba(60, 160, 255, 0.05);
    }
    
    /* ===== 数据表格 ===== */
    .stDataFrame {
        background: rgba(12,22,48,0.3) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(60,160,255,0.06) !important;
    }
    .stDataFrame thead tr th {
        color: #7ab8ff !important;
        background: rgba(60,160,255,0.05) !important;
        font-weight: 400 !important;
    }
    .stDataFrame tbody tr td {
        color: #8aaac8 !important;
    }
    
    /* ===== 按钮 ===== */
    .stButton button {
        background: rgba(60, 160, 255, 0.1) !important;
        color: #7ab8ff !important;
        border: 1px solid rgba(60, 160, 255, 0.15) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background: rgba(60, 160, 255, 0.2) !important;
        border-color: rgba(60, 160, 255, 0.3) !important;
        box-shadow: 0 0 20px rgba(60, 160, 255, 0.05) !important;
    }
    
    /* ===== 底部 ===== */
    .footer {
        color: #3a5a7a;
        font-size: 12px;
        text-align: center;
        border-top: 1px solid rgba(60,160,255,0.06);
        padding-top: 18px;
        margin-top: 10px;
        letter-spacing: 1px;
    }
    .footer .highlight {
        color: #5a8aba;
    }
    
    /* ===== 零碳山海拓展页 ===== */
    .scenario-card {
        background: rgba(12, 22, 48, 0.6);
        border: 1px solid rgba(60, 160, 255, 0.1);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    .scenario-card:hover {
        border-color: rgba(60, 160, 255, 0.25);
        box-shadow: 0 4px 30px rgba(0, 100, 255, 0.05);
    }
    .scenario-title {
        color: #8ab4e8;
        font-size: 16px;
        font-weight: 500;
        letter-spacing: 1px;
    }
    .scenario-desc {
        color: #7a9bcb;
        font-size: 13px;
        line-height: 1.6;
        margin-top: 6px;
    }
    .scenario-tag {
        display: inline-block;
        background: rgba(60, 160, 255, 0.1);
        color: #7ab8ff;
        font-size: 11px;
        padding: 2px 12px;
        border-radius: 20px;
        margin-right: 6px;
        margin-top: 6px;
        letter-spacing: 0.5px;
    }
    
    /* 移除多余空白 */
    .block-container {
        padding-top: 20px !important;
        padding-bottom: 10px !important;
        max-width: 1200px !important;
    }
    .element-container {
        margin-bottom: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================== 第4部分：标题区域 =====================
st.markdown('<p class="main-title">🏛️ 数碳校园 · 能碳监测平台</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">高校楼宇能耗与碳排放一体化智能监控</p>', unsafe_allow_html=True)
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# ---- 右上角状态 ----
status_col1, status_col2, status_col3 = st.columns([6, 1, 1.2])
with status_col2:
    st.markdown('<p style="color:#4cd9a0;text-align:right;font-size:12px;border:1px solid rgba(76,217,160,0.15);border-radius:20px;padding:4px 14px;background:rgba(76,217,160,0.05);">● 在线</p>', unsafe_allow_html=True)
with status_col3:
    st.markdown(f'<p style="color:#4a6a8a;text-align:right;font-size:12px;">{datetime.now().strftime("%Y-%m-%d %H:%M")}</p>', unsafe_allow_html=True)

# ===================== 第5部分：数据上传 =====================
st.markdown('<div class="upload-area">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=['csv'], label_visibility="collapsed")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    required_columns = ['日期', '楼宇', '能耗', '人数']
    if all(col in df.columns for col in required_columns):
        df['日期'] = pd.to_datetime(df['日期'])
        df['人数'] = pd.to_numeric(df['人数'], errors='coerce')
        df['能耗'] = pd.to_numeric(df['能耗'], errors='coerce')
        st.markdown('<p class="upload-success">✅ 数据加载成功 · 系统就绪</p>', unsafe_allow_html=True)
        st.session_state['df'] = df
    else:
        st.error("❌ 文件格式错误，需要列：日期, 楼宇, 能耗, 人数")
        st.stop()
else:
    st.markdown('<p class="upload-hint">📂 请上传 <strong>CSV</strong> 格式的数据文件（包含：日期、楼宇、能耗、人数）</p>', unsafe_allow_html=True)
    st.stop()

df = st.session_state['df']
st.markdown('</div>', unsafe_allow_html=True)

# ===================== 第6部分：侧边栏（新增日期筛选） =====================
with st.sidebar:
    st.markdown('<p class="sidebar-header">⚙ 控制面板</p>', unsafe_allow_html=True)
    
    building_list = ['全部'] + list(df['楼宇'].unique())
    selected_building = st.selectbox("🏢 选择楼宇", building_list)
    
    st.markdown('<div style="margin-top:10px;">', unsafe_allow_html=True)
    st.markdown('<p style="color:#7a9bcb;font-size:13px;letter-spacing:1px;">📅 日期范围</p>', unsafe_allow_html=True)
    min_date = df['日期'].min().date()
    max_date = df['日期'].max().date()
    date_range = st.date_input(
        "",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (df['日期'].dt.date >= start_date) & (df['日期'].dt.date <= end_date)
        date_filtered_df = df[mask]
    else:
        date_filtered_df = df
    
    if selected_building == '全部':
        filtered_df = date_filtered_df
    else:
        filtered_df = date_filtered_df[date_filtered_df['楼宇'] == selected_building]
    
    st.markdown('<div style="margin-top:20px;">', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-stat">数据记录 <span>{len(filtered_df)} 条</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-stat">楼宇数量 <span>{len(df["楼宇"].unique())} 栋</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-stat">日期范围 <span>{filtered_df["日期"].min().strftime("%m/%d")} - {filtered_df["日期"].max().strftime("%m/%d")}</span></p>', unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top:20px;padding:12px 14px;background:rgba(60,160,255,0.04);border-radius:10px;border:1px solid rgba(60,160,255,0.06);">', unsafe_allow_html=True)
    st.markdown('<p style="color:#5a7a9a;font-size:11px;letter-spacing:0.5px;">碳排放因子</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#7ab8ff;font-size:18px;font-weight:600;">0.5777</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4a6a8a;font-size:11px;">kg CO₂ / kWh</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== 第7部分：核心指标卡片 =====================
total_energy = filtered_df['能耗'].sum()
total_co2 = total_energy * 0.5777
total_people = filtered_df['人数'].sum()
days_count = filtered_df['日期'].nunique()
avg_daily = total_energy / days_count if days_count > 0 else 0

st.markdown('<div style="padding:4px 0 10px 0;">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚡ 总能耗</div>
        <div class="metric-number"><span class="highlight-blue">{total_energy:,.0f}</span><span class="metric-unit">kWh</span></div>
        <div class="metric-footer">统计周期 {days_count} 天</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🌍 碳排放</div>
        <div class="metric-number"><span class="highlight-green">{total_co2:,.0f}</span><span class="metric-unit">kg CO₂</span></div>
        <div class="metric-footer">约 {total_co2/1000:.1f} 吨 CO₂</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">👥 覆盖人数</div>
        <div class="metric-number"><span class="highlight-blue">{total_people:,.0f}</span><span class="metric-unit">人</span></div>
        <div class="metric-footer">累计人次</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 日均能耗</div>
        <div class="metric-number"><span class="highlight-gold">{avg_daily:,.0f}</span><span class="metric-unit">kWh/日</span></div>
        <div class="metric-footer">人均 {avg_daily/total_people*1000:.1f} kWh/人·日</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===================== 第7.5部分：环保等效换算 =====================
st.markdown('<div style="padding:0 0 10px 0;">', unsafe_allow_html=True)
st.markdown('<div class="chart-container" style="padding:16px 20px 16px 20px;">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"><span class="emoji">🌱</span>你的减碳贡献 · 环保等效</div>', unsafe_allow_html=True)

# 计算各种等效值
trees_equivalent = total_co2 / 20  # 一棵树每年吸收约20kg CO₂
cars_km = total_co2 * 4.5  # 每kg CO₂ ≈ 4.5 km 开车排放
smartphones_charged = total_co2 * 200  # 每kg CO₂ ≈ 200次手机充电
incandescent_bulbs = total_co2 * 10  # 每kg CO₂ ≈ 10个灯泡工作24小时

eco_col1, eco_col2, eco_col3, eco_col4 = st.columns(4)

with eco_col1:
    st.markdown(f"""
    <div class="eco-card">
        <div class="eco-icon">🌳</div>
        <div class="eco-number">{trees_equivalent:,.0f}</div>
        <div class="eco-label">棵树的年吸碳量</div>
    </div>
    """, unsafe_allow_html=True)

with eco_col2:
    st.markdown(f"""
    <div class="eco-card">
        <div class="eco-icon">🚗</div>
        <div class="eco-number">{cars_km:,.0f}</div>
        <div class="eco-label">公里汽车行驶</div>
    </div>
    """, unsafe_allow_html=True)

with eco_col3:
    st.markdown(f"""
    <div class="eco-card">
        <div class="eco-icon">📱</div>
        <div class="eco-number">{smartphones_charged:,.0f}</div>
        <div class="eco-label">次手机充电</div>
    </div>
    """, unsafe_allow_html=True)

with eco_col4:
    st.markdown(f"""
    <div class="eco-card">
        <div class="eco-icon">💡</div>
        <div class="eco-number">{incandescent_bulbs:,.0f}</div>
        <div class="eco-label">个灯泡工作24h</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===================== 第8部分：主页面 / 拓展页 Tab 切换 =====================
main_tab, extra_tab = st.tabs(["📊 数据看板", "🌊 零碳山海 · 拓展"])

# ===================== 主Tab：数据看板 =====================
with main_tab:
    
    # ---- 板块1：能耗趋势 ----
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><span class="emoji">📈</span>能耗变化趋势</div>', unsafe_allow_html=True)
    
    daily_trend = filtered_df.groupby('日期')['能耗'].sum().reset_index()
    fig1 = px.line(daily_trend, x='日期', y='能耗',
                   color_discrete_sequence=['#5bb8ff'],
                   labels={'能耗': '能耗 (kWh)', '日期': ''})
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       font_color='#5a7a9a',
                       xaxis=dict(showgrid=False, linecolor='rgba(60,160,255,0.08)'),
                       yaxis=dict(gridcolor='rgba(60,160,255,0.06)', linecolor='rgba(60,160,255,0.08)'),
                       margin=dict(l=10, r=10, t=10, b=10),
                       height=350)
    fig1.update_traces(line=dict(width=2.5), mode='lines+markers', marker=dict(size=5, color='#5bb8ff'))
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    
    # ---- 板块2：两列布局（楼宇能耗对比 + 能耗占比） ----
    col_left, col_right = st.columns(2, gap="medium")
    
    with col_left:
        st.markdown('<div class="chart-container" style="height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><span class="emoji">🏢</span>各楼宇能耗对比</div>', unsafe_allow_html=True)
        
        building_compare = filtered_df.groupby('楼宇')['能耗'].sum().reset_index().sort_values('能耗', ascending=True)
        fig2 = px.bar(building_compare, x='能耗', y='楼宇', orientation='h',
                      color='能耗', color_continuous_scale=['#2a4a7a', '#5bb8ff', '#4cd9a0'],
                      labels={'能耗': '总能耗 (kWh)', '楼宇': ''})
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)',
                           font_color='#5a7a9a',
                           xaxis=dict(gridcolor='rgba(60,160,255,0.06)', linecolor='rgba(60,160,255,0.08)'),
                           yaxis=dict(showgrid=False),
                           margin=dict(l=10, r=10, t=10, b=10),
                           height=320,
                           coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="chart-container" style="height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><span class="emoji">🧩</span>能耗占比分布</div>', unsafe_allow_html=True)
        
        building_pct = filtered_df.groupby('楼宇')['能耗'].sum().reset_index()
        fig3 = px.pie(building_pct, values='能耗', names='楼宇',
                      color_discrete_sequence=['#2a6a9a', '#4a8aba', '#6aaada', '#8ac8ea', '#aae0f5'],
                      hole=0.45)
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)',
                           font_color='#5a7a9a',
                           margin=dict(l=10, r=10, t=10, b=10),
                           height=320,
                           legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5))
        fig3.update_traces(textposition='inside', textinfo='percent', textfont_color='#ffffff', textfont_size=11)
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    
    # ---- 板块3：楼宇能耗排行榜（新增） ----
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><span class="emoji">🏆</span>楼宇能耗排行榜</div>', unsafe_allow_html=True)
    
    rank_df = filtered_df.groupby('楼宇')['能耗'].sum().reset_index()
    rank_df = rank_df.sort_values('能耗', ascending=False)
    rank_df['排名'] = range(1, len(rank_df) + 1)
    max_energy = rank_df['能耗'].max()
    
    medals = ['🥇', '🥈', '🥉']
    
    for idx, row in rank_df.iterrows():
        rank = row['排名']
        medal = medals[rank-1] if rank <= 3 else f'#{rank}'
        bar_width = (row['能耗'] / max_energy) * 100 if max_energy > 0 else 0
        
        st.markdown(f"""
        <div class="rank-card">
            <div style="display:flex;align-items:center;flex:1;">
                <span class="rank-medal">{medal}</span>
                <span class="rank-name">{row['楼宇']}</span>
                <div class="rank-bar-bg">
                    <div class="rank-bar-fill" style="width:{bar_width}%;"></div>
                </div>
            </div>
            <span class="rank-value">{row['能耗']:,.0f} kWh</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    
    # ---- 板块4：预测 + 明细 ----
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    tab_pred, tab_data = st.tabs(["🔮 能耗预测", "📋 明细数据"])
    
    with tab_pred:
        st.markdown('<div style="padding:6px 0 4px 0;">', unsafe_allow_html=True)
        if len(filtered_df) < 3:
            st.info("数据量较少（至少需要3天），预测结果仅供参考。")
        
        filtered_sorted = filtered_df.sort_values('日期')
        min_d = filtered_sorted['日期'].min()
        filtered_sorted['天数序号'] = (filtered_sorted['日期'] - min_d).dt.days
        
        X_train = filtered_sorted[['天数序号']]
        y_train = filtered_sorted['能耗']
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        last_day_num = filtered_sorted['天数序号'].max()
        future_nums = np.array([[last_day_num + i] for i in range(1, 8)])
        pred_vals = model.predict(future_nums)
        last_date = filtered_sorted['日期'].max()
        future_dates_list = [last_date + pd.Timedelta(days=i) for i in range(1, 8)]
        
        pred_df = pd.DataFrame({
            '日期': future_dates_list,
            '预测能耗 (kWh)': pred_vals.round(1)
        })
        
        col_pred1, col_pred2 = st.columns([2, 1])
        with col_pred1:
            fig_pred = px.line(pred_df, x='日期', y='预测能耗 (kWh)',
                               markers=True, color_discrete_sequence=['#4cd9a0'])
            fig_pred.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   font_color='#5a7a9a',
                                   xaxis=dict(gridcolor='rgba(60,160,255,0.06)'),
                                   yaxis=dict(gridcolor='rgba(60,160,255,0.06)'),
                                   margin=dict(l=10, r=10, t=10, b=10),
                                   height=280)
            fig_pred.update_traces(line=dict(width=2), marker=dict(size=7, color='#4cd9a0'))
            st.plotly_chart(fig_pred, use_container_width=True, config={'displayModeBar': False})
        with col_pred2:
            st.markdown('<div style="padding:10px 0 0 10px;">', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#8ab4e8;font-size:13px;font-weight:500;">📊 预测结果</p>', unsafe_allow_html=True)
            for i, row in pred_df.iterrows():
                st.markdown(f'<p style="color:#7a9bcb;font-size:12px;margin:2px 0;">{row["日期"].strftime("%m-%d")} <span style="color:#4cd9a0;float:right;">{row["预测能耗 (kWh)"]:.0f} kWh</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#4a6a8a;font-size:11px;margin-top:10px;">模型 R² = {model.score(X_train, y_train):.3f}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab_data:
        st.dataframe(filtered_df.sort_values('日期'), use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ---- 板块5：数据导出功能 ----
    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container" style="padding:16px 20px 16px 20px;">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><span class="emoji">💾</span>数据导出</div>', unsafe_allow_html=True)
    
    export_col1, export_col2, export_col3 = st.columns([1, 1, 2])
    
    with export_col1:
        # 导出CSV
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 导出 CSV",
            data=csv_data,
            file_name=f"数碳校园_数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with export_col2:
        # 导出汇总报告
        summary_data = pd.DataFrame({
            '指标': ['总能耗 (kWh)', '碳排放 (kg CO₂)', '覆盖人数 (人)', '日均能耗 (kWh/日)', '统计天数'],
            '数值': [f'{total_energy:,.0f}', f'{total_co2:,.0f}', f'{total_people:,.0f}', f'{avg_daily:,.0f}', f'{days_count}']
        })
        csv_summary = summary_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 导出汇总报告",
            data=csv_summary,
            file_name=f"数碳校园_汇总报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with export_col3:
        st.markdown("""
        <div style="background:rgba(60,160,255,0.04);border-radius:10px;padding:10px 14px;border:1px solid rgba(60,160,255,0.06);">
            <p style="color:#5a7a9a;font-size:12px;margin:0;">
                💡 点击按钮导出当前筛选后的数据。<br>
                CSV 格式可在 Excel 中打开查看。
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== 拓展Tab：零碳山海 =====================
with extra_tab:
    st.markdown('<div style="padding:10px 0 10px 0;">', unsafe_allow_html=True)
    
    # 拓展页标题
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px 0;">
        <p style="color:#60b0ff;font-size:32px;font-weight:700;letter-spacing:4px;background:linear-gradient(90deg,#60b0ff,#4cd9a0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">🌊 零碳山海 · 技术拓展</p>
        <p style="color:#5a7a9a;font-size:14px;letter-spacing:3px;">宁德典型文旅场景零碳技术创新应用方案</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
    
    # ---- 拓展背景 ----
    st.markdown("""
    <div class="scenario-card">
        <p class="scenario-title">📌 拓展背景</p>
        <p class="scenario-desc">
            基于「数碳校园」平台的能碳监测与智能预测技术，本拓展方案将其迁移至宁德文旅场景，
            针对海岛、山地景区、滨海旅游、特色村落及大型赛事等多元场景，提出零碳技术创新解决方案。
            本技术框架具有良好的可迁移性，能够适配不同尺度的用能场景。
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ---- 技术迁移路径 ----
    st.markdown("""
    <div class="scenario-card">
        <p class="scenario-title">🔗 技术迁移路径</p>
        <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:10px;">
            <span class="scenario-tag">📊 数据采集架构 → 景区能耗监测</span>
            <span class="scenario-tag">🤖 智能预测模型 → 游客流量能耗预测</span>
            <span class="scenario-tag">📈 碳排放核算 → 文旅活动碳足迹</span>
            <span class="scenario-tag">🏆 排行榜机制 → 低碳景区/商户评比</span>
            <span class="scenario-tag">🌱 环保换算 → 游客碳普惠激励</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ---- 应用场景（3列） ----
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
    
    scene_col1, scene_col2, scene_col3 = st.columns(3)
    
    with scene_col1:
        st.markdown("""
        <div class="scenario-card" style="height:100%;">
            <p class="scenario-title" style="font-size:14px;">🏝️ 海岛旅游交通</p>
            <p class="scenario-desc" style="font-size:12px;">
                针对海岛电动接驳车、游船等交通工具，部署能耗监测终端，实时核算交通碳排放，优化调度路径。
            </p>
            <div style="margin-top:8px;">
                <span class="scenario-tag" style="font-size:10px;">电动接驳车</span>
                <span class="scenario-tag" style="font-size:10px;">游船碳排放</span>
                <span class="scenario-tag" style="font-size:10px;">路径优化</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with scene_col2:
        st.markdown("""
        <div class="scenario-card" style="height:100%;">
            <p class="scenario-title" style="font-size:14px;">⛰️ 景区零碳能源</p>
            <p class="scenario-desc" style="font-size:12px;">
                对景区光伏、储能、充电桩进行一体化能碳监测，结合游客流量预测，实现能源智能调度与供需平衡。
            </p>
            <div style="margin-top:8px;">
                <span class="scenario-tag" style="font-size:10px;">光伏监测</span>
                <span class="scenario-tag" style="font-size:10px;">储能调度</span>
                <span class="scenario-tag" style="font-size:10px;">供需预测</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with scene_col3:
        st.markdown("""
        <div class="scenario-card" style="height:100%;">
            <p class="scenario-title" style="font-size:14px;">🎪 赛事活动碳中和</p>
            <p class="scenario-desc" style="font-size:12px;">
                对大型赛事活动的用能、交通、废弃物进行全链条碳足迹追踪，实时计算碳排放并提供碳中和方案。
            </p>
            <div style="margin-top:8px;">
                <span class="scenario-tag" style="font-size:10px;">碳足迹追踪</span>
                <span class="scenario-tag" style="font-size:10px;">实时核算</span>
                <span class="scenario-tag" style="font-size:10px;">中和方案</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
    
    # ---- 拓展案例展示 ----
    st.markdown("""
    <div class="scenario-card">
        <p class="scenario-title">🧩 典型应用案例 · 海岛零碳交通</p>
        <p class="scenario-desc">
            <strong style="color:#8ab4e8;">场景：</strong>宁德某海岛景区，日均游客 5000 人，电动接驳车 30 辆，游船 10 艘。<br>
            <strong style="color:#8ab4e8;">方案：</strong>部署「数碳海洋」轻量化监测终端，采集电动车辆与游船的充放电数据、行驶里程，接入平台进行碳排放核算。<br>
            <strong style="color:#8ab4e8;">预期效益：</strong>年减碳约 120 吨 CO₂，节约燃油成本 30 万元，提升能源利用效率 20% 以上。
        </p>
        <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
            <span class="scenario-tag" style="background:rgba(76,217,160,0.1);color:#4cd9a0;">✅ 可复制</span>
            <span class="scenario-tag" style="background:rgba(76,217,160,0.1);color:#4cd9a0;">✅ 可推广</span>
            <span class="scenario-tag" style="background:rgba(76,217,160,0.1);color:#4cd9a0;">✅ 可量化</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ---- 与大赛命题的关联 ----
    st.markdown("""
    <div style="background:rgba(60,160,255,0.04);border:1px solid rgba(60,160,255,0.1);border-radius:12px;padding:16px 20px;margin-top:10px;">
        <p style="color:#5a7a9a;font-size:12px;letter-spacing:1px;margin:0;">
            🏆 <strong style="color:#8ab4e8;">赛道关联</strong> · 本拓展方案紧扣大赛「零碳山海——宁德典型文旅场景零碳技术创新挑战」命题，
            展示了「数碳校园」平台技术的可迁移性与应用潜力，为文旅场景零碳转型提供技术参考。
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================== 第9部分：底部 =====================
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
st.markdown(f"""
<div class="footer">
    数据来源 · 用户上传 ｜ 碳排放因子 0.5777 kg CO₂/kWh ｜
    更新于 <span class="highlight">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span> ｜
    数碳校园 v3.0 · 零碳山海拓展
</div>
""", unsafe_allow_html=True)
