"""Gaya antarmuka Streamlit: AI expert system console yang profesional."""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@500;600;700&display=swap');

:root {
    --bg: #050816;
    --bg-soft: #0b1120;
    --panel: rgba(15, 23, 42, 0.72);
    --panel-solid: #0f172a;
    --line: rgba(148, 163, 184, 0.16);
    --line-strong: rgba(148, 163, 184, 0.28);
    --text: #e6edf8;
    --muted: #94a3b8;
    --violet: #8b5cf6;
    --blue: #3b82f6;
    --cyan: #22d3ee;
    --emerald: #34d399;
    --amber: #fbbf24;
    --rose: #fb7185;
    --radius: 16px;
    --shadow: 0 24px 80px rgba(2, 6, 23, 0.45);
}

#MainMenu, footer, [data-testid="stAppDeployButton"] {
    visibility: hidden;
    display: none;
}
[data-testid="stHeader"] {
    background: transparent;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: "Plus Jakarta Sans", "Segoe UI", sans-serif;
    color: var(--text);
    font-size: 16px;
}

[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(rgba(148, 163, 184, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(148, 163, 184, 0.035) 1px, transparent 1px),
        radial-gradient(circle at 12% 4%, rgba(139, 92, 246, 0.20), transparent 34%),
        radial-gradient(circle at 88% 10%, rgba(34, 211, 238, 0.14), transparent 32%),
        radial-gradient(circle at 50% 100%, rgba(37, 99, 235, 0.12), transparent 45%),
        linear-gradient(135deg, #050816 0%, #070c1a 54%, #0b1120 100%);
    background-size: 44px 44px, 44px 44px, auto, auto, auto, auto;
    background-attachment: fixed;
}

h1, h2, h3, h4, h5 {
    font-family: "Sora", "Segoe UI", sans-serif;
    color: #f8fafc;
    letter-spacing: -0.02em;
    line-height: 1.25;
}
h1 { font-size: 2rem; }
h2 { font-size: 1.45rem; margin-top: 1.4rem; }
h3 { font-size: 1.1rem; }
h4 { font-size: 0.95rem; }

p, li {
    color: #cbd5e1;
    line-height: 1.7;
}
strong { color: #f8fafc; }
a { color: #67e8f9; text-decoration: none; }
a:hover { color: #c4b5fd; }

[data-testid="stCaptionContainer"] {
    color: var(--muted);
    font-size: 0.82rem;
}

code, pre, [data-testid="stCode"] {
    font-family: "IBM Plex Mono", "Consolas", monospace !important;
    background: #070c19 !important;
    color: #bae6fd !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
}

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #070c19; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #7c3aed, #0891b2);
    border-radius: 999px;
}

.block-container {
    max-width: 1180px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 20% 0%, rgba(139, 92, 246, 0.16), transparent 40%),
        linear-gradient(180deg, #0b1120 0%, #060a16 100%);
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.4rem;
}
[data-testid="stSidebar"] a {
    border-radius: 10px;
    color: #aebbd0;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 0.92rem;
    font-weight: 500;
    letter-spacing: 0;
    text-transform: none;
    padding: 0.5rem 0.65rem;
    transition: background 160ms ease, color 160ms ease;
}
[data-testid="stSidebar"] a:hover {
    background: rgba(139, 92, 246, 0.12);
    color: #f5f3ff;
}
[data-testid="stSidebar"] a[aria-current="page"] {
    background: linear-gradient(90deg, rgba(124, 58, 237, 0.55), rgba(37, 99, 235, 0.35));
    color: #ffffff;
    font-weight: 600;
    box-shadow: inset 0 0 0 1px rgba(196, 181, 253, 0.22);
}

/* Brand */
.merek {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.9rem;
    margin: 0.2rem 0 0.8rem 0;
    border: 1px solid rgba(139, 92, 246, 0.28);
    border-radius: 16px;
    background:
        linear-gradient(135deg, rgba(139, 92, 246, 0.16), rgba(34, 211, 238, 0.06)),
        rgba(15, 23, 42, 0.55);
}
.merek-ikon {
    flex: 0 0 auto;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: linear-gradient(135deg, #7c3aed, #0891b2);
    color: #ffffff;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.78rem;
    font-weight: 600;
    box-shadow: 0 0 24px rgba(139, 92, 246, 0.35);
}
.merek strong {
    display: block;
    color: #ffffff;
    font-family: "Sora", sans-serif;
    font-size: 0.92rem;
    line-height: 1.2;
}
.merek span {
    display: block;
    margin-top: 0.18rem;
    color: var(--muted);
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.status-sidebar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 1rem 0;
    padding: 0.55rem 0.7rem;
    border: 1px solid rgba(52, 211, 153, 0.18);
    border-radius: 10px;
    background: rgba(52, 211, 153, 0.06);
    color: #86efac;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.64rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.status-dot {
    width: 8px;
    height: 8px;
    flex: 0 0 auto;
    border-radius: 50%;
    background: var(--emerald);
    box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.45);
    animation: pulse 2.2s infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.45); }
    50% { box-shadow: 0 0 0 5px rgba(52, 211, 153, 0); }
}

/* Buttons */
.stButton > button, .stFormSubmitButton > button, [data-testid="stPageLink"] a {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    letter-spacing: 0;
    text-transform: none;
    border-radius: 10px;
    border: 1px solid var(--line-strong);
    background: rgba(15, 23, 42, 0.75);
    color: var(--text);
    padding: 0.58rem 1rem;
    box-shadow: none;
    transition: background 160ms ease, border-color 160ms ease, transform 160ms ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, [data-testid="stPageLink"] a:hover {
    background: rgba(139, 92, 246, 0.14);
    border-color: rgba(167, 139, 250, 0.55);
    color: #ffffff;
    transform: translateY(-1px);
}
.stButton > button:active, .stFormSubmitButton > button:active {
    transform: translateY(0);
}
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    border: 1px solid rgba(196, 181, 253, 0.45) !important;
    color: #ffffff !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.28) !important;
}
[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(135deg, #8b5cf6, #3b82f6) !important;
    color: #ffffff !important;
}

/* Inputs */
[data-testid="stWidgetLabel"] p {
    color: #cbd5e1;
    font-size: 0.85rem;
    font-weight: 500;
}
[data-baseweb="input"], [data-baseweb="textarea"] {
    border-radius: 10px !important;
    border: 1px solid var(--line-strong) !important;
    background: #0b1224 !important;
}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
    color: var(--text) !important;
    font-family: "Plus Jakarta Sans", sans-serif !important;
}
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within {
    border-color: rgba(139, 92, 246, 0.65) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.16) !important;
}
[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border: 1px solid var(--line-strong) !important;
    background: #0b1224 !important;
    color: var(--text) !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: rgba(139, 92, 246, 0.65) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.16) !important;
}
[data-testid="stChatInput"] {
    border: 1px solid var(--line-strong) !important;
    border-radius: 14px !important;
    background: #0b1224 !important;
    box-shadow: 0 10px 30px rgba(2, 6, 23, 0.35);
}
[data-testid="stChatInput"] textarea {
    font-family: "Plus Jakarta Sans", sans-serif !important;
    font-size: 0.95rem !important;
    color: var(--text) !important;
}

/* Surfaces */
[data-testid="stMetric"] {
    background: linear-gradient(150deg, rgba(30, 41, 59, 0.62), rgba(15, 23, 42, 0.45));
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 1rem 1.1rem;
}
[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    color: #ffffff;
    font-family: "Sora", sans-serif;
    font-size: 1.55rem;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius) !important;
    background: rgba(15, 23, 42, 0.45) !important;
    padding: 0.25rem;
}
[data-testid="stExpander"] {
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.52);
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #dbeafe;
}
[data-testid="stExpander"] summary:hover { color: #c4b5fd; }
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
}
[data-testid="stTabs"] button {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 0.86rem;
    font-weight: 600;
    color: var(--muted);
    border-radius: 8px;
}
[data-testid="stTabs"] button:hover { color: #c4b5fd; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #ffffff;
    border-bottom: 2px solid var(--violet);
}
[data-testid="stProgress"] > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #22d3ee) !important;
    border-radius: 999px;
}
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid var(--line) !important;
    background: rgba(15, 23, 42, 0.72) !important;
}
[data-testid="stCheckbox"] label span { border-radius: 5px !important; }

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(139, 92, 246, 0.32);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 1.6rem;
    background:
        radial-gradient(circle at 85% 20%, rgba(34, 211, 238, 0.12), transparent 38%),
        radial-gradient(circle at 10% 0%, rgba(139, 92, 246, 0.20), transparent 42%),
        linear-gradient(145deg, rgba(15, 23, 42, 0.92), rgba(7, 12, 25, 0.96));
    box-shadow: var(--shadow);
}
.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(139, 92, 246, 0.08), transparent 38%, rgba(34, 211, 238, 0.05));
    pointer-events: none;
}
.hero > * { position: relative; z-index: 1; }
.hero-grid {
    display: grid;
    grid-template-columns: 1.5fr 0.85fr;
    gap: 2rem;
    align-items: center;
}
.hero-label {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    padding: 0.38rem 0.7rem;
    border: 1px solid rgba(139, 92, 246, 0.35);
    border-radius: 999px;
    background: rgba(139, 92, 246, 0.1);
    color: #c4b5fd;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.hero h1 {
    margin: 0 0 0.85rem 0;
    font-family: "Sora", sans-serif;
    font-size: clamp(2.2rem, 5vw, 4rem);
    line-height: 1.02;
    letter-spacing: -0.055em;
    background: linear-gradient(90deg, #ffffff 0%, #c4b5fd 50%, #67e8f9 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    max-width: 46rem;
    margin: 0 0 0.75rem 0;
    color: #b7c4d9;
    font-size: 1rem;
    line-height: 1.7;
}
.hero-note {
    max-width: 46rem;
    margin: 0;
    color: var(--muted);
    font-size: 0.84rem;
    line-height: 1.6;
}
.hero-panel {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem;
    background: rgba(2, 6, 23, 0.48);
    backdrop-filter: blur(8px);
}
.hero-panel-label {
    margin-bottom: 0.7rem;
    color: var(--muted);
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.hero-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    color: #86efac;
    font-size: 0.86rem;
    font-weight: 600;
}
.hero-status-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.5rem 0;
    border-top: 1px solid var(--line);
    font-size: 0.78rem;
}
.hero-status-row span { color: var(--muted); }
.hero-status-row strong {
    color: #e2e8f0;
    font-weight: 600;
    text-align: right;
}

.statistik {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 1.5rem;
}
.stat {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.85rem 0.95rem;
    background: rgba(15, 23, 42, 0.46);
}
.stat span {
    display: block;
    color: var(--muted);
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.6rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.stat strong {
    display: block;
    margin-top: 0.3rem;
    font-family: "Sora", sans-serif;
    font-size: 1.45rem;
    color: #ffffff;
}
.stat small {
    display: block;
    margin-top: 0.12rem;
    color: #7d8ca3;
    font-size: 0.68rem;
}
.stat:nth-child(1) strong { color: #c4b5fd; }
.stat:nth-child(2) strong { color: #67e8f9; }
.stat:nth-child(3) strong { color: #86efac; }
.stat:nth-child(4) strong { color: #fcd34d; }

/* Section headings */
.section-heading { margin: 2rem 0 1rem 0; }
.section-kicker {
    display: block;
    margin-bottom: 0.4rem;
    color: #67e8f9;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.section-heading h2 {
    margin: 0;
    font-family: "Sora", sans-serif;
    font-size: 1.45rem;
    letter-spacing: -0.03em;
}
.section-heading p {
    max-width: 64rem;
    margin: 0.35rem 0 0 0;
    color: var(--muted);
    font-size: 0.9rem;
}

/* Expert system pipeline */
.pipeline {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.8rem;
    margin-bottom: 1.6rem;
}
.pipeline-step {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem;
    background: linear-gradient(155deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.42));
}
.pipeline-step .nomor {
    color: #67e8f9;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.66rem;
    letter-spacing: 0.12em;
}
.pipeline-step h3 {
    margin: 0.55rem 0 0.35rem 0;
    font-family: "Sora", sans-serif;
    font-size: 0.95rem;
    color: #f1f5f9;
}
.pipeline-step p {
    margin: 0;
    color: var(--muted);
    font-size: 0.8rem;
    line-height: 1.55;
}

/* Feature cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
    margin-bottom: 1.6rem;
}
.feature-card {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.05rem;
    background: rgba(15, 23, 42, 0.48);
}
.feature-tag {
    color: #67e8f9;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.feature-card h3 {
    margin: 0.45rem 0 0.4rem 0;
    font-family: "Sora", sans-serif;
    font-size: 1rem;
}
.feature-card p {
    margin: 0;
    color: var(--muted);
    font-size: 0.84rem;
    line-height: 1.6;
}

/* Steps and callouts */
.langkah {
    border: 1px solid var(--line);
    border-left: 3px solid var(--violet);
    border-radius: 0 10px 10px 0;
    background: rgba(15, 23, 42, 0.5);
    padding: 0.72rem 0.9rem;
    margin-bottom: 0.55rem;
    color: #cbd5e1;
    font-size: 0.88rem;
    line-height: 1.55;
}
.langkah:nth-child(2) { border-left-color: var(--blue); }
.langkah:nth-child(3) { border-left-color: var(--cyan); }
.langkah:nth-child(4) { border-left-color: var(--emerald); }
.note-panel {
    border: 1px solid rgba(251, 191, 36, 0.28);
    border-radius: 16px;
    padding: 1.1rem;
    background:
        linear-gradient(135deg, rgba(251, 191, 36, 0.08), rgba(15, 23, 42, 0.5));
}
.note-panel h3 {
    margin: 0 0 0.45rem 0;
    font-family: "Sora", sans-serif;
    font-size: 1rem;
    color: #fde68a;
}
.note-panel p, .note-panel li {
    color: #d6c7a6;
    font-size: 0.84rem;
    line-height: 1.6;
}
.note-panel ul { margin: 0.45rem 0 0 1.1rem; padding: 0; }

/* Page heading */
.judul-halaman {
    margin-bottom: 1.4rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--line);
}
.judul-halaman h1 {
    margin: 0.2rem 0 0 0;
    font-family: "Sora", sans-serif;
    font-size: clamp(1.7rem, 3.2vw, 2.3rem);
    letter-spacing: -0.04em;
    color: #ffffff;
}
.judul-halaman p {
    max-width: 64rem;
    margin: 0.5rem 0 0 0;
    color: var(--muted);
    font-size: 0.92rem;
}

/* Console bar */
.console-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.45rem;
    margin: 0.8rem 0 1rem 0;
    padding: 0.6rem 0.7rem;
    border: 1px solid var(--line);
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.55);
}
.console-bar .label {
    margin-right: 0.2rem;
    color: var(--muted);
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.55rem;
    border: 1px solid var(--line);
    border-radius: 999px;
    background: rgba(2, 6, 23, 0.4);
    color: #cbd5e1;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.6rem;
}
.pill.ok {
    border-color: rgba(52, 211, 153, 0.3);
    background: rgba(52, 211, 153, 0.08);
    color: #86efac;
}

/* Sidebar status */
.sidebar-panel {
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.5);
    padding: 0.8rem 0.85rem;
    margin: 1rem 0;
}
.sidebar-title {
    margin-bottom: 0.55rem;
    color: var(--muted);
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.sidebar-row {
    display: flex;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.38rem 0;
    border-top: 1px solid var(--line);
    color: #cbd5e1;
    font-size: 0.76rem;
}
.sidebar-row span { color: var(--muted); }
.sidebar-row strong {
    color: #f1f5f9;
    font-weight: 600;
    text-align: right;
}

/* Chat */
.jendela-chat {
    border: 1px solid var(--line);
    border-radius: 18px;
    background:
        radial-gradient(circle at 0% 0%, rgba(139, 92, 246, 0.08), transparent 35%),
        linear-gradient(180deg, rgba(15, 23, 42, 0.72), rgba(7, 12, 25, 0.84));
    box-shadow: var(--shadow);
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
}
.baris-pesan {
    display: flex;
    gap: 0.65rem;
    align-items: flex-start;
    margin: 0.7rem 0;
}
.baris-pesan.user { flex-direction: row-reverse; }
.avatar {
    flex: 0 0 auto;
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: linear-gradient(135deg, #7c3aed, #0891b2);
    color: #ffffff;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.58rem;
    font-weight: 600;
    box-shadow: 0 0 22px rgba(34, 211, 238, 0.16);
}
.baris-pesan.user .avatar {
    background: #1e293b;
    color: #a5f3fc;
    border: 1px solid var(--line-strong);
    box-shadow: none;
}
.gelembung {
    max-width: 76%;
    border: 1px solid var(--line);
    border-left: 2px solid var(--violet);
    border-radius: 4px 14px 14px 14px;
    background: rgba(30, 41, 59, 0.55);
    color: #e2e8f0;
    padding: 0.72rem 0.9rem;
    font-size: 0.92rem;
    line-height: 1.6;
    word-wrap: break-word;
}
.gelembung.user {
    border: 1px solid rgba(147, 197, 253, 0.3);
    border-left: 1px solid rgba(147, 197, 253, 0.3);
    border-radius: 14px 4px 14px 14px;
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.9), rgba(37, 99, 235, 0.9));
    color: #ffffff;
}
.gelembung .kode-gejala {
    display: inline-block;
    margin-right: 0.35rem;
    padding: 0.08rem 0.28rem;
    border: 1px solid rgba(34, 211, 238, 0.28);
    border-radius: 4px;
    background: rgba(34, 211, 238, 0.1);
    color: #67e8f9;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.58rem;
    vertical-align: middle;
}
.gelembung.user .kode-gejala {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.22);
    color: #ffffff;
}
.peringatan-chat {
    border: 1px solid rgba(251, 191, 36, 0.28);
    border-radius: 10px;
    background: rgba(251, 191, 36, 0.08);
    padding: 0.65rem 0.75rem;
    color: #fde68a;
    font-size: 0.85rem;
    line-height: 1.55;
}
.petunjuk-chat {
    margin: 0.2rem 0 0.45rem 0;
    color: var(--muted);
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.7rem;
    letter-spacing: 0.04em;
}

/* Results */
.hasil-judul {
    margin-bottom: 0.5rem;
    color: #c4b5fd;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.hasil-kartu {
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(2, 6, 23, 0.35);
    padding: 0.85rem 0.9rem;
    margin: 0.6rem 0;
}
.hasil-kartu.utama {
    border-color: rgba(139, 92, 246, 0.38);
    border-top: 2px solid var(--violet);
    background:
        radial-gradient(circle at 0% 0%, rgba(139, 92, 246, 0.16), transparent 45%),
        linear-gradient(135deg, rgba(30, 41, 59, 0.55), rgba(15, 23, 42, 0.4));
}
.hasil-nama {
    margin-bottom: 0.5rem;
    color: #c4b5fd;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.66rem;
    letter-spacing: 0.04em;
    line-height: 1.6;
    text-transform: uppercase;
}
.bar {
    height: 8px;
    margin: 0.4rem 0;
    border: none;
    border-radius: 999px;
    background: rgba(148, 163, 184, 0.16);
    overflow: hidden;
}
.bar > span {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #8b5cf6, #22d3ee);
}
.hasil-meta, .hasil-arti {
    color: #dbeafe;
    font-size: 0.86rem;
}
.hasil-saran {
    margin-top: 0.3rem;
    color: #cbd5e1;
    font-size: 0.84rem;
    line-height: 1.6;
}
.hasil-bagian {
    margin-top: 0.65rem;
    color: #67e8f9;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.hasil-alasan {
    margin: 0.35rem 0 0.1rem 1.1rem;
    padding: 0;
}
.hasil-alasan li {
    margin: 0.15rem 0;
    color: #cbd5e1;
    font-size: 0.84rem;
}
.hasil-catatan {
    margin-top: 0.65rem;
    padding: 0.55rem 0.65rem;
    border: 1px solid rgba(251, 191, 36, 0.22);
    border-radius: 10px;
    background: rgba(251, 191, 36, 0.07);
    color: #fde68a;
    font-size: 0.8rem;
    line-height: 1.55;
}
.hasil-kartu details { margin-top: 0.4rem; }
.hasil-kartu summary {
    cursor: pointer;
    color: #a5b4fc;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
}
.hasil-kartu pre {
    margin: 0.4rem 0 0 0;
    padding: 0.6rem 0.7rem;
    border: 1px solid var(--line);
    border-radius: 10px;
    background: #070c19;
    color: #bae6fd;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.7rem;
    white-space: pre-wrap;
    overflow: auto;
}
.daftar-sumber { margin-top: 0.35rem; }
.sumber-butir {
    margin-bottom: 0.4rem;
    color: #cbd5e1;
    font-size: 0.78rem;
    line-height: 1.5;
}
.sumber-jenis {
    display: inline-block;
    margin-right: 0.25rem;
    padding: 0.08rem 0.3rem;
    border: 1px solid rgba(34, 211, 238, 0.25);
    border-radius: 4px;
    background: rgba(34, 211, 238, 0.08);
    color: #67e8f9;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.56rem;
}
.sumber-butir a { color: #67e8f9; word-break: break-all; }

/* Inference trace */
.trace-conclusion {
    margin-top: 0.7rem;
    padding: 0.7rem 0.8rem;
    border: 1px solid rgba(52, 211, 153, 0.22);
    border-radius: 10px;
    background: rgba(52, 211, 153, 0.06);
    color: #bbf7d0;
    font-size: 0.84rem;
    line-height: 1.55;
}

/* Footer */
.footer-note {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--line);
    color: #64748b;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.62rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-align: center;
}

@media (max-width: 900px) {
    .hero-grid { grid-template-columns: 1fr; gap: 1.2rem; }
    .statistik { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .pipeline { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .feature-grid { grid-template-columns: 1fr; }
}
@media (max-width: 600px) {
    .hero { padding: 1.25rem; }
    .statistik { grid-template-columns: 1fr; }
    .pipeline { grid-template-columns: 1fr; }
    .gelembung { max-width: 88%; }
}
</style>
"""


def terapkan_gaya():
    """Pasang CSS console AI dan identitas aplikasi pada sidebar."""
    st.markdown(_CSS, unsafe_allow_html=True)
    st.sidebar.markdown(
        """
        <div class="merek">
            <div class="merek-ikon">AI</div>
            <div>
                <strong>PB Expert AI</strong>
                <span>Expert System Console</span>
            </div>
        </div>
        <div class="status-sidebar">
            <span class="status-dot"></span> Inference engine aktif
        </div>
        """,
        unsafe_allow_html=True,
    )


def judul_halaman(judul, subjudul=None, label="PB EXPERT AI"):
    """Tampilkan judul halaman dengan kicker dan garis pemisah konsisten."""
    bagian = (
        f'<div class="judul-halaman">'
        f'<span class="section-kicker">{label}</span>'
        f"<h1>{judul}</h1>"
    )
    if subjudul:
        bagian += f"<p>{subjudul}</p>"
    bagian += "</div>"
    st.markdown(bagian, unsafe_allow_html=True)


def alur_expert_system(jumlah_aturan=None):
    """Tampilkan pipeline penalaran sistem pakar yang dipakai aplikasi."""
    aturan = str(jumlah_aturan) if jumlah_aturan else "13"
    st.markdown(
        f"""
        <div class="pipeline">
            <div class="pipeline-step">
                <div class="nomor">01 / AKUISISI FAKTA</div>
                <h3>Working memory</h3>
                <p>Jawaban Iya direkam sebagai fakta gejala dengan nilai CF pengguna 1.0.</p>
            </div>
            <div class="pipeline-step">
                <div class="nomor">02 / FORWARD CHAINING</div>
                <h3>Rule matching</h3>
                <p>Fakta dicocokkan dengan {aturan} aturan IF-THEN pada basis pengetahuan pakar.</p>
            </div>
            <div class="pipeline-step">
                <div class="nomor">03 / CERTAINTY FACTOR</div>
                <h3>Uncertainty handling</h3>
                <p>CF pengguna dan CF pakar digabungkan berurutan untuk setiap jenis cheat.</p>
            </div>
            <div class="pipeline-step">
                <div class="nomor">04 / EXPLANATION</div>
                <h3>Traceable output</h3>
                <p>Hasil menampilkan ranking, alasan, jejak hitung, dan sumber ilmiah.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
