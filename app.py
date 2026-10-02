
import streamlit as st
import hashlib
import json
import re
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CyberShield | Multi-Agent SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CYBERSECURITY COMMAND CENTER THEME
# ============================================================

st.markdown("""
<style>

/* Main application background */

.stApp {
    background:
        radial-gradient(ellipse at 10% 10%, rgba(0, 180, 255, 0.13), transparent 35%),
        radial-gradient(ellipse at 90% 20%, rgba(0, 100, 255, 0.12), transparent 35%),
        radial-gradient(ellipse at 50% 100%, rgba(0, 220, 200, 0.07), transparent 45%),
        linear-gradient(135deg, #050b18 0%, #081426 50%, #050b18 100%);
    color: #e5f0ff;
}

/* Subtle background grid */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0, 180, 255, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 180, 255, 0.035) 1px, transparent 1px);
    background-size: 42px 42px;
    pointer-events: none;
    z-index: 0;
}

/* Keep application content above background */

.stApp > header,
.stApp > div {
    position: relative;
    z-index: 1;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081426 0%, #050b18 100%);
    border-right: 1px solid rgba(0, 200, 255, 0.18);
}

/* Main hero header */

.cyber-hero {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(120deg, rgba(5, 20, 42, 0.97), rgba(9, 35, 65, 0.92));
    border: 1px solid rgba(0, 210, 255, 0.35);
    border-radius: 18px;
    padding: 32px 35px;
    margin-bottom: 25px;
    box-shadow:
        0 0 25px rgba(0, 180, 255, 0.10),
        inset 0 0 30px rgba(0, 150, 255, 0.04);
}

.cyber-hero::after {
    content: "";
    position: absolute;
    top: -100px;
    right: -60px;
    width: 300px;
    height: 300px;
    border: 1px solid rgba(0, 220, 255, 0.12);
    border-radius: 50%;
    box-shadow:
        0 0 0 35px rgba(0, 200, 255, 0.025),
        0 0 0 70px rgba(0, 200, 255, 0.02);
}

.cyber-title {
    color: #38dfff;
    font-size: 2.7rem;
    font-weight: 850;
    letter-spacing: 2px;
    margin: 0;
    text-shadow: 0 0 20px rgba(0, 210, 255, 0.35);
}

.cyber-subtitle {
    color: #c2d7ed;
    font-size: 1.05rem;
    letter-spacing: 2px;
    margin-top: 8px;
}

.cyber-credit {
    color: #8faec9;
    font-size: 0.9rem;
    margin-top: 18px;
}

.cyber-credit span {
    color: #38dfff;
    font-weight: 700;
}

/* Dashboard status cards */

.status-card {
    background: linear-gradient(145deg, #10243b, #09172a);
    border: 1px solid rgba(0, 190, 255, 0.22);
    border-radius: 12px;
    padding: 17px;
    text-align: center;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.18);
}

.status-label {
    color: #91abc4;
    font-size: 0.78rem;
    letter-spacing: 1px;
}

.status-value {
    color: #40e0ff;
    font-size: 1.2rem;
    font-weight: 750;
    margin-top: 5px;
}

/* Agent cards */

.agent-card {
    background: linear-gradient(110deg, #10243a, #0a192b);
    border: 1px solid rgba(0, 190, 255, 0.18);
    border-radius: 9px;
    padding: 11px 13px;
    margin-bottom: 9px;
    color: #d6e9fa;
    transition: border 0.2s ease;
}

.agent-card:hover {
    border: 1px solid rgba(0, 220, 255, 0.65);
}

/* Section headings */

h1, h2, h3 {
    color: #d9f4ff !important;
}

h4 {
    color: #42dfff !important;
}

/* Inputs */

.stTextArea textarea,
.stTextInput input {
    background-color: #09182a !important;
    color: #e4f3ff !important;
    border: 1px solid #24516e !important;
    border-radius: 9px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #24d7ff !important;
    box-shadow: 0 0 10px rgba(0, 210, 255, 0.15) !important;
}

/* Buttons */

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(100deg, #087da9, #0754a5);
    color: white;
    border: 1px solid rgba(0, 220, 255, 0.45);
    border-radius: 9px;
    font-weight: 700;
    padding: 0.55rem 1.1rem;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(100deg, #079fc9, #0871cf);
    border-color: #46e5ff;
    box-shadow: 0 0 15px rgba(0, 200, 255, 0.25);
    color: white;
}

/* Metrics */

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #10243b, #09172a);
    border: 1px solid rgba(0, 190, 255, 0.2);
    padding: 14px;
    border-radius: 10px;
}

/* Code blocks */

.stCodeBlock {
    border: 1px solid rgba(0, 190, 255, 0.22);
    border-radius: 9px;
}

/* Tabs */

.stTabs [data-baseweb="tab"] {
    color: #a9c5dd;
}

.stTabs [aria-selected="true"] {
    color: #40ddff !important;
}

/* Dividers */

hr {
    border-color: rgba(0, 190, 255, 0.2);
}

/* Footer */

.cyber-footer {
    text-align: center;
    padding: 25px 10px;
    margin-top: 30px;
    border-top: 1px solid rgba(0, 190, 255, 0.2);
    color: #829bb3;
    font-size: 0.85rem;
}

.cyber-footer strong {
    color: #40dfff;
}

/* About card */

.about-card {
    background: linear-gradient(145deg, #10243b, #081426);
    border: 1px solid rgba(0, 190, 255, 0.25);
    border-radius: 12px;
    padding: 15px;
    color: #c7dced;
    font-size: 0.88rem;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO HEADER
# ============================================================

st.markdown("""
<div class="cyber-hero">

    <div class="cyber-title">🛡️ CYBERSHIELD</div>

    <div class="cyber-subtitle">
        MULTI-AGENT SECURITY OPERATIONS CENTER
    </div>

    <p style="color:#a8c5df; margin-top:15px;">
        AI-ASSISTED DEFENSIVE CYBERSECURITY INVESTIGATION PLATFORM
    </p>

    <div class="cyber-credit">
        Concept &amp; Development by
        <span>Imtiaz Ali</span>
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# DASHBOARD STATUS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="status-card">
        <div class="status-label">SYSTEM STATUS</div>
        <div class="status-value">🟢 ONLINE</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="status-card">
        <div class="status-label">SPECIALIST AGENTS</div>
        <div class="status-value">🤖 6 ACTIVE</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="status-card">
        <div class="status-label">IOC ENGINE</div>
        <div class="status-value">🔎 READY</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛡️ CYBERSHIELD")

    st.success("🟢 SOC Platform Online")

    st.markdown("---")

    st.subheader("🤖 Specialist Agents")

    agents = [
        "📧 Email / Phishing Agent",
        "🔗 URL Analysis Agent",
        "📁 File Analysis Agent",
        "🦠 Malware Analysis Agent",
        "🔎 IOC Analysis Agent",
        "🌐 Threat Intelligence Agent",
    ]

    for agent in agents:
        st.markdown(
            f'<div class="agent-card">{agent}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.subheader("⚙️ Analysis Engine")

    st.caption("AI Provider: Groq")
    st.caption("Application: Streamlit")
    st.caption("Language: Python")

    st.markdown("---")

    st.subheader("👨‍💻 About This Project")

    st.markdown("""
    <div class="about-card">

    <b>Project:</b><br>
    CyberShield Multi-Agent SOC

    <br><br>

    <b>Concept & Development:</b><br>
    <span style="color:#40dfff;">Imtiaz Ali</span>

    <br><br>

    <b>Purpose:</b><br>
    AI-assisted defensive SOC investigation.

    <br><br>

    <b>Focus Areas:</b><br>
    • Phishing Detection<br>
    • IOC Analysis<br>
    • Threat Intelligence<br>
    • Security Risk Assessment<br>
    • Incident Investigation

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.caption("Cybersecurity Portfolio Project | 2026")


# ============================================================
# GROQ CONFIGURATION
# ============================================================

DEFAULT_MODEL = "openai/gpt-oss-120b"

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
GROQ_MODEL = st.secrets.get("GROQ_MODEL", DEFAULT_MODEL)

MAX_INPUT_CHARS = 3500

SPECIALIST_MAX_TOKENS = 350
RISK_MAX_TOKENS = 450
SOC_MAX_TOKENS = 650

if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY is missing. "
        "Please configure it in Streamlit Secrets."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text, limit=MAX_INPUT_CHARS):

    if not text:
        return ""

    text = str(text)
    text = " ".join(text.split())

    if len(text) > limit:
        text = text[:limit] + "\n[Evidence truncated]"

    return text


# ============================================================
# GROQ CALL
# ============================================================

def call_groq(system_prompt, user_prompt, max_tokens=350):

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.1,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": clean_text(system_prompt, 2200),
            },
            {
                "role": "user",
                "content": clean_text(user_prompt, MAX_INPUT_CHARS),
            },
        ],
    )

    content = response.choices[0].message.content

    if not content:
        return "No finding was returned by this agent."

    return content.strip()


# ============================================================
# SPECIALIST AGENT
# ============================================================

def specialist_agent(agent_name, evidence, task, ioc_context):

    system_prompt = f"""
You are the {agent_name} in a defensive SOC.

Task:
{task}

STRICT EVIDENCE RULES:

1. Analyze only supplied evidence.
2. Never invent facts or external reputation results.
3. Never invent DNS, WHOIS, VirusTotal, sandbox,
   malware, geolocation, or threat intelligence results.
4. IOCs appearing together do not prove a relationship.
5. Do not say an IP belongs to or resolves from a domain
   unless the evidence explicitly establishes this.
6. Do not associate a hash with a URL, file, email,
   or malware unless evidence explicitly establishes this.
7. Do not call an IOC malicious merely because it exists.
8. HTTP means no TLS encryption; it does not prove maliciousness.
9. Distinguish observed evidence from interpretation.
10. Say "Needs external verification" when appropriate.
11. Never provide malware execution instructions.

Return:
Finding:
Evidence:
Assessment:
Risk: Low / Medium / High
Recommended action:
Confidence: Low / Medium / High
"""

    user_prompt = f"""
INVESTIGATION EVIDENCE:

{clean_text(evidence)}

EXTRACTED IOC INFORMATION:

{clean_text(ioc_context, 1800)}

The IOC list identifies indicators found in the evidence.
It does not establish relationships between indicators.

Do not infer DNS resolution, IP ownership, URL hosting,
or hash relationships unless explicitly stated.

Provide your specialist finding.
"""

    return call_groq(
        system_prompt,
        user_prompt,
        SPECIALIST_MAX_TOKENS,
    )


# ============================================================
# RISK AGENT
# ============================================================

def risk_agent(findings, ioc_context):

    compact_findings = clean_text(findings, 5000)

    system_prompt = """
You are the Risk Agent of a defensive SOC.

Determine:
- Overall risk: Low, Medium, or High
- Main reason
- Most important observed indicators
- Immediate defensive actions
- Confidence

STRICT RULES:

1. Use only supplied evidence.
2. Never invent external intelligence.
3. Never invent DNS, WHOIS, VirusTotal, sandbox,
   reputation, or threat actor information.
4. Do not create relationships between separate IOCs.
5. Do not claim an IP resolves to a domain unless
   evidence explicitly establishes that.
6. Do not associate a hash with a URL or file without evidence.
7. HTTP does not automatically mean malicious.
8. Separate confirmed observations from assumptions.
9. State when external verification is required.
10. Recommendations must be proportional to evidence.

Keep the answer concise.
"""

    user_prompt = f"""
SPECIALIST FINDINGS:

{compact_findings}

EXTRACTED IOC INFORMATION:

{clean_text(ioc_context, 1800)}

The IOC list does not prove relationships between indicators.
Only use relationships explicitly supported by the evidence.

Produce the risk assessment.
"""

    return call_groq(
        system_prompt,
        user_prompt,
        RISK_MAX_TOKENS,
    )


# ============================================================
# SOC ANALYST
# ============================================================

def soc_analyst(original_evidence, specialist_findings, risk):

    evidence = clean_text(original_evidence, 2400)
    findings = clean_text(specialist_findings, 4200)
    risk = clean_text(risk, 1800)

    system_prompt = """
You are the senior SOC Analyst.

Prepare a professional defensive incident assessment.

Include:
- Executive Summary
- Risk Level
- Key Findings
- Indicators
- Recommended Containment
- Recommended Investigation
- Confidence

STRICT RULES:

1. Use only supplied evidence.
2. Never invent external intelligence.
3. Never invent DNS, WHOIS, VirusTotal, sandbox,
   reputation, geolocation, or attribution results.
4. Do not infer relationships between IOCs.
5. Do not claim an IP resolves a domain without evidence.
6. Do not associate a hash with a URL or file without evidence.
7. HTTP does not automatically prove maliciousness.
8. Separate confirmed observations from suspected activity.
9. State when additional verification is required.
10. Never provide malware execution instructions.
11. Never present assumptions as facts.

Use professional SOC terminology.
"""

    user_prompt = f"""
ORIGINAL EVIDENCE:

{evidence}

SPECIALIST FINDINGS:

{findings}

RISK ASSESSMENT:

{risk}

Prepare the final SOC assessment.
Every important claim must be traceable to supplied evidence.
"""

    return call_groq(
        system_prompt,
        user_prompt,
        SOC_MAX_TOKENS,
    )


# ============================================================
# IOC EXTRACTION
# ============================================================

def empty_ioc_result():

    return {
        "ip_addresses": [],
        "urls": [],
        "domains": [],
        "email_addresses": [],
        "md5": [],
        "sha1": [],
        "sha256": [],
    }


def valid_ipv4(ip):

    try:
        parts = ip.split(".")

        if len(parts) != 4:
            return False

        return all(
            0 <= int(part) <= 255
            for part in parts
        )

    except (ValueError, TypeError):
        return False


def extract_iocs(text):

    if not text:
        return empty_ioc_result()

    text = str(text)

    # IP addresses
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

    raw_ips = re.findall(ip_pattern, text)

    ip_addresses = []

    for ip in raw_ips:
        if valid_ipv4(ip) and ip not in ip_addresses:
            ip_addresses.append(ip)

    # URLs
    url_pattern = r'https?://[^\s<>"\']+'

    raw_urls = re.findall(url_pattern, text)

    urls = []

    for url in raw_urls:
        url = url.rstrip(".,;:!?)]}")

        if url and url not in urls:
            urls.append(url)

    # Email addresses
    email_pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}\b"
    )

    email_addresses = list(
        dict.fromkeys(re.findall(email_pattern, text))
    )

    # Hashes
    md5 = list(
        dict.fromkeys(
            re.findall(r"\b[a-fA-F0-9]{32}\b", text)
        )
    )

    sha1 = list(
        dict.fromkeys(
            re.findall(r"\b[a-fA-F0-9]{40}\b", text)
        )
    )

    sha256 = list(
        dict.fromkeys(
            re.findall(r"\b[a-fA-F0-9]{64}\b", text)
        )
    )

    # Domains
    domain_pattern = (
        r"\b(?:[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)"
        r"+[a-zA-Z]{2,}\b"
    )

    raw_domains = re.findall(domain_pattern, text)

    domains = list(
        dict.fromkeys(
            domain.lower() for domain in raw_domains
        )
    )

    return {
        "ip_addresses": ip_addresses,
        "urls": urls,
        "domains": domains,
        "email_addresses": email_addresses,
        "md5": md5,
        "sha1": sha1,
        "sha256": sha256,
    }


# ============================================================
# IOC DISPLAY
# ============================================================

def display_ioc_summary(iocs):

    total_iocs = sum(
        len(value) for value in iocs.values()
    )

    st.subheader("🔎 IOC Extraction")

    st.write(f"**{total_iocs} IOC(s) detected**")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("IP Addresses", len(iocs["ip_addresses"]))
    col2.metric("URLs", len(iocs["urls"]))
    col3.metric("Domains", len(iocs["domains"]))

    hash_count = (
        len(iocs["md5"])
        + len(iocs["sha1"])
        + len(iocs["sha256"])
    )

    col4.metric("Hashes", hash_count)

    sections = [
        ("🌐 IP Addresses", "ip_addresses"),
        ("🔗 URLs", "urls"),
        ("🏷️ Domains", "domains"),
        ("📧 Email Addresses", "email_addresses"),
        ("🔐 MD5", "md5"),
        ("🔐 SHA1", "sha1"),
        ("🔐 SHA256", "sha256"),
    ]

    for title, key in sections:

        if iocs[key]:

            st.markdown(f"### {title}")

            for item in iocs[key]:
                st.code(item)


# ============================================================
# FILE HASHING
# ============================================================

def calculate_sha256(file_bytes):

    return hashlib.sha256(file_bytes).hexdigest()


def get_file_metadata(uploaded_file, file_bytes):

    return {
        "filename": uploaded_file.name,
        "file_type": uploaded_file.type or "Unknown",
        "size_bytes": len(file_bytes),
        "sha256": calculate_sha256(file_bytes),
    }


# ============================================================
# INVESTIGATION INPUT
# ============================================================

st.markdown("---")

st.header("📥 Security Investigation")

st.caption(
    "Submit suspicious email content, security logs, URLs, "
    "network indicators, or files for defensive analysis."
)

input_tab, file_tab = st.tabs([
    "📝 Text Investigation",
    "📁 File Investigation",
])

investigation_text = ""
analyze_text = False


# ============================================================
# TEXT INVESTIGATION
# ============================================================

with input_tab:

    st.markdown("#### 📝 Enter Investigation Evidence")

    text_input = st.text_area(
        "Security Evidence",
        height=250,
        placeholder=(
            "From: security@example.com\n"
            "Subject: Urgent account verification required\n\n"
            "Please verify your account:\n"
            "http://example.com/login\n\n"
            "Suspicious connection observed:\n"
            "185.220.101.45\n\n"
            "MD5: d41d8cd98f00b204e9800998ecf8427e"
        ),
    )

    analyze_text = st.button(
        "🚀 Start SOC Investigation",
        type="primary",
        key="analyze_text_button",
    )

    if analyze_text:

        if not text_input.strip():
            st.warning("Please enter investigation evidence.")

        else:
            investigation_text = text_input


# ============================================================
# FILE INVESTIGATION
# ============================================================

with file_tab:

    st.markdown("#### 📁 Upload Evidence File")

    st.info(
        "Safety: Files are hashed and their metadata is inspected. "
        "Uploaded files are never executed."
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=None,
        key="investigation_file",
    )

    analyze_file = st.button(
        "🔬 Analyze Uploaded File",
        type="primary",
        key="analyze_file_button",
    )

    if analyze_file:

        if uploaded_file is None:

            st.warning("Please upload a file first.")

        else:

            file_bytes = uploaded_file.getvalue()

            metadata = get_file_metadata(
                uploaded_file,
                file_bytes,
            )

            st.subheader("📄 File Information")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Filename:** {metadata['filename']}")
                st.write(f"**File type:** {metadata['file_type']}")
                st.write(f"**Size:** {metadata['size_bytes']} bytes")

            with col2:
                st.write("**SHA-256:**")
                st.code(metadata["sha256"])

            st.success(
                "File processed safely. No execution performed."
            )

            investigation_text = f"""
Uploaded file metadata:

Filename: {metadata['filename']}
File type: {metadata['file_type']}
Size: {metadata['size_bytes']} bytes
SHA-256: {metadata['sha256']}

The file was not executed.
No external reputation or malware scan was performed.
"""

            analyze_text = True


# ============================================================
# MULTI-AGENT INVESTIGATION PIPELINE
# ============================================================

if analyze_text and investigation_text.strip():

    st.markdown("---")

    # IOC extraction

    iocs = extract_iocs(investigation_text)

    display_ioc_summary(iocs)

    ioc_context = json.dumps(iocs, indent=2)

    st.markdown("---")

    st.subheader("🤖 Multi-Agent Investigation")

    specialist_definitions = [
        {
            "name": "Email / Phishing Agent",
            "task": (
                "Analyze email evidence for phishing characteristics, "
                "urgency, impersonation, suspicious requests, "
                "and credential-harvesting language."
            ),
        },
        {
            "name": "URL Agent",
            "task": (
                "Analyze URL characteristics such as HTTP versus HTTPS, "
                "suspicious paths, and unusual formatting."
            ),
        },
        {
            "name": "File Agent",
            "task": (
                "Analyze file metadata and hashes. Do not claim a file "
                "is malicious without supporting evidence."
            ),
        },
        {
            "name": "Malware Agent",
            "task": (
                "Look for evidence of malware or malicious payloads. "
                "Do not identify malware families without evidence."
            ),
        },
        {
            "name": "IOC Agent",
            "task": (
                "Review IPs, URLs, domains, emails, and hashes. "
                "Identify indicators that require verification."
            ),
        },
        {
            "name": "Threat Intelligence Agent",
            "task": (
                "Assess supplied evidence from a threat intelligence "
                "perspective. Do not fabricate external intelligence."
            ),
        },
    ]

    specialist_results = []

    with st.spinner("🤖 Specialist agents are investigating..."):

        for definition in specialist_definitions:

            result = specialist_agent(
                definition["name"],
                investigation_text,
                definition["task"],
                ioc_context,
            )

            specialist_results.append({
                "agent": definition["name"],
                "finding": result,
            })

    st.success("Multi-agent investigation completed.")

    # Specialist findings

    st.markdown("---")

    st.subheader("🧩 Specialist Agent Findings")

    for item in specialist_results:

        with st.expander(
            f"🤖 {item['agent']}",
            expanded=True,
        ):

            st.text(item["finding"])

    combined_findings = "\n\n".join(
        [
            f"Agent: {item['agent']}\n{item['finding']}"
            for item in specialist_results
        ]
    )

    # Risk assessment

    st.markdown("---")

    st.subheader("⚠️ Risk Assessment")

    with st.spinner("Risk Agent is assessing the evidence..."):

        risk_result = risk_agent(
            combined_findings,
            ioc_context,
        )

    st.text(risk_result)

    # SOC analyst report

    st.markdown("---")

    st.subheader("🛡️ SOC Analyst Report")

    with st.spinner("Senior SOC Analyst is preparing the report..."):

        final_report = soc_analyst(
            investigation_text,
            combined_findings,
            risk_result,
        )

    st.markdown(final_report)

    # Download report

    st.markdown("---")

    st.subheader("📦 Investigation Report")

    report = {
        "project": "CyberShield Multi-Agent SOC",
        "developer": "Imtiaz Ali",
        "model": GROQ_MODEL,
        "investigation": investigation_text,
        "iocs": iocs,
        "specialist_findings": specialist_results,
        "risk_assessment": risk_result,
        "soc_analyst_report": final_report,
    }

    report_json = json.dumps(
        report,
        indent=2,
        ensure_ascii=False,
    )

    st.download_button(
        label="⬇️ Download SOC Investigation Report",
        data=report_json,
        file_name="CyberShield_SOC_Report.json",
        mime="application/json",
        key="download_json_report",
    )


# ============================================================
# PROFESSIONAL FOOTER
# ============================================================

st.markdown("""
<div class="cyber-footer">

    <div style="font-size:1.15rem; margin-bottom:8px;">
        🛡️ <strong>CYBERSHIELD MULTI-AGENT SOC</strong>
    </div>

    <div>
        AI-Assisted Defensive Cybersecurity Investigation Platform
    </div>

    <div style="margin-top:12px;">
        Concept &amp; Development by
        <strong>Imtiaz Ali</strong>
    </div>

    <div style="margin-top:8px; font-size:0.75rem;">
        © 2026 Imtiaz Ali | Cybersecurity Portfolio Project
    </div>

    <div style="margin-top:12px; font-size:0.72rem;">
        AI-generated findings require validation before operational action.
    </div>

</div>
""", unsafe_allow_html=True)
