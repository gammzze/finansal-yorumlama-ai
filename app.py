import streamlit as st
import yfinance as yf
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic()

st.set_page_config(page_title="Finansal AI Analiz", page_icon="📊", layout="wide")


# --- VERİ FONKSİYONLARI (öncekiyle aynı) ---
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


def coklu_veri_hazirla(semboller):
    tum_veri = ""
    basarili_semboller = []
    tum_oranlar = {}
    for sembol in semboller:
        try:
            oranlar = veri_hazirla(sembol)
            tum_veri += f"\n--- {sembol} ---\n{oranlar.to_string()}\n"
            basarili_semboller.append(sembol)
            tum_oranlar[sembol] = oranlar
        except Exception as e:
            st.warning(f"{sembol} yüklenemedi: {e}")
    return tum_veri, basarili_semboller, tum_oranlar


# --- SESSION STATE BAŞLATMA (hafıza için) ---
if "konusma_gecmisi" not in st.session_state:
    st.session_state.konusma_gecmisi = []
if "veri_metni" not in st.session_state:
    st.session_state.veri_metni = ""
if "basarili_semboller" not in st.session_state:
    st.session_state.basarili_semboller = []
if "tum_oranlar" not in st.session_state:
    st.session_state.tum_oranlar = {}


# --- SOL PANEL: Şirket seçimi ---
st.sidebar.title("📊 Finansal AI Analiz")
st.sidebar.markdown("Şirketlerin finansal verilerini yapay zeka ile analiz et")

girdi = st.sidebar.text_input(
    "Borsa sembollerini virgülle ayırarak gir",
    placeholder="AAPL,MSFT,TSLA,AMZN"
)

if st.sidebar.button("Verileri Yükle"):
    semboller = [s.strip().upper() for s in girdi.split(",") if s.strip()]
    with st.spinner("Veriler çekiliyor..."):
        veri_metni, basarili_semboller, tum_oranlar = coklu_veri_hazirla(semboller)
    st.session_state.veri_metni = veri_metni
    st.session_state.basarili_semboller = basarili_semboller
    st.session_state.tum_oranlar = tum_oranlar
    st.session_state.konusma_gecmisi = []  # yeni veri gelince sohbeti sıfırla
    st.sidebar.success(f"Yüklendi: {', '.join(basarili_semboller)}")


# --- ANA EKRAN ---
st.title("Finansal AI Analiz Asistanı")

if not st.session_state.basarili_semboller:
    st.info("Başlamak için sol panelden şirket sembollerini gir ve 'Verileri Yükle' butonuna bas.")
else:
    # Oranları tablo halinde göster
    st.subheader("📈 Finansal Oranlar")
    secili_sirket = st.selectbox("Tablo için şirket seç", st.session_state.basarili_semboller)
    st.dataframe(st.session_state.tum_oranlar[secili_sirket])

    st.divider()

    # --- SOHBET BÖLÜMÜ ---
    st.subheader("💬 Sohbet")

    sistem_talimati = f"""Sen bir finansal analiz asistanısın. Aşağıda birden fazla 
şirketin son 4 yıllık finansal oranları var. Kullanıcı bu şirketler hakkında soru 
sorabilir, karşılaştırma isteyebilir. SADECE bu verilere dayanarak cevapla. 
Elinde olmayan bir şirket sorulursa bunu açıkça belirt.
Veride olmayan bir şeyi (gelecek tahmini, hisse fiyatı vb.) asla uydurma.

MEVCUT ŞİRKETLER: {', '.join(st.session_state.basarili_semboller)}

VERİLER:
{st.session_state.veri_metni}
"""

    # Geçmiş mesajları ekrana yazdır
    for mesaj in st.session_state.konusma_gecmisi:
        with st.chat_message(mesaj["role"]):
            st.markdown(mesaj["content"])

    # Yeni mesaj girişi
    soru = st.chat_input("Şirketler hakkında bir şey sor...")

    if soru:
        st.session_state.konusma_gecmisi.append({"role": "user", "content": soru})
        with st.chat_message("user"):
            st.markdown(soru)

        with st.chat_message("assistant"):
            with st.spinner("Düşünüyor..."):
                yanit = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=600,
                    system=sistem_talimati,
                    messages=st.session_state.konusma_gecmisi
                )
                cevap = yanit.content[0].text
                st.markdown(cevap)

        st.session_state.konusma_gecmisi.append({"role": "assistant", "content": cevap})