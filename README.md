# 🏥 Intelligent Clinical Decision Support System (CDSS)
**Empowering Emergency Triage with BioBERT & Social Determinants of Health (SDOH)**

![Python](https://img.shields.io/badge/Python-3.10+-green.svg)
![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)
![Field](https://img.shields.io/badge/Field-Health%20Informatics-blue.svg)

---

## 🌟 Overview
This project is an advanced **Triage Support Tool** designed to reduce clinical errors and physician burnout in Emergency Departments. It utilizes **Natural Language Processing (NLP)** to analyze clinical notes and integrates **Social Determinants of Health (SDOH)** to provide a 360-degree patient risk profile.

## 🚀 Key Features
- **🧠 BioBERT-Powered Analysis:** Automatically scans physician notes for high-risk flags (e.g., Sepsis, Stroke) using specialized medical NLP.
- **⚖️ SDOH Integration:** Quantifies non-clinical risks (Food Insecurity, Caregiver Availability, Housing) to predict and prevent post-discharge risks.
- **🩺 Active Protocol Guidance:** Suggests real-time, evidence-based clinical actions based on international standards.
- **🌍 Multi-Language Interface:** Fully localized in **Turkish, English, and German** for international healthcare environments.
- **📄 FHIR-Ready Documentation:** Generates structured PDF reports compatible with modern hospital information system (HIS) standards.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **NLP Engine:** BioBERT (Transformer-based architecture)
- **Reporting:** FPDF
- **Data Handling:** Pandas (FHIR-aligned structured data)

## 🌐 Live Demo
You can try the application here:  
👉 **[https://medical-triage-ai.streamlit.app](https://medical-triage-ai.streamlit.app)**

## 📦 Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone [https://github.com/ustab/medical-triage-ai.git](https://github.com/ustab/medical-triage-ai.git)
  Install the necessary dependencies:

Bash

pip install -r requirements.txt
Launch the application:

Bash

streamlit run triaj.py
🎯 Vision for Future Healthcare
This CDSS aims to bridge the gap between medical data and social context. By automating administrative burdens and highlighting hidden risks, we empower physicians to focus on what matters most: Patient Care. 
