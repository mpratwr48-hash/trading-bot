import os
import time
import requests
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# --- إعدادات الحساب والبوت ---
# ضع التوكن والآيدي الخاص بك هنا بين علامات التنصيص
TELEGRAM_BOT_TOKEN = "ضع_توكن_البوت_هنا"
TELEGRAM_CHAT_ID = "ضع_ايدي_القناة_او_حسابك_هنا"

# قائمة أزواج OTC المشهورة في Pocket Option
OTC_PAIRS = [
    "EURUSD_OTC", "GBPUSD_OTC", "AUDUSD_OTC", "USDCAD_OTC", 
    "USDCHF_OTC", "EURGBP_OTC", "EURJPY_OTC", "GBPJPY_OTC"
]

def send_telegram_signal(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"خطأ في إرسال التليجرام: {e}")

def get_live_candles(pair):
    # دالة جلب الأسعار اللحظية (تُغذي ببيانات المنصة لاحقاً)
    return pd.DataFrame() 

def calculate_indicators(df):
    # الفلتر الأول: المتوسطات الثقيلة المتوازية
    df['SMMA_40'] = ta.rma(df['close'], length=40)
    df['SMMA_50'] = ta.rma(df['close'], length=50)
    df['SMMA_70'] = ta.rma(df['close'], length=70)
    df['SMMA_100'] = ta.rma(df['close'], length=100)
    
    # الفلتر الثاني والثالث: المتوسطات السريعة والعادية
    df['SMA_50'] = ta.sma(df['close'], length=50)
    df['SMA_100'] = ta.sma(df['close'], length=100)
    df['SMA_10'] = ta.sma(df['close'], length=10)
    df['WMA_20'] = ta.wma(df['close'], length=20)
    df['TMA_5'] = ta.sma(ta.sma(df['close'], length=3), length=3)
    
    # مؤشرات التأكيد الإضافية (RSI والزخم بإعدادات 45)
    df['RSI'] = ta.rsi(df['close'], length=14)
    df['MOM'] = ta.mom(df['close'], length=45)
    return df

def check_trading_strategy(df, pair):
    if len(df) < 100: return
    row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # فحص استقرار الاتجاه وانتظام المتوسطات الثقيلة
    m_up = (row['SMMA_40'] > row['SMMA_50'] > row['SMMA_70'] > row['SMMA_100'])
    m_down = (row['SMMA_40'] < row['SMMA_50'] < row['SMMA_70'] < row['SMMA_100'])
    stable = m_up or m_down

    # شروط تأكيد المؤشرات المساعدة
    rsi_buy, rsi_sell = row['RSI'] > 50, row['RSI'] < 50
    mom_buy, mom_sell = row['MOM'] > 0, row['MOM'] < 0

    # [1] استراتيجية نقطة الصفر (انعكاس الشمعة اللحظي)
    if stable:
        tma_up = (prev_row['TMA_5'] <= prev_row['SMA_10']) and (row['TMA_5'] > row['SMA_10'])
        tma_down = (prev_row['TMA_5'] >= prev_row['SMA_10']) and (row['TMA_5'] < row['SMA_10'])
        
        if tma_up and rsi_buy and mom_buy:
            send_signal_message(pair, "🟢 CALL (صعود)", "نقطة الصفر (الانعكاس المفاجئ)")
            return
        if tma_down and rsi_sell and mom_sell:
            send_signal_message(pair, "🔴 PUT (هبوط)", "نقطة الصفر (الانعكاس المفاجئ)")
            return

    # [2] استراتيجية الاختراق (تقاطع المتوسطات الثلاثية مع 50 و 100 SMA)
