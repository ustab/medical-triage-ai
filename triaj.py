import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Triage CDSS", layout="wide")

# Dil Ayarları
translations = {
    "TR": {"title": "Akıllı Klinik Karar Destek Sistemi", "clinic_score": "Klinik Risk Skoru", "social_score": "Sosyal Risk Puanı", "hospital": "Hastane Adı"},
    "EN": {"title": "Intelligent Clinical Decision Support System", "clinic_score": "Clinical Risk Score", "social_score": "Social Risk Score", "hospital": "Hospital Name"}
}

lang = st.sidebar.selectbox("Dil / Language", ["TR", "EN"])
T = translations[lang]

st.title(f"🏥 {T['title']}")

# Hastane İsmi Kaydı (Persistent)
if 'hosp_name' not in st.session_state:
    st.session_state['hosp_name'] = "Merkezi Şehir Hastanesi"

hosp_input = st.sidebar.text_input(T['hospital'], st.session_state['hosp_name'])
st.session_state['hosp_name'] = hosp_input
st.subheader(f"🏢 {st.session_state['hosp_name']}")

# --- GİRİŞ PANELİ ---
st.markdown("### Hasta Kayıt Paneli")
notlar = st.text_area("Klinik Notlar (Semptomlar, şikayetler)", height=150)

# --- KLİNİK ANALİZ MANTIĞI ---
def analiz_yap(metin):
    metin = metin.lower()
    skor = 0
    # Vaka metnine özel anahtar kelimeler
    if any(k in metin for k in ["acute coronary", "chest pain", "myocardial", "göğüs ağrısı"]): skor += 40
    if any(k in metin for k in ["cardiogenic shock", "kardiyojenik şok", "dehydrated"]): skor += 40
    if any(k in metin for k in ["anxious", "breath", "nefes darlığı"]): skor += 20
    return min(skor, 100)

klinik_skor = analiz_yap(notlar)

# --- GÖRSELLEŞTİRME ---
col1, col2 = st.columns(2)

with col1:
    st.write(f"**{T['clinic_score']}**")
    if klinik_skor >= 80:
        st.error(f"%{klinik_skor} - KRİTİK RİSK")
        st.progress(klinik_skor / 100)
    else:
        st.info(f"%{klinik_skor}")
        st.progress(klinik_skor / 100)

with col2:
    # Sosyal Risk (SDOH)
    st.write(f"**{T['social_score']}**")
    sosyal_skor = 75 if any(k in notlar.lower() for k in ["alone", "financial", "no caregiver"]) else 0
    st.write(f"{sosyal_skor}")
    if sosyal_skor > 50:
        st.warning("🚨 SOSYAL UYARI: Taburcu sonrası geri dönüş riski yüksek!")

st.divider()
if klinik_skor >= 80:
    st.markdown("## 🚩 TAVSİYE: ACİL MÜDAHALE (DÜZEY 1)")
    st.markdown("⚠️ *Hasta akut koroner sendrom ve şok belirtileri gösteriyor.*")

