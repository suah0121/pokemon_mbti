import streamlit as st
import json

st.set_page_config(
    page_title="⚡ MBTI x 포켓몬 단짝 찾기 ⚡",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Neon Pink & Blue Color Palette */
    :root {
        --neon-pink: #FF007F;
        --neon-blue: #00E5FF;
        --neon-purple: #B026FF;
        --dark-bg: #0A0A16;
        --card-bg: rgba(18, 18, 42, 0.85);
    }

    /* Overall Page Background & Typography */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #200B3B, #0A0A16 80%) !important;
        color: #FFFFFF !important;
        font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif;
    }

    /* Hide Default Header/Footer */
    header[data-testid="stHeader"], footer {
        visibility: hidden;
        height: 0;
    }

    /* Glowing Neon Title */
    .neon-title {
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        text-align: center;
        background: linear-gradient(135deg, var(--neon-pink), var(--neon-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 0, 127, 0.5), 0 0 40px rgba(0, 229, 255, 0.4);
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .neon-subtitle {
        font-size: 1.3rem;
        text-align: center;
        color: var(--neon-blue);
        font-weight: 600;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.6);
    }

    /* Custom Glassmorphism Card */
    .glass-card {
        background: var(--card-bg);
        border: 2px solid var(--neon-pink);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.3), inset 0 0 15px rgba(0, 229, 255, 0.1);
        backdrop-filter: blur(16px);
        margin-top: 1rem;
    }

    /* Type Badges */
    .type-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 1.1rem;
        color: #FFFFFF;
        background: linear-gradient(135deg, var(--neon-pink), var(--neon-purple));
        box-shadow: 0 0 12px rgba(255, 0, 127, 0.6);
        margin-bottom: 1rem;
    }

    /* Pokemon Image Floating Animation */
    .pokemon-img-box img {
        filter: drop-shadow(0 0 25px rgba(0, 229, 255, 0.7));
        animation: float 3.5s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-12px) scale(1.03); }
    }

    /* Reason & Features Box */
    .feature-box {
        background: rgba(0, 229, 255, 0.08);
        border-left: 4px solid var(--neon-blue);
        padding: 1.2rem 1.5rem;
        border-radius: 0 16px 16px 0;
        margin-top: 1rem;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #E2E8F0;
    }

    /* Custom Button Overrides for Streamlit */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.2), rgba(0, 229, 255, 0.2)) !important;
        border: 2px solid var(--neon-blue) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        padding: 0.8rem 1rem !important;
        border-radius: 16px !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.2) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--neon-pink), var(--neon-blue)) !important;
        border-color: #FFFFFF !important;
        color: #FFFFFF !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.8), 0 0 35px rgba(0, 229, 255, 0.8) !important;
    }

    /* Selectbox Styling */
    div[data-baseweb="select"] > div {
        background-color: rgba(18, 18, 42, 0.9) !important;
        border: 2px solid var(--neon-pink) !important;
        border-radius: 16px !important;
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }

    /* Celebration Banner */
    .celebrate-banner {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 900;
        color: var(--neon-blue);
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.8);
        margin-bottom: 1rem;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.85; transform: scale(1.02); }
    }
</style>
""", unsafe_allow_html=True)

# 16 MBTI Pokemon Mapping with High-Definition Official Artwork from PokeAPI
pokemon_db = {
    "ISTJ": {
        "kor_name": "거북왕",
        "eng_name": "Blastoise",
        "poke_id": 9,
        "type": "💧 물 타입",
        "feature": "신중함, 강력한 단단함, 철저한 책임감",
        "reason": "매사에 철두철미하고 강한 책임감을 가진 당신! 단단한 껍질과 물대포로 어떤 상황에서도 신뢰할 수 있는 버팀목이 되어주는 거북왕과 완벽한 파트너입니다."
    },
    "ISFJ": {
        "kor_name": "해피너스",
        "eng_name": "Blissey",
        "poke_id": 242,
        "type": "⭐ 노멀 타입",
        "feature": "따뜻한 배려, 세심함, 온화한 헌신",
        "reason": "주변 사람들의 행복을 가장 먼저 챙기는 따뜻한 당신! 타인의 아픔을 치료해 주고 깊은 온기를 선사하는 해피너스가 최고의 마음 치료사 단짝입니다."
    },
    "INFJ": {
        "kor_name": "뮤",
        "eng_name": "Mew",
        "poke_id": 151,
        "type": "🔮 에스퍼 타입",
        "feature": "신비로운 직관, 깊은 통찰력, 조용한 영향력",
        "reason": "풍부한 이상과 신비로운 직관력을 가슴속에 품은 당신! 세상의 진리를 조용히 탐구하는 희귀한 환상의 포켓몬 뮤와 영혼의 주파수가 일치합니다."
    },
    "INTJ": {
        "kor_name": "뮤츠",
        "eng_name": "Mewtwo",
        "poke_id": 150,
        "type": "🔮 에스퍼 타입",
        "feature": "철저한 전략, 높은 지능, 독립적 사고",
        "reason": "치밀한 계획과 냉철한 분석으로 미래를 설계하는 마인드 컨트롤러! 높은 지능과 독보적인 포스로 목표를 이루어 내는 뮤츠와 명콤비입니다."
    },
    "ISTP": {
        "kor_name": "루카리오",
        "eng_name": "Lucario",
        "poke_id": 448,
        "type": "🥊 격투 / ⚙️ 강철 타입",
        "feature": "냉철한 판단력, 뛰어난 신체 감각, 즉각적 해결",
        "reason": "위기 상황에서도 당황하지 않고 솔루션을 찾아내는 위풍당당 해결사! 상대의 파동을 감지하고 신속하게 행동하는 루카리오와 최고의 호흡을 자랑합니다."
    },
    "ISFP": {
        "kor_name": "메타몽",
        "eng_name": "Ditto",
        "poke_id": 132,
        "type": "⭐ 노멀 타입",
        "feature": "유연한 적응력, 온순함, 자유로운 감성",
        "reason": "어디서든 부드럽게 대처하며 자유로운 영혼을 가지고 있는 당신! 어떤 모양으로든 유연하게 변신하며 주변을 편안하게 만드는 메타몽이 딱입니다."
    },
    "INFP": {
        "kor_name": "이브이",
        "eng_name": "Eevee",
        "poke_id": 133,
        "type": "⭐ 노멀 타입",
        "feature": "무한한 가능성, 순수한 감수성, 풍부한 꿈",
        "reason": "가슴속에 무한한 상상력과 따뜻한 감성을 간직한 당신! 어떤 형태로든 자유롭게 진화할 수 있는 잠재력을 지닌 이브이가 최고의 단짝 포켓몬입니다."
    },
    "INTP": {
        "kor_name": "후딘",
        "eng_name": "Alakazam",
        "poke_id": 65,
        "type": "🔮 에스퍼 타입",
        "feature": "높은 지적 호기심, 원리 탐구, 창의적 분석",
        "reason": "세상의 모든 원리와 복잡한 지식을 분석하기 좋아하는 천재적 탐구가! IQ 5000의 상징이자 초능력의 대명사 후딘과 지적 시너지가 폭발합니다."
    },
    "ESTP": {
        "kor_name": "리자몽",
        "eng_name": "Charizard",
        "poke_id": 6,
        "type": "🔥 불꽃 / 🕊️ 비행 타입",
        "feature": "화끈한 에너지, 과감한 도전, 강렬한 리더십",
        "reason": "위험을 두려워하지 않고 스릴 넘치는 도전을 즐기는 행동파! 뜨거운 불꽃을 내뿜으며 현장을 이끄는 리자몽과 함께라면 무엇이든 돌파할 수 있습니다."
    },
    "ESFP": {
        "kor_name": "푸린",
        "eng_name": "Jigglypuff",
        "poke_id": 39,
        "type": "⭐ 노멀 / 🧚 페어리 타입",
        "feature": "통통 튀는 매력, 분위기 메이커, 긍정 에너지",
        "reason": "어디서나 스포트라이트를 받는 유쾌하고 통통 튀는 무대의 주인공! 사랑스러운 노래와 밝은 에너지로 사람들을 사로잡는 푸린과 최고의 무대를 만들어보세요."
    },
    "ENFP": {
        "kor_name": "피카츄",
        "eng_name": "Pikachu",
        "poke_id": 25,
        "type": "⚡ 전기 타입",
        "feature": "번개 같은 열정, 친근한 매력, 무한 긍정",
        "reason": "상상력이 풍부하고 매 순간 에너지가 번개처럼 뿜어져 나오는 당신! 전 세계의 사랑을 받는 백만볼트 에너지의 피카츄와 환상의 콤비입니다."
    },
    "ENTP": {
        "kor_name": "팬텀",
        "eng_name": "Gengar",
        "poke_id": 94,
        "type": "👻 고스트 / ☠️ 독 타입",
        "feature": "재치 있는 장난기, 독창적 생각, 기발한 유머",
        "reason": "고정관념을 깨부수고 색다른 아이디어로 세상을 놀라게 하는 기발한 토론가! 신선한 장난기와 독창성을 지닌 팬텀이 최고의 파트너입니다."
    },
    "ESTJ": {
        "kor_name": "괴력몬",
        "eng_name": "Machamp",
        "poke_id": 68,
        "type": "🥊 격투 타입",
        "feature": "체계적인 추진력, 확실한 리더십, 규칙 준수",
        "reason": "목표가 정해지면 망설임 없이 일사불란하게 완수해내는 강력한 지도자! 4개의 팔로 어떤 난관도 신속히 해결하는 괴력몬이 든든한 동반자입니다."
    },
    "ESFJ": {
        "kor_name": "라이츄",
        "eng_name": "Raichu",
        "poke_id": 26,
        "type": "⚡ 전기 타입",
        "feature": "친절한 다정함, 공동체 화합, 세심한 케어",
        "reason": "주변 사람들을 살뜰히 챙기고 밝고 화목한 분위기를 만드는 인싸 리더! 따뜻하고 강력한 전기에너지로 모두를 지켜주는 라이츄와 찰떡궁합입니다."
    },
    "ENFJ": {
        "kor_name": "토게키스",
        "eng_name": "Togekiss",
        "poke_id": 468,
        "type": "🧚 페어리 / 🕊️ 비행 타입",
        "feature": "평화와 축복, 카리스마 넘치는 격려, 동기부여",
        "reason": "타인의 성장을 진심으로 도우며 조화로운 세상을 꿈꾸는 선한 영향력의 리더! 기쁨과 평화를 가져다주는 축복 포켓몬 토게키스와 깊게 공명합니다."
    },
    "ENTJ": {
        "kor_name": "자시안",
        "eng_name": "Zacian",
        "poke_id": 888,
        "type": "🧚 페어리 / ⚙️ 강철 타입",
        "feature": "압도적 비전, 결단력, 정복의 카리스마",
        "reason": "거침없는 결단력과 명확한 비전으로 시련을 기회로 바꾸는 정복자! 검을 휘두르듯 단숨에 승리를 이끄는 검왕 포켓몬 자시안과 최강의 조합을 이룹니다."
    }
}

st.markdown('<div class="neon-title">⚡ MBTI x 포켓몬 단짝 찾기 ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">당신의 MBTI 성격 유형에 딱 맞는 환상의 포켓몬 파트너를 만나보세요!</div>', unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    mbti_list = list(pokemon_db.keys())
    selected_mbti = st.selectbox(
        "✨ 당신의 MBTI 유형을 선택하세요:",
        options=mbti_list,
        index=mbti_list.index("ENFP")
    )
    
    find_button = st.button("💖 단짝 포켓몬 소환하기! 💖")

if find_button or "first_run" not in st.session_state:
    st.session_state["first_run"] = True
    
    # Trigger Celebration Effect
    st.balloons()
    
    data = pokemon_db[selected_mbti]
    img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['poke_id']}.png"

    st.markdown('<div class="celebrate-banner">🎉 축하합니다! 단짝 포켓몬을 찾았습니다! 🎉</div>', unsafe_allow_html=True)
    
    # Glassmorphism Result Container
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.3])
    
    with col1:
        st.markdown(f'<div class="pokemon-img-box text-center"><img src="{img_url}" width="320" alt="{data["kor_name"]}"></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="type-badge">{data["type"]}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <h1 style="font-size: 2.8rem; font-weight: 900; margin: 0; color: #FFFFFF; text-shadow: 0 0 15px rgba(255, 0, 127, 0.7);">
            {data["kor_name"]} <span style="font-size: 1.5rem; color: #00E5FF; font-weight: 600;">({data["eng_name"]})</span>
        </h1>
        <p style="font-size: 1.2rem; color: #FF007F; font-weight: 700; margin-top: 0.5rem;">
            🎯 매칭 MBTI: <span style="color: #00E5FF; text-decoration: underline;">{selected_mbti}</span>
        </p>
        <div style="font-size: 1.15rem; color: #F1F5F9; margin-top: 1rem;">
            <strong>✨ 핵심 특징:</strong> {data["feature"]}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="feature-box">
            <strong>💌 단짝이 된 이유:</strong><br>
            {data["reason"]}
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<br><hr style="border-color: rgba(255, 0, 127, 0.3);">
<div style="text-align: center; color: rgba(255, 255, 255, 0.5); font-size: 0.9rem;">
    ⚡ MBTI Pokemon Matcher • Powered by Streamlit & Official PokeAPI Artwork
</div>
""", unsafe_allow_html=True)
```
