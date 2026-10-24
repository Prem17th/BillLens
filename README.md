# BillLens — Autonomous MSME Cash-Flow & Underwriting Intelligence

**IMPULSE '26 — 24-Hour National Hackathon | Mentoring Round**  
*AWS Student Builder Group · REVA University, Bengaluru*  
*Team: CodeStorm*

---

## 🌟 Overview
BillLens is an AI-powered cash-flow early warning & autonomous underwriting platform designed for India's 63M+ MSMEs and Kirana stores. It continuously ingests paper supplier bills via Amazon Textract, monitors wholesale price creep (+4.3%), projects rolling 30-day liquidity bottlenecks 18 days before loan EMI auto-debits bounce, and dispatches multi-channel alerts (SMS/WhatsApp) backed by institutional DSCR credit readiness (1.12x).

---

## 🏗️ Architecture & AWS Cloud Services
- **AWS Step Functions:** 10-State ASL Orchestrator (`ExtractInvoiceOCR` $\rightarrow$ `DualParallelUnderwriting` $\rightarrow$ `ChoiceDay18Deficit` $\rightarrow$ `AmazonSNSEmergencyDispatch`).
- **Amazon Aurora Serverless v2:** PostgreSQL relational double-entry ledger tracking rolling vendor price creep index.
- **Amazon Textract & S3:** High-precision automated invoice OCR line-item extraction.
- **Amazon SNS:** Multi-channel high-priority merchant alerts via SMS and WhatsApp Business API.
- **ArmorIQ Agent SDK:** Cryptographic ECDSA zero-tamper intent locking and audit trail.
- **Geoapify Spatial API:** Hyperlocal Bangalore Wholesale Arbitrage Radar (Yeshwanthpur APMC vs Chickpet vs Koramangala).
- **Paytm Soundbox & ElevenLabs AI:** Real-time UPI voice telemetry and vernacular audio briefs in Kannada/Hindi.

---

## 🚀 Quickstart

### Local Setup
```bash
git clone https://github.com/mohammedsafwankhan/billlens.git
cd billlens
pip install -r requirements.txt
python server.py
```
Visit `http://localhost:8080` in your browser.

---

## ☁️ Deployment on Render
This repository includes a `render.yaml` blueprint for 1-click zero-config deployment:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python server.py`
- **Environment:** `PORT` injected automatically by Render.
