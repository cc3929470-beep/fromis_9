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
        background: linear-gradient(-45deg, #E8FAF8, #FFF1F5, #EBF4FF, #dffff2) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 12s ease infinite !important;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

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

# 곡 데이터 (샘플 음원 링크 - 실제 MP3/AAC 파일 URL로 교체하여 사용 가능합니다)
QUIZ_DATA = [
    {
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "start_sec": 30,
        "answer": "Supersonic",
        "options": ["Supersonic", "WE GO", "Sky Runner", "Vitamin Me"]
    },
    {
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "start_sec": 20,
        "answer": "WE GO",
        "options": ["From", "WE GO", "I Like You Better", "하얀 그리움"]
    },
    {
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "start_sec": 15,
        "answer": "Sky Runner",
        "options": ["Supersonic", "Sky Runner", "Vitamin Me", "WE GO"]
    }
]

if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "is_finished" not in st.session_state:
    st.session_state.is_finished = False

current_q = QUIZ_DATA[st.session_state.q_idx]

# 접속 기기 내장 스피커 강제 라우팅 플레이어
def render_device_speaker_player(audio_url, start_sec):
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
        </style>
    </head>
    <body>
        <div class="card">
            <button class="btn-play" onclick="playOnDeviceSpeaker()">▶ 5초 하이라이트 듣기</button>
            <div class="status" id="txt-status">버튼을 누르면 기기 스피커로 5초간 재생됩니다.</div>
        </div>

        <audio id="audio-element" src="{audio_url}" preload="auto"></audio>

        <script>
            var timer = null;

            async function playOnDeviceSpeaker() {{
                var audio = document.getElementById('audio-element');
                var status = document.getElementById('txt-status');

                try {{
                    // 접속 기기의 기본 내장 출력 디바이스(Default Speaker) 검색 및 라우팅
                    if (typeof audio.setSinkId === 'function' && navigator.mediaDevices) {{
                        const devices = await navigator.mediaDevices.enumerateDevices();
                        const defaultSpeaker = devices.find(d => d.kind === 'audiooutput' && d.deviceId === 'default');
                        if (defaultSpeaker) {{
                            await audio.setSinkId(defaultSpeaker.deviceId);
                        }}
                    }}

                    audio.currentTime = {start_sec};
                    audio.volume = 1.0;
                    await audio.play();

                    status.innerText = "🎵 기기 스피커로 5초간 재생 중...";

                    if (timer) clearTimeout(timer);
                    timer = setTimeout(function() {{
                        audio.pause();
                        status.innerText = "🔒 5초 미리듣기가 완료되었습니다!";
                    }}, 5000);

                }} catch (err) {{
                    console.error("오디오 재생 오류:", err);
                    status.innerText = "⚠️ 재생 중 오류가 발생했습니다. 브라우저 설정을 확인해주세요.";
                }}
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=140)

# 게임 진행 화면
if not st.session_state.is_finished:
    st.markdown(f"### 🎵 Q{st.session_state.q_idx + 1}. 이 노래의 제목은?")
    
    render_device_speaker_player(current_q["audio_url"], current_q["start_sec"])

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
