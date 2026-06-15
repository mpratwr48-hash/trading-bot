import pandas as pd
import pandas_ta as ta


def main():
    data = {
        "Date": [
            "2026-06-01",
            "2026-06-02",
            "2026-06-03",
            "2026-06-04",
            "2026-06-05",
            "2026-06-06",
            "2026-06-07",
            "2026-06-08",
            "2026-06-09",
            "2026-06-10",
        ],
        "Open": [100, 102, 101, 105, 107, 108, 110, 111, 109, 112],
        "High": [103, 104, 106, 108, 109, 112, 113, 114, 112, 115],
        "Low": [99, 100, 100, 104, 106, 107, 109, 110, 108, 111],
        "Close": [102, 101, 105, 107, 108, 111, 112, 113, 110, 114],
        "Volume": [1200, 1500, 1300, 1600, 1700, 1550, 1800, 1750, 1400, 1900],
    }

    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    print("=" * 60)
    print("بيانات الأسعار الأصلية:")
    print("=" * 60)
    print(df)
    print()

    # حساب مؤشر ADX باستخدام ta.adx
    print("=" * 60)
    print("حساب مؤشر ADX (Average Directional Index):")
    print("=" * 60)
    try:
        adx_result = ta.adx(high=df["High"], low=df["Low"], close=df["Close"], length=14)
        if adx_result is not None and not adx_result.empty:
            print("نتائج ADX:")
            print(adx_result)
        else:
            print("⚠️ مؤشر ADX يتطلب بيانات أكثر (حد أدنى 14 شمعة)")
            print("النتيجة الحالية: فارغة (البيانات المتاحة: 10 شموع فقط)")
    except Exception as e:
        print(f"خطأ في حساب ADX: {e}")
    print()

    # حساب مؤشر الستوكاستك باستخدام ta.stoch
    print("=" * 60)
    print("حساب مؤشر الستوكاستك (Stochastic Oscillator):")
    print("=" * 60)
    try:
        stoch_result = ta.stoch(high=df["High"], low=df["Low"], close=df["Close"], k=14, d=3, smooth_k=3)
        if stoch_result is not None and not stoch_result.empty:
            print("نتائج الستوكاستك:")
            print(stoch_result)
        else:
            print("⚠️ مؤشر الستوكاستك يتطلب بيانات أكثر (حد أدنى 14 شمعة)")
            print("النتيجة الحالية: فارغة (البيانات المتاحة: 10 شموع فقط)")
    except Exception as e:
        print(f"خطأ في حساب الستوكاستك: {e}")
    print()

    print("=" * 60)
    print("ملاحظة: للحصول على نتائج حقيقية للمؤشرات")
    print("تحتاج البيانات إلى عدد أكبر من الفترات الزمنية")
    print("=" * 60)


if __name__ == "__main__":
    main()
