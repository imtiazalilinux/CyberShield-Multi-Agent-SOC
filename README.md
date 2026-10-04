# 🛡️ CyberShield Multi-Agent SOC

> **Defensive AI-assisted Security Operations Center investigation platform**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/LLM-Groq-111111)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Launch%20App-FF4B4B?logo=streamlit&logoColor=white)](https://cybershield-multi-agent-soc-udwevac2waqnbtkgz4jher.streamlit.app/)

## 🌐 Live Demo

Try the deployed Streamlit application:

### [Launch CyberShield Multi-Agent SOC](https://cybershield-multi-agent-soc-udwevac2waqnbtkgz4jher.streamlit.app/)

> Use the demo only with authorized, non-sensitive security evidence. Do not upload credentials, confidential files, private data, or production incident information.

## 📌 Overview

CyberShield Multi-Agent SOC is a defensive cybersecurity application designed to help analysts investigate suspicious security evidence. It transforms unstructured input—such as email content, URLs, IP addresses, domains, hashes, logs, and uploaded files—into structured Indicators of Compromise (IOCs), specialist findings, risk assessment, and a final SOC-style investigation report.

The application uses **eight logical AI agents/components**:

- Six specialist investigation agents.
- A Risk Agent that consolidates specialist findings.
- A SOC Analyst Agent that produces the final defensive assessment.

CyberShield is designed to assist a human analyst rather than replace a real Security Operations Center.

## 🎯 Product Goal

> Convert security evidence into structured IOC information, evidence-based specialist findings, risk assessment, and a downloadable SOC analyst report.

The workflow is intended to reduce repetitive investigation work while preserving evidence control, uncertainty awareness, and human validation.

## ✨ Key Features

| Feature | Description |
|---|---|
| **Text Investigation** | Analyze suspicious emails, URLs, IP addresses, hashes, logs, domains, and other textual evidence. |
| **File Investigation** | Inspect uploaded-file metadata, file type, size, and locally calculated SHA-256 hash. |
| **IOC Extraction** | Extract IPv4 addresses, URLs, domains, email addresses, MD5, SHA-1, and SHA-256 hashes. |
| **IPv4 Validation** | Reject invalid IPv4 values such as `999.999.999.999`. |
| **Multi-Agent Analysis** | Run six specialist agents over the supplied evidence and extracted IOC context. |
| **Risk Assessment** | Produce a Low, Medium, or High risk assessment with reasoning, actions, and confidence. |
| **SOC Report** | Generate an executive summary, key findings, indicators, containment guidance, investigation steps, and confidence. |
| **JSON Export** | Download the complete investigation as `cybershield_soc_report.json`. |
| **Evidence Controls** | Prevent unsupported claims about reputation, DNS, WHOIS, sandboxing, attribution, and external intelligence. |
| **Defensive File Handling** | Uploaded files are read for metadata and hashing only; they are never executed. |

## 🔄 Investigation Workflow

```text
Security Evidence
        │
        ├── Text Investigation
        │       └── Email, URL, IP, domain, hash, log, or other evidence
        │
        └── File Investigation
                └── Filename, type, size, and SHA-256 metadata
        │
        ▼
IOC Extraction & Validation
        │
        ▼
Six Specialist AI Agents
        │
        ├── Email / Phishing Agent
        ├── URL Agent
        ├── File Agent
        ├── Malware Agent
        ├── IOC Agent
        └── Threat Intelligence Agent
        │
        ▼
Risk Agent
        │
        ▼
SOC Analyst Agent
        │
        ▼
Structured Investigation Report
        │
        ▼
Downloadable JSON Report
```

## 🤖 Multi-Agent System

| Agent | Main Responsibility |
|---|---|
| **Email / Phishing Agent** | Analyze urgency, suspicious requests, impersonation indicators, links, and credential-harvesting language. |
| **URL Agent** | Review observable URL characteristics such as HTTP versus HTTPS, suspicious paths, and unusual formatting. HTTP alone is not treated as proof of maliciousness. |
| **File Agent** | Analyze filename, file type, file size, and hash-related evidence without declaring a file malicious without supporting evidence. |
| **Malware Agent** | Look for evidence of malicious payloads without inventing malware-family identification. |
| **IOC Agent** | Review extracted IPs, URLs, domains, email addresses, and hashes and identify indicators requiring verification. |
| **Threat Intelligence Agent** | Assess evidence from a threat-intelligence perspective without claiming results from external platforms. |
| **Risk Agent** | Combine specialist findings and determine overall risk, key reasons, observed indicators, actions, and confidence. |
| **SOC Analyst Agent** | Produce the final defensive incident assessment from the evidence, specialist findings, and risk assessment. |

## 🔎 IOC Extraction

CyberShield performs local Python-based IOC extraction before sending investigation context to the AI agents. The extractor identifies:

- IPv4 addresses, with octet validation.
- URLs.
- Domains.
- Email addresses.
- MD5 hashes.
- SHA-1 hashes.
- SHA-256 hashes.

IOC extraction identifies what appears in the supplied evidence. It does **not** determine whether an indicator is malicious or establish relationships between indicators.

### Relationship protection

CyberShield does not automatically assume that indicators are related merely because they appear in the same investigation:

- An IP and a domain appearing together does not prove that the IP hosts or resolves to the domain.
- A hash and a URL appearing together does not prove that the hash belongs to the URL or its payload.
- An email address and a domain appearing together does not prove ownership or attribution.

## 🛡️ Evidence-Based AI Design

All agents are instructed to analyze only the supplied evidence and specialist findings. They must not fabricate:

- DNS or WHOIS results.
- VirusTotal, AbuseIPDB, OTX, URLhaus, or other reputation results.
- Sandbox or malware-scan results.
- Geolocation or threat-actor attribution.
- Unsupported malware-family identification.
- Relationships between separate IOCs.

The system distinguishes between:

```text
Observed Evidence → Reasonable Interpretation → Unverified Information
```

When confirmation requires data that is not available, the analysis should state:

> **Needs external verification.**

## 📁 File Safety

Uploaded files are handled defensively and are **never executed**. CyberShield currently:

- Identifies the filename.
- Identifies the file type.
- Calculates the file size.
- Calculates the SHA-256 hash locally.
- Creates safe metadata for the AI investigation.

The generated evidence explicitly records that the file was not executed and that no external reputation or malware scan was performed.

## 📊 Investigation Report

After analysis, CyberShield creates a structured JSON report containing:

- Project name.
- Configured model.
- Investigation evidence.
- Extracted IOCs.
- Specialist agent findings.
- Risk assessment.
- Final SOC Analyst report.

The report can be downloaded from the application as:

```text
cybershield_soc_report.json
```

## 🖥️ User Interface

The Streamlit application provides an analyst-oriented interface with:

- **Investigation Input** section.
- **Text Investigation** tab.
- **File Investigation** tab.
- **IOC Extraction** dashboard.
- **Specialist Agent Findings** section.
- **Risk Assessment** section.
- **SOC Analyst Report** section.
- **Download JSON Report** action.

The sidebar displays system status, all eight active agents, and the defensive-use notice that uploaded files are never executed.

## ⚙️ Current AI Configuration

| Setting | Configuration |
|---|---|
| **Provider** | Groq API |
| **Default model** | `openai/gpt-oss-120b` |
| **Model override** | `GROQ_MODEL` through Streamlit Secrets |
| **API key** | `GROQ_API_KEY` through Streamlit Secrets |
| **Maximum evidence length** | 3,500 characters |
| **Risk levels** | Low, Medium, High |

Longer evidence is truncated and marked with `[Evidence truncated]` to help control token usage.

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/imtiazalilinux/CyberShield-Multi-Agent-SOC.git
cd CyberShield-Multi-Agent-SOC
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Streamlit Secrets

Create `.streamlit/secrets.toml` locally and add your Groq credentials:

```toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

Never commit API keys or other secrets to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will normally be available at `http://localhost:8501`.

## 🧪 Example Investigation Evidence

You can test the text investigation workflow with non-sensitive sample data:

```text
From: security@example.com
Subject: Urgent account verification required

Please verify your account immediately:
http://example.com/login

Connection observed to 185.220.101.45
MD5: d41d8cd98f00b204e9800998ecf8427e
```

This example is for demonstrating extraction and analysis behavior only. The presence of an indicator does not automatically prove that it is malicious.

## 👥 Project Team

| Team Member | Role | LinkedIn Profile |
|---|---|---|
| **Muhammad Usman** | Contributor | [LinkedIn Profile](https://www.linkedin.com/in/iusman07/) |
| **Ibrahim Masood** | Contributor | [LinkedIn Profile](https://www.linkedin.com/in/ibrahim-masood-404984379) |
| **Zeeshan Ahmad** | Contributor | [LinkedIn Profile](https://www.linkedin.com/in/zeeshier) |
| **Khadija Ikram** | Contributor | [LinkedIn Profile](https://www.linkedin.com/in/khadija-ikram-cs?utm_source=share_via&utm_content=profile&utm_medium=member_android) |
| **Zeemal Emaan** | Contributor | [LinkedIn Profile](https://www.linkedin.com/in/zeemal-emaan-3a3941424?utm_source=share_via&utm_content=profile&utm_medium=member_android) |

## 🔐 Responsible Security Use

CyberShield is intended for authorized defensive security analysis, education, and research. Use it only with systems, accounts, files, URLs, and data that you are permitted to investigate.

- Treat all submitted evidence as untrusted input.
- Protect confidential and personally identifiable information.
- Do not upload credentials, secrets, or sensitive production evidence.
- Keep API keys server-side through Streamlit Secrets.
- Validate AI-generated findings against trusted security sources.
- Do not treat automated risk assessments as definitive proof.
- Do not use the application to generate malware execution instructions or conduct unauthorized activity.

## ⚠️ Current Limitations

The current MVP does not include:

- External threat-intelligence API integrations.
- VirusTotal, AbuseIPDB, AlienVault OTX, or URLhaus lookups.
- SIEM integrations such as Splunk, Wazuh, Elastic, or Microsoft Sentinel.
- EDR integration.
- Malware execution or sandbox analysis.
- Persistent investigation history or a database-backed case-management system.
- Automated response actions such as blocking IPs, disabling accounts, quarantining files, modifying firewalls, or isolating endpoints.

AI-generated findings require analyst validation before operational action.

## 🔭 Future Development

Potential future phases include:

### Phase 2 — Threat Intelligence

- VirusTotal integration.
- AbuseIPDB integration.
- AlienVault OTX integration.
- URLhaus integration.
- External intelligence enrichment between IOC extraction and agent analysis.

### Phase 3 — SOC Integration

- Wazuh.
- Splunk.
- TheHive.
- MISP.
- OpenCTI.

### Phase 4 — Advanced Analysis

- MITRE ATT&CK mapping.
- Sigma rule analysis.
- YARA integration.
- Malware sandbox integration.
- DNS and WHOIS investigation.
- IP, domain, and URL reputation.
- Investigation history.
- Analyst accounts and case management.

## 📁 Repository & Resources

- **Source code:** [CyberShield Multi-Agent SOC on GitHub](https://github.com/imtiazalilinux/CyberShield-Multi-Agent-SOC)
- **Live application:** [Open the Streamlit demo](https://cybershield-multi-agent-soc-udwevac2waqnbtkgz4jher.streamlit.app/)
- **Application entry point:** [`app.py`](app.py)
- **Python dependencies:** [`requirements.txt`](requirements.txt)
- **License:** [MIT License](LICENSE)

## ⚖️ Disclaimer

CyberShield Multi-Agent SOC is an AI-assisted cybersecurity project for defensive, educational, and research purposes. AI-generated analysis may be incomplete, inaccurate, or affected by the quality of the submitted evidence. The application does not provide definitive malware detection, external reputation verification, legal advice, or guaranteed incident conclusions. Always verify findings with qualified security professionals and trusted sources before taking incident-response or business action.

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for the complete license text.
