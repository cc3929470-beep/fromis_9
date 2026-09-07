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

# 유튜브 ID 기반 퀴즈 데이터 (Start시간 / End시간 설정)
# 예시: https://www.youtube.com/watch?v=N8qTbdE3OqE 라면 youtube_id는 N8qTbdE3OqE
QUIZ_DATA = [
    {
        "youtube_id": "N8qTbdE3OqE", # Supersonic MV ID
        "start_sec": 30,             # 시작 시간(초)
        "answer": "Supersonic",
        "options": ["Supersonic", "WE GO", "Sky Runner", "Vitamin Me"]
    },
    {
        "youtube_id": "v632k_J_EGA", # WE GO MV ID
        "start_sec": 45,
        "answer": "WE GO",
        "options": ["From", "WE GO", "I Like You Better", "하얀 그리움"]
    },
    {
        "youtube_id": "N8qTbdE3OqE",
        "start_sec": 60,
        "answer": "Sky Runner",
        "options": ["Supersonic", "Sky Runner", "Vitamin Me", "WE GO"]
    },
    {
        "youtube_id": "v632k_J_EGA",
        "start_sec": 10,
        "answer": "Vitamin Me",
        "options": ["하얀 그리움", "From", "Vitamin Me", "I Like You Better"]
    },
    {
        "youtube_id": "N8qTbdE3OqE",
        "start_sec": 15,
        "answer": "I Like You Better",
        "options": ["I Like You Better", "Supersonic", "WE GO", "Sky Runner"]
    },
    {
        "youtube_id": "v632k_J_EGA",
        "start_sec": 20,
        "answer": "하얀 그리움",
        "options": ["From", "Vitamin Me", "하얀 그리움", "Sky Runner"]
    },
    {
        "youtube_id": "N8qTbdE3OqE",
        "start_sec": 80,
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

# 5초 자동 제어 유튜브 임베드 컴포넌트
def render_youtube_5sec(yt_id, start_sec):
    end_sec = start_sec + 5
    yt_html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; padding:0; background:transparent; text-align:center;">
        <div style="background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); border-radius: 20px; padding: 15px; border: 2px solid #FFF;">
            <div id="player"></div>
            <div style="margin-top: 10px; font-family: 'Pretendard', sans-serif; font-size: 0.85rem; color: #FF4B8B; font-weight: 700;" id="status">
                ⏱️ 재생 버튼을 누르면 5초간 자동 재생됩니다.
            </div>
        </div>

        <script>
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

            var player;
            function onYouTubeIframeAPIReady() {{
                player = new YT.Player('player', {{
                    height: '200',
                    width: '100%',
                    videoId: '{yt_id}',
                    playerVars: {{
                        'playsinline': 1,
                        'start': {start_sec},
                        'end': {end_sec},
                        'controls': 1
                    }},
                    events: {{
                        'onStateChange': onPlayerStateChange
                    }}
                }});
            }}

            function onPlayerStateChange(event) {{
                if (event.data == YT.PlayerState.PLAYING) {{
                    document.getElementById('status').innerText = "🎵 5초 감상 중...";
                }}
                if (event.data == YT.PlayerState.ENDED) {{
                    document.getElementById('status').innerText = "🔒 5초 미리듣기가 완료되었습니다!";
                }}
            }}
        </script>
    </body>
    </html>
    """
    components.html(yt_html, height=260)

# 게임 진행 화면
if not st.session_state.is_finished:
    st.markdown(f"### 🎵 Q{st.session_state.q_idx + 1}. 이 노래의 제목은?")
    
    render_youtube_5sec(current_q["youtube_id"], current_q["start_sec"])

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
    else:
        st.write("👍 수고하셨습니다! 다시 도전해보세요.")

    if st.button("다시 도전하기 🔄"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.is_finished = False
        st.rerun()
