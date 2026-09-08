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
    
    /* 1. 움직이는 파스텔 그라데이션 애니메이션 배경 */
    .stApp {
        background: linear-gradient(-45deg, #E8FAF8, #FFF1F5, #EBF4FF, #dffff2) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 12s ease infinite !important;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. 메인 컨텐츠 영역 글래스모피즘 */
    .block-container {
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 3rem 2rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(142, 209, 252, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.6);
    }

    /* 3. 헤더 영역 업그레이드 */
    .fromis-header {
        text-align: center;
        padding: 30px 20px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px);
        border-radius: 28px;
        border: 2px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 15px 35px rgba(93, 226, 164, 0.2);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    .fromis-header::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: linear-gradient(
            to right, 
            rgba(255,255,255,0) 0%, 
            rgba(255,255,255,0.6) 50%, 
            rgba(255,255,255,0) 100%
        );
        transform: rotate(45deg);
        animation: shine 4s infinite;
        pointer-events: none;
    }

    @keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }

    .fromis-badge {
        display: inline-block;
        background: linear-gradient(90deg, #3BCEAC 0%, #FF7597 100%);
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        padding: 8px 22px;
        border-radius: 20px;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(255, 117, 151, 0.3);
    }

    .fromis-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B8B, #22D3EE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
    }

    /* 선택지 라디오 버튼 */
    div[data-testid="stRadio"] > label { 
        font-weight: 800 !important; 
        color: #2D3748 !important; 
        font-size: 1.05rem;
    }

    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.75);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.02);
    }

    /* 정답 제출 버튼 */
    .stButton>button {
        background: linear-gradient(135deg, #FF7597 0%, #FF4B8B 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 12px 30px !important;
        box-shadow: 0 6px 20px rgba(255, 75, 139, 0.3) !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(255, 75, 139, 0.5) !important;
    }

    /* 오디오 안내 박스 스타일 */
    .audio-notice {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 117, 151, 0.3);
        border-radius: 12px;
        padding: 10px;
        font-size: 0.8rem;
        color: #555;
        margin-top: 10px;
        text-align: center;
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

# 곡 데이터
QUIZ_DATA = [
    {
        "yt_id": "OrrZ-TiTbPg", # Supersonic
        "start_sec": 45,
        "answer": "Supersonic",
        "options": ["Supersonic", "WE GO", "Sky Runner", "Vitamin Me"]
    },
    {
        "yt_id": "sWyZMFmTfQs", # WE GO
        "start_sec": 35,
        "answer": "WE GO",
        "options": ["From", "WE GO", "I Like You Better", "하얀 그리움"]
    },
    {
        "yt_id": "J_Ou8BsADlA", # Sky Runner
        "start_sec": 20,
        "answer": "Sky Runner",
        "options": ["Supersonic", "Sky Runner", "Vitamin Me", "WE GO"]
    },
    {
        "yt_id": "hFVehbANxQE", # Vitamin Me
        "start_sec": 30,
        "answer": "Vitamin Me",
        "options": ["하얀 그리움", "From", "Vitamin Me", "I Like You Better"]
    },
    {
        "yt_id": "4pXfGL4tiTE", # I Like You Better
        "start_sec": 25,
        "answer": "I Like You Better",
        "options": ["I Like You Better", "Supersonic", "WE GO", "Sky Runner"]
    },
    {
        "yt_id": "gkJsrDEVask", # 하얀 그리움
        "start_sec": 40,
        "answer": "하얀 그리움",
        "options": ["From", "Vitamin Me", "하얀 그리움", "Sky Runner"]
    },
    {
        "yt_id": "ZuCc2Oi2fM0", # From
        "start_sec": 30,
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

# 유튜브 공식 음원 5초 렌더링 함수
def render_youtube_5sec_player(yt_id, start_sec, q_num):
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
                position: absolute;
                width: 1px;
                height: 1px;
                opacity: 0.01;
                overflow: hidden;
                left: -9999px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <button class="btn-play" onclick="startPlay()">▶ 5초 하이라이트 듣기</button>
            <div class="status" id="txt-status">버튼을 누르면 공식 음원이 5초간 재생됩니다.</div>
        </div>

        <div class="hidden-yt">
            <div id="player"></div>
        </div>

        <script>
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

            var player;
            var timer = null;
            var isReady = false;

            function onYouTubeIframeAPIReady() {{
                player = new YT.Player('player', {{
                    height: '1',
                    width: '1',
                    videoId: '{yt_id}',
                    playerVars: {{
                        'playsinline': 1,
                        'controls': 0,
                        'disablekb': 1,
                        'rel': 0
                    }},
                    events: {{
                        'onReady': onPlayerReady
                    }}
                }});
            }}

            function onPlayerReady(event) {{
                isReady = true;
            }}

            function startPlay() {{
                var status = document.getElementById('txt-status');
                if (!isReady || !player) {{
                    status.innerText = "⏳ 음원을 불러오는 중입니다. 잠시 후 다시 눌러주세요.";
                    return;
                }}

                if (timer) clearTimeout(timer);

                // 재생 및 볼륨/음소거 해제 강제 적용
                player.unMute();
                player.setVolume(100);
                player.seekTo({start_sec}, true);
                player.playVideo();

                status.innerText = "🎵 프로미스나인 공식 음원 5초 재생 중...";

                timer = setTimeout(function() {{
                    player.pauseVideo();
                    status.innerText = "🔒 5초 미리듣기가 완료되었습니다!";
                }}, 5000);
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=140)

# 게임 진행 화면
if not st.session_state.is_finished:
    st.markdown(f"### 🎵 Q{st.session_state.q_idx + 1}. 이 노래의 제목은?")
    
    render_youtube_5sec_player(current_q["yt_id"], current_q["start_sec"], st.session_state.q_idx)

    # 출력 기기 체크 안내 메시지
    st.markdown("""
    <div class="audio-notice">
        💡 <b>소리가 들리지 않나요?</b><br>
        • PC/모바일의 시스템 미디어 볼륨을 확인해주세요.<br>
        • 아이폰(iOS)의 경우 무음 모드 스위치가 켜져 있으면 소리가 나지 않을 수 있습니다.<br>
        • 블루투스 이어폰 연결 상태를 점검해주세요.
    </div>
    """, unsafe_allow_html=True)

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
            if st.button("다음 문제로 ➡️", key=f"btn_next_{st.session_state.q_idx}"):
                st.session_state.q_idx += 1
                st.rerun()
        else:
            if st.button("결과 확인하기 🏆", key="btn_finish"):
                st.session_state.is_finished = True
                st.rerun()

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
