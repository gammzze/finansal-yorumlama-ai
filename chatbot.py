import yfinance as yf
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic()

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

import time

def coklu_veri_hazirla(semboller):
    """Birden fazla şirketin verisini tek metinde birleştirir"""
    tum_veri = ""
    basarili_semboller = []
    for sembol in semboller:
        try:
            oranlar = veri_hazirla(sembol)
            tum_veri += f"\n--- {sembol} ---\n{oranlar.to_string()}\n"
            basarili_semboller.append(sembol)
            print(f"✓ {sembol} yüklendi")
        except Exception as e:
            print(f"✗ {sembol} yüklenemedi: {e}")
        time.sleep(1)  # her istekten sonra 1 saniye bekle, rate limit'e takılmamak için
    return tum_veri, basarili_semboller

def sohbet_baslat(semboller):
    print("\nŞirket verileri hazırlanıyor...")
    veri_metni, basarili_semboller = coklu_veri_hazirla(semboller)

    sistem_talimati = f"""Sen bir finansal analiz asistanısın. Aşağıda birden fazla 
şirketin son 4 yıllık finansal oranları var. Kullanıcı bu şirketler hakkında soru 
sorabilir, karşılaştırma isteyebilir. SADECE bu verilere dayanarak cevapla. 
Elinde olmayan bir şirket sorulursa (örn: veri listesinde yoksa) bunu açıkça belirt.
Veride olmayan bir şeyi (gelecek tahmini, hisse fiyatı vb.) asla uydurma.

MEVCUT ŞİRKETLER: {', '.join(basarili_semboller)}

VERİLER:
{veri_metni}
"""

    konusma_gecmisi = []

    print(f"\nŞu şirketler hakkında soru sorabilirsin: {', '.join(basarili_semboller)}")
    print("Çıkmak için 'çık' yaz.\n")

    while True:
        soru = input("Sen: ")
        if soru.lower() in ["çık", "exit", "quit"]:
            print("Görüşürüz!")
            break

        konusma_gecmisi.append({"role": "user", "content": soru})

        yanit = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=600,
            system=sistem_talimati,
            messages=konusma_gecmisi
        )

        cevap = yanit.content[0].text
        print(f"\nBot: {cevap}\n")

        konusma_gecmisi.append({"role": "assistant", "content": cevap})


if __name__ == "__main__":
    print("Hangi şirketler hakkında konuşmak istersin?")
    girdi = input("Sembolleri virgülle ayırarak yaz (örn: AAPL,MSFT,TSLA,AMZN): ")
    semboller = [s.strip().upper() for s in girdi.split(",")]
    sohbet_baslat(semboller)