import numpy as np

# --- 대시보드 설정 ---
TITLE = "BOND YIELD DASHBOARD (2602 TEST)"
SYMBOLS = {
    "US 10Y": "^TNX",      # CBOE Interest Rate 10 Year T-Note Yield
    "US 5Y": "^FVX",       # 5 Year Treasury Yield
    "US 30Y": "^TYX",      # 30 Year Treasury Yield
    "US 2Y": "^IRX"        # 13 Week Treasury Bill Proxy
}

# --- 사용자 지정 수식 영역 (이곳을 수정하여 로직을 바꿀 수 있습니다) ---

def calculate_spread(yield1, yield2):
    """장단기 금리차 계산: 예) 10Y - 2Y"""
    return yield1 - yield2

def calculate_moving_average(series, window=20):
    """이동평균선 계산"""
    return series.rolling(window=window).mean()

def calculate_bond_volatility(series, window=20):
    """수익률 변동성 (표준편차)"""
    return series.rolling(window=window).std()
