import streamlit as st
import hashlib
import json
import re
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CyberShield Multi-Agent SOC",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    /* ========================================================
       CYBERSHIELD FUTURISTIC SOC COMMAND-CENTER THEME
       VISUAL-ONLY CSS — APPLICATION LOGIC UNCHANGED
       ======================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 82% 5%, rgba(0, 196, 255, 0.18), transparent 24%),
            radial-gradient(circle at 12% 20%, rgba(0, 116, 255, 0.10), transparent 27%),
            radial-gradient(circle at 58% 78%, rgba(80, 70, 255, 0.055), transparent 32%),
            linear-gradient(135deg, #010711 0%, #031526 42%, #020b17 72%, #01050c 100%) !important;
        color: #dcefff;
    }

    [data-testid="stAppViewContainer"] {
        position: relative;
        overflow: hidden;
    }

    /* Futuristic circuit grid */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            linear-gradient(rgba(0, 200, 255, 0.045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 200, 255, 0.045) 1px, transparent 1px);
        background-size: 44px 44px;
        opacity: 0.72;
        mask-image: linear-gradient(to bottom, black 0%, black 62%, transparent 100%);
        z-index: 0;
    }

    /* Subtle digital globe / radar rings */
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        right: -165px;
        top: -205px;
        width: 560px;
        height: 560px;
        border-radius: 50%;
        border: 1px solid rgba(0, 210, 255, 0.22);
        box-shadow:
            0 0 0 20px rgba(0, 210, 255, 0.035),
            0 0 0 48px rgba(0, 210, 255, 0.025),
            0 0 0 82px rgba(0, 210, 255, 0.018),
            0 0 90px rgba(0, 190, 255, 0.10),
            inset 0 0 70px rgba(0, 190, 255, 0.045);
        pointer-events: none;
        opacity: 0.78;
        z-index: 0;
    }

    [data-testid="stHeader"] {
        background: rgba(1, 7, 15, 0.88) !important;
        border-bottom: 1px solid rgba(0, 210, 255, 0.18);
        box-shadow: 0 0 22px rgba(0, 180, 255, 0.035);
    }

    [data-testid="stMain"] {
        position: relative;
        z-index: 1;
    }

    .main {
        background: transparent !important;
    }

    .block-container {
        padding-top: 1.35rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* Header */
    .cyber-header {
        position: relative;
        padding: 25px 30px 24px;
        margin-bottom: 24px;
        border: 1px solid rgba(0, 210, 255, 0.36);
        border-left: 4px solid #00dfff;
        border-radius: 14px;
        background:
            linear-gradient(135deg,
                rgba(0, 69, 112, 0.42),
                rgba(2, 15, 31, 0.96) 46%,
                rgba(4, 22, 43, 0.88));
        box-shadow:
            0 0 38px rgba(0, 190, 255, 0.11),
            inset 0 0 38px rgba(0, 180, 255, 0.035),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);
        overflow: hidden;
    }

    .cyber-header::before {
        content: "";
        position: absolute;
        right: 0;
        top: 0;
        width: 52%;
        height: 100%;
        background:
            linear-gradient(90deg, transparent, rgba(0, 190, 255, 0.035)),
            repeating-linear-gradient(
                135deg,
                transparent 0 18px,
                rgba(0, 205, 255, 0.025) 19px,
                transparent 20px 38px
            );
        border-left: 1px solid rgba(0, 210, 255, 0.08);
        pointer-events: none;
    }

    .cyber-header::after {
        content: "DETECT   //   ANALYZE   //   RESPOND   //   DEFEND";
        position: absolute;
        right: 24px;
        bottom: 12px;
        font-family: monospace;
        font-size: 0.64rem;
        letter-spacing: 0.12em;
        color: rgba(92, 215, 255, 0.46);
        pointer-events: none;
    }

    .cyber-title {
        position: relative;
        z-index: 2;
        font-size: 2.35rem;
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: 0.015em;
        color: #f2fbff;
        margin: 0 0 8px 0;
        text-shadow: 0 0 18px rgba(0, 210, 255, 0.25);
    }

    .cyber-subtitle {
        position: relative;
        z-index: 2;
        color: #73ddff;
        font-size: 1rem;
        letter-spacing: 0.035em;
        margin: 0 0 7px 0;
    }

    .cyber-credit {
        position: relative;
        z-index: 2;
        color: #91aebe;
        font-family: monospace;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(4, 31, 55, 0.94), rgba(2, 17, 34, 0.94));
        border: 1px solid rgba(0, 205, 255, 0.22);
        border-radius: 10px;
        padding: 11px;
        box-shadow:
            0 0 18px rgba(0, 180, 255, 0.045),
            inset 0 0 16px rgba(0, 190, 255, 0.025);
    }

    [data-testid="stMetricLabel"] {
        color: #79abc0 !important;
    }

    [data-testid="stMetricValue"] {
        color: #00e5ff !important;
        text-shadow: 0 0 10px rgba(0, 220, 255, 0.22);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #010914 0%, #031a2f 46%, #020b17 100%) !important;
        border-right: 1px solid rgba(0, 210, 255, 0.20);
        box-shadow: 5px 0 30px rgba(0, 150, 255, 0.035);
    }

    section[data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background-image:
            linear-gradient(rgba(0, 200, 255, 0.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 200, 255, 0.035) 1px, transparent 1px);
        background-size: 30px 30px;
        opacity: 0.55;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #c6deea;
    }

    /* Agent cards */
    .agent-card {
        position: relative;
        background: linear-gradient(90deg, rgba(4, 30, 54, 0.96), rgba(3, 20, 38, 0.84));
        border: 1px solid rgba(0, 190, 255, 0.17);
        border-left: 3px solid rgba(0, 211, 255, 0.66);
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 7px;
        color: #d5edf7;
        box-shadow: inset 0 0 16px rgba(0, 180, 255, 0.025);
        transition: all 0.2s ease;
    }

    .agent-card:hover {
        border-color: rgba(0, 220, 255, 0.45);
        box-shadow: 0 0 15px rgba(0, 190, 255, 0.08), inset 0 0 15px rgba(0, 180, 255, 0.04);
        transform: translateX(2px);
    }

    /* Inputs */
    [data-baseweb="textarea"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div {
        background: rgba(2, 15, 29, 0.94) !important;
        border: 1px solid rgba(0, 200, 255, 0.22) !important;
        border-radius: 9px !important;
        box-shadow: inset 0 0 15px rgba(0, 170, 255, 0.025);
    }

    textarea,
    input {
        color: #dff8ff !important;
    }

    textarea:focus,
    input:focus {
        border-color: #00dfff !important;
        box-shadow: 0 0 14px rgba(0, 210, 255, 0.12) !important;
    }

    /* File uploader */
    [data-testid="stFileUploaderDropzone"] {
        background: linear-gradient(145deg, rgba(3, 25, 45, 0.86), rgba(2, 14, 28, 0.96));
        border: 1px dashed rgba(0, 210, 255, 0.38);
        border-radius: 10px;
        box-shadow: inset 0 0 20px rgba(0, 180, 255, 0.025);
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: rgba(0, 225, 255, 0.65);
    }

    /* Primary buttons */
    button[kind="primary"] {
        background: linear-gradient(90deg, #008dff 0%, #005cff 50%, #4b35ff 100%) !important;
        border: 1px solid rgba(75, 220, 255, 0.60) !important;
        color: #ffffff !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        box-shadow: 0 0 18px rgba(0, 110, 255, 0.18);
        transition: all 0.2s ease;
    }

    button[kind="primary"]:hover {
        border-color: #00eaff !important;
        box-shadow: 0 0 25px rgba(0, 190, 255, 0.30);
        transform: translateY(-1px);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #83aabd !important;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00e5ff !important;
        text-shadow: 0 0 10px rgba(0, 220, 255, 0.25);
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background: linear-gradient(145deg, rgba(3, 27, 48, 0.88), rgba(2, 16, 32, 0.94));
        border: 1px solid rgba(0, 195, 255, 0.20);
        border-radius: 10px;
        box-shadow: inset 0 0 20px rgba(0, 180, 255, 0.02);
    }

    /* IOC / code display */
    .ioc-box {
        background: linear-gradient(145deg, rgba(4, 27, 48, 0.90), rgba(2, 16, 31, 0.94));
        border: 1px solid rgba(0, 200, 255, 0.18);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: inset 0 0 15px rgba(0, 180, 255, 0.025);
    }

    code {
        color: #00e5ff !important;
        text-shadow: 0 0 8px rgba(0, 220, 255, 0.18);
    }

    pre {
        background: #020b15 !important;
        border: 1px solid rgba(0, 190, 255, 0.16);
        border-radius: 8px;
        box-shadow: inset 0 0 20px rgba(0, 150, 255, 0.025);
    }

    /* Alerts */
    [data-testid="stAlert"] {
        background: rgba(3, 28, 49, 0.86);
        border: 1px solid rgba(0, 190, 255, 0.20);
        border-radius: 9px;
    }

    .success-box {
        background: rgba(0, 80, 65, 0.32);
        border: 1px solid rgba(0, 220, 170, 0.45);
        border-radius: 9px;
        padding: 12px;
        color: #8fffe0;
    }

    .warning-box {
        background: rgba(75, 45, 0, 0.38);
        border: 1px solid rgba(255, 175, 55, 0.48);
        border-radius: 9px;
        padding: 12px;
        color: #ffe2a1;
    }

    /* Headings and separators */
    h1, h2, h3, h4 {
        color: #eafaff !important;
        text-shadow: 0 0 10px rgba(0, 190, 255, 0.08);
    }

    hr {
        border: none !important;
        border-top: 1px solid rgba(0, 205, 255, 0.14) !important;
        margin: 22px 0 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #020812;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#006f9f, #003b62);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #00bde8;
    }

    </style>
    """,
    unsafe_allow_html=True,
)



# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="cyber-header">
        <div class="cyber-title">🛡️ CyberShield Multi-Agent SOC</div>
        <div class="cyber-subtitle">AI-Assisted Defensive Security Operations Platform</div>
        <div class="cyber-credit">Concept &amp; Development by Imtiaz Ali</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("⚙️ SOC Status")

    st.success("🟢 System Online")

    st.markdown("---")

    st.subheader("🤖 Active Agents")

    agents = [
        "📧 Email / Phishing Agent",
        "🔗 URL Agent",
        "📁 File Agent",
        "🦠 Malware Agent",
        "🔎 IOC Agent",
        "🌐 Threat Intelligence Agent",
        "⚠️ Risk Agent",
        "🛡️ SOC Analyst Agent",
    ]

    for agent in agents:
        st.markdown(
            f'<div class="agent-card">{agent}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.caption(
        "CyberShield performs defensive analysis only. "
        "Uploaded files are never executed."
    )


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
        "GROQ_API_KEY is not configured. "
        "Add it to Streamlit Secrets before running an investigation."
    )
    st.stop()


client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text, limit=MAX_INPUT_CHARS):
    """
    Clean and limit text before sending it to the AI model.
    This helps control token usage.
    """

    if not text:
        return ""

    text = str(text)

    # Normalize whitespace while preserving readable content.
    text = " ".join(text.split())

    if len(text) > limit:
        text = text[:limit] + "\n[Evidence truncated]"

    return text


# ============================================================
# GROQ CALL
# ============================================================

def call_groq(system_prompt, user_prompt, max_tokens=350):
    """
    Send a request to Groq.

    The prompts are intentionally compact to reduce token usage.
    """

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
    """
    Run one specialist SOC agent.

    Important:
    The agent is explicitly instructed not to establish relationships
    between separate indicators unless those relationships are present
    in the supplied evidence.
    """

    system_prompt = f"""
You are the {agent_name} in a defensive Security Operations Center.

Your task:
{task}

STRICT EVIDENCE RULES:

1. Analyze ONLY the supplied evidence.
2. Never invent facts.
3. Never invent external reputation results.
4. Never invent DNS, WHOIS, VirusTotal, sandbox, malware,
   geolocation, or threat-intelligence results.
5. An IOC appearing in the same investigation does NOT prove
   that it is related to another IOC.
6. Do NOT say an IP belongs to, resolves from, or hosts a domain
   unless the supplied evidence explicitly establishes that relationship.
7. Do NOT say a hash belongs to a URL, file, email, payload,
   or malware unless the supplied evidence explicitly establishes
   that relationship.
8. Do NOT call an IOC malicious merely because it exists.
9. HTTP means the connection is not protected by TLS. It does NOT,
   by itself, prove that the website is malicious.
10. Clearly distinguish:
    - Observed evidence
    - Reasonable interpretation
    - Unverified information
11. If something cannot be confirmed, say:
    "Needs external verification."
12. Do not provide malware execution instructions.

Return a concise SOC finding with:

Finding:
Evidence:
Assessment:
Risk: Low / Medium / High
Recommended action:
Confidence: Low / Medium / High
"""

    user_prompt = f"""
SUPPLIED INVESTIGATION EVIDENCE:

{clean_text(evidence)}

EXTRACTED IOC INFORMATION:

{clean_text(ioc_context, 1800)}

IMPORTANT:

The extracted IOC list only tells you that these indicators were
found in the supplied evidence.

It does NOT establish relationships between them.

For example:
- An IP and a domain appearing together does not prove DNS resolution.
- A URL and an IP appearing together does not prove the IP hosts the URL.
- A hash and a URL appearing together does not prove the hash belongs
  to the URL.
- An email address and a domain appearing together does not prove
  ownership or attribution.

Use only relationships explicitly stated in the evidence.

Provide the final specialist finding.
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
    """
    Combine specialist findings into an overall risk assessment.

    The Risk Agent must not invent relationships between IOCs.
    """

    compact_findings = clean_text(findings, 5000)

    system_prompt = """
You are the Risk Agent of a defensive SOC.

Combine the specialist findings and determine:

- Overall risk: Low, Medium, or High
- Main reason
- Most important observed indicators
- Immediate defensive actions
- Confidence

STRICT RULES:

1. Use only supplied evidence and specialist findings.
2. Never invent external intelligence.
3. Never invent DNS, WHOIS, VirusTotal, sandbox,
   reputation, geolocation, or threat actor information.
4. Do not create relationships between IOCs merely because they
   appear in the same investigation.
5. Do not claim an IP belongs to or resolves a domain unless
   the evidence explicitly states that.
6. Do not claim a hash belongs to a URL, file, email, or payload
   unless the evidence explicitly states that.
7. HTTP indicates lack of TLS encryption, but does not by itself
   prove malicious intent.
8. Separate confirmed observations from assumptions.
9. If verification is required, clearly state:
   "Needs external verification."
10. Defensive recommendations must be proportional to the evidence.

Keep the answer concise.
"""

    user_prompt = f"""
SPECIALIST FINDINGS:

{compact_findings}

EXTRACTED IOC INFORMATION:

{clean_text(ioc_context, 1800)}

Remember:

The IOC list identifies indicators found in the evidence.

It does NOT automatically establish relationships between indicators.

Only use a relationship if it is explicitly supported by the evidence
or specialist findings.

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
    """
    Senior SOC Analyst produces the final incident assessment.
    """

    evidence = clean_text(original_evidence, 2400)
    findings = clean_text(specialist_findings, 4200)
    risk = clean_text(risk, 1800)

    system_prompt = """
You are the senior SOC Analyst.

Create a concise defensive incident assessment.

Include:

- Executive Summary
- Risk Level
- Key Findings
- Indicators
- Recommended Containment
- Recommended Investigation
- Confidence

STRICT EVIDENCE RULES:

1. Use only supplied evidence.
2. Do not invent external intelligence.
3. Do not invent DNS, WHOIS, VirusTotal, sandbox,
   reputation, geolocation, attribution, or malware results.
4. Do not infer that two IOCs are related simply because they
   appear in the same evidence.
5. Do not say an IP belongs to or resolves a domain unless this
   relationship is explicitly established.
6. Do not say a hash belongs to a URL, email, file, or payload
   unless this relationship is explicitly established.
7. Do not automatically classify HTTP as malicious.
8. Clearly distinguish confirmed observations from suspected activity.
9. State when additional verification is required.
10. Do not provide malware execution instructions.
11. Do not present assumptions as facts.

Use professional SOC terminology.
"""

    user_prompt = f"""
ORIGINAL EVIDENCE:

{evidence}

SPECIALIST FINDINGS:

{findings}

RISK ASSESSMENT:

{risk}

Prepare the final defensive SOC assessment.

Every important claim must be traceable to the supplied evidence.
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
    """
    Validate IPv4 octets.

    Example:
    192.168.1.1 -> valid
    999.999.999.999 -> invalid
    """

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
    """
    Extract common IOC types from supplied evidence.

    This function only extracts indicators.
    It does not determine whether they are malicious.
    """

    if not text:
        return empty_ioc_result()

    text = str(text)

    # --------------------------------------------------------
    # IP addresses
    # --------------------------------------------------------

    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

    raw_ips = re.findall(ip_pattern, text)

    ip_addresses = []

    for ip in raw_ips:
        if valid_ipv4(ip) and ip not in ip_addresses:
            ip_addresses.append(ip)

    # --------------------------------------------------------
    # URLs
    # --------------------------------------------------------

    url_pattern = r'https?://[^\s<>"\']+'

    raw_urls = re.findall(url_pattern, text)

    urls = []

    for url in raw_urls:
        url = url.rstrip(".,;:!?)]}")

        if url and url not in urls:
            urls.append(url)

    # --------------------------------------------------------
    # Email addresses
    # --------------------------------------------------------

    email_pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}\b"
    )

    email_addresses = []

    for email in re.findall(email_pattern, text):
        if email not in email_addresses:
            email_addresses.append(email)

    # --------------------------------------------------------
    # Hashes
    # --------------------------------------------------------

    md5_pattern = r"\b[a-fA-F0-9]{32}\b"
    sha1_pattern = r"\b[a-fA-F0-9]{40}\b"
    sha256_pattern = r"\b[a-fA-F0-9]{64}\b"

    md5 = list(dict.fromkeys(re.findall(md5_pattern, text)))
    sha1 = list(dict.fromkeys(re.findall(sha1_pattern, text)))
    sha256 = list(dict.fromkeys(re.findall(sha256_pattern, text)))

    # --------------------------------------------------------
    # Domains
    # --------------------------------------------------------

    domain_pattern = (
        r"\b(?:[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)"
        r"+[a-zA-Z]{2,}\b"
    )

    raw_domains = re.findall(domain_pattern, text)

    domains = []

    for domain in raw_domains:
        domain = domain.lower()

        if domain not in domains:
            domains.append(domain)

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
    """
    Display extracted IOC information.
    """

    total_iocs = sum(
        len(value)
        for value in iocs.values()
    )

    st.subheader("🔎 IOC Extraction")

    st.write(f"**{total_iocs} IOC(s) detected**")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "IP Addresses",
        len(iocs["ip_addresses"]),
    )

    col2.metric(
        "URLs",
        len(iocs["urls"]),
    )

    col3.metric(
        "Domains",
        len(iocs["domains"]),
    )

    hash_count = (
        len(iocs["md5"])
        + len(iocs["sha1"])
        + len(iocs["sha256"])
    )

    col4.metric(
        "Hashes",
        hash_count,
    )

    # --------------------------------------------------------
    # IP addresses
    # --------------------------------------------------------

    if iocs["ip_addresses"]:
        st.markdown("### 🌐 IP Addresses")

        for item in iocs["ip_addresses"]:
            st.code(item)

    # --------------------------------------------------------
    # URLs
    # --------------------------------------------------------

    if iocs["urls"]:
        st.markdown("### 🔗 URLs")

        for item in iocs["urls"]:
            st.code(item)

    # --------------------------------------------------------
    # Domains
    # --------------------------------------------------------

    if iocs["domains"]:
        st.markdown("### 🏷️ Domains")

        for item in iocs["domains"]:
            st.code(item)

    # --------------------------------------------------------
    # Emails
    # --------------------------------------------------------

    if iocs["email_addresses"]:
        st.markdown("### 📧 Email Addresses")

        for item in iocs["email_addresses"]:
            st.code(item)

    # --------------------------------------------------------
    # MD5
    # --------------------------------------------------------

    if iocs["md5"]:
        st.markdown("### 🔐 MD5")

        for item in iocs["md5"]:
            st.code(item)

    # --------------------------------------------------------
    # SHA1
    # --------------------------------------------------------

    if iocs["sha1"]:
        st.markdown("### 🔐 SHA1")

        for item in iocs["sha1"]:
            st.code(item)

    # --------------------------------------------------------
    # SHA256
    # --------------------------------------------------------

    if iocs["sha256"]:
        st.markdown("### 🔐 SHA256")

        for item in iocs["sha256"]:
            st.code(item)


# ============================================================
# FILE HASHING
# ============================================================

def calculate_sha256(file_bytes):
    """
    Calculate SHA-256 hash locally.

    The file is NOT executed.
    """

    return hashlib.sha256(file_bytes).hexdigest()


def get_file_metadata(uploaded_file, file_bytes):
    """
    Collect safe metadata about an uploaded file.
    """

    sha256 = calculate_sha256(file_bytes)

    return {
        "filename": uploaded_file.name,
        "file_type": uploaded_file.type or "Unknown",
        "size_bytes": len(file_bytes),
        "sha256": sha256,
    }


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("---")

st.header("📥 Investigation Input")

input_tab, file_tab = st.tabs(
    [
        "📝 Text Investigation",
        "📁 File Investigation",
    ]
)


# ============================================================
# TEXT INPUT
# ============================================================

investigation_text = ""
analyze_text = False

with input_tab:

    st.markdown(
        "Paste suspicious email content, logs, URLs, "
        "IP addresses, hashes, or other security evidence."
    )

    text_input = st.text_area(
        "Investigation Evidence",
        height=250,
        placeholder=(
            "Example:\n\n"
            "From: security@example.com\n"
            "Subject: Urgent account verification required\n\n"
            "Please verify your account:\n"
            "http://example.com/login\n\n"
            "Connection observed to 185.220.101.45\n"
            "MD5: d41d8cd98f00b204e9800998ecf8427e"
        ),
    )

    analyze_text = st.button(
        "🚀 Analyze Evidence",
        type="primary",
        key="analyze_text_button",
    )

    if analyze_text:
        if not text_input.strip():
            st.warning("Please provide investigation evidence.")

        else:
            investigation_text = text_input


# ============================================================
# FILE INPUT
# ============================================================

with file_tab:

    st.markdown(
        "Upload a file for safe metadata and SHA-256 analysis. "
        "The application never executes uploaded files."
    )

    uploaded_file = st.file_uploader(
        "Upload Evidence File",
        type=None,
        key="investigation_file",
    )

    analyze_file = st.button(
        "🔬 Analyze File",
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

            st.subheader("📁 File Information")

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**Filename:** {metadata['filename']}"
                )

                st.write(
                    f"**Type:** {metadata['file_type']}"
                )

                st.write(
                    f"**Size:** {metadata['size_bytes']} bytes"
                )

            with col2:
                st.write("**SHA-256:**")

                st.code(metadata["sha256"])

            st.success(
                "File processed safely. "
                "No file execution was performed."
            )

            # Build safe investigation evidence.
            investigation_text = f"""
Uploaded file metadata:

Filename: {metadata['filename']}
File type: {metadata['file_type']}
Size: {metadata['size_bytes']} bytes
SHA-256: {metadata['sha256']}

Important:
The file was NOT executed.
No external reputation or malware scan was performed.
"""

            analyze_text = True


# ============================================================
# COMMON ANALYSIS PIPELINE
# ============================================================

if analyze_text and investigation_text.strip():

    # --------------------------------------------------------
    # Extract IOCs
    # --------------------------------------------------------

    iocs = extract_iocs(investigation_text)

    display_ioc_summary(iocs)

    # --------------------------------------------------------
    # Create IOC context
    # --------------------------------------------------------

    ioc_context = json.dumps(
        iocs,
        indent=2,
    )

    # --------------------------------------------------------
    # Multi-Agent Investigation
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("🤖 Multi-Agent Investigation")

    with st.spinner(
        "Running CyberShield specialist agents..."
    ):

        specialist_definitions = [
            {
                "name": "Email / Phishing Agent",
                "task": (
                    "Analyze email-related evidence for phishing "
                    "characteristics such as urgency, suspicious "
                    "requests, impersonation indicators, links, "
                    "and credential-harvesting language."
                ),
            },
            {
                "name": "URL Agent",
                "task": (
                    "Analyze URLs for observable characteristics "
                    "such as HTTP versus HTTPS, suspicious paths, "
                    "unusual formatting, and other evidence explicitly "
                    "present in the supplied data."
                ),
            },
            {
                "name": "File Agent",
                "task": (
                    "Analyze file-related evidence, metadata, and "
                    "hashes. Do not claim a file is malicious without "
                    "supporting evidence."
                ),
            },
            {
                "name": "Malware Agent",
                "task": (
                    "Look for evidence of malware or malicious payloads. "
                    "Do not identify malware families without evidence "
                    "supporting that identification."
                ),
            },
            {
                "name": "IOC Agent",
                "task": (
                    "Review extracted IPs, URLs, domains, emails, "
                    "and hashes. Confirm what was observed and identify "
                    "which indicators require external verification."
                ),
            },
            {
                "name": "Threat Intelligence Agent",
                "task": (
                    "Assess the supplied evidence from a threat "
                    "intelligence perspective. Do not fabricate external "
                    "reputation or attribution information."
                ),
            },
        ]

        specialist_results = []

        for definition in specialist_definitions:

            result = specialist_agent(
                definition["name"],
                investigation_text,
                definition["task"],
                ioc_context,
            )

            specialist_results.append(
                {
                    "agent": definition["name"],
                    "finding": result,
                }
            )

    st.success(
        "Multi-agent investigation completed."
    )

    # --------------------------------------------------------
    # Specialist Findings
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("🧩 Specialist Agent Findings")

    for item in specialist_results:

        st.markdown(
            f"#### 🤖 {item['agent']}"
        )

        # IMPORTANT:
        # st.text() prevents the AI's Markdown from being
        # interpreted as UI formatting.
        #
        # This fixes the previous situation where actual findings
        # appeared as "-", "1.", "*" etc.
        st.text(item["finding"])

        st.markdown("---")

    # --------------------------------------------------------
    # Combine findings
    # --------------------------------------------------------

    combined_findings = "\n\n".join(
        [
            f"Agent: {item['agent']}\n"
            f"{item['finding']}"
            for item in specialist_results
        ]
    )

    # --------------------------------------------------------
    # Risk Agent
    # --------------------------------------------------------

    st.subheader("⚠️ Risk Assessment")

    with st.spinner(
        "Risk Agent is assessing the investigation..."
    ):

        risk_result = risk_agent(
            combined_findings,
            ioc_context,
        )

    # Display risk as plain text to avoid accidental
    # Markdown interpretation of unsupported AI formatting.
    st.text(risk_result)

    # --------------------------------------------------------
    # SOC Analyst
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("🛡️ SOC Analyst Report")

    with st.spinner(
        "Senior SOC Analyst is preparing the final assessment..."
    ):

        final_report = soc_analyst(
            investigation_text,
            combined_findings,
            risk_result,
        )

    st.markdown(final_report)

    # --------------------------------------------------------
    # JSON REPORT
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("📦 Investigation Report")

    report = {
        "project": "CyberShield Multi-Agent SOC",
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
        label="⬇️ Download JSON Report",
        data=report_json,
        file_name="cybershield_soc_report.json",
        mime="application/json",
        key="download_json_report",
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "CyberShield Multi-Agent SOC • Defensive cybersecurity "
    "analysis platform • AI-generated findings must be validated "
    "against trusted security sources before operational action."
)
