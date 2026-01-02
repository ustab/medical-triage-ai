import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

# --- 1. DİL SÖZLÜĞÜ (TR, EN, DE) ---
LANG = {
    "TR": {
        "title": "Akıllı Klinik Karar Destek Sistemi",
        "h_name": "Hastane Adı (Opsiyonel)",
        "p_info": "Hasta Kayıt Paneli",
        "p_name": "Hasta Adı / Soyadı",
        "notes": "Klinik Notlar (Semptomlar, şikayetler)",
        "social": "Sosyal Belirleyiciler (SDOH)",
        "food": "Gıda Güvensizliği",
        "unemp": "İşsizlik / Ekonomik Risk",
        "alone": "Yalnız Yaşama / Bakım Eksikliği",
        "analysis": "AI Klinik Analiz Sonuçları",
        "risk_score": "Klinik Risk Skoru",
        "social_score": "Sosyal Risk Puanı",
        "recommendations": "🩺 Klinik Tavsiye ve Protokol Hatırlatıcı",
        "save": "Kayıt ve PDF Raporu Oluştur",
        "warning": "🚨 SOSYAL UYARI: Taburcu sonrası geri dönüş riski yüksek!",
        "success": "Veriler başarıyla işlendi ve PDF raporu hazırlandı."
    },
    "EN": {
        "title": "Smart Clinical Decision Support System",
        "h_name": "Hospital Name (Optional)",
        "p_info": "Patient Entry Panel",
        "p_name": "Patient Full Name",
        "notes": "Clinical Notes (Symptoms, complaints)",
        "social": "Social Determinants (SDOH)",
        "food": "Food Insecurity",
        "unemp": "Unemployment / Economic Risk",
        "alone": "Living Alone / Lack of Care",
        "analysis": "AI Clinical Analysis Results",
        "risk_score": "Clinical Risk Score",
        "social_score": "Social Risk Score",
        "recommendations": "🩺 Clinical Recommendations & Protocols",
        "save": "Save & Generate PDF Report",
        "warning": "🚨 SOCIAL ALERT: High risk of readmission!",
        "success": "Data processed successfully and PDF report is ready."
    },
    "DE": {
        "title": "Intelligentes Klinisches Entscheidungssystem",
        "h_name": "Krankenhausname (Optional)",
        "p_info": "Patienten-Eingabepanel",
        "p_name": "Patientenname",
        "notes": "Klinische Notizen (Symptome, Beschwerden)",
        "social": "Soziale Determinanten (SDOH)",
        "food": "Ernährungsunsicherheit",
        "unemp": "Arbeitslosigkeit",
        "alone": "Allein lebend",
        "analysis": "KI-Klinische Analyseergebnisse",
        "risk_score": "Klinisches Risiko",
        "social_score": "Soziales Risiko",
        "recommendations": "🩺 Klinische Empfehlungen & Protokolle",
        "save": "Speichern & PDF-Bericht erstellen",
        "warning": "🚨 SOZIALER ALARM: Hohes Wiederaufnahme-Risiko!",
        "success": "Daten verarbeitet und PDF-Bericht bereit."
    }
}

# --- 2. AYARLAR ---
st.set_page_config(page_title="Merkezi Şehir Hastanesi", layout="wide")
sel_lang = st.sidebar.selectbox("Dil Seçimi / Select Language", ["TR", "EN", "DE"])
L = LANG[sel_lang]

# --- 3. KLİNİK TAVSİYE MOTORU ---
def klinik_tavsiye_uret(p_notes, ai_score, s_score):
    advices = []
    n_lower = p_notes.lower()
    
    # Klinik Senaryolar (Doktoru yönlendiren kısımlar)
    if any(x in n_lower for x in ["sepsis", "enfeksiyon", "ates"]):
        advices.append("👉 **SEPSİS:** Laktat takibi yapın ve 1 saat içinde geniş spektrumlu antibiyotik başlayın.")
    if any(x in n_lower for x in ["inme", "felc", "felç", "strok"]):
        advices.append("👉 **NÖROLOJİ:** Kapı-BT süresini kontrol edin. Trombolitik tedavi penceresini değerlendirin.")
    if any(x in n_lower for x in ["kalp", "agri", "gogus", "infarkt"]):
        advices.append("👉 **KARDİYOLOJİ:** 10 dakika içinde EKG çekilmeli ve Troponin takibi yapılmalıdır.")
    
    # Sosyal Senaryolar
    if s_score >= 45:
        advices.append("🏠 **SOSYAL HİZMET:** Hastanın sosyal risk puanı yüksek. Evde bakım desteği onaylanmadan taburcu edilmemesi önerilir.")
    
    if not advices:
        advices.append("✅ Mevcut bulgular stabil görünmektedir. Rutin klinik takip önerilir.")
    
    return advices

# --- 4. PDF SİSTEMİ (TÜRKÇE KARAKTER TEMİZLİĞİYLE) ---
def create_pdf(h_name, p_name, a_score, s_score, advice_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Karakter temizleme fonksiyonu (Unicode hatalarını önlemek için)
    def clean(text):
        rep = {"ş": "s", "Ş": "S", "ı": "i", "İ": "I", "ğ": "g", "Ğ": "G", "ü": "u", "Ü": "U", "ö": "o", "Ö": "O", "ç": "c", "Ç": "C"}
        for k, v in rep.items():
            text = text.replace(k, v)
        return str(text).encode('ascii', 'ignore').decode('ascii')

    pdf.cell(200, 10, txt=clean(h_name), ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Patient: {clean(p_name)}", ln=True)
    pdf.cell(200, 10, txt=f"Clinical Risk: %{a_score}", ln=True)
    pdf.cell(200, 10, txt=f"Social Risk: {s_score}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Clinical Recommendations:", ln=True)
    for adv in advice_list:
        pdf.multi_cell(0, 10, txt=f"- {clean(adv)}")
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 5. ANA PANEL TASARIMI ---
st.title(f"🏥 {L['title']}")

# Opsiyonel Hastane İsmi (Persist özelliği Sidebar'da)
h_name = st.sidebar.text_input(L['h_name'], value="Merkezi Sehir Hastanesi")

with st.sidebar:
    st.divider()
    st.header(L['p_info'])
    p_name = st.text_input(L['p_name'], "Hasta X")
    p_notes = st.text_area(L['notes'], placeholder="Örn: Hastada göğüs ağrısı ve nefes darlığı mevcut...")
    st.subheader(L['social'])
    f_risk = st.checkbox(L['food'])
    u_risk = st.checkbox(L['unemp'])
    a_risk = st.checkbox(L['alone'])

# Mantıksal Analiz (BioBERT Simülasyonu)
s_score = (30 if f_risk else 0) + (20 if u_risk else 0) + (25 if a_risk else 0)
ai_score = 85 if any(x in p_notes.lower() for x in ["sepsis", "inme", "felc", "infarkt", "strok"]) else 25

# Görsel Dashboard
col1, col2 = st.columns(2)
with col1:
    st.metric(L['risk_score'], f"%{ai_score}")
    st.progress(ai_score / 100)

with col2:
    st.metric(L['social_score'], s_score)
    if s_score >= 45:
        st.error(L['warning'])

st.divider()

# Tavsiye Bölümü
st.header(L['recommendations'])
advices = klinik_tavsiye_uret(p_notes, ai_score, s_score)
for a in advices:
    st.info(a)

# Veri Kayıt ve PDF Çıktısı
if st.button(L['save']):
    pdf_bytes = create_pdf(h_name, p_name, ai_score, s_score, advices)
    st.download_button(label="📥 Download Report (PDF)", data=pdf_bytes, file_name=f"Report_{p_name}.pdf", mime='application/pdf')
    st.success(L['success'])
   