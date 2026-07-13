import yfinance as yf

apple = yf.Ticker("AAPL")
gelir_tablosu = apple.financials
print(gelir_tablosu)

gelir_tablosu.to_csv("apple_gelir_tablosu.csv")
import yfinance as yf

apple = yf.Ticker("AAPL")
gelir_tablosu = apple.financials

# Sadece ihtiyacımız olan satırları seçelim
onemli_kalemler = [
    "Total Revenue",
    "Cost Of Revenue", 
    "Gross Profit",
    "Operating Expense",
    "Operating Income",
    "Net Income"
]

ozet_tablo = gelir_tablosu.loc[onemli_kalemler]
print(ozet_tablo)

ozet_tablo.to_csv("apple_ozet.csv")
import yfinance as yf
import pandas as pd

apple = yf.Ticker("AAPL")
gelir_tablosu = apple.financials

onemli_kalemler = [
    "Total Revenue",
    "Cost Of Revenue", 
    "Gross Profit",
    "Operating Expense",
    "Operating Income",
    "Net Income"
]

ozet_tablo = gelir_tablosu.loc[onemli_kalemler]

# 2021 sütununu at (boş geliyor)
ozet_tablo = ozet_tablo.dropna(axis=1)

# Sütunları yıla göre eskiden yeniye sırala (soldan sağa kronolojik olsun)
ozet_tablo = ozet_tablo[sorted(ozet_tablo.columns)]

print("=== HAM VERİ ===")
print(ozet_tablo)

# --- ORAN HESAPLAMALARI ---
oranlar = pd.DataFrame(index=ozet_tablo.columns)

oranlar["Toplam Gelir"] = ozet_tablo.loc["Total Revenue"]
oranlar["Net Kâr"] = ozet_tablo.loc["Net Income"]
oranlar["Net Kâr Marjı (%)"] = (ozet_tablo.loc["Net Income"] / ozet_tablo.loc["Total Revenue"]) * 100
oranlar["Brüt Kâr Marjı (%)"] = (ozet_tablo.loc["Gross Profit"] / ozet_tablo.loc["Total Revenue"]) * 100
oranlar["Operasyonel Kâr Marjı (%)"] = (ozet_tablo.loc["Operating Income"] / ozet_tablo.loc["Total Revenue"]) * 100

# Gelir büyüme oranı (bir önceki yıla göre)
oranlar["Gelir Büyüme Oranı (%)"] = ozet_tablo.loc["Total Revenue"].pct_change() * 100

print("\n=== HESAPLANAN ORANLAR ===")
print(oranlar.round(2))

oranlar.to_csv("apple_oranlar.csv")