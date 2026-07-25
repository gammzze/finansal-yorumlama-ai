import yfinance as yf
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic()
key = os.getenv("ANTHROPIC_API_KEY")
print(f"Key uzunluğu: {len(key) if key else 'BULUNAMADI'}")
print(f"Key başlangıcı: {key[:15] if key else ''}")
print(f"Key sonu: {key[-5:] if key else ''}")

def veri_hazirla(sembol):
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

def yapay_zeka_yorumu(sirket_adi, oranlar_tablosu):
    veri_metni = oranlar_tablosu.to_string()

    prompt = f"""Aşağıda {sirket_adi} şirketinin son 4 yıllık finansal oranları var:

{veri_metni}

Bu verilere dayanarak, bir finansal analist gibi kısa ve öz bir yorum yaz (maksimum 150 kelime). 
Şunlara değin: 
1) Gelir ve kârlılık trendi nasıl gidiyor
2) Dikkat çeken bir risk veya güçlü yön var mı
3) Genel değerlendirme

Sadece somut rakamlara dayan, uydurma yorum yapma."""

    yanit = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return yanit.content[0].text

if __name__ == "__main__":
    sembol = "AAPL"
    oranlar = veri_hazirla(sembol)
    print("=== ORANLAR ===")
    print(oranlar)

    print("\n=== YAPAY ZEKA YORUMU ===")
    yorum = yapay_zeka_yorumu(sembol, oranlar)
    print(yorum)