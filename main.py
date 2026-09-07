import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="fromis_9 5초 음원 퀴즈",
    page_icon="🍀",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #E8FAF8 0%, #FFF1F5 50%, #EBF4FF 100%) !important;
    }

    .fromis-header {
        text-align: center;
        padding: 25px 20px;
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px);
        border-radius: 28px;
        border: 2px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 15px 35px rgba(93, 226, 164, 0.15);
        margin-bottom: 25px;
    }

    .fromis-badge {
        display: inline-block;
        background: linear-gradient(90deg, #3BCEAC 0%, #FF7597 100%);
        color: white;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 6px 18px;
        border-radius: 20px;
        letter-spacing: 1.2px;
        margin-bottom: 10px;
    }

    .fromis-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B8B, #22D3EE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 5px 0;
    }

    div[data-testid="stRadio"] > label { font-weight: 700 !important; color: #2D3748 !important; }

    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.6);
        padding: 15px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.9);
    }

    .stButton>button {
        background: linear-gradient(135deg, #FF7597 0%, #FF4B8B 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 18px !important;
        border: none !important;
        padding: 10px 28px !important;
        box-shadow: 0 6px 20px rgba(255, 75, 139, 0.3) !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="fromis-header">
    <span class="fromis-badge">🍀 FLOVER MUSIC QUIZ</span>
    <div class="fromis-title">프로미스나인 5초 음원 맞히기</div>
    <div style="color: #4A5568; font-size: 0.95rem; font-weight: 600;">하이라이트 5초를 듣고 어떤 노래인지 맞춰보세요! ✨</div>
</div>
""", unsafe_allow_html=True)

# 프로미스나인 검증된 공식 유튜브 ID 및 하이라이트 구간 설정
QUIZ_DATA = [
    {
        "yt_id": "B0yioML-1j8",  # Supersonic (공식 MV)
        "start_sec": 45,
        "answer": "Supersonic",
        "options": ["Supersonic", "WE GO", "DM", "Stay This Way"]
    },
    {
        "yt_id": "HM633a928Bw",  # WE GO (공식 MV)
        "start_sec": 38,
        "answer": "WE GO",
        "options": ["LOVE BOMB", "WE GO", "FUN!", "Talk & Talk"]
    },
    {
        "yt_id": "4gX_lOuE34k",  # DM (공식 MV)
        "start_sec": 50,
        "answer": "DM",
        "options": ["Supersonic", "DM", "WE GO", "Stay This Way"]
    },
    {
        "yt_id": "51a3_fJTo3U",  # Stay This Way (공식 MV)
        "start_sec": 40,
        "answer": "Stay This Way",
        "options": ["FUN!", "LOVE BOMB", "Stay This Way", "DM"]
    },
    {
        "yt_id": "893y322I_Wk",  # LOVE BOMB (공식 MV)
        "start_sec": 55,
        "answer": "LOVE BOMB",
        "options": ["LOVE BOMB", "WE GO", "Talk & Talk", "Supersonic"]
    },
    {
        "yt_id": "3M_yDq-88_s",  # FUN! (공식 MV)
        "start_sec": 42,
        "answer": "FUN!",
        "options": ["DM", "Stay This Way", "FUN!", "LOVE BOMB"]
    },
    {
        "yt_id": "hw4T0EaR6k8",  # Talk & Talk (공식 MV)
        "start_sec": 35,
        "answer": "Talk & Talk",
        "options": ["WE GO", "Talk & Talk", "Supersonic", "FUN!"]
    }
]

if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "is_finished" not in st.session_state:
    st.session_state.is_finished = False

current_q = QUIZ_DATA[st.session_state.q_idx]

# 5초 자동 멈춤 유튜브 플레이어 렌더링
def render_youtube_5sec_player(yt_id, start_sec):
    end_sec = start_sec + 5
    embed_src = f"https://www.youtube.com/embed/{yt_id}?start={start_sec}&end={end_sec}&autoplay=1&rel=0&enablejsapi=1"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
            body {{
                font-family: 'Pretendard', sans-serif;
                margin: 0;
                padding: 5px;
                background: transparent;
                text-align: center;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.85);
                backdrop-filter: blur(12px);
                border-radius: 20px;
                padding: 18px;
                border: 2px solid #FFF;
                box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            }}
            .btn-play {{
                background: linear-gradient(135deg, #3BCEAC, #22D3EE);
                border: none;
                color: white;
                font-weight: 700;
                font-size: 1rem;
                padding: 12px 30px;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(59, 206, 172, 0.35);
            }}
            .status {{
                margin-top: 10px;
                font-size: 0.85rem;
                color: #FF4B8B;
                font-weight: 700;
            }}
            .hidden-yt {{
                width: 0;
                height: 0;
                opacity: 0;
                pointer-events: none;
                position: absolute;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <button class="btn-play" onclick="startPlay()">▶ 5초 하이라이트 듣기</button>
            <div class="status" id="txt-status">버튼을 누르면 공식 음원이 5초간 재생됩니다.</div>
        </div>

        <div id="yt-box" class="hidden-yt"></div>

        <script>
            var timer = null;
            function startPlay() {{
                var box = document.getElementById('yt-box');
                var status = document.getElementById('txt-status');
                
                box.innerHTML = '';
                if(timer) clearTimeout(timer);

                var iframe = document.createElement('iframe');
                iframe.setAttribute('src', '{embed_src}');
                iframe.setAttribute('allow', 'autoplay');
                box.appendChild(iframe);

                status.innerText = "🎵 프로미스나인 공식 음원 5초 재생 중...";

                timer = setTimeout(function() {{
                    box.innerHTML = '';
                    status.innerText = "🔒 5초 미리듣기가 완료되었습니다!";
                }}, 5500);
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=140)

# 게임 진행 화면
if not st.session_state.is_finished:
    st.markdown(f"### 🎵 Q{st.session_state.q_idx + 1}. 이 노래의 제목은?")
    
    render_youtube_5sec_player(current_q["yt_id"], current_q["start_sec"])

    st.write("")
    user_choice = st.radio("정답을 선택해주세요:", current_q["options"], key=f"radio_q_{st.session_state.q_idx}")

    st.write("")
    if st.button("정답 제출 🍀", key=f"btn_sub_{st.session_state.q_idx}"):
        if user_choice == current_q["answer"]:
            st.success("정답입니다! 🎉")
            st.session_state.score += 10
        else:
            st.error(f"아쉽네요! 정답은 [{current_q['answer']}] 입니다. 😅")

        if st.session_state.q_idx + 1 < len(QUIZ_DATA):
            st.session_state.q_idx += 1
            st.button("다음 문제로 ➡️", key=f"btn_next_{st.session_state.q_idx}")
        else:
            st.session_state.is_finished = True
            st.button("결과 확인하기 🏆", key="btn_finish")

# 결과 화면
else:
    st.balloons()
    st.header("🏆 게임 종료!")
    max_score = len(QUIZ_DATA) * 10
    st.write(f"최종 점수: **{st.session_state.score}** / {max_score} 점")
    
    if st.session_state.score == max_score:
        st.write("🥇 만점입니다! 당신은 완벽한 플로버(flover)입니다. 🍀")
    elif st.session_state.score >= 50:
        st.write("🥈 훌륭한 실력이에요!")
    else:
        st.write("👍 수고하셨습니다! 다시 도전해보세요.")

    if st.button("다시 도전하기 🔄", key="btn_reset"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.is_finished = False
        st.rerun()
