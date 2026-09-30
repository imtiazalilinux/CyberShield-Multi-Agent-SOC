import streamlit as st
from groq import Groq
import hashlib
import json
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="CyberShield | Multi-Agent SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Cybersecurity-style UI
# -----------------------------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 8% 8%, rgba(0,255,170,.10), transparent 25%),
      radial-gradient(circle at 92% 12%, rgba(0,150,255,.12), transparent 28%),
      radial-gradient(circle at 50% 100%, rgba(150,70,255,.10), transparent 30%),
      linear-gradient(135deg,#030712 0%,#071421 48%,#030712 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#030811 0%,#071521 100%);
    border-right: 1px solid rgba(0,255,170,.16);
}
.hero {
    padding: 30px;
    border: 1px solid rgba(0,255,170,.20);
    border-radius: 24px;
    background: linear-gradient(135deg,rgba(8,35,46,.94),rgba(5,14,27,.92));
    box-shadow: 0 0 55px rgba(0,255,170,.08);
    margin-bottom: 22px;
}
.hero h1 { margin:0; font-size:42px; font-weight:800; letter-spacing:-1px; }
.hero p { margin:8px 0 0; color:#91a9b9; }
.card {
    border:1px solid rgba(120,170,200,.16);
    border-radius:16px;
    padding:17px;
    background:rgba(8,20,32,.72);
    min-height:118px;
    margin-bottom:10px;
}
.card h4 { margin:0 0 7px; color:#dcecf5; }
.card p { margin:0; color:#8da5b5; font-size:13px; }
.metric {
    border:1px solid rgba(0,255,170,.15);
    background:rgba(6,20,29,.78);
    border-radius:15px;
    padding:15px;
    text-align:center;
}
.metric-value { font-size:25px; font-weight:800; color:#65ffc6; }
.metric-label { color:#8da5b5; font-size:12px; }
.stButton > button { border-radius:12px; border:1px solid rgba(0,255,170,.25); }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Configuration
# -----------------------------
DEFAULT_MODEL = "llama-3.3-70b-versatile"

def secret(name, default=None):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default

GROQ_API_KEY = secret("GROQ_API_KEY")
GROQ_MODEL = secret("GROQ_MODEL", DEFAULT_MODEL)

AGENTS = [
    ("📧", "Email Agent", "Phishing, sender clues, urgency and social engineering"),
    ("🔗", "URL Agent", "URL structure, domains, redirects and suspicious patterns"),
    ("📁", "File Agent", "Filename, extension, metadata and supplied file indicators"),
    ("🦠", "Malware Agent", "Malware-family and behavior indicators from supplied evidence"),
    ("🔎", "IOC Agent", "IP addresses, domains, URLs, hashes and other indicators"),
    ("🧠", "Threat Intel Agent", "Threat patterns and MITRE ATT&CK-oriented correlation"),
    ("⚖️", "Risk Agent", "Evidence-based risk and confidence assessment"),
    ("🛡️", "SOC Analyst Agent", "Final incident summary and defensive recommendations"),
]


def groq_call(system_prompt: str, user_prompt: str) -> str:
    client = Groq(api_key=GROQ_API_KEY)
    result = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.1,
        max_tokens=1800,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return result.choices[0].message.content


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_agents(evidence: str, filename: str = ""):
    system = """You are a defensive cybersecurity analyst in CyberShield.
Analyze ONLY the evidence provided. Do not invent external reputation results,
sandbox results, threat-intelligence hits, or observations. Do not execute files.
Clearly distinguish facts, hypotheses, and uncertainty. Give defensive analysis only."""

    prompts = {
        "Email Agent": f"""Analyze this evidence for phishing and social-engineering indicators.
Look for sender impersonation, urgency, credential requests, suspicious language,
attachments and links.

EVIDENCE:\n{evidence}""",

        "URL Agent": f"""Analyze supplied URLs/domains for suspicious structure,
lookalikes, encoding, redirects, credential harvesting and other indicators.
Do not claim external reputation results.

EVIDENCE:\n{evidence}""",

        "File Agent": f"""Analyze supplied file information defensively.
Discuss filename, extension, SHA-256, metadata and any static indicators present.
Never claim that the file was executed.

FILENAME: {filename}\nEVIDENCE:\n{evidence}""",

        "Malware Agent": f"""Assess possible malware indicators including trojan,
ransomware, worm, downloader, persistence or command-and-control behavior only
when supported by the evidence.

EVIDENCE:\n{evidence}""",

        "IOC Agent": f"""Extract IOCs from the evidence and categorize them as IP,
domain, URL, email, hash, filename or other useful indicator. Say 'none found'
when appropriate.

EVIDENCE:\n{evidence}""",

        "Threat Intel Agent": f"""Correlate the supplied evidence with defensive
threat-intelligence concepts and MITRE ATT&CK techniques where reasonably supported.
Do not pretend to have queried an external database.

EVIDENCE:\n{evidence}""",
    }

    results = {}
    for name, prompt in prompts.items():
        results[name] = groq_call(system, prompt)

    combined = "\n\n".join(f"### {name}\n{text}" for name, text in results.items())

    results["Risk Agent"] = groq_call(system, f"""Review these specialist findings:\n\n{combined}

Return:
1. Risk: Informational / Low / Medium / High / Critical
2. Confidence: Low / Medium / High
3. Strongest evidence
4. Important uncertainty
5. Defensive next steps

Do not invent external results.""")

    results["SOC Analyst Agent"] = groq_call(system, f"""Act as the senior SOC analyst.
Use the following specialist findings and risk assessment:

{combined}

RISK ASSESSMENT:
{results['Risk Agent']}

Produce:
- Executive summary
- Likely threat type
- Key IOCs
- Evidence
- Uncertainty / limitations
- Recommended containment
- Recommended investigation steps
- MITRE ATT&CK techniques only where supported

Do not claim that a response action has already been performed.""")
    return results


def detect_risk(text: str) -> str:
    lower = text.lower()
    for level in ["critical", "high", "medium", "low", "informational"]:
        if level in lower:
            return level.title()
    return "Unknown"

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
  <h1>🛡️ CYBERSHIELD</h1>
  <p>Multi-Agent Cybersecurity Analysis Platform • Phishing • Malware • IOC • Threat Intelligence • SOC</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🛡️ CyberShield")
    st.caption("AI-assisted defensive security laboratory")
    st.divider()
    page = st.radio("Workspace", ["🔬 Investigation", "🤖 Agent Center", "ℹ️ About"])
    st.divider()
    st.markdown("### System Status")
    st.success("UI: ONLINE")
    st.info(f"Model: {GROQ_MODEL}")
    if GROQ_API_KEY:
        st.success("Groq API: CONFIGURED")
    else:
        st.warning("Groq API: NOT CONFIGURED")
    st.caption("Never commit your API key to GitHub.")

if page == "🤖 Agent Center":
    st.subheader("🤖 CyberShield Agent Center")
    cols = st.columns(2)
    for i, (icon, name, description) in enumerate(AGENTS):
        with cols[i % 2]:
            st.markdown(f"<div class='card'><h4>{icon} {name}</h4><p>{description}</p></div>", unsafe_allow_html=True)
    st.info("The MVP uses Groq for reasoning. Production malware sandboxing should be isolated from the Streamlit host.")
    st.stop()

if page == "ℹ️ About":
    st.subheader("About CyberShield")
    st.write("CyberShield is an AI-assisted defensive investigation dashboard. Specialist agents examine supplied evidence, then a risk agent and SOC analyst agent correlate the findings.")
    st.markdown("### Architecture")
    st.code("Evidence → Specialist Agents → Risk/Correlation → SOC Analyst → Report")
    st.markdown("### Safety boundary")
    st.warning("This MVP never executes uploaded files. Do not use it as a production malware sandbox. Add an isolated sandbox service later.")
    st.stop()

# -----------------------------
# Investigation workspace
# -----------------------------
st.subheader("🔬 New Security Investigation")

left, right = st.columns([1.35, 1])
with left:
    evidence = st.text_area(
        "Paste suspicious email, URL, log excerpt, IOC list, or analyst notes",
        height=280,
        placeholder="Example:\nFrom: security@example.com\nSubject: Urgent account verification\nPlease verify your account immediately...\nhttps://example.invalid/login"
    )

with right:
    uploaded = st.file_uploader(
        "Optional evidence file",
        type=["txt", "csv", "log", "json", "pdf", "docx", "xlsx", "zip", "exe", "dll"],
        help="The MVP calculates file metadata/hash but does not execute the file."
    )
    filename = ""
    if uploaded:
        filename = uploaded.name
        data = uploaded.getvalue()
        file_hash = sha256(data)
        st.markdown(f"**File:** `{filename}`")
        st.markdown(f"**Size:** `{len(data):,} bytes`")
        st.markdown(f"**SHA-256:** `{file_hash}`")
        if not evidence.strip():
            evidence = f"Uploaded file: {filename}\nSize: {len(data)} bytes\nSHA-256: {file_hash}\nExtension: {Path(filename).suffix}\nThe file was not executed."

st.divider()

run = st.button("🚀 RUN MULTI-AGENT ANALYSIS", type="primary", use_container_width=True)

if run:
    if not evidence.strip():
        st.error("Please provide evidence or upload a file.")
        st.stop()
    if not GROQ_API_KEY:
        st.error("Groq API key is missing. Configure GROQ_API_KEY in .streamlit/secrets.toml locally or in Streamlit Cloud Secrets.")
        st.stop()

    case_id = "CS-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    progress = st.progress(0)
    status = st.empty()
    status.info("🧠 Starting specialist agents...")
    progress.progress(10)

    try:
        with st.spinner("Agents are analyzing the evidence..."):
            results = run_agents(evidence, filename)
        progress.progress(100)
        status.success("✅ Multi-agent investigation completed")
    except Exception as exc:
        st.error(f"Analysis failed: {exc}")
        st.stop()

    risk = detect_risk(results.get("Risk Agent", ""))

    st.markdown(f"### Case `{case_id}`")
    m1, m2, m3, m4 = st.columns(4)
    metrics = [(m1, risk, "Risk Level"), (m2, "8", "Agents"), (m3, "Groq", "AI Engine"), (m4, "NO", "Host Execution")]
    for box, value, label in metrics:
        with box:
            st.markdown(f"<div class='metric'><div class='metric-value'>{value}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("🧠 Specialist Findings")
    for icon, name, _ in AGENTS[:6]:
        with st.expander(f"{icon} {name}"):
            st.markdown(results.get(name, "No result."))

    st.subheader("⚖️ Risk Assessment")
    st.markdown(results.get("Risk Agent", "No risk assessment."))

    st.subheader("🛡️ Final SOC Analyst Report")
    st.markdown(results.get("SOC Analyst Agent", "No report generated."))

    report = {
        "case_id": case_id,
        "timestamp": datetime.now().isoformat(),
        "filename": filename,
        "risk": risk,
        "agents": results,
        "host_execution": False,
    }
    st.download_button(
        "📥 Download JSON Investigation Report",
        json.dumps(report, indent=2),
        file_name=f"{case_id}.json",
        mime="application/json",
    )

st.caption("CyberShield MVP • Defensive analysis only • Never execute suspicious files on the host.")
