import streamlit as st
import hashlib
import json
import re
from groq import Groq


# ============================================================
# CYBERSHIELD MULTI-AGENT SOC
# Token-efficient MVP for Groq free/on-demand limits
# ============================================================

st.set_page_config(
    page_title="CyberShield Multi-Agent SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_MODEL = "openai/gpt-oss-120b"

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
GROQ_MODEL = st.secrets.get("GROQ_MODEL", DEFAULT_MODEL)


# ============================================================
# CYBER UI
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, #0b2435 0%, #050914 40%, #03060d 100%);
        color: #e8f0f7;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #00e6a8;
        margin-bottom: 0;
    }

    .subtitle {
        color: #8fa7b8;
        font-size: 16px;
        margin-top: 0;
    }

    .agent-box {
        background: rgba(8, 21, 33, 0.85);
        border: 1px solid #17364a;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
    }

    .status-online {
        color: #00e6a8;
        font-weight: bold;
    }

    .status-warning {
        color: #ffc857;
        font-weight: bold;
    }

    .risk-high {
        color: #ff5c5c;
        font-weight: bold;
    }

    .risk-medium {
        color: #ffc857;
        font-weight: bold;
    }

    .risk-low {
        color: #00e6a8;
        font-weight: bold;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ CyberShield Multi-Agent SOC</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">AI-assisted defensive cybersecurity investigation platform</div>',
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ SOC Status")

    if GROQ_API_KEY:
        st.markdown(
            '<span class="status-online">● Groq API: CONFIGURED</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="status-warning">● Groq API: NOT CONFIGURED</span>',
            unsafe_allow_html=True,
        )

    st.write(f"Model: `{GROQ_MODEL}`")

    st.divider()

    st.subheader("🤖 Active Agents")

    agents = [
        "Email / Phishing Agent",
        "URL Agent",
        "File Agent",
        "Malware Agent",
        "IOC Agent",
        "Threat Intelligence Agent",
        "Risk Agent",
        "SOC Analyst Agent",
    ]

    for agent in agents:
        st.write(f"✓ {agent}")

    st.divider()

    st.caption(
        "Defensive analysis only. Uploaded files are hashed and inspected as metadata/text. "
        "CyberShield does not execute unknown files."
    )


# ============================================================
# SECURITY CHECK
# ============================================================

if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY is not configured. Add it in "
        "Streamlit → Settings → Secrets."
    )
    st.stop()


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# TOKEN / INPUT LIMITS
# ============================================================

# Keep evidence short so every agent request remains small.
MAX_INPUT_CHARS = 3500

# Specialist agents should answer briefly.
SPECIALIST_MAX_TOKENS = 350

# Risk and SOC agents need slightly more space.
RISK_MAX_TOKENS = 450
SOC_MAX_TOKENS = 650


def clean_text(text, limit=MAX_INPUT_CHARS):
    """Normalize and truncate investigation evidence."""

    if not text:
        return ""

    text = str(text)

    # Remove excessive whitespace
    text = " ".join(text.split())

    if len(text) > limit:
        text = text[:limit] + "\n[Evidence truncated]"

    return text


# ============================================================
# GROQ CALL
# ============================================================

def call_groq(system_prompt, user_prompt, max_tokens=350):
    """
    Make a compact Groq request.

    Small prompts and small outputs are intentional because
    the free/on-demand organization limit is currently 8K TPM.
    """

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.1,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": clean_text(system_prompt, 1800),
            },
            {
                "role": "user",
                "content": clean_text(user_prompt, MAX_INPUT_CHARS),
            },
        ],
    )

    return response.choices[0].message.content.strip()


# ============================================================
# SPECIALIST AGENT
# ============================================================

def specialist_agent(agent_name, evidence, task, ioc_context):

    system_prompt = f"""
You are the {agent_name} in a defensive SOC.

Task:
{task}

Rules:
- Analyze only the supplied evidence.
- Do not invent reputation, sandbox, WHOIS, VirusTotal, or external lookup results.
- Clearly say when evidence is insufficient.
- Focus on defensive cybersecurity.
- Return concise findings.
- Do not provide malware execution instructions.

Return:
1. Finding
2. Evidence
3. Risk: Low/Medium/High
4. Recommended action
"""

    user_prompt = f"""
Investigation evidence:

{clean_text(evidence)}

Extracted IOC information:

{clean_text(ioc_context, 1800)}

Use the extracted IOCs as supporting evidence.
If an IOC has not been externally verified, do not claim that it is malicious.

Provide a concise SOC finding.
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

Combine the specialist findings.

Determine:
- Overall risk: Low, Medium, or High
- Main reason
- Most important indicators
- Immediate defensive action

Do not invent facts.
Do not claim external reputation checks that were not supplied.

Keep the answer concise.
"""

    user_prompt = f"""
Specialist findings:

{compact_findings}

Extracted IOC information:

{clean_text(ioc_context, 1800)}

Use the extracted IOCs as supporting evidence.
Do not assume that an IOC is malicious unless the supplied evidence supports that conclusion.
"""

    return call_groq(
        system_prompt,
        user_prompt,
        RISK_MAX_TOKENS,
    )


# ============================================================
# SOC ANALYST AGENT
# ============================================================

def soc_analyst(original_evidence, specialist_findings, risk):

    evidence = clean_text(original_evidence, 2200)
    findings = clean_text(specialist_findings, 4000)
    risk = clean_text(risk, 1800)

    system_prompt = """
You are the senior SOC Analyst.

Create a concise defensive incident assessment.

Include:
- Executive summary
- Risk level
- Key findings
- Indicators
- Recommended containment
- Recommended investigation
- Confidence

Important:
- Use only supplied evidence.
- Do not invent external intelligence.
- If an indicator needs external validation, say so.
- Do not provide instructions for executing malware.
"""

    user_prompt = f"""
ORIGINAL EVIDENCE:
{evidence}

SPECIALIST FINDINGS:
{findings}

RISK ASSESSMENT:
{risk}

Produce the final SOC assessment.
"""

    return call_groq(
        system_prompt,
        user_prompt,
        SOC_MAX_TOKENS,
    )

# ============================================================
# IOC EXTRACTION
# ============================================================

def extract_iocs(text):
    """
    Extract common Indicators of Compromise (IOCs)
    from investigation evidence.

    This is local pattern matching only.
    No external reputation lookup is performed.
    """

    if not text:
        return {
            "ip_addresses": [],
            "urls": [],
            "domains": [],
            "email_addresses": [],
            "md5": [],
            "sha1": [],
            "sha256": [],
        }

    # IPv4 addresses
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

    # URLs
    url_pattern = r"https?://[^\s<>\"]+"

    # Email addresses
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    # MD5 = 32 hexadecimal characters
    md5_pattern = r"\b[a-fA-F0-9]{32}\b"

    # SHA-1 = 40 hexadecimal characters
    sha1_pattern = r"\b[a-fA-F0-9]{40}\b"

    # SHA-256 = 64 hexadecimal characters
    sha256_pattern = r"\b[a-fA-F0-9]{64}\b"

    ips = sorted(set(re.findall(ip_pattern, text)))

    urls = sorted(set(re.findall(url_pattern, text)))

    emails = sorted(set(re.findall(email_pattern, text)))

    md5_hashes = sorted(set(re.findall(md5_pattern, text)))

    sha1_hashes = sorted(set(re.findall(sha1_pattern, text)))

    sha256_hashes = sorted(set(re.findall(sha256_pattern, text)))

    # Extract domains from URLs
    domains = []

    for url in urls:
        match = re.search(
            r"https?://([^/:?#]+)",
            url,
            re.IGNORECASE,
        )

        if match:
            domains.append(match.group(1).lower())

    # Also detect standalone domains
    domain_pattern = (
        r"\b(?:[a-zA-Z0-9-]+\.)+"
        r"(?:com|net|org|info|biz|io|co|pk|uk|us|gov|edu)\b"
    )

    standalone_domains = re.findall(
        domain_pattern,
        text,
        re.IGNORECASE,
    )

    domains.extend(
        [domain.lower() for domain in standalone_domains]
    )

    domains = sorted(set(domains))

    return {
        "ip_addresses": ips,
        "urls": urls,
        "domains": domains,
        "email_addresses": emails,
        "md5": md5_hashes,
        "sha1": sha1_hashes,
        "sha256": sha256_hashes,
    }


def display_ioc_summary(iocs):
    """
    Display extracted IOCs in the Streamlit interface.
    """

    total_iocs = sum(
        len(values)
        for values in iocs.values()
    )

    st.subheader("🔎 IOC Extraction")

    if total_iocs == 0:
        st.info(
            "No common IOCs were detected in the supplied evidence."
        )
        return

    st.success(
        f"{total_iocs} IOC(s) detected"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "IP Addresses",
            len(iocs["ip_addresses"]),
        )

    with col2:
        st.metric(
            "URLs",
            len(iocs["urls"]),
        )

    with col3:
        st.metric(
            "Domains",
            len(iocs["domains"]),
        )

    with col4:
        st.metric(
            "Hashes",
            (
                len(iocs["md5"])
                + len(iocs["sha1"])
                + len(iocs["sha256"])
            ),
        )

    if iocs["ip_addresses"]:
        st.write("**🌐 IP Addresses**")
        for item in iocs["ip_addresses"]:
            st.code(item)

    if iocs["urls"]:
        st.write("**🔗 URLs**")
        for item in iocs["urls"]:
            st.code(item)

    if iocs["domains"]:
        st.write("**🏷️ Domains**")
        for item in iocs["domains"]:
            st.code(item)

    if iocs["email_addresses"]:
        st.write("**📧 Email Addresses**")
        for item in iocs["email_addresses"]:
            st.code(item)

    if iocs["md5"]:
        st.write("**🔐 MD5**")
        for item in iocs["md5"]:
            st.code(item)

    if iocs["sha1"]:
        st.write("**🔐 SHA-1**")
        for item in iocs["sha1"]:
            st.code(item)

    if iocs["sha256"]:
        st.write("**🔐 SHA-256**")
        for item in iocs["sha256"]:
            st.code(item)
# ============================================================
# FILE HASHING
# ============================================================

def calculate_sha256(uploaded_file):

    data = uploaded_file.getvalue()

    sha256 = hashlib.sha256(data).hexdigest()

    return sha256, len(data)


# ============================================================
# FILE METADATA
# ============================================================

def get_file_metadata(uploaded_file):

    sha256, size = calculate_sha256(uploaded_file)

    filename = uploaded_file.name

    extension = ""

    if "." in filename:
        extension = filename.rsplit(".", 1)[1].lower()

    return {
        "filename": filename,
        "size_bytes": size,
        "extension": extension,
        "sha256": sha256,
        "content_type": uploaded_file.type,
    }


# ============================================================
# INVESTIGATION INPUT
# ============================================================

st.header("🔎 New Investigation")

input_tab, file_tab = st.tabs(
    [
        "📝 Text / Email / IOC",
        "📁 File Metadata",
    ]
)


# ============================================================
# TEXT INVESTIGATION
# ============================================================

with input_tab:

    st.write(
        "Paste a phishing email, suspicious URL, IOC, alert, log excerpt, "
        "or other defensive cybersecurity evidence."
    )

    investigation_text = st.text_area(
        "Investigation Evidence",
        height=220,
        placeholder=(
            "Example:\n"
            "From: security-alert@example.com\n"
            "Subject: Urgent account verification\n"
            "Click this link immediately: http://example.com/login"
        ),
    )

    analyze_text = st.button(
        "🚀 Analyze with Multi-Agent SOC",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# FILE INVESTIGATION
# ============================================================

with file_tab:

    st.write(
        "Upload a file for defensive metadata and hash analysis. "
        "The application does not execute uploaded files."
    )

    uploaded_file = st.file_uploader(
        "Upload file",
        type=[
            "txt",
            "csv",
            "log",
            "json",
            "pdf",
            "docx",
            "xlsx",
            "zip",
            "exe",
            "dll",
        ],
    )

    analyze_file = st.button(
        "🔬 Analyze File",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# FILE ANALYSIS
# ============================================================

if analyze_file:

    if uploaded_file is None:
        st.warning("Please upload a file first.")
        st.stop()

    metadata = get_file_metadata(uploaded_file)

    st.subheader("📋 File Metadata")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "File Size",
            f"{metadata['size_bytes']:,} bytes",
        )

    with col2:
        st.metric(
            "Type",
            metadata["extension"].upper()
            if metadata["extension"]
            else "Unknown",
        )

    with col3:
        st.metric(
            "Hash",
            metadata["sha256"][:12] + "...",
        )

    st.code(
        metadata["sha256"],
        language="text",
    )

    evidence = f"""
Filename: {metadata['filename']}
File size: {metadata['size_bytes']} bytes
Extension: {metadata['extension']}
Content type: {metadata['content_type']}
SHA-256: {metadata['sha256']}
"""

    investigation_text = evidence
    analyze_text = True


# ============================================================
# RUN MULTI-AGENT ANALYSIS
# ============================================================

if analyze_text:

    if not investigation_text or not investigation_text.strip():
        st.warning("Please provide investigation evidence.")
        st.stop()

evidence = clean_text(investigation_text)

# Extract IOCs before running the AI agents
iocs = extract_iocs(evidence)

display_ioc_summary(iocs)

ioc_context = json.dumps(
    iocs,
    indent=2,
    ensure_ascii=False,
)
st.divider()

st.subheader("🤖 Multi-Agent Investigation")

progress = st.progress(0)
status = st.empty()

# --------------------------------------------------------
# Specialist definitions
# --------------------------------------------------------

specialist_definitions = [
        (
            "Email / Phishing Agent",
            "Identify phishing characteristics, social engineering, suspicious sender details, urgency, credential theft indicators, and email anomalies.",
        ),
        (
            "URL Agent",
            "Identify suspicious URLs, domains, redirects, URL obfuscation, phishing patterns, and indicators requiring external validation.",
        ),
        (
            "File Agent",
            "Assess supplied file metadata, filename, extension, hash, and any supplied textual evidence for suspicious characteristics.",
        ),
        (
            "Malware Agent",
            "Look for evidence suggesting malware, trojans, worms, payload delivery, persistence, or malicious behavior. Do not assume malware without evidence.",
        ),
        (
            "IOC Agent",
            "Extract and classify possible IP addresses, domains, URLs, hashes, email addresses, filenames, and other indicators of compromise.",
        ),
        (
            "Threat Intelligence Agent",
            "Assess the supplied indicators from the evidence. Identify what would require external threat-intelligence validation. Do not invent reputation data.",
        ),
    ]

specialist_results = []

total_agents = len(specialist_definitions)

    # --------------------------------------------------------
    # Run specialists
    # --------------------------------------------------------

for index, (agent_name, task) in enumerate(
    specialist_definitions,
    start=1,
):

    status.info(
        f"Running {agent_name}..."
    )

    result = specialist_agent(
        agent_name,
        evidence,
        task,
        ioc_context,
    )

    specialist_results.append(
            {
                "agent": agent_name,
                "finding": result,
            }
        )

    progress.progress(
            int((index / (total_agents + 2)) * 100)
        )

    # --------------------------------------------------------
    # Combine specialist results
    # --------------------------------------------------------

    findings_text = "\n\n".join(
        [
            f"[{item['agent']}]\n{item['finding']}"
            for item in specialist_results
        ]
    )

    # Keep combined findings compact.
    findings_text = clean_text(
        findings_text,
        5000,
    )

    # --------------------------------------------------------
    # Risk Agent
    # --------------------------------------------------------

status.info("Running Risk Agent...")

risk_result = risk_agent(
    findings_text,
    ioc_context,
)

progress.progress(
    int((8 / 8) * 100)
)

    # --------------------------------------------------------
    # SOC Analyst
    # --------------------------------------------------------

    status.info(
        "Running SOC Analyst Agent..."
    )

    final_report = soc_analyst(
        evidence,
        findings_text,
        risk_result,
    )

    progress.progress(100)

    status.success(
        "Multi-agent investigation completed."
    )

    # ========================================================
    # DISPLAY SPECIALIST RESULTS
    # ========================================================

    st.divider()

    st.subheader("🧩 Specialist Agent Findings")

    for item in specialist_results:

        with st.expander(
            f"🤖 {item['agent']}",
            expanded=False,
        ):

            st.write(
                item["finding"]
            )

    # ========================================================
    # RISK ASSESSMENT
    # ========================================================

    st.divider()

    st.subheader("⚠️ Risk Assessment")

    st.markdown(
        risk_result
    )

    # ========================================================
    # FINAL SOC REPORT
    # ========================================================

    st.divider()

    st.subheader("🛡️ SOC Analyst Report")

    st.markdown(
        final_report
    )

    # ========================================================
    # JSON REPORT
    # ========================================================

    report = {
        "application": "CyberShield Multi-Agent SOC",
        "model": GROQ_MODEL,
        "investigation": evidence,
        "specialist_agents": specialist_results,
        "risk_assessment": risk_result,
        "soc_analyst_report": final_report,
    }

    report_json = json.dumps(
        report,
        indent=2,
        ensure_ascii=False,
    )

st.download_button(
    label="⬇️ Download JSON Investigation Report",
    data=report_json,
    file_name="cybershield_investigation_report.json",
    mime="application/json",
    use_container_width=True,
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CyberShield Multi-Agent SOC • Defensive cybersecurity analysis • "
    "AI-generated findings require analyst validation."
)
