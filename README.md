# 📊 Finansal AI Analiz Asistanı

Şirketlerin yıllık gelir, gider ve kârlılık verilerini gerçek borsa kaynaklarından çekip, hesaplanan finansal oranlar üzerinden yapay zeka ile doğal dilde yorumlayan bir analiz asistanı.

🔗 **Canlı Demo:** [finansal-yorumlama-ai.streamlit.app](https://finansal-yorumlama-ai-kstzitmydrofsg2g3ivuxc.streamlit.app)

## 🎯 Proje Ne Yapıyor?

1. **Veri Çekme:** `yfinance` kütüphanesi ile seçilen şirketlerin (Apple, Microsoft, Tesla, Amazon vb.) gerçek finansal tablolarını (gelir tablosu) çeker.
2. **Analiz:** Ham finansal verilerden anlamlı oranlar hesaplar — net kâr marjı, brüt kâr marjı, operasyonel kâr marjı, yıllık gelir büyüme oranı.
3. **Yapay Zeka Yorumlama:** Hesaplanan oranları Claude (Anthropic API) modeline yapılandırılmış şekilde sunarak, kullanıcının sorularına **sadece gerçek verilere dayalı**, uydurmayan cevaplar üretir.
4. **İnteraktif Sohbet:** Kullanıcı birden fazla şirketi karşılaştırabilir, geçmiş konuşmayı hatırlayan bir sohbet botu ile serbestçe soru sorabilir.

## 🛠️ Kullanılan Teknolojiler

- **Python** — veri işleme ve backend mantığı
- **yfinance** — gerçek zamanlı finansal veri kaynağı
- **pandas** — veri temizleme ve oran hesaplama
- **Anthropic API (Claude)** — doğal dil yorumlama ve sohbet
- **Streamlit** — web arayüzü ve canlı deploy

## 💡 Öne Çıkan Teknik Detaylar

- **Halüsinasyon önleme:** LLM'e ham veri yerine, önceden hesaplanmış ve doğrulanmış oranlar sunularak modelin uydurma yapması engellendi (RAG'e benzer bir yaklaşım).
- **System prompt ile davranış sınırlama:** Bot, elindeki veri dışına çıkmayacak şekilde talimatlandırıldı; sorulan bir şirket veri setinde yoksa bunu açıkça belirtiyor.
- **Konuşma hafızası:** `session_state` ile kullanıcı-bot arasındaki konuşma geçmişi korunuyor, bot önceki soruları hatırlayarak bağlamsal cevaplar veriyor.

## 🚀 Yerelde Çalıştırma

```bash
# Depoyu klonla
git clone https://github.com/gammzze/finansal-yorumlama-ai.git
cd finansal-yorumlama-ai

# Sanal ortam oluştur ve aktive et
conda create -n finansal python=3.11
conda activate finansal

# Gerekli kütüphaneleri kur
pip install -r requirements.txt

# .env dosyası oluştur, içine kendi API key'ini ekle
echo ANTHROPIC_API_KEY=senin_key_in > .env

# Uygulamayı başlat
streamlit run app.py
```

## 📸 Ekran Görüntüleri


## 📌 Gelecek Planları

- [ ] Likidite ve borçluluk oranları eklenmesi
- [ ] Sektör ortalamasıyla karşılaştırma
- [ ] PDF rapor çıktısı
- [ ] Kullanıcının kendi CSV/Excel verisini yükleyebilmesi

## 👤 Geliştirici

**Gamze Ayar**
Kocaeli Üniversitesi — Bilişim Sistemleri Mühendisliği