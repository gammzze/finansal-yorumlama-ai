import yfinance as yf
import pandas as pd

def veri_hazirla(sembol):
    """Bir şirketin finansal oranlarını hesaplar"""
    sirket = yf.Ticker(sembol)
    gelir_tablosu = sirket.financials

    onemli_kalemler = [
        "Total Revenue", "Cost Of Revenue", "Gross Profit",
        "Operating Expense", "Operating Income", "Net Income"
    ]
    ozet = gelir_tablosu.loc[onemli_kalemler].dropna(axis=1)
    ozet = ozet[sorted(ozet.columns)]

    oranlar = pd.DataFrame(index=ozet.columns)
    oranlar["Toplam Gelir"] = ozet.loc["Total Revenue"]
    oranlar["Net Kâr"] = ozet.loc["Net Income"]
    oranlar["Net Kâr Marjı (%)"] = (ozet.loc["Net Income"] / ozet.loc["Total Revenue"]) * 100
    oranlar["Brüt Kâr Marjı (%)"] = (ozet.loc["Gross Profit"] / ozet.loc["Total Revenue"]) * 100
    oranlar["Operasyonel Kâr Marjı (%)"] = (ozet.loc["Operating Income"] / ozet.loc["Total Revenue"]) * 100
    oranlar["Gelir Büyüme Oranı (%)"] = ozet.loc["Total Revenue"].pct_change() * 100

    return oranlar.round(2)


if __name__ == "__main__":
    sirketler = ["AAPL", "MSFT", "TSLA", "AMZN"]

    for sembol in sirketler:
        print(f"\n{'='*50}")
        print(f"{sembol} işleniyor...")
        print('='*50)
        try:
            oranlar = veri_hazirla(sembol)
            print(oranlar)
            oranlar.to_csv(f"{sembol}_oranlar.csv")
            print(f"✓ {sembol}_oranlar.csv kaydedildi")
        except Exception as e:
            print(f"✗ {sembol} için hata: {e}")