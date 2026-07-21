import streamlit as st
import pandas as pd
import plotly.express as px
from modules.sentiment import predict_sentiment
from modules.emotion import predict_emotion
from modules.fake_review import predict_fake_review
from modules.rating_prediction import predict_rating
from modules.aspect_analysis import predict_aspect
from modules.bulk_analysis import (
    read_uploaded_file,
    detect_review_column,
    get_text_like_columns,
    analyze_reviews_bulk,
    build_summary_dashboard,
    to_csv_bytes,
    to_excel_bytes,
)

# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="InsightAI – Customer Feedback Intelligence",
    page_icon="🤖",
    layout="wide",
)

# =========================================================
# Global Styling
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    *, *::before, *::after { box-sizing: border-box; }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(1200px 600px at 80% -10%, rgba(99,102,241,0.10), transparent 60%),
            radial-gradient(1000px 500px at -10% 10%, rgba(37,99,235,0.08), transparent 60%),
            #F8FAFC;
    }

    #MainMenu, header, footer { visibility: hidden; }

    .block-container {
        padding-top: 0 !important;
        padding-bottom: 4rem;
        max-width: 1240px;
    }

    /* ========================================
       KEYFRAME ANIMATIONS
    ======================================== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.96); }
        to   { opacity: 1; transform: scale(1); }
    }
    @keyframes pulseRing {
        0%, 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0.40); }
        50%      { box-shadow: 0 0 0 10px rgba(99,102,241,0); }
    }
    @keyframes starPop {
        0%   { transform: scale(0.5); opacity: 0; }
        70%  { transform: scale(1.2); }
        100% { transform: scale(1);   opacity: 1; }
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes floatParticle {
        0%   { transform: translateY(0) translateX(0); opacity: 0; }
        10%  { opacity: 0.8; }
        90%  { opacity: 0.8; }
        100% { transform: translateY(-120px) translateX(20px); opacity: 0; }
    }
    @keyframes glowPulse {
        0%, 100% { opacity: 0.55; transform: scale(1); }
        50%      { opacity: 0.85; transform: scale(1.06); }
    }
    @keyframes shimmer {
        0%   { background-position: -400px 0; }
        100% { background-position: 400px 0; }
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    @keyframes barFill {
        from { width: 0%; }
    }

    /* ========================================
       HERO SECTION
    ======================================== */
    .hero-section {
        position: relative;
        background: linear-gradient(120deg, #0F172A 0%, #1E3A8A 35%, #4338CA 70%, #6D28D9 100%);
        background-size: 220% 220%;
        animation: gradientShift 14s ease infinite;
        border-radius: 28px;
        padding: 64px 48px 52px 48px;
        text-align: center;
        margin-bottom: 28px;
        overflow: hidden;
        box-shadow: 0 24px 60px rgba(67, 56, 202, 0.28);
    }
    .hero-glow {
        position: absolute;
        width: 420px; height: 420px;
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        animation: glowPulse 7s ease-in-out infinite;
    }
    .hero-glow.g1 { background: rgba(99,102,241,0.55); top: -120px; left: -80px; }
    .hero-glow.g2 { background: rgba(168,85,247,0.45); bottom: -140px; right: -60px; animation-delay: 2s; }
    .hero-particles {
        position: absolute; inset: 0; pointer-events: none; overflow: hidden;
    }
    .particle {
        position: absolute; bottom: -20px;
        width: 6px; height: 6px; border-radius: 50%;
        background: rgba(255,255,255,0.7);
        animation: floatParticle linear infinite;
    }
    .hero-content { position: relative; z-index: 2; }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.25);
        color: #E0E7FF;
        padding: 8px 20px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 28px;
        backdrop-filter: blur(12px);
    }
    .hero-badge .dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #A78BFA;
        box-shadow: 0 0 10px #A78BFA;
        animation: pulseRing 2.2s infinite;
    }
    .hero-logo {
        font-size: 58px;
        font-weight: 900;
        margin: 0 0 14px 0;
        line-height: 1.05;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #FFFFFF 0%, #C7D2FE 50%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-headline {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0 0 12px 0;
        letter-spacing: 0.2px;
    }
    .hero-subtitle {
        font-size: 15.5px;
        font-weight: 500;
        color: rgba(255,255,255,0.72);
        max-width: 620px;
        margin: 0 auto;
        line-height: 1.7;
    }
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 0;
        margin-top: 44px;
        flex-wrap: wrap;
    }
    .hero-stat {
        text-align: center;
        padding: 0 26px;
        position: relative;
    }
    .hero-stat:not(:last-child)::after {
        content: '';
        position: absolute;
        right: 0; top: 50%;
        transform: translateY(-50%);
        width: 1px; height: 40px;
        background: rgba(255,255,255,0.18);
    }
    .hero-stat-num {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
    }
    .hero-stat-label {
        font-size: 11.5px;
        color: rgba(255,255,255,0.65);
        font-weight: 600;
        margin-top: 8px;
        letter-spacing: 0.6px;
        text-transform: uppercase;
    }

    /* ========================================
       TABS — Segmented Control
    ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(12px);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 6px;
        box-shadow: 0 4px 18px rgba(15,23,42,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 11px 22px;
        font-weight: 600;
        font-size: 14px;
        color: #64748B;
        background: transparent;
        border: none;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #FFFFFF;
        color: #1E293B;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4F46E5 0%, #6D28D9 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 18px rgba(79,70,229,0.35) !important;
    }
    .stTabs [data-baseweb="tab-border"] { display: none; }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* ========================================
       INPUT SECTION
    ======================================== */
    .input-card {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(14px);
        border: 1px solid #E2E8F0;
        border-radius: 22px;
        padding: 32px 32px 24px 32px;
        box-shadow: 0 12px 36px rgba(15, 23, 42, 0.07);
        margin-top: 24px;
        position: relative;
        animation: fadeInUp 0.6s ease both;
        animation-delay: 0.1s;
    }
    .input-card-label {
        font-size: 12.5px;
        font-weight: 700;
        color: #6366F1;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 14px;
    }
    .char-counter {
        text-align: right;
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 6px;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 14px !important;
        border: 1.5px solid #E2E8F0 !important;
        background: #F8FAFC !important;
        font-size: 15px !important;
        padding: 16px 18px !important;
        box-shadow: none !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
        font-family: 'Inter', sans-serif !important;
        color: #1E293B !important;
        line-height: 1.6 !important;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border: 1.5px solid #6366F1 !important;
        background: #FFFFFF !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.14) !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #6D28D9 100%);
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: 14px 0;
        font-size: 15px;
        font-weight: 700;
        width: 100%;
        letter-spacing: 0.3px;
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.32);
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 14px 30px rgba(79, 70, 229, 0.42);
        background: linear-gradient(135deg, #4338CA 0%, #5B21B6 100%);
        color: #fff;
    }
    div.stButton > button:active {
        transform: translateY(0) scale(0.99);
    }
    /* Secondary / outline button (Clear / Download) */
    .stDownloadButton > button,
    div.stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #4F46E5 !important;
        border: 1.5px solid #C7D2FE !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover,
    div.stButton > button[kind="secondary"]:hover {
        background: #EEF2FF !important;
        border-color: #6366F1 !important;
        box-shadow: 0 6px 16px rgba(99,102,241,0.14) !important;
        transform: translateY(-2px) !important;
    }

    /* Spinner override */
    .stSpinner > div { border-top-color: #6366F1 !important; }

    /* Upload zone */
    div[data-testid="stFileUploader"] {
        border-radius: 14px !important;
    }
    div[data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #C7D2FE !important;
        border-radius: 14px !important;
        background: #F8FAFC !important;
        transition: all 0.22s ease !important;
    }
    div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #6366F1 !important;
        background: #EEF2FF !important;
        box-shadow: 0 0 0 6px rgba(99,102,241,0.10) !important;
    }

    /* Loading panel */
    .loading-panel {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(14px);
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 28px 30px;
        box-shadow: 0 12px 36px rgba(15,23,42,0.07);
        animation: fadeInUp 0.5s ease both;
    }
    .loading-title {
        font-size: 16px; font-weight: 700; color: #1E293B;
        display: flex; align-items: center; gap: 10px; margin-bottom: 6px;
    }
    .loading-spin {
        width: 18px; height: 18px;
        border: 2.5px solid #E2E8F0;
        border-top-color: #6366F1;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        display: inline-block;
    }
    .loading-status {
        font-size: 13px; color: #6366F1; font-weight: 600;
        margin-top: 10px;
    }

    /* File meta card */
    .file-meta {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 12px;
        margin-top: 18px;
    }
    .file-meta-item {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(10px);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px 16px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .file-meta-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(15,23,42,0.06);
    }
    .file-meta-label {
        font-size: 11px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 4px;
    }
    .file-meta-value {
        font-size: 15px;
        font-weight: 700;
        color: #0F172A;
    }

    /* ========================================
       SECTION HEADERS
    ======================================== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 48px;
        margin-bottom: 18px;
    }
    .section-icon-wrap {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
        border: 1px solid #C7D2FE;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 19px;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(99,102,241,0.12);
    }
    .section-title {
        font-size: 20px;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        line-height: 1.2;
    }
    .section-sub {
        color: #94A3B8;
        font-size: 13px;
        margin: 3px 0 0 0;
        font-weight: 500;
    }

    /* ========================================
       METRIC CARDS (Executive Dashboard)
    ======================================== */
    .metric-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(14px);
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 24px 20px;
        text-align: center;
        box-shadow: 0 6px 22px rgba(15, 23, 42, 0.06);
        transition: transform 0.28s cubic-bezier(0.4,0,0.2,1),
                    box-shadow 0.28s cubic-bezier(0.4,0,0.2,1),
                    border-color 0.28s;
        min-height: 178px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        animation: scaleIn 0.5s ease both;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4F46E5, #A78BFA);
    }
    .metric-card:hover {
        transform: translateY(-7px);
        box-shadow: 0 22px 44px rgba(79, 70, 229, 0.16);
        border-color: #C7D2FE;
    }
    .metric-icon {
        font-size: 32px;
        margin-bottom: 10px;
        line-height: 1;
    }
    .metric-label {
        font-size: 11px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 6px;
    }
    .metric-positive .metric-value { color: #16A34A; }
    .metric-negative .metric-value { color: #DC2626; }
    .metric-warn    .metric-value { color: #D97706; }

    /* Star rating */
    .star-display {
        font-size: 18px;
        margin-bottom: 6px;
        letter-spacing: 2px;
        animation: starPop 0.6s ease both;
    }
    .star-rating-big {
        font-size: 30px;
        font-weight: 800;
        color: #F59E0B;
        line-height: 1;
    }
    .star-rating-label {
        font-size: 11px;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ========================================
       ASPECT ANALYSIS – CARD GRID
    ======================================== */
    .aspect-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
        gap: 14px;
        animation: fadeInUp 0.6s ease both;
    }
    .aspect-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(12px);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px 18px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
        box-shadow: 0 4px 16px rgba(15,23,42,0.05);
        transition: transform 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease;
        animation: scaleIn 0.5s ease both;
    }
    .aspect-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 16px 34px rgba(79,70,229,0.14);
        border-color: #C7D2FE;
    }
    .aspect-card-name {
        font-size: 15px;
        font-weight: 700;
        color: #1E293B;
    }
    .badge-positive {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #DCFCE7;
        color: #15803D;
        padding: 5px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
        border: 1px solid #BBF7D0;
    }
    .badge-negative {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #FEE2E2;
        color: #B91C1C;
        padding: 5px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
        border: 1px solid #FECACA;
    }
    .badge-neutral {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #FEF3C7;
        color: #92400E;
        padding: 5px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
        border: 1px solid #FDE68A;
    }

    /* ========================================
       BUSINESS INSIGHTS
    ======================================== */
    .insight-card {
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 10px;
        font-size: 15px;
        font-weight: 600;
        color: #1E293B;
        display: flex;
        align-items: center;
        gap: 14px;
        border: 1px solid transparent;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
        animation: fadeInUp 0.5s ease both;
    }
    .insight-card:hover {
        transform: translateX(6px);
        box-shadow: 0 10px 24px rgba(15,23,42,0.08);
    }
    .insight-icon-wrap {
        width: 40px;
        height: 40px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 19px;
        flex-shrink: 0;
    }
    .insight-title {
        font-size: 14.5px;
        font-weight: 700;
        margin: 0 0 2px 0;
    }
    .insight-desc {
        font-size: 12.5px;
        font-weight: 400;
        opacity: 0.78;
        margin: 0;
    }

    .insight-success {
        background: linear-gradient(90deg, #F0FDF4, #FFFFFF);
        border-color: #BBF7D0;
        border-left: 4px solid #22C55E;
    }
    .insight-success .insight-icon-wrap { background: #DCFCE7; }
    .insight-success .insight-title     { color: #15803D; }

    .insight-warning {
        background: linear-gradient(90deg, #FFFBEB, #FFFFFF);
        border-color: #FDE68A;
        border-left: 4px solid #F59E0B;
    }
    .insight-warning .insight-icon-wrap { background: #FEF3C7; }
    .insight-warning .insight-title     { color: #92400E; }

    .insight-danger {
        background: linear-gradient(90deg, #FFF1F2, #FFFFFF);
        border-color: #FECDD3;
        border-left: 4px solid #EF4444;
    }
    .insight-danger .insight-icon-wrap { background: #FEE2E2; }
    .insight-danger .insight-title     { color: #991B1B; }

    .insight-info {
        background: linear-gradient(90deg, #EEF2FF, #FFFFFF);
        border-color: #C7D2FE;
        border-left: 4px solid #6366F1;
    }
    .insight-info .insight-icon-wrap { background: #E0E7FF; }
    .insight-info .insight-title     { color: #4338CA; }

    /* ========================================
       EXECUTIVE SUMMARY
    ======================================== */
    .summary-card {
        background: linear-gradient(135deg, rgba(238,242,255,0.95) 0%, rgba(255,255,255,0.95) 100%);
        backdrop-filter: blur(14px);
        border: 1px solid #C7D2FE;
        border-left: 5px solid #6366F1;
        border-radius: 18px;
        padding: 30px 34px;
        box-shadow: 0 12px 36px rgba(99,102,241,0.10);
        animation: fadeInUp 0.6s ease both;
    }
    .summary-heading {
        font-size: 12px;
        font-weight: 700;
        color: #4F46E5;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .summary-body {
        font-size: 15.5px;
        line-height: 1.85;
        color: #1E293B;
        font-weight: 400;
    }
    .summary-body strong {
        color: #4338CA;
        font-weight: 700;
    }
    .summary-highlight {
        background: linear-gradient(120deg, #EEF2FF, #E0E7FF);
        border-radius: 6px;
        padding: 2px 8px;
        font-weight: 700;
        color: #4338CA;
    }

    /* ========================================
       BULK SUMMARY METRICS
    ======================================== */
    .bulk-metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 14px;
        animation: fadeInUp 0.6s ease both;
    }
    .bulk-metric {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(12px);
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 16px;
        text-align: center;
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        animation: scaleIn 0.5s ease both;
    }
    .bulk-metric:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(79,70,229,0.12);
        border-color: #C7D2FE;
    }
    .bulk-metric-icon { font-size: 22px; margin-bottom: 6px; }
    .bulk-metric-value {
        font-size: 20px; font-weight: 800; color: #0F172A; line-height: 1.1;
    }
    .bulk-metric-label {
        font-size: 11px; font-weight: 600; color: #94A3B8;
        text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px;
    }

    /* Chart card wrapper */
    .chart-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(12px);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 8px 8px 4px 8px;
        box-shadow: 0 6px 22px rgba(15,23,42,0.05);
        animation: fadeInUp 0.6s ease both;
    }

    /* Download cards */
    .download-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(12px);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px 20px;
        text-align: center;
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        animation: fadeInUp 0.5s ease both;
    }
    .download-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(79,70,229,0.12);
        border-color: #C7D2FE;
    }
    .download-icon {
        font-size: 30px; margin-bottom: 8px;
    }
    .download-title {
        font-size: 14px; font-weight: 700; color: #1E293B; margin-bottom: 4px;
    }
    .download-desc {
        font-size: 12px; color: #94A3B8; font-weight: 500; margin-bottom: 14px;
    }

    /* ========================================
       FOOTER
    ======================================== */
    .app-footer {
        text-align: center;
        margin-top: 64px;
        padding: 30px 0 16px 0;
        border-top: 1px solid #E2E8F0;
        animation: fadeIn 0.8s ease both;
    }
    .footer-brand {
        font-size: 18px;
        font-weight: 800;
        background: linear-gradient(135deg, #4F46E5 0%, #6D28D9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 6px;
    }
    .footer-tagline {
        font-size: 12.5px; color: #94A3B8; font-weight: 500; margin-bottom: 14px;
    }
    .footer-tech-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .footer-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 999px;
        padding: 5px 13px;
        font-size: 12px;
        font-weight: 600;
        color: #475569;
        transition: all 0.2s ease;
    }
    .footer-chip:hover {
        border-color: #C7D2FE;
        color: #4F46E5;
        transform: translateY(-1px);
    }
    .footer-meta {
        display: flex; justify-content: center; gap: 18px;
        margin-top: 14px; flex-wrap: wrap;
        font-size: 12px; color: #94A3B8; font-weight: 500;
    }
    .footer-meta a { color: #6366F1; text-decoration: none; font-weight: 600; }
    .footer-meta a:hover { text-decoration: underline; }
    .footer-copy {
        color: #94A3B8;
        font-size: 12px;
        margin-top: 12px;
    }
    .footer-copy b {
        color: #6366F1;
    }

    /* ========================================
       PROGRESS BAR STYLING
    ======================================== */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4F46E5, #A78BFA) !important;
        border-radius: 99px !important;
    }

    /* ========================================
       DATAFRAME
    ======================================== */
    .stDataFrame {
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 6px 22px rgba(15,23,42,0.05);
    }

    /* ========================================
       RESPONSIVE
    ======================================== */
    @media (max-width: 768px) {
        .hero-logo { font-size: 40px; }
        .hero-headline { font-size: 18px; }
        .hero-section { padding: 44px 24px 36px 24px; }
        .hero-stat { padding: 0 14px; }
        .hero-stat:not(:last-child)::after { display: none; }
        .input-card { padding: 24px 20px 18px 20px; }
        .section-title { font-size: 18px; }
        .summary-card { padding: 24px 22px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================================================================
# HERO SECTION
# ================================================================
# Floating particles
particles_html = '<div class="hero-particles">'
for i in range(18):
    left = (i * 5.5) % 100
    dur = 7 + (i % 5)
    delay = (i * 0.6) % 6
    size = 4 + (i % 3)
    particles_html += (
        f'<span class="particle" style="left:{left}%; '
        f'width:{size}px; height:{size}px; '
        f'animation-duration:{dur}s; animation-delay:{delay}s;"></span>'
    )
particles_html += '</div>'

st.markdown(
    f"""
    <div class="hero-section">
        <div class="hero-glow g1"></div>
        <div class="hero-glow g2"></div>
        {particles_html}
        <div class="hero-content">
            <div class="hero-badge"><span class="dot"></span> AI-POWERED · FEEDBACK INTELLIGENCE</div>
            <p class="hero-logo">InsightAI</p>
            <p class="hero-headline">Understand every customer review at AI speed</p>
            <p class="hero-subtitle">
                Paste a review or upload thousands — get sentiment, emotion, authenticity,
                predicted rating, aspect-level breakdown, business insights, and an
                AI-generated executive summary in one premium dashboard.
            </p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-num">5</div>
                    <div class="hero-stat-label">AI Models</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">Real-Time</div>
                    <div class="hero-stat-label">Analysis</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">Bulk</div>
                    <div class="hero-stat-label">CSV Analysis</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">NLP</div>
                    <div class="hero-stat-label">Powered</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">Fast</div>
                    <div class="hero-stat-label">Processing</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ================================================================
# INPUT SECTION — Tabs
# ================================================================
tab_single, tab_bulk = st.tabs(["📝  Single Review Analysis", "📂  Bulk Review Analysis"])

# ================================================================
# TAB 1: SINGLE REVIEW ANALYSIS
# ================================================================
with tab_single:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="input-card-label">📝 Paste Customer Review</div>', unsafe_allow_html=True)

    review = st.text_area(
        "Customer Review",
        height=170,
        placeholder='e.g. "The product quality is amazing but delivery was very late and the packaging arrived damaged. Quite disappointed."',
        label_visibility="collapsed"
    )

    st.markdown(
        f'<div class="char-counter">{len(review)} characters</div>',
        unsafe_allow_html=True
    )

    col_btn, col_clear, col_pad = st.columns([1, 1, 2])
    with col_btn:
        analyze_clicked = st.button("🚀  Analyze Review")
    with col_clear:
        clear_clicked = st.button("✕  Clear", key="clear_single")

    st.markdown('</div>', unsafe_allow_html=True)

    if clear_clicked:
        review = ""
        st.rerun()

    # ============================================================
    # ANALYSIS LOGIC
    # ============================================================
    if analyze_clicked:
        if review.strip() == "":
            st.warning("⚠️ Please enter a customer review before analyzing.")
        else:
            progress_placeholder = st.empty()
            status_placeholder = st.empty()

            with progress_placeholder:
                prog = st.progress(0)
            with status_placeholder:
                st.markdown(
                    """
                    <div class="loading-panel">
                        <div class="loading-title"><span class="loading-spin"></span> AI Processing...</div>
                        <div class="loading-status">Initializing models</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            prog.progress(10)
            status_placeholder.markdown(
                """
                <div class="loading-panel">
                    <div class="loading-title"><span class="loading-spin"></span> AI Processing...</div>
                    <div class="loading-status">Running Sentiment model...</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # ── Model calls (unchanged) ──────────────────────────
            sentiment = predict_sentiment(review)
            prog.progress(30)
            status_placeholder.markdown(
                """
                <div class="loading-panel">
                    <div class="loading-title"><span class="loading-spin"></span> AI Processing...</div>
                    <div class="loading-status">Running Emotion model...</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            emotion = predict_emotion(review)
            prog.progress(50)
            status_placeholder.markdown(
                """
                <div class="loading-panel">
                    <div class="loading-title"><span class="loading-spin"></span> AI Processing...</div>
                    <div class="loading-status">Running Authenticity model...</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            fake_review = predict_fake_review(review)
            prog.progress(65)
            status_placeholder.markdown(
                """
                <div class="loading-panel">
                    <div class="loading-title"><span class="loading-spin"></span> AI Processing...</div>
                    <div class="loading-status">Running Rating model...</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            rating = predict_rating(review)
            prog.progress(80)
            status_placeholder.markdown(
                """
                <div class="loading-panel">
                    <div class="loading-title"><span class="loading-spin"></span> AI Processing...</div>
                    <div class="loading-status">Generating Insights...</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            aspect = predict_aspect(review)
            prog.progress(100)

            progress_placeholder.empty()
            status_placeholder.empty()

            # ── Derived helpers (unchanged) ──────────────────────
            emoji_map = {
                "Happy": "😊", "Sad": "😢",
                "Angry": "😡", "Frustrated": "😤",
                "Satisfied": "😌"
            }
            emotion_icon = emoji_map.get(emotion, "😌")
            review_lower = review.lower()

            if fake_review == "Genuine":
                auth_value = "✅ Genuine"
                auth_color = "metric-positive"
            elif fake_review == "Fake":
                auth_value = "⚠️ Fake"
                auth_color = "metric-negative"
            else:
                auth_value = "🔍 Unknown"
                auth_color = ""

            sent_color = (
                "metric-positive" if sentiment == "Positive" else
                "metric-negative" if sentiment == "Negative" else ""
            )

            # ── Build aspect rows (unchanged) ─────────────────────
            if aspect:
                aspect_rows = aspect
            else:
                aspect_rows = [
                    ("Quality",          "Positive"),
                    ("Packaging",        "Negative"),
                    ("Delivery",         "Negative"),
                    ("Price",            "Positive"),
                    ("Customer Service", "Positive"),
                ]

            total_aspects = len(aspect_rows)
            pos_count = sum(1 for _, s in aspect_rows if s.lower() == "positive")
            neu_count = sum(1 for _, s in aspect_rows if s.lower() == "neutral")
            neg_count = total_aspects - pos_count - neu_count

            # ============================================================
            # SECTION: EXECUTIVE DASHBOARD (METRICS ROW)
            # ============================================================
            st.markdown(
                """
                <div class="section-header">
                    <div class="section-icon-wrap">📈</div>
                    <div>
                        <p class="section-title">Executive Dashboard</p>
                        <p class="section-sub">Snapshot of all detected signals from this review.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            rating_display = f"{rating}/5" if rating is not None else "N/A"

            m1, m2, m3, m4, m5 = st.columns(5)
            with m1:
                st.markdown(
                    f"""
                    <div class="metric-card {sent_color}">
                        <div class="metric-icon">😊</div>
                        <div class="metric-label">Sentiment</div>
                        <div class="metric-value">{sentiment}</div>
                        <div class="metric-sub">Overall tone</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-icon">{emotion_icon}</div>
                        <div class="metric-label">Emotion</div>
                        <div class="metric-value">{emotion}</div>
                        <div class="metric-sub">Detected mood</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m3:
                st.markdown(
                    f"""
                    <div class="metric-card {auth_color}">
                        <div class="metric-icon">🛡️</div>
                        <div class="metric-label">Authenticity</div>
                        <div class="metric-value">{auth_value}</div>
                        <div class="metric-sub">Review validity</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m4:
                if rating is not None:
                    star_filled = "⭐" * int(rating)
                    star_empty = "☆" * (5 - int(rating))
                    rating_html = f"""
                    <div class="star-display">{star_filled}{star_empty}</div>
                    <div class="star-rating-big">{rating}/5</div>
                    <div class="star-rating-label">Predicted Rating</div>
                    """
                else:
                    rating_html = '<div class="metric-value">N/A</div><div class="metric-sub">Coming Soon</div>'
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-icon">⭐</div>
                        <div class="metric-label">Rating</div>
                        {rating_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m5:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-icon">🔍</div>
                        <div class="metric-label">Aspects</div>
                        <div class="metric-value">{total_aspects}</div>
                        <div class="metric-sub">Detected topics</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ============================================================
            # SECTION: ASPECT ANALYSIS
            # ============================================================
            st.markdown(
                f"""
                <div class="section-header">
                    <div class="section-icon-wrap">🔍</div>
                    <div>
                        <p class="section-title">Aspect Analysis</p>
                        <p class="section-sub">Breakdown of sentiment by product aspect &nbsp;|&nbsp;
                            <span style="color:#16A34A;font-weight:700;">{pos_count} Positive</span>
                            &nbsp;·&nbsp;
                            <span style="color:#DC2626;font-weight:700;">{neg_count} Negative</span>
                            &nbsp;·&nbsp;
                            <span style="color:#D97706;font-weight:700;">{neu_count} Neutral</span>
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            aspect_cards_html = '<div class="aspect-grid">'
            for name, status in aspect_rows:
                sl = status.lower()
                if sl == "positive":
                    badge = '<span class="badge-positive">✓ Positive</span>'
                elif sl == "negative":
                    badge = '<span class="badge-negative">✗ Negative</span>'
                else:
                    badge = f'<span class="badge-neutral">~ {status}</span>'

                aspect_cards_html += (
                    f'<div class="aspect-card">'
                    f'<div class="aspect-card-name">{name}</div>'
                    f'{badge}'
                    f'</div>'
                )
            aspect_cards_html += "</div>"

            st.markdown(aspect_cards_html, unsafe_allow_html=True)

            # ============================================================
            # SECTION: BUSINESS INSIGHTS
            # ============================================================
            st.markdown(
                """
                <div class="section-header">
                    <div class="section-icon-wrap">💡</div>
                    <div>
                        <p class="section-title">AI Business Insights</p>
                        <p class="section-sub">Actionable recommendations generated from the analysis.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Build insights list (unchanged logic)
            insights = []

            if sentiment == "Positive":
                insights.append(("success", "✔️", "Maintain Product Quality",
                                 "Customers are responding positively — keep up the standard."))
            elif sentiment == "Negative":
                insights.append(("danger", "🚨", "Address Customer Dissatisfaction",
                                 "Negative sentiment detected — immediate action recommended."))

            if emotion in ("Angry", "Frustrated"):
                insights.append(("danger", "😡", "Improve Customer Experience",
                                 "Strong negative emotion detected. Review touchpoints urgently."))
            elif emotion == "Sad":
                insights.append(("warning", "😢", "Customer Expectations Not Met",
                                 "Customer seems disappointed. Consider follow-up support."))

            if "delivery" in review_lower or "late" in review_lower:
                insights.append(("warning", "🚚", "Improve Delivery Speed",
                                 "Delivery issues mentioned. Optimize your logistics pipeline."))
            if "packaging" in review_lower or "damaged" in review_lower:
                insights.append(("warning", "📦", "Improve Packaging Standards",
                                 "Packaging concerns noted. Review material and handling protocols."))
            if "price" in review_lower or "expensive" in review_lower:
                insights.append(("success", "💰", "Customers Appreciate Pricing",
                                 "Pricing perception is positive — maintain competitive rates."))

            if not insights:
                insights.append(("info", "ℹ️", "No Strong Signals Detected",
                                 "The review does not indicate specific actionable issues."))

            for kind, icon, title, desc in insights:
                css_class = f"insight-{kind}"
                st.markdown(
                    f"""
                    <div class="insight-card {css_class}">
                        <div class="insight-icon-wrap">{icon}</div>
                        <div>
                            <p class="insight-title">{title}</p>
                            <p class="insight-desc">{desc}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ============================================================
            # SECTION: EXECUTIVE SUMMARY
            # ============================================================
            st.markdown(
                """
                <div class="section-header">
                    <div class="section-icon-wrap">📝</div>
                    <div>
                        <p class="section-title">Executive Summary</p>
                        <p class="section-sub">AI-generated narrative report for stakeholders.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Build summary (unchanged logic)
            sentiment_phrase = {
                "Positive": "positive",
                "Negative": "negative",
                "Neutral":  "neutral"
            }.get(sentiment, sentiment.lower() if isinstance(sentiment, str) else "mixed")

            summary_parts = [
                f"Overall customer experience is <span class='summary-highlight'>{sentiment_phrase}</span>,"
                f" with a detected emotion of <span class='summary-highlight'>{emotion}</span>."
            ]

            if "delivery" in review_lower or "late" in review_lower or "packaging" in review_lower or "damaged" in review_lower:
                summary_parts.append(
                    "The customer appreciates the <strong>product quality</strong> but is dissatisfied "
                    "with <strong>delivery speed</strong> and <strong>packaging integrity</strong>."
                )
                summary_parts.append(
                    "The company should prioritize improving its <strong>logistics pipeline</strong> "
                    "and packaging protocols while maintaining current product quality standards."
                )
            else:
                summary_parts.append(
                    "The feedback highlights the customer's overall experience with the product and "
                    "provides a baseline signal for ongoing quality improvement."
                )

            if rating is not None:
                summary_parts.append(
                    f"The AI predicts a <strong>{rating}/5 star rating</strong> based on the review content."
                )

            if fake_review:
                summary_parts.append(
                    f"The review has been classified as <strong>{fake_review}</strong> by the authenticity model."
                )

            summary_body = " ".join(summary_parts)

            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-heading">📝 AI-GENERATED EXECUTIVE SUMMARY</div>
                    <div class="summary-body">{summary_body}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ================================================================
# TAB 2: BULK REVIEW ANALYSIS
# ================================================================
with tab_bulk:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="input-card-label">📂 Upload Customer Reviews (CSV / XLSX)</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload file",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        try:
            bulk_df = read_uploaded_file(uploaded_file)
        except ValueError as exc:
            st.error(f"⚠️ {exc}")
            bulk_df = None

        if bulk_df is not None:
            detected_col = detect_review_column(bulk_df)
            text_cols = get_text_like_columns(bulk_df)

            if detected_col is not None and detected_col not in text_cols:
                text_cols = [detected_col] + text_cols

            if detected_col is not None:
                default_index = text_cols.index(detected_col) if detected_col in text_cols else 0
            else:
                default_index = 0

            # File meta card
            st.markdown(
                f"""
                <div class="file-meta">
                    <div class="file-meta-item">
                        <div class="file-meta-label">Filename</div>
                        <div class="file-meta-value">{uploaded_file.name}</div>
                    </div>
                    <div class="file-meta-item">
                        <div class="file-meta-label">Rows</div>
                        <div class="file-meta-value">{len(bulk_df)}</div>
                    </div>
                    <div class="file-meta-item">
                        <div class="file-meta-label">Columns</div>
                        <div class="file-meta-value">{len(bulk_df.columns)}</div>
                    </div>
                    <div class="file-meta-item">
                        <div class="file-meta-label">Detected Review Column</div>
                        <div class="file-meta-value">{detected_col if detected_col else 'None'}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if not text_cols:
                st.error(
                    "⚠️ No suitable text column was found in the uploaded file. "
                    "Please make sure it contains a column with customer reviews "
                    "(e.g. 'review', 'reviewText', 'feedback', 'comments')."
                )
            else:
                st.markdown(
                    '<div class="input-card-label" style="margin-top:20px;">'
                    '🧭 Select the Review Column</div>',
                    unsafe_allow_html=True
                )
                review_column = st.selectbox(
                    "Review column",
                    options=text_cols,
                    index=default_index,
                    label_visibility="collapsed"
                )

                run_bulk_clicked = st.button("🚀  Analyze Bulk Reviews")

                if run_bulk_clicked:
                    non_empty = bulk_df[review_column].notna() & (
                        bulk_df[review_column].astype(str).str.strip() != ""
                    )
                    if non_empty.sum() == 0:
                        st.warning("⚠️ No valid (non-empty) reviews were found in the selected column.")
                    else:
                        progress_placeholder = st.empty()
                        status_placeholder = st.empty()

                        with progress_placeholder:
                            bulk_prog = st.progress(0)
                        with status_placeholder:
                            st.markdown(
                                """
                                <div class="loading-panel">
                                    <div class="loading-title"><span class="loading-spin"></span> AI Processing...</div>
                                    <div class="loading-status">Running AI models on all reviews...</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        total_rows = int(non_empty.sum())

                        def _update_bulk_progress(done, total):
                            pct = int(done / total * 100) if total else 100
                            bulk_prog.progress(pct)
                            status_placeholder.markdown(
                                f"""
                                <div class="loading-panel">
                    <div class="loading-title"><span class="loading-spin"></span> AI Processing...</div>
                    <div class="loading-status">Processed {done}/{total} reviews...</div>
                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        results_df = analyze_reviews_bulk(
                            bulk_df, review_column,
                            progress_callback=_update_bulk_progress
                        )

                        progress_placeholder.empty()
                        status_placeholder.empty()

                        # ============================================================
                        # SECTION: SUMMARY METRICS
                        # ============================================================
                        summary = build_summary_dashboard(results_df)

                        st.markdown(
                            """
                            <div class="section-header">
                                <div class="section-icon-wrap">📈</div>
                                <div>
                                    <p class="section-title">Summary Metrics</p>
                                    <p class="section-sub">Aggregated insights across all uploaded reviews.</p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"""
                            <div class="bulk-metric-grid">
                                <div class="bulk-metric">
                                    <div class="bulk-metric-icon">📦</div>
                                    <div class="bulk-metric-value">{summary['total_reviews']}</div>
                                    <div class="bulk-metric-label">Total Reviews</div>
                                </div>
                                <div class="bulk-metric">
                                    <div class="bulk-metric-icon">😊</div>
                                    <div class="bulk-metric-value">{summary['positive_reviews']}</div>
                                    <div class="bulk-metric-label">Positive ({summary['positive_pct']}%)</div>
                                </div>
                                <div class="bulk-metric">
                                    <div class="bulk-metric-icon">😞</div>
                                    <div class="bulk-metric-value">{summary['negative_reviews']}</div>
                                    <div class="bulk-metric-label">Negative ({summary['negative_pct']}%)</div>
                                </div>
                                <div class="bulk-metric">
                                    <div class="bulk-metric-icon">😐</div>
                                    <div class="bulk-metric-value">{summary.get('neutral_reviews', summary['total_reviews'] - summary['positive_reviews'] - summary['negative_reviews'])}</div>
                                    <div class="bulk-metric-label">Neutral</div>
                                </div>
                                <div class="bulk-metric">
                                    <div class="bulk-metric-icon">⭐</div>
                                    <div class="bulk-metric-value">{summary['average_rating']}</div>
                                    <div class="bulk-metric-label">Average Rating</div>
                                </div>
                                <div class="bulk-metric">
                                    <div class="bulk-metric-icon">✅</div>
                                    <div class="bulk-metric-value">{summary['genuine_pct']}%</div>
                                    <div class="bulk-metric-label">Genuine Reviews</div>
                                </div>
                                <div class="bulk-metric">
                                    <div class="bulk-metric-icon">⚠️</div>
                                    <div class="bulk-metric-value">{summary['fake_pct']}%</div>
                                    <div class="bulk-metric-label">Fake Reviews</div>
                                </div>
                                <div class="bulk-metric">
                                    <div class="bulk-metric-icon">🎭</div>
                                    <div class="bulk-metric-value">{summary['most_common_emotion']}</div>
                                    <div class="bulk-metric-label">Average Emotion</div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Top aspects row
                        col_a, col_b, col_c, col_d = st.columns(4)
                        with col_a:
                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-icon">🎭</div>
                                    <div class="metric-label">Most Common Emotion</div>
                                    <div class="metric-value">{summary['most_common_emotion']}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        with col_b:
                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-icon">🔍</div>
                                    <div class="metric-label">Most Mentioned Aspect</div>
                                    <div class="metric-value">{summary['most_mentioned_aspect']}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        with col_c:
                            st.markdown(
                                f"""
                                <div class="metric-card metric-positive">
                                    <div class="metric-icon">👍</div>
                                    <div class="metric-label">Top Positive Aspect</div>
                                    <div class="metric-value">{summary['top_positive_aspect']}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        with col_d:
                            st.markdown(
                                f"""
                                <div class="metric-card metric-negative">
                                    <div class="metric-icon">👎</div>
                                    <div class="metric-label">Top Negative Aspect</div>
                                    <div class="metric-value">{summary['top_negative_aspect']}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        # ============================================================
                        # SECTION: INTERACTIVE DATAFRAME
                        # ============================================================
                        st.markdown(
                            """
                            <div class="section-header">
                                <div class="section-icon-wrap">📋</div>
                                <div>
                                    <p class="section-title">Bulk Analysis Results</p>
                                    <p class="section-sub">AI-generated insights for every uploaded review. Use the controls to search, sort, and filter.</p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.dataframe(
                            results_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Review": st.column_config.TextColumn("Review", width="large"),
                            }
                        )

                        # ============================================================
                        # SECTION: VISUALIZATIONS
                        # ============================================================
                        st.markdown(
                            """
                            <div class="section-header">
                                <div class="section-icon-wrap">📊</div>
                                <div>
                                    <p class="section-title">Visual Insights</p>
                                    <p class="section-sub">Charts summarizing sentiment, emotion, aspects, and ratings.</p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        chart_col1, chart_col2 = st.columns(2)

                        with chart_col1:
                            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                            sentiment_counts = results_df["Sentiment"].value_counts().reset_index()
                            sentiment_counts.columns = ["Sentiment", "Count"]
                            fig_sentiment = px.bar(
                                sentiment_counts, x="Sentiment", y="Count",
                                title="Sentiment Distribution",
                                color="Sentiment",
                                color_discrete_map={
                                    "Positive": "#16A34A",
                                    "Negative": "#DC2626",
                                    "Neutral": "#94A3B8"
                                }
                            )
                            fig_sentiment.update_layout(
                                plot_bgcolor="#FFFFFF",
                                paper_bgcolor="#FFFFFF",
                                font=dict(family="Inter", size=12, color="#475569"),
                                margin=dict(l=10, r=10, t=40, b=10),
                                showlegend=False
                            )
                            st.plotly_chart(fig_sentiment, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                        with chart_col2:
                            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                            emotion_counts = results_df["Emotion"].value_counts().reset_index()
                            emotion_counts.columns = ["Emotion", "Count"]
                            fig_emotion = px.pie(
                                emotion_counts, names="Emotion", values="Count",
                                title="Emotion Distribution",
                                color_discrete_sequence=px.colors.sequential.Blues_r
                            )
                            fig_emotion.update_layout(
                                plot_bgcolor="#FFFFFF",
                                paper_bgcolor="#FFFFFF",
                                font=dict(family="Inter", size=12, color="#475569"),
                                margin=dict(l=10, r=10, t=40, b=10),
                                showlegend=True
                            )
                            st.plotly_chart(fig_emotion, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                        chart_col3, chart_col4 = st.columns(2)

                        with chart_col3:
                            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                            aspect_totals = summary.get("aspect_total_counts", {})
                            if aspect_totals:
                                aspect_df = pd.DataFrame(
                                    list(aspect_totals.items()), columns=["Aspect", "Mentions"]
                                ).sort_values("Mentions", ascending=False).head(10)
                                fig_aspects = px.bar(
                                    aspect_df, x="Aspect", y="Mentions",
                                    title="Top 10 Aspects",
                                    color_discrete_sequence=["#6366F1"]
                                )
                                fig_aspects.update_layout(
                                    plot_bgcolor="#FFFFFF",
                                    paper_bgcolor="#FFFFFF",
                                    font=dict(family="Inter", size=12, color="#475569"),
                                    margin=dict(l=10, r=10, t=40, b=10),
                                    showlegend=False
                                )
                                st.plotly_chart(fig_aspects, use_container_width=True)
                            else:
                                st.info("No aspects were detected across the uploaded reviews.")
                            st.markdown('</div>', unsafe_allow_html=True)

                        with chart_col4:
                            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                            rating_series = pd.to_numeric(results_df["Rating"], errors="coerce").dropna()
                            if not rating_series.empty:
                                fig_rating = px.histogram(
                                    rating_series, nbins=5,
                                    title="Rating Distribution",
                                    labels={"value": "Rating"},
                                    color_discrete_sequence=["#F59E0B"]
                                )
                                fig_rating.update_layout(
                                    plot_bgcolor="#FFFFFF",
                                    paper_bgcolor="#FFFFFF",
                                    font=dict(family="Inter", size=12, color="#475569"),
                                    margin=dict(l=10, r=10, t=40, b=10),
                                    showlegend=False
                                )
                                st.plotly_chart(fig_rating, use_container_width=True)
                            else:
                                st.info("No ratings available to display.")
                            st.markdown('</div>', unsafe_allow_html=True)

                        # ============================================================
                        # SECTION: DOWNLOAD
                        # ============================================================
                        st.markdown(
                            """
                            <div class="section-header">
                                <div class="section-icon-wrap">⬇️</div>
                                <div>
                                    <p class="section-title">Download Results</p>
                                    <p class="section-sub">Export the processed data for offline use.</p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        dl_col1, dl_col2 = st.columns(2)
                        with dl_col1:
                            st.markdown(
                                """
                                <div class="download-card">
                                    <div class="download-icon">📄</div>
                                    <div class="download-title">CSV Export</div>
                                    <div class="download-desc">Comma-separated values for spreadsheets & pipelines</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.download_button(
                                "⬇️  Download CSV",
                                data=to_csv_bytes(results_df),
                                file_name="bulk_review_analysis.csv",
                                mime="text/csv"
                            )
                        with dl_col2:
                            st.markdown(
                                """
                                <div class="download-card">
                                    <div class="download-icon">📊</div>
                                    <div class="download-title">Excel Export</div>
                                    <div class="download-desc">Formatted workbook for reports & sharing</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.download_button(
                                "⬇️  Download Excel",
                                data=to_excel_bytes(results_df),
                                file_name="bulk_review_analysis.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )

# ================================================================
# FOOTER
# ================================================================
st.markdown(
    """
    <div class="app-footer">
        <div class="footer-brand">InsightAI</div>
        <div class="footer-tagline">Customer Feedback Intelligence Platform</div>
        <div class="footer-tech-row">
            <span class="footer-chip">🐍 Python</span>
            <span class="footer-chip">🎈 Streamlit</span>
            <span class="footer-chip">🤖 Scikit-learn</span>
            <span class="footer-chip">🧠 NLTK</span>
            <span class="footer-chip">⚙️ Joblib</span>
        </div>
        <div class="footer-meta">
            <span>Version 2.0</span>
            <span>·</span>
            <a href="https://github.com/ka0913560-hub/InsightAI" target="_blank">GitHub</a>
            <span>·</span>
            <span>Made with AI</span>
        </div>
        <p class="footer-copy">
            <b>InsightAI</b> · Built with Python, Streamlit, Scikit-learn, NLTK & Joblib
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
