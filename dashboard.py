import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_manager import fetch_bond_data
from config import TITLE, calculate_spread

# --- 페이지 설정 ---
st.set_page_config(page_title=TITLE, layout="wide", initial_sidebar_state="expanded")

# --- 스타일 적용 (Mockup과 유사한 프리미엄 디자인) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fc; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
    }
    .metric-value { font-size: 24px; font-weight: bold; color: #1e293b; }
    .metric-label { font-size: 14px; color: #64748b; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 타이틀 ---
st.title(f"📊 {TITLE}")

# --- 데이터 로드 ---
@st.cache_data(ttl=600)  # 10분마다 갱신
def get_data():
    return fetch_bond_data()

df = get_data()

if df.empty:
    st.error("데이터를 불러오지 못했습니다. Yahoo Finance 연결을 확인하세요.")
else:
    # --- 상단 메트릭 카드 ---
    cols = st.columns(len(df.columns) - 1)
    for i, col_name in enumerate(df.columns[1:]):
        with cols[i]:
            latest_val = df[col_name].iloc[-1]
            prev_val = df[col_name].iloc[-2]
            delta = latest_val - prev_val
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{col_name} Yield</div>
                    <div class="metric-value">{latest_val:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            st.metric(label="", value="", delta=f"{delta:+.3f}")

    # --- 메인 차트 영역 ---
    st.subheader("Time Series Analysis")
    fig = go.Figure()
    
    for col in df.columns[1:]:
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df[col], 
            mode='lines', 
            name=col,
            hovertemplate='%{x}<br>%{y:.2f}%'
        ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', ticksuffix="%"),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- 하단 분석 탭 ---
    st.subheader("Detailed Analysis")
    tab1, tab2 = st.tabs(["Yield Spreads", "Raw Data"])
    
    with tab1:
        spread_10y_2y = calculate_spread(df['US 10Y'], df['US 2Y'])
        fig_spread = go.Figure()
        fig_spread.add_trace(go.Scatter(x=df['date'], y=spread_10y_2y, name="10Y-2Y Spread", fill='tozeroy'))
        fig_spread.update_layout(title="US 10Y - 2Y Yield Spread", height=300)
        st.plotly_chart(fig_spread, use_container_width=True)
        
    with tab2:
        st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)

# --- 사이드바 ---
with st.sidebar:
    st.header("Settings")
    st.info("Yahoo Finance(yfinance)를 통해 실시간 데이터를 호출합니다.")
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()
