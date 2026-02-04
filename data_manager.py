import yfinance as yf
import pandas as pd
import os
from config import SYMBOLS

def fetch_bond_data(period="1y", interval="1d"):
    """yfinance를 통해 채권 금리 데이터를 가져옵니다."""
    data_frames = {}
    for name, ticker in SYMBOLS.items():
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(period=period, interval=interval)
        if not df.empty:
            # 종가(Close)를 금리 값으로 사용
            data_frames[name] = df['Close']
    
    if not data_frames:
        return pd.DataFrame()

    # 모든 데이터를 날짜 기준으로 결합
    combined_df = pd.DataFrame(data_frames)
    
    # 결측치 보간 (Interpolation) - 선형 보간 적용
    combined_df = combined_df.interpolate(method='linear', limit_direction='both')
    
    # 인덱스 초기화 및 날짜 포맷 통일
    combined_df.index = combined_df.index.strftime('%Y-%m-%d')
    combined_df = combined_df.reset_index().rename(columns={'Date': 'date'})
    
    return combined_df

def save_to_csv(df, filename="history.csv"):
    """데이터를 CSV 파일로 저장합니다."""
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", filename)
    df.to_csv(path, index=False)
    return path

if __name__ == "__main__":
    # 데이터 수집 테스트
    print("Fetching data...")
    df = fetch_bond_data()
    if not df.empty:
        print(df.tail())
        path = save_to_csv(df)
        print(f"Data saved to {path}")
    else:
        print("No data fetched.")
