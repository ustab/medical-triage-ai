import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Triage AI", layout="wide")

# Dil Seçimi
lang = st.sidebar.selectbox("Language / Dil", ["EN", "TR"])

t = {
    "EN": {"title": "Intelligent Clinical Decision Support System", "clinic": "Clinical Risk Score", "social": "Social Risk Score", "alert": "EMERGENCY: IMMEDIATE INTERVENTION"},
    "TR": {"title": "Akıllı Klinik Karar Destek Sistemi", "clinic": "Klinik Risk Skoru", "social": "Sosyal Risk Puanı", "alert": "ACİL: HEMEN MÜDAHALE"}
}[lang]

st.title(f"🏥 {t['title']}")

# Hastane İsmi
if 'h_name' not in st.session_state: st.session_state['h_name'] = "NIZAMIYE HOSPITAL NIGERIA"
st.session_state['h_name'] = st.sidebar.text_input("Hospital", st.session_state['h_name'])
st.subheader(f"🏢 {st.session_state['h_name']}")

# Giriş Alanı
notlar = st.text_area("Physician Notes / Doktor Notları", height=150)

# --- ANALİZ MANTIĞI (Burayı Çok Hassas Ayarladım) ---
def analiz(txt):
    txt = txt.lower()
    s = 0
    # Eğer bu kelimelerden biri varsa skoru artır
    if "acute coronary" in txt or "chest pain" in txt: s += 50
    if "shock" in txt or "cardiogenic" in txt: s += 50
    return min(s, 100)

c_score = analiz(notlar)
s_score = 75 if ("alone" in notlar.lower() or "financial" in notlar.lower()) else 0

# Görsel Çıktı
col1, col2 = st.columns(2)
with col1:
    st.metric(t['clinic'], f"%{c_score}")
    st.progress(c_score / 100)
    if c_score >= 80: st.error(t['alert'])

with col2:
    st.metric(t['social'], s_score)
    if s_score > 50: st.warning("⚠️ High Social Risk")

st.divider()
if c_score >= 80:
    st.markdown(f"### 🚩 **{t['alert']}**")
    st.balloons()
