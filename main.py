import os
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="fromis_9 5초 음원 퀴즈",
    page_icon="🍀",
    layout="centered"
)

# 프로미스나인 감성 Custom CSS
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
    <div style="color: #4A5568; font-size: 0.95rem; font-weight: 600;">음원을 5초간 듣고 어떤 노래인지 맞춰보세요! ✨</div>
</div>
""", unsafe_allow_html=True)

# Requested 7 Songs Data
QUIZ_DATA = [
    {
        "audio_path": "assets/supersonic.mp3",
        "answer": "Supersonic",
        "options": ["Supersonic", "WE GO", "Sky Runner", "Vitamin Me"]
    },
    {
        "audio_path": "assets/we_go.mp3",
        "answer": "WE GO",
        "options": ["From", "WE GO", "I Like You Better", "하얀 그리움"]
    },
    {
        "audio_path": "assets/sky_runner.mp3",
        "answer": "Sky Runner",
        "options": ["Supersonic", "Sky Runner", "Vitamin Me", "WE GO"]
    },
    {
        "audio_path": "assets/vitamin_me.mp3",
        "answer": "Vitamin Me",
        "options": ["하얀 그리움", "From", "Vitamin Me", "I Like You Better"]
    },
    {
        "audio_path": "assets/i_like_you_better.mp3",
        "answer": "I Like You Better",
        "options": ["I Like You Better", "Supersonic", "WE GO", "Sky Runner"]
    },
    {
        "audio_path": "assets/hayan_geurium.mp3",
        "answer": "하얀 그리움",
        "options": ["From", "Vitamin Me", "하얀 그리움", "Sky Runner"]
    },
    {
        "audio_path": "assets/from.mp3",
        "answer": "From",
        "options": ["WE GO", "From", "I Like You Better", "Supersonic"]
    }
]

if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "is_finished" not in st.session_state:
    st.session_state.is_finished = False

current_q = QUIZ_DATA[st.session_state.q_idx]

# 5초 제한 오디오 플레이어 (HTML5 Audio Context 기반)
def render_5sec_player(source):
    player_html = f"""
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
            .box {{
                background: rgba(255, 255, 255, 0.85);
                backdrop-filter: blur(12px);
                border: 2px solid #FFF;
                border-radius: 20px;
                padding: 20px;
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
                transition: all 0.2s ease;
            }}
            .btn-play:hover {{ transform: scale(1.03); }}
            .status {{
                margin-top: 12px;
                font-size: 0.85rem;
                color: #FF4B8B;
                font-weight: 700;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <audio id="audio" src="{source}"></audio>
            <button class="btn-play" onclick="play5Sec()">▶ 5초 음원 재생</button>
            <div class="status" id="status">버튼을 눌러 5초간 음원을 들어보세요!</div>
        </div>

        <script>
            const audio = document.getElementById('audio');
            const statusElem = document.getElementById('status');
            let timer = null;

            function play5Sec() {{
                if (timer) clearTimeout(timer);
                
                audio.currentTime = 0;
                audio.play().then(() => {{
                    statusElem.innerText = "🎵 5초 음원 감상 중...";
                    timer = setTimeout(() => {{
                        audio.pause();
                        statusElem.innerText = "🔒 5초 미리듣기가 완료되었습니다!";
                    }}, 5000);
                }}).catch(err => {{
                    statusElem.innerText = "⚠️ 음원 재생 오류: 파일 경로를 확인해 주세요.";
                }});
            }}
        </script>
    </body>
    </html>
    """
    components.html(player_html, height=150)

# 게임 진행 화면
if not st.session_state.is_finished:
    st.markdown(f"### 🎵 Q{st.session_state.q_idx + 1}. 이 노래의 제목은?")
    
    audio_file = current_q["audio_path"]
    if os.path.exists(audio_file):
        render_5sec_player(audio_file)
    else:
        st.warning(f"⚠️ `{audio_file}` 파일이 준비되지 않았습니다. assets/ 폴더에 MP3 파일을 넣어주세요.")

    st.write("")
    user_choice = st.radio("정답을 선택해주세요:", current_q["options"], key=f"q_{st.session_state.q_idx}")

    st.write("")
    if st.button("정답 제출 🍀"):
        if user_choice == current_q["answer"]:
            st.success("정답입니다! 🎉")
            st.session_state.score += 10
        else:
            st.error(f"아쉽네요! 정답은 [{current_q['answer']}] 입니다. 😅")

        if st.session_state.q_idx + 1 < len(QUIZ_DATA):
            st.session_state.q_idx += 1
            st.button("다음 문제로 ➡️")
        else:
            st.session_state.is_finished = True
            st.button("결과 확인하기 🏆")

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

    if st.button("다시 도전하기 🔄"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.is_finished = False
        st.rerun()
