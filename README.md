# BillLens — Autonomous MSME Cash-Flow & Underwriting Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/AWS-Step%20Functions%20%7C%20Aurora%20%7C%20Textract-orange.svg)](#architecture--cloud-services)
[![Security](https://img.shields.io/badge/ArmorIQ-Cryptographic%20Intent%20Tokens-10B981.svg)](https://armoriq.ai)
[![Maintainer](https://img.shields.io/badge/Maintainer-Prem%20T%20H-slate.svg)](https://github.com/Prem17th)

BillLens is an AI-powered financial intelligence and autonomous underwriting platform designed for India's 63M+ micro, small, and medium enterprises (MSMEs) and Kirana merchants.

The platform continuously audits paper distributor invoices, flags wholesale price creep (+4.3%), models rolling 30-day liquidity runways, identifies Day-18 cash deficits before EMI auto-debits fail, and structures institutional Debt Service Coverage Ratio (DSCR) underwriting profiles.

This repository is maintained by **[Prem T H](https://github.com/Prem17th)** at [Prem17th/BillLens](https://github.com/Prem17th/BillLens).

---

## 🌟 Key Features

1. **Autonomous Invoice Auditing & Margin Creep Detection:**
   - Ingests distributor line-items, verifies SKU rates against past purchases, and flags unnotified margin leakage (e.g. ₹7,840 across recent bills).
2. **AWS Step Functions ASL State Machine:**
   - Full 10-state Amazon States Language (ASL) execution engine coordinating OCR extraction, parallel spatial arbitrage, liquidity runways, and emergency dispatches.
3. **ArmorIQ Cryptographic Intent Security:**
   - Mints tamper-proof cryptographic intent tokens (ECDSA / SHA-256 HMAC Merkle proofs) to guarantee LLM and agent execution boundaries against unauthorized actions. Operates with live ArmorIQ SDK or built-in zero-dependency local fallback.
4. **30-Day Cash-Flow Runway & Day-18 Deficit Warning:**
   - Dynamically forecasts daily liquidity traps where upcoming supplier dues and bank EMIs trigger negative balances.
5. **Hyperlocal Mandi Arbitrage Radar:**
   - Leverages Geoapify spatial APIs and Leaflet to map wholesale vendor price differentials across local APMC markets.
6. **Vernacular Audio Telemetry (ElevenLabs & Soundbox):**
   - Synthesizes morning voice briefings and UPI audio alerts in Kannada, Hindi, and English with bundled studio master audio fallback.
7. **Institutional Underwriting & DSCR Scoring:**
   - Evaluates bankability, working capital health, quick ratio, and TReDS invoice discounting viability.

---

## 🏗️ Architecture & Technology Stack

```
BillLens/
├── server.py                              # Python backend HTTP server & Step Functions engine
├── index.html                             # Single-page executive financial dashboard (Tailwind CSS)
├── step_function_state_machine.asl.json   # 10-State AWS Step Functions ASL definition
├── requirements.txt                       # Python dependency manifest
├── render.yaml                            # 1-click cloud deployment blueprint for Render
├── netlify.toml                           # Static hosting routing configuration
├── .env.example                           # Safe environment variable template
├── tests/
│   └── test_server.py                     # Automated pytest test suite (100% pass)
├── elevenlabs_*.mp3                       # Bundled vernacular studio master audio briefs
└── BillLens_Impulse26_Mentoring_Presentation.pptx # Technical presentation deck
```

### Verified Technology Stack

- **Backend Runtime:** Python 3.10+ using `http.server.ThreadingHTTPServer` (zero heavy framework overhead).
- **Security & Integrity:** `armoriq_sdk` (v0.6.2), `cryptography`, HMAC-SHA256 zero-tamper tokens.
- **Frontend:** Responsive HTML5, Vanilla ES6+ JavaScript, Tailwind CSS (via CDN), FontAwesome icons, and Leaflet.js maps.
- **Orchestration:** AWS Step Functions ASL (`step_function_state_machine.asl.json`).
- **Testing:** `pytest` unit testing suite with simulated socketless HTTP handler mocking.

---

## 📋 Prerequisites

- **Python 3.10 or higher**
- **pip** package manager
- (Optional) API keys for live cloud features (OpenAI, Gemini, ElevenLabs, Geoapify, ArmorIQ). The application runs with 100% functionality using pre-calculated institutional fallbacks and bundled audio if keys are omitted.

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Prem17th/BillLens.git
cd BillLens
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

Copy the example template:

```bash
# Windows PowerShell:
Copy-Item .env.example .env

# Linux/macOS:
cp .env.example .env
```

Edit `.env` to supply optional API keys:

```ini
PORT=8080
ARMORIQ_API_KEY=your_armoriq_key_here
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
GEOAPIFY_API_KEY=your_geoapify_key_here
```

### 5. Start the Application Server

```bash
python server.py
```

Open your browser and navigate to:
```
http://localhost:8080
```

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:

```bash
python -m pytest tests/ -v
```

The test suite validates:
- Health check endpoint (`/api/health`)
- ArmorIQ status telemetry and dynamic token minting (`/api/armoriq/*`)
- AWS Step Functions workflow execution and state status (`/api/step-functions/*`)
- ASL state machine syntax and schema validity
- Static asset serving and branding integrity

---

## ☁️ Deployment

### Deploy to Render

This repository includes a `render.yaml` blueprint:
1. Connect your GitHub repository `Prem17th/BillLens` to [Render](https://render.com/).
2. Select **New Blueprint Instance**.
3. Render will automatically detect `render.yaml`:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
4. Set optional environment variables in the Render dashboard.

### Deploy to Netlify

A `netlify.toml` file is provided for hosting static dashboard files with client-side routing.

---

## 🔒 Security & Privacy

- **No Hardcoded Secrets:** All external API keys and live credentials have been audited and replaced with environment variables and secure fallback handlers.
- **Cryptographic Guardrails:** Action enforcement verifies signatures before sensitive actions (e.g. TReDS factoring).
- **Safe Fallback Mode:** The server functions securely offline or without third-party credentials.

---

## ⚠️ Known Limitations

- **Simulated Cloud Connectors:** The local prototype simulates AWS Aurora Serverless and AWS Textract OCR payloads in memory rather than requiring a live AWS billable account.
- **Execution Storage:** Step Functions execution histories and recent intent tokens are maintained in an in-memory ring buffer (up to 50 records) and reset on server restart.

---

## 📄 License & Attribution

This project is licensed under the **[MIT License](LICENSE)**.

### Acknowledgments
- Original prototype created by Mohammed Safwan Khan and contributors for the IMPULSE '26 Hackathon (AWS Student Builder Group, REVA University).
- Enhanced, audited, secured, and maintained by **[Prem T H](https://github.com/Prem17th)**.
