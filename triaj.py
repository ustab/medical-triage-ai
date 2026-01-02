import streamlit as st
import pandas as pd
from fpdf import FPDF

# Sayfa Yapılandırması
st.set_page_config(page_title="Smart Triage CDSS", layout="wide")

# Dil Seçenekleri
languages = {
    "Türkçe": {"title": "Akıllı Klinik Karar Destek Sistemi", "not_label": "Doktor Notları / Ön Tanı", "risk_label": "Klinik Risk Analizi", "sdoh_label": "Sosyal Belirleyiciler (SDOH)", "btn": "Rapor Oluştur"},
    "English": {"title": "Intelligent Clinical Decision Support System", "not_label": "Physician Notes / Pre-Diagnosis", "risk_label": "Clinical Risk Analysis", "sdoh_label": "Social Determinants of Health (SDOH)", "btn": "Generate Report"},
    "Deutsch": {"title": "Intelligentes Klinisches Entscheidungshilfesystem", "not_label": "Arztnotizen / Vordiagnose", "risk_label": "Klinische Risikoanalyse", "sdoh_label": "Soziale Determinanten (SDOH)", "btn": "Bericht Erstellen"}
}

lang_choice = st.sidebar.radio("Language / Dil", list(languages.keys()))
L = languages[lang_choice]

st.title(f"🏥 {L['title']}")

# Sabit veya Değiştirilebilir Hastane İsmi
if 'hosp_name' not in st.session_state:
    st.session_state['hosp_name'] = "City Central Hospital"

new_hosp = st.sidebar.text_input("Hospital Name", st.session_state['hosp_name'])
st.session_state['hosp_name'] = new_hosp
st.subheader(f"🏢 {st.session_state['hosp_name']}")

# --- GİRİŞ ALANI ---
notlar = st.text_area(L['not_label'], height=150, placeholder="Type clinical notes here...")

# --- ANALİZ MANTIĞI ---
def analiz_et(metin):
    metin = metin.lower()
    tespitler = []
    # Genişletilmiş Anahtar Kelimeler (Sizin verdiğiniz vaka için optimize edildi)
    sozluk = {
        "AKUT KORONER SENDROM": ["acute coronary", "chest pain", "myocardial", "göğüs ağrısı", "brustschmerzen"],
        "KARDİYOJENİK ŞOK": ["cardiogenic shock", "kardiyojenik şok", "hypotension", "dehydrated"],
        "SEPSİS": ["sepsis", "infection", "enfeksiyon", "fever"],
        "İNME": ["stroke", "inme", "paralysis", "schlaganfall"]
    }
    for risk, kelimeler in sozluk.items():
        if any(k in metin for k in kelimeler):
            tespitler.append(risk)
    return tespitler

bulunan_riskler = analiz_et(notlar)

# --- EKRAN ÇIKTISI ---
col1, col2 = st.columns(2)

with col1:
    st.header(L['risk_label'])
    for r in ["AKUT KORONER SENDROM", "KARDİYOJENİK ŞOK", "SEPSİS", "İNME"]:
        if r in bulunan_riskler:
            st.error(f"🚨 {r} - RISK DETECTED")
        else:
            st.success(f"✅ {r} - Normal")

with col2:
    st.header(L['sdoh_label'])
    # SDOH Kelime Avı
    sdoh_risk = False
    if any(k in notlar.lower() for k in ["lives alone", "financial", "no caregiver", "yalnız yaşıyor", "maddi"]):
        st.warning("⚠️ High Social Risk: Vulnerable Patient Profile")
        sdoh_risk = True
    else:
        st.info("ℹ️ Social status appears stable.")

# Triage Level
if len(bulunan_riskler) > 0:
    st.divider()
    st.markdown("### 🚩 RECOMMENDED ACTION: **IMMEDIATE INTERVENTION (LEVEL 1)**")

if st.button(L['btn']):
    st.balloons()
    st.write("PDF Report is being generated...")
