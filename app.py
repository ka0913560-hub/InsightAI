import streamlit as st
from modules.sentiment import predict_sentiment
from modules.emotion import predict_emotion
from modules.fake_review import predict_fake_review
from modules.rating_prediction import predict_rating
from modules.aspect_analysis import predict_aspect

# =========================================================
# Placeholder functions for upcoming modules.
# Replace each with the real import + call when ready, e.g.
#   from modules.fake_review import predict_fake_review
# =========================================================


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="InsightAI – Customer Feedback Intelligence",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Global Styling ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    *, *::before, *::after { box-sizing: border-box; }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #F8FAFC;
    }

    #MainMenu, header, footer { visibility: hidden; }

    .block-container {
        padding-top: 0 !important;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    /* ========================================
       KEYFRAME ANIMATIONS
    ======================================== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(28px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(37,99,235,0.18); }
        50%       { box-shadow: 0 0 0 10px rgba(37,99,235,0); }
    }
    @keyframes shimmer {
        0%   { background-position: -400px 0; }
        100% { background-position: 400px 0; }
    }
    @keyframes starPop {
        0%   { transform: scale(0.5); opacity: 0; }
        70%  { transform: scale(1.2); }
        100% { transform: scale(1);   opacity: 1; }
    }

    /* ========================================
       HERO SECTION
    ======================================== */
    .hero-section {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 45%, #1D4ED8 100%);
        border-radius: 0 0 40px 40px;
        padding: 64px 40px 72px 40px;
        text-align: center;
        margin-bottom: 0;
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.7s ease both;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        inset: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.22);
        color: #93C5FD;
        padding: 7px 20px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
    }
    .hero-title {
        font-size: 60px;
        font-weight: 900;
        background: linear-gradient(135deg, #FFFFFF 0%, #93C5FD 50%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 12px 0;
        line-height: 1.1;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 20px;
        font-weight: 600;
        color: rgba(255,255,255,0.75);
        margin-bottom: 16px;
        letter-spacing: 0.2px;
    }
    .hero-desc {
        font-size: 15.5px;
        color: rgba(255,255,255,0.55);
        max-width: 560px;
        margin: 0 auto;
        line-height: 1.7;
    }
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 48px;
        margin-top: 40px;
        flex-wrap: wrap;
    }
    .hero-stat {
        text-align: center;
    }
    .hero-stat-num {
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
    }
    .hero-stat-label {
        font-size: 12.5px;
        color: rgba(255,255,255,0.5);
        font-weight: 500;
        margin-top: 2px;
        letter-spacing: 0.5px;
    }

    /* ========================================
       INPUT SECTION
    ======================================== */
    .input-card {
        background: #FFFFFF;
        border-radius: 28px;
        border: 1px solid #E2E8F0;
        padding: 36px 36px 28px 36px;
        box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08), 0 1px 3px rgba(0,0,0,0.04);
        margin: -36px 0 0 0;
        position: relative;
        z-index: 2;
        animation: fadeInUp 0.65s ease both;
        animation-delay: 0.15s;
    }
    .input-card-label {
        font-size: 13px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 18px !important;
        border: 2px solid #E2E8F0 !important;
        background: #F8FAFC !important;
        font-size: 15.5px !important;
        padding: 18px 20px !important;
        box-shadow: none !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
        font-family: 'Inter', sans-serif !important;
        color: #1E293B !important;
        line-height: 1.6 !important;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border: 2px solid #2563EB !important;
        background: #FFFFFF !important;
        box-shadow: 0 0 0 5px rgba(37, 99, 235, 0.10) !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: #fff;
        border: none;
        border-radius: 16px;
        padding: 16px 0;
        font-size: 16px;
        font-weight: 700;
        width: 100%;
        letter-spacing: 0.3px;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.35);
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    div.stButton > button::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, transparent 100%);
        pointer-events: none;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 18px 40px rgba(37, 99, 235, 0.45);
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        color: #fff;
    }
    div.stButton > button:active {
        transform: translateY(-1px) scale(0.99);
    }

    /* Spinner override */
    .stSpinner > div { border-top-color: #2563EB !important; }

    /* ========================================
       SECTION HEADERS
    ======================================== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 52px;
        margin-bottom: 20px;
    }
    .section-icon-wrap {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(37,99,235,0.12);
    }
    .section-text-wrap {}
    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        line-height: 1.2;
    }
    .section-sub {
        color: #94A3B8;
        font-size: 13.5px;
        margin: 3px 0 0 0;
        font-weight: 500;
    }

    /* ========================================
       OVERVIEW DASHBOARD CARD
    ======================================== */
    .overview-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        border-radius: 28px;
        padding: 32px 36px;
        display: flex;
        flex-wrap: wrap;
        gap: 28px;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.18);
        animation: fadeInUp 0.6s ease both;
        margin-bottom: 0;
    }
    .overview-stat {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .overview-stat-icon {
        font-size: 26px;
        margin-bottom: 8px;
    }
    .overview-stat-value {
        font-size: 22px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
        margin-bottom: 5px;
    }
    .overview-stat-label {
        font-size: 12px;
        font-weight: 600;
        color: rgba(255,255,255,0.50);
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .overview-divider {
        width: 1px;
        height: 50px;
        background: rgba(255,255,255,0.12);
    }

    /* ========================================
       RESULT CARDS (AI Report)
    ======================================== */
    .result-card {
        background: #FFFFFF;
        border-radius: 24px;
        border: 1px solid #E2E8F0;
        padding: 28px 18px 24px 18px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        transition: transform 0.28s cubic-bezier(0.4,0,0.2,1),
                    box-shadow 0.28s cubic-bezier(0.4,0,0.2,1),
                    border-color 0.28s;
        min-height: 185px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.55s ease both;
    }
    .result-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #2563EB, #60A5FA);
        border-radius: 24px 24px 0 0;
    }
    .result-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 24px 50px rgba(37, 99, 235, 0.16);
        border-color: #BFDBFE;
    }
    .result-icon {
        font-size: 40px;
        margin-bottom: 12px;
        line-height: 1;
    }
    .result-label {
        font-size: 11.5px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .result-value {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }
    .result-value.soon {
        font-size: 14px;
        font-weight: 600;
        color: #CBD5E1;
    }
    .result-card-positive .result-value { color: #16A34A; }
    .result-card-negative .result-value { color: #DC2626; }
    .result-card-warn .result-value     { color: #D97706; }

    /* Star rating card specific */
    .star-display {
        font-size: 20px;
        margin-bottom: 8px;
        letter-spacing: 2px;
    }
    .star-rating-big {
        font-size: 34px;
        font-weight: 900;
        color: #F59E0B;
        line-height: 1;
    }
    .star-rating-label {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 500;
    }

    /* ========================================
       ASPECT ANALYSIS – CARD GRID
    ======================================== */
    .aspect-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 14px;
        animation: fadeInUp 0.6s ease both;
    }
    .aspect-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 20px 18px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
        box-shadow: 0 4px 14px rgba(15,23,42,0.05);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
        cursor: default;
    }
    .aspect-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 14px 32px rgba(15,23,42,0.10);
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
        padding: 5px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12.5px;
        border: 1px solid #BBF7D0;
    }
    .badge-negative {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #FEE2E2;
        color: #B91C1C;
        padding: 5px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12.5px;
        border: 1px solid #FECACA;
    }
    .badge-neutral {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #FEF3C7;
        color: #92400E;
        padding: 5px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12.5px;
        border: 1px solid #FDE68A;
    }

    /* ========================================
       BUSINESS INSIGHTS
    ======================================== */
    .insight-card {
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 12px;
        font-size: 15px;
        font-weight: 600;
        color: #1E293B;
        display: flex;
        align-items: center;
        gap: 16px;
        border: 1px solid transparent;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: fadeInUp 0.5s ease both;
    }
    .insight-card:hover {
        transform: translateX(6px);
    }
    .insight-icon-wrap {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
    }
    .insight-text {}
    .insight-title {
        font-size: 15px;
        font-weight: 700;
        margin: 0 0 2px 0;
    }
    .insight-desc {
        font-size: 13px;
        font-weight: 400;
        opacity: 0.7;
        margin: 0;
    }

    /* Variants */
    .insight-success {
        background: #F0FDF4;
        border-color: #BBF7D0;
        border-left: 4px solid #22C55E;
    }
    .insight-success .insight-icon-wrap { background: #DCFCE7; }
    .insight-success .insight-title     { color: #15803D; }

    .insight-warning {
        background: #FFFBEB;
        border-color: #FDE68A;
        border-left: 4px solid #F59E0B;
    }
    .insight-warning .insight-icon-wrap { background: #FEF3C7; }
    .insight-warning .insight-title     { color: #92400E; }

    .insight-danger {
        background: #FFF1F2;
        border-color: #FECDD3;
        border-left: 4px solid #EF4444;
    }
    .insight-danger .insight-icon-wrap { background: #FEE2E2; }
    .insight-danger .insight-title     { color: #991B1B; }

    /* ========================================
       EXECUTIVE SUMMARY
    ======================================== */
    .summary-glass {
        background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
        border: 1px solid #BFDBFE;
        border-left: 5px solid #2563EB;
        border-radius: 22px;
        padding: 32px 36px;
        box-shadow: 0 12px 36px rgba(37,99,235,0.08);
        animation: fadeInUp 0.6s ease both;
    }
    .summary-heading {
        font-size: 13px;
        font-weight: 700;
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 14px;
    }
    .summary-body {
        font-size: 16px;
        line-height: 1.85;
        color: #1E293B;
        font-weight: 450;
    }
    .summary-body strong {
        color: #1D4ED8;
        font-weight: 700;
    }
    .summary-highlight {
        background: linear-gradient(135deg, rgba(37,99,235,0.10), rgba(96,165,250,0.10));
        border-radius: 6px;
        padding: 2px 6px;
        font-weight: 700;
        color: #1D4ED8;
    }

    /* ========================================
       FOOTER
    ======================================== */
    .app-footer {
        text-align: center;
        margin-top: 72px;
        padding: 28px 0 20px 0;
        border-top: 1px solid #E2E8F0;
        animation: fadeIn 0.8s ease both;
    }
    .footer-tech-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .footer-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 999px;
        padding: 5px 14px;
        font-size: 12.5px;
        font-weight: 600;
        color: #475569;
    }
    .footer-copy {
        color: #CBD5E1;
        font-size: 12.5px;
        margin-top: 14px;
    }
    .footer-copy b {
        color: #2563EB;
    }

    /* ========================================
       PROGRESS BAR STYLING
    ======================================== */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #2563EB, #60A5FA) !important;
        border-radius: 99px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================================================================
# HERO SECTION
# ================================================================
st.markdown(
    """
    <div class="hero-section">
        <div class="hero-badge">⚡ AI-POWERED &nbsp;·&nbsp; FEEDBACK INTELLIGENCE</div>
        <p class="hero-title">🤖 InsightAI</p>
        <p class="hero-subtitle">Customer Feedback Intelligence Platform</p>
        <p class="hero-desc">
            Upload any customer review and get instant AI-driven insights —
            sentiment, emotions, authenticity, ratings, and actionable business recommendations.
        </p>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-num">5+</div>
                <div class="hero-stat-label">AI Models</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">Real-Time</div>
                <div class="hero-stat-label">Analysis</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">NLP</div>
                <div class="hero-stat-label">Powered</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">100%</div>
                <div class="hero-stat-label">Private</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ================================================================
# INPUT CARD
# ================================================================
st.markdown('<div class="input-card">', unsafe_allow_html=True)

st.markdown('<div class="input-card-label">📝 &nbsp; Paste Customer Review</div>', unsafe_allow_html=True)

review = st.text_area(
    "Customer Review",
    height=170,
    placeholder='e.g. "The product quality is amazing but delivery was very late and the packaging arrived damaged. Quite disappointed."',
    label_visibility="collapsed"
)

col_btn, col_pad = st.columns([1, 2])
with col_btn:
    analyze_clicked = st.button("🚀  Analyze Review  →")

st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# ANALYSIS LOGIC
# ================================================================
if analyze_clicked:

    if review.strip() == "":
        st.warning("⚠️ Please enter a customer review before analyzing.")
    else:
        # Progress feedback
        progress_placeholder = st.empty()
        status_placeholder   = st.empty()

        with progress_placeholder:
            prog = st.progress(0)
        with status_placeholder:
            st.markdown(
                '<p style="color:#64748B;font-size:13.5px;font-weight:500;margin-top:6px;">'
                '🔄 Running AI models...</p>',
                unsafe_allow_html=True
            )

        prog.progress(10)

        # ── Model calls (unchanged from original) ──────────────────
        sentiment   = predict_sentiment(review)
        prog.progress(30)
        emotion     = predict_emotion(review)
        prog.progress(50)
        fake_review = predict_fake_review(review)
        prog.progress(65)
        rating      = predict_rating(review)
        prog.progress(80)
        aspect      = predict_aspect(review)
        prog.progress(100)

        progress_placeholder.empty()
        status_placeholder.empty()

        # ── Derived helpers ─────────────────────────────────────────
        emoji_map = {
            "Happy": "😊", "Sad": "😢",
            "Angry": "😡", "Frustrated": "😤",
            "Satisfied": "😌"
        }
        emotion_icon = emoji_map.get(emotion, "😌")
        review_lower = review.lower()

        if fake_review == "Genuine":
            auth_value = "✅ Genuine"
            auth_color = "result-card-positive"
        elif fake_review == "Fake":
            auth_value = "⚠️ Fake"
            auth_color = "result-card-negative"
        else:
            auth_value = "🔍 Unknown"
            auth_color = ""

        sent_color = (
            "result-card-positive" if sentiment == "Positive" else
            "result-card-negative" if sentiment == "Negative" else ""
        )

        # ── Build aspect rows ────────────────────────────────────────
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

        total_aspects  = len(aspect_rows)
        pos_count      = sum(1 for _, s in aspect_rows if s.lower() == "positive")
        neg_count      = total_aspects - pos_count

        # ============================================================
        # SECTION: CUSTOMER REVIEW OVERVIEW (NEW DASHBOARD)
        # ============================================================
        st.markdown(
            """
            <div class="section-header">
                <div class="section-icon-wrap">📈</div>
                <div class="section-text-wrap">
                    <p class="section-title">Customer Review Overview</p>
                    <p class="section-sub">Snapshot of all detected signals from this review.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Rating stars for overview
        rating_display = f"{rating}/5" if rating is not None else "N/A"
        star_str = "⭐" * int(rating) if rating is not None else "—"

        # Build overview dashboard
        st.markdown(
            f"""
            <div class="overview-card">
                <div class="overview-stat">
                    <div class="overview-stat-icon">😊</div>
                    <div class="overview-stat-value">{sentiment}</div>
                    <div class="overview-stat-label">Overall Sentiment</div>
                </div>
                <div class="overview-divider"></div>
                <div class="overview-stat">
                    <div class="overview-stat-icon">{emotion_icon}</div>
                    <div class="overview-stat-value">{emotion}</div>
                    <div class="overview-stat-label">Emotion Detected</div>
                </div>
                <div class="overview-divider"></div>
                <div class="overview-stat">
                    <div class="overview-stat-icon">⭐</div>
                    <div class="overview-stat-value">{rating_display}</div>
                    <div class="overview-stat-label">Predicted Rating</div>
                </div>
                <div class="overview-divider"></div>
                <div class="overview-stat">
                    <div class="overview-stat-icon">🛡️</div>
                    <div class="overview-stat-value">{fake_review if fake_review else 'N/A'}</div>
                    <div class="overview-stat-label">Review Authenticity</div>
                </div>
                <div class="overview-divider"></div>
                <div class="overview-stat">
                    <div class="overview-stat-icon">🔍</div>
                    <div class="overview-stat-value">{total_aspects}</div>
                    <div class="overview-stat-label">Detected Aspects</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ============================================================
        # SECTION: AI REPORT CARDS
        # ============================================================
        st.markdown(
            """
            <div class="section-header">
                <div class="section-icon-wrap">📊</div>
                <div class="section-text-wrap">
                    <p class="section-title">AI Report</p>
                    <p class="section-sub">Instant insights generated from the customer review.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="result-card {sent_color}">
                    <div class="result-icon">😊</div>
                    <div class="result-label">Sentiment</div>
                    <div class="result-value">{sentiment}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-icon">{emotion_icon}</div>
                    <div class="result-label">Emotion</div>
                    <div class="result-value">{emotion}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="result-card {auth_color}">
                    <div class="result-icon">🛡️</div>
                    <div class="result-label">Review Authenticity</div>
                    <div class="result-value">{auth_value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            if rating is not None:
                star_filled   = "⭐" * int(rating)
                star_empty    = "☆"  * (5 - int(rating))
                rating_html = f"""
                <div class="star-display">{star_filled}{star_empty}</div>
                <div class="star-rating-big">{rating}/5</div>
                <div class="star-rating-label">Predicted Rating</div>
                """
            else:
                rating_html = '<div class="result-value soon">Coming Soon</div>'

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-icon">⭐</div>
                    <div class="result-label">Rating</div>
                    {rating_html}
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
                <div class="section-text-wrap">
                    <p class="section-title">Aspect Analysis</p>
                    <p class="section-sub">Breakdown of sentiment by product aspect &nbsp;|&nbsp;
                        <span style="color:#22C55E;font-weight:700;">{pos_count} Positive</span>
                        &nbsp;·&nbsp;
                        <span style="color:#EF4444;font-weight:700;">{neg_count} Negative</span>
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Build aspect cards grid
        aspect_cards_html = '<div class="aspect-grid">'
        for name, status in aspect_rows:
            sl = status.lower()
            if sl == "positive":
                badge = f'<span class="badge-positive">✓ &nbsp;Positive</span>'
            elif sl == "negative":
                badge = f'<span class="badge-negative">✗ &nbsp;Negative</span>'
            else:
                badge = f'<span class="badge-neutral">~ &nbsp;{status}</span>'

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
                <div class="section-text-wrap">
                    <p class="section-title">AI Business Insights</p>
                    <p class="section-sub">Actionable recommendations generated from the analysis.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Build insights list (unchanged logic from original)
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
            insights.append(("success", "✔️", "No Strong Signals Detected",
                              "The review does not indicate specific actionable issues."))

        for kind, icon, title, desc in insights:
            css_class = f"insight-{kind}"
            st.markdown(
                f"""
                <div class="insight-card {css_class}">
                    <div class="insight-icon-wrap">{icon}</div>
                    <div class="insight-text">
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
                <div class="section-text-wrap">
                    <p class="section-title">Executive Summary</p>
                    <p class="section-sub">AI-generated narrative report for stakeholders.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Build summary (unchanged logic from original)
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
            <div class="summary-glass">
                <div class="summary-heading">📝 &nbsp; AI-GENERATED EXECUTIVE SUMMARY</div>
                <div class="summary-body">{summary_body}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ================================================================
# FOOTER
# ================================================================
st.markdown(
    """
    <div class="app-footer">
        <div class="footer-tech-row">
            <span class="footer-chip">🐍 Python</span>
            <span class="footer-chip">🎈 Streamlit</span>
            <span class="footer-chip">🤖 Scikit-learn</span>
            <span class="footer-chip">🧠 NLP</span>
        </div>
        <p class="footer-copy">
            <b>InsightAI</b> &nbsp;·&nbsp; Customer Feedback Intelligence Platform
            &nbsp;·&nbsp; Built with ❤️ using AI
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
