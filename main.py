import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="MBTI x 단짝 포켓몬 찾기 ⚡",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 파이버펑크 / 네온 핑크 & 블루 커스텀 CSS 적용
st.markdown("""
<style>
    /* Google Fonts 로드 */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Noto+Sans+KR:wght@400;700;900&display=swap');

    /* 전체 배경 설정 (다크 네온 분위기) */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #15052A 0%, #0A0118 70%, #05000C 100%);
        color: #FFFFFF;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 메인 타이틀 커스텀 */
    .main-title {
        font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #FF007F 0%, #00E5FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 0, 127, 0.5);
        margin-top: -20px;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #00E5FF;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.6);
        margin-bottom: 30px;
        font-weight: 700;
    }

    /* Streamlit Selectbox 라벨 & 스타일 커스텀 */
    div[data-baseweb="select"] {
        border-radius: 16px !important;
        border: 2px solid #FF007F !important;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.4) !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #120326 !important;
        color: #00E5FF !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
    }

    /* 결과 카드 스타일 (글래스모피즘 + 네온 테두리) */
    .pokemon-card {
        background: rgba(18, 3, 38, 0.75);
        border: 3px solid #00E5FF;
        border-radius: 24px;
        padding: 30px 24px;
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.35), inset 0 0 15px rgba(255, 0, 127, 0.2);
        backdrop-filter: blur(10px);
        text-align: center;
        margin-top: 20px;
        animation: pulseBorder 3s infinite alternate;
    }

    @keyframes pulseBorder {
        0% {
            border-color: #00E5FF;
            box-shadow: 0 0 25px rgba(0, 229, 255, 0.4);
        }
        100% {
            border-color: #FF007F;
            box-shadow: 0 0 35px rgba(255, 0, 127, 0.6);
        }
    }

    .mbti-badge {
        display: inline-block;
        background: linear-gradient(90deg, #FF007F, #9D00FF);
        color: #FFFFFF;
        font-size: 1.4rem;
        font-weight: 900;
        padding: 8px 24px;
        border-radius: 30px;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.8);
        margin-bottom: 15px;
        letter-spacing: 2px;
    }

    .poke-name {
        font-size: 2.3rem;
        font-weight: 900;
        color: #FFFFFF;
        text-shadow: 0 0 12px #00E5FF;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .poke-en-name {
        font-size: 1.1rem;
        color: #FF77BC;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
    }

    .type-badge {
        display: inline-block;
        background: rgba(0, 229, 255, 0.15);
        border: 1px solid #00E5FF;
        color: #00E5FF;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.05rem;
        margin: 4px;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
    }

    .reason-box {
        background: rgba(255, 0, 127, 0.1);
        border-left: 4px solid #FF007F;
        border-radius: 12px;
        padding: 18px 20px;
        margin-top: 25px;
        text-align: left;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #F3E8FF;
        word-break: keep-all;
    }

    .feature-box {
        background: rgba(0, 229, 255, 0.08);
        border-left: 4px solid #00E5FF;
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 15px;
        text-align: left;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #E0F2FE;
        word-break: keep-all;
    }

    .box-title {
        font-weight: 900;
        font-size: 1.2rem;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 16가지 MBTI 포켓몬 데이터베이스 (공식 PokeAPI 고화질 이미지 URL 연결)
POKEMON_DATABASE = {
    "ISTJ": {
        "ko_name": "거북왕",
        "en_name": "Blastoise",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "types": ["물 💧"],
        "feature": "신중하고 신뢰할 수 있으며, 등 뒤의 포신으로 강력한 물대포를 정확하게 분사합니다.",
        "reason": "원칙을 준수하고 책임감이 강한 ISTJ처럼, 거북왕은 단단한 방어력과 신뢰할 수 있는 실행력으로 언제나 팀을 지키는 든든한 버팀목이 되어줍니다."
    },
    "ISFJ": {
        "ko_name": "해피너스",
        "en_name": "Blissey",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/242.png",
        "types": ["노멀 🥚"],
        "feature": "사랑이 가득 담긴 알을 내어주어 아프거나 슬픈 타인을 진심으로 케어합니다.",
        "reason": "타인의 감정에 세심하고 침착하게 배려하는 ISFJ와 해피너스는 찰떡궁합입니다. 함께 있는 것만으로도 상대방에게 따뜻한 안식처를 선사합니다."
    },
    "INFJ": {
        "ko_name": "뮤",
        "en_name": "Mew",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/151.png",
        "types": ["에스퍼 ✨"],
        "feature": "모든 포켓몬의 기술을 배울 수 있는 신비롭고 영리하며 순수한 환상의 포켓몬입니다.",
        "reason": "깊은 통찰력과 이상주의적인 철학을 품은 INFJ의 영혼과 어울립니다. 보이지 않는 가치를 탐구하고 세상에 선한 영향력을 전합니다."
    },
    "INTJ": {
        "ko_name": "뮤츠",
        "en_name": "Mewtwo",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "types": ["에스퍼 🧬"],
        "feature": "지능이 매우 높고 사이코 파워를 완벽히 통제하는 전략적 수재입니다.",
        "reason": "철저한 계획과 합리적 사고를 중시하는 INTJ와 높은 지능으로 완벽한 전략을 구사하는 뮤츠는 최고의 지성파 파트너 조합입니다."
    },
    "ISTP": {
        "ko_name": "루카리오",
        "en_name": "Lucario",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "types": ["격투 🥊", "강철 🛡️"],
        "feature": "상대방의 파동을 감지하여 상황을 냉철하게 분석하고 순발력 있게 대처합니다.",
        "reason": "상황 판단이 빠르고 현실적인 도구 및 기술 활용에 능한 ISTP처럼, 루카리오는 과묵하지만 실전에서 완벽한 능력을 발휘합니다."
    },
    "ISFP": {
        "ko_name": "메타몽",
        "en_name": "Ditto",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png",
        "types": ["노멀 🫠"],
        "feature": "상대방의 모습과 능력을 있는 그대로 유연하게 복사해 맞추어 변화합니다.",
        "reason": "온순하고 감수성이 풍부하며 환경에 맞춰 유연하게 조화를 이루는 ISFP에게 메타몽의 유연하고 편안한 에너지는 최고의 편안함을 줍니다."
    },
    "INFP": {
        "ko_name": "이브이",
        "en_name": "Eevee",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "types": ["노멀 🦊"],
        "feature": "무한한 가능성을 품고 있으며, 환경과 진심에 따라 다양한 형태로 아름답게 진화합니다.",
        "reason": "풍부한 가치관과 끝없는 무한한 잠재력을 지닌 INFP에게 이브이는 꿈과 가능성을 공유할 수 있는 가장 특별한 분신입니다."
    },
    "INTP": {
        "ko_name": "후딘",
        "en_name": "Alakazam",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png",
        "types": ["에스퍼 🥄"],
        "feature": "IQ 5000에 달하는 슈퍼 브레인으로 세상의 모든 이치와 논리를 기억하고 계산합니다.",
        "reason": "끊임없이 호기심을 가지고 원리를 탐구하는 지적 탐험가 INTP와 복잡한 문제를 해결하는 후딘은 수수께끼를 함께 풀어나갈 완벽한 짝꿍입니다."
    },
    "ESTP": {
        "ko_name": "리자몽",
        "en_name": "Charizard",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "types": ["불꽃 🔥", "비행 🕊️"],
        "feature": "강한 상대일수록 승부욕이 타오르며 뜨거운 불꽃을 내뿜는 과감한 행동파입니다.",
        "reason": "스릴을 즐기고 모험에 당당히 부딪히는 ESTP처럼, 리자몽은 거침없는 열정과 화려한 에너지를 함께 발산할 최고의 모험 동반자입니다."
    },
    "ESFP": {
        "ko_name": "푸린",
        "en_name": "Jigglypuff",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png",
        "types": ["노멀 🎤", "페어리 ✨"],
        "feature": "무대 위에서 노래 부르는 것을 즐기며 통통 튀는 사랑스러운 자태로 주목받습니다.",
        "reason": "풍부한 유흥과 즐거움을 전파하며 주위 사람들을 미소 짓게 만드는 스타성을 지닌 ESFP에게 푸린의 밝고 사랑스러운 매력이 딱 맞습니다."
    },
    "ENFP": {
        "ko_name": "피카츄",
        "en_name": "Pikachu",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "types": ["전기 ⚡"],
        "feature": "호기심이 풍부하고 밝은 전기를 뿜어내어 사방을 활기차게 만드는 피스메이커입니다.",
        "reason": "스파크처럼 튀는 생기발랄함과 매력으로 누구와도 금방 친구가 되는 ENFP와 피카츄의 에너지는 세상을 밝히는 환상의 케미를 자아냅니다."
    },
    "ENTP": {
        "ko_name": "팬텀",
        "en_name": "Gengar",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "types": ["고스트 👻", "독 🧪"],
        "feature": "장난기가 가득하며 통념을 깨는 재치 있는 허점 공격으로 상대를 기분 좋게 놀라게 합니다.",
        "reason": "독창적이고 창의적인 아이디어로 판을 뒤흔드는 토론가 ENTP에게 팬텀의 엉뚱함과 재치는 하루도 지루할 틈 없는 신나는 자극을 줍니다."
    },
    "ESTJ": {
        "ko_name": "괴력몬",
        "en_name": "Machamp",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/68.png",
        "types": ["격투 💪"],
        "feature": "4개의 팔로 1초에 1000번의 펀치를 날릴 만큼 압도적인 실행력과 규칙적인 강함을 자랑합니다.",
        "reason": "목표 설정과 철저한 조직 관리에 뛰어난 리더인 ESTJ처럼, 괴력몬의 강인한 추진력은 어떠한 과제든 시원시원하게 해결해 냅니다."
    },
    "ESFJ": {
        "ko_name": "라이츄",
        "en_name": "Raichu",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png",
        "types": ["전기 🐭"],
        "feature": "긴 꼬리로 전기를 땅으로 방출하여 동료들이 놀라지 않게 보호하는 상냥하고 스윗한 포켓몬입니다.",
        "reason": "주변 사람들을 살뜰히 챙기고 밝은 친화력으로 분위기를 이끄는 ESFJ에게 온화함과 든든함을 모두 갖춘 라이츄가 제격입니다."
    },
    "ENFJ": {
        "ko_name": "토게키스",
        "en_name": "Togekiss",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/468.png",
        "types": ["페어리 ✨", "비행 🕊️"],
        "feature": "서로를 존중하고 다툼이 없는 평화로운 곳에 나타나 은혜로운 축복을 나누어 줍니다.",
        "reason": "타인의 성장을 도모하고 공동체의 화합을 이끄는 카리스마 넘치는 리더 ENFJ에게 토게키스는 평화와 선의의 상징으로서 완벽한 조화를 이룹니다."
    },
    "ENTJ": {
        "ko_name": "자시안",
        "en_name": "Zacian",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/888.png",
        "types": ["페어리 🗡️", "강철 🛡️"],
        "feature": "검을 입에 물고 전장을 누비며 한 치의 오차도 없이 전설적인 승리를 이끄는 당당한 전사입니다.",
        "reason": "높은 비전과 확고한 결단력으로 목표를 향해 당당히 나아가는 비전형 리더 ENTJ에게 자시안의 위엄과 결단력은 최고의 시너지를 냅니다."
    }
}

# 4. 앱 헤더 선언
st.markdown("<div class="main-title">MBTI x POKÉMON</div>", unsafe_allow_html=True)
st.markdown("<div class="sub-title">⚡ 나만의 단짝 포켓몬 파트너 찾기 ⚡</div>", unsafe_allow_html=True)

# 5. MBTI 선택 셀렉트박스
mbti_list = list(POKEMON_DATABASE.keys())
selected_mbti = st.selectbox(
    "👉 당신의 MBTI 유형을 선택해 주세요!",
    options=mbti_list,
    index=10 # 기본 선택: ENFP
)

# 6. 매칭 결과 표시 및 축하 효과
if selected_mbti:
    # 스트림릿 축하 기본 풍선 애니메이션 실행
    st.balloons()

    # 네온 사운드/파티클 캔버스 효과 JS 추가
    confetti_js = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#FF007F', '#00E5FF', '#FFFFFF', '#FFE066']
        });
    </script>
    """
    components.html(confetti_js, height=0, width=0)

    poke = POKEMON_DATABASE[selected_mbti]

    # 포켓몬 결과 카드 생성
    types_html = "".join([f'<span class="type-badge">{t}</span>' for t in poke['types']])

    card_html = f"""
    <div class="pokemon-card">
        <div class="mbti-badge">✨ YOUR MBTI: {selected_mbti} ✨</div>
        <br>
        <img src="{poke['img']}" style="width: 260px; height: 260px; object-fit: contain; filter: drop-shadow(0 0 20px rgba(0, 229, 255, 0.6)); margin: 10px 0;" alt="{poke['ko_name']}">
        <div class="poke-name">{poke['ko_name']}</div>
        <div class="poke-en-name">{poke['en_name'].upper()}</div>
        <div style="margin-bottom: 15px;">{types_html}</div>
        
        <div class="feature-box">
            <div class="box-title" style="color: #00E5FF;">📌 단짝 포켓몬의 특징</div>
            {poke['feature']}
        </div>

        <div class="reason-box">
            <div class="box-title" style="color: #FF007F;">💖 어울리는 이유</div>
            {poke['reason']}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
