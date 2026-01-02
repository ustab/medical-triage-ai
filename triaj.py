import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Triage AI", layout="wide")

# Dil Sözlüğü
lang_dict = {
    "EN": {
        "title": "Intelligent Clinical Decision Support System",
        "hosp_label": "Hospital Name",
        "notes_label": "Physician Notes / Symptoms",
        "clinic_score": "Clinical Risk Score",
        "social_score": "Social Risk Score",
        "critical": "CRITICAL RISK",
        "social_warn": "🚨 SOCIAL ALERT: High risk of readmission!",
        "advice_title": "🚩 ADVICE: IMMEDIATE INTERVENTION (LEVEL 1)",
        "advice_desc": "⚠️ Patient shows symptoms of acute coronary syndrome and shock."
    },
    "TR": {
        "title": "Akıllı Klinik Karar Destek Sistemi",
        "hosp_label": "Hastane Adı",
        "notes_label": "Doktor Notları / Semptomlar",
        "clinic_score": "Klinik Risk Skoru",
        "social_score": "Sosyal Risk Puanı",
        "critical": "KRİTİK RİSK",
        "social_warn": "🚨 SOSYAL UYARI: Taburcu sonrası geri dönüş riski yüksek!",
        "advice_title": "🚩 TAVSİYE: ACİL MÜDAHALE (DÜZEY 1)",
        "advice_desc": "⚠️ Hasta akut koroner sendrom ve şok belirtileri gösteriyor."
    }
}

# Dil Seçimi
selected_lang = st.sidebar.selectbox("Language / Dil", ["EN", "TR"])
T = lang_dict[selected_lang]

st.title(f"🏥 {T['title']}")

# Hastane İsmi (Persistent)
if 'h_name' not in st.session_state:
    st.session_state['h_name'] = "Merkezi Şehir Hastanesi"

h_input = st.sidebar.text_input(T['hosp_label'], st.session_state['h_name'])
st.session_state['h_name'] = h_input
st.subheader(f"🏢 {st.session_state['h_name']}")

# Giriş Alanı
notlar = st.text_area(T['notes_label'], height=150)

# Analiz Mantığı
def analiz(txt):
    txt = txt.lower()
    s = 0
    if any(k in txt for k in ["acute coronary", "chest pain", "göğüs ağrısı"]): s += 50
    if any(k in txt for k in ["shock", "cardiogenic", "şok"]): s += 50
    return min(s, 100)

c_score = analiz(notlar)
s_score = 75 if any(k in notlar.lower() for k in ["alone", "financial", "yalnız", "maddi"]) else 0

# Görsel Çıktı
col1, col2 = st.columns(2)
with col1:
    st.write(f"**{T['clinic_score']}**")
    if c_score >= 80:
        st.error(f"%{c_score} - {T['critical']}")
        st.progress(c_score / 100)
    else:
        st.info(f"%{c_score}")
        st.progress(c_score / 100)

with col2:
    st.write(f"**{T['social_score']}**")
    st.write(f"{s_score}")
    if s_score > 50:
        st.warning(T['social_warn'])

# Tavsiye Bölümü
if c_score >= 80:
    st.divider()
    st.markdown(f"## {T['advice_title']}")
    st.markdown(f"{T['advice_desc']}")
