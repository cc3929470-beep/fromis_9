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
    
    /* 전체 배경: 프로미스나인 특유의 산뜻하고 화사한 수채화 톤 */
    .stApp {
        background: linear-gradient(135deg, #E8FAF8 0%, #FFF1F5 50%, #EBF4FF 100%) !important;
    }

    /* 메인 헤더 디자인 */
    .fromis-header {
        text-align: center;
        padding: 30px 20px;
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 28px;
        border: 2px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 15px 35px rgba(93, 226, 164, 0.15), 0 5px 15px rgba(255, 117, 151, 0.1);
        margin-bottom: 25px;
    }

    /* 상단 배지 */
    .fromis-badge {
        display: inline-block;
        background: linear-gradient(90deg, #3BCEAC 0%, #FF7597 100%);
        color: white;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 6px 18px;
        border-radius: 20px;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(59, 206, 172, 0.35);
    }

    /* 타이틀 텍스트 */
    .fromis-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B8B, #22D3EE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 6px 0;
        letter-spacing: -0.5px;
    }

    /* 서브타이틀 */
    .fromis-subtitle {
        color: #4A5568;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 6px;
    }

    /* 라디오 버튼 선택창 감성 스타일링 */
    div[data-testid="stRadio"] > label {
        font-weight: 700 !important;
        color: #2D3748 !important;
    }

    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.6);
        padding: 15px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 8px 20px rgba(0,0,0,0.03);
    }

    /* 기본 버튼 디자인 커스텀 */
    .stButton>button {
        background: linear-gradient(135deg, #FF7597 0%, #FF4B8B 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 18px !important;
        border: none !important;
        padding: 10px 28px !important;
        box-shadow: 0 6px 20px rgba(255, 75, 139, 0.3) !important;
        transition: all 0.25s ease !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(255, 75, 139, 0.45) !important;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="fromis-header">
    <span class="fromis-badge">🍀 FLOVER MUSIC QUIZ</span>
    <div class="fromis-title">프로미스나인 5초 음원 맞히기</div>
    <div class="fromis-subtitle">음원을 5초간 듣고 어떤 노래인지 맞춰보세요! ✨</div>
</div>
""", unsafe_allow_html=True)

# 퀴즈 데이터
QUIZ_DATA = [
    {
        "audio_url": "assets/supersonic.mp3",
        "fallback_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "answer": "Supersonic",
        "options": ["Supersonic", "WE GO", "Sky Runner", "Vitamin Me"]
    },
    {
        "audio_url": "assets/we_go.mp3",
        "fallback_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "answer": "WE GO",
        "options": ["From", "WE GO", "I Like You Better", "하얀 그리움"]
    },
    {
        "audio_url": "assets/sky_runner.mp3",
        "fallback_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "answer": "Sky Runner",
        "options": ["Supersonic", "Sky Runner", "Vitamin Me", "WE GO"]
    },
    {
        "audio_url": "assets/vitamin_me.mp3",
        "fallback_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "answer": "Vitamin Me",
        "options": ["하얀 그리움", "From", "Vitamin Me", "I Like You Better"]
    },
    {
        "audio_url": "assets/i_like_you_better.mp3",
        "fallback_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
        "answer": "I Like You Better",
        "options": ["I Like You Better", "Supersonic", "WE GO", "Sky Runner"]
    },
    {
        "audio_url": "assets/hayan_geurium.mp3",
        "fallback_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
        "answer": "하얀 그리움",
        "options": ["From", "Vitamin Me", "하얀 그리움", "Sky Runner"]
    },
    {
        "audio_url": "assets/from.mp3",
        "fallback_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
        "answer": "From",
        "options": ["WE GO", "From", "I Like You Better", "Supersonic"]
    }
]

# 세션 상태 초기화
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "is_finished" not in st.session_state:
    st.session_state.is_finished = False

current_q = QUIZ_DATA[st.session_state.q_idx]

# 5초 제한 커스텀 플레이어 (청량 파스텔 테마)
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
            }}
            .player-container {{
                background: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(12px);
                border: 2px solid #FFFFFF;
                border-radius: 24px;
                padding: 20px;
                box-shadow: 0 12px 30px rgba(59, 206, 172, 0.18);
                text-align: center;
                max-width: 480px;
                margin: 0 auto;
            }}
            .timer-badge {{
                display: inline-block;
                background: linear-gradient(135deg, #FF7597, #FF4B8B);
                color: white;
                font-size: 0.85rem;
                font-weight: 700;
                padding: 5px 14px;
                border-radius: 20px;
                margin-bottom: 12px;
                box-shadow: 0 4px 10px rgba(255, 117, 151, 0.3);
            }}
            .controls {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                margin-bottom: 12px;
            }}
            .btn-play {{
                background: linear-gradient(135deg, #3BCEAC, #22D3EE);
                border: none;
                color: white;
                font-weight: 700;
                font-size: 0.95rem;
                padding: 10px 24px;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(59, 206, 172, 0.35);
                transition: all 0.2s ease;
            }}
            .btn-play:hover {{ transform: translateY(-2px); }}
            
            .device-select-box {{
                margin: 10px 0 15px 0;
                text-align: left;
            }}
            .device-label {{
                font-size: 0.8rem;
                font-weight: 700;
                color: #4A5568;
                margin-bottom: 4px;
                display: block;
            }}
            .device-select {{
                width: 100%;
                padding: 8px 12px;
                border-radius: 12px;
                border: 1.5px solid #3BCEAC;
                font-size: 0.8rem;
                outline: none;
                background-color: rgba(255, 255, 255, 0.9);
                color: #2D3748;
            }}

            .progress-bar-container {{
                width: 100%;
                background-color: #E2F8F4;
                height: 8px;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 8px;
            }}
            .progress-bar {{
                width: 0%;
                height: 100%;
                background: linear-gradient(90deg, #3BCEAC, #FF7597);
                transition: width 0.1s linear;
            }}
            .time-display {{
                font-size: 0.85rem;
                color: #718096;
                font-weight: 600;
            }}
            .alert-msg {{
                color: #FF4757;
                font-size: 0.8rem;
                font-weight: 700;
                margin-top: 6px;
                height: 16px;
            }}
        </style>
    </head>
    <body>

    <div class="player-container">
        <div class="timer-badge" id="statusBadge">⏱️ 최대 5초 감상 가능</div>
        
        <audio id="myAudio" src="{source}" preload="metadata"></audio>
        
        <div class="device-select-box">
            <label class="device-label" for="audioOutputSelect">🎧 사운드 출력 장치:</label>
            <select id="audioOutputSelect" class="device-select" onchange="changeAudioOutput()">
                <option value="">장치 검색 중...</option>
            </select>
        </div>

        <div class="controls">
            <button class="btn-play" id="playBtn" onclick="togglePlay()">▶ 재생하기</button>
            <button class="btn-play" style="background: #A0AEC0; box-shadow: none;" onclick="resetAudio()">🔄 처음부터</button>
        </div>

        <div class="progress-bar-container">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <div class="time-display">
            <span id="currentTime">00:00</span> / <span id="maxTime">00:05</span>
        </div>
        <div class="alert-msg" id="alertMsg"></div>
    </div>

    <script>
        const audio = document.getElementById('myAudio');
        const playBtn = document.getElementById('playBtn');
        const progressBar = document.getElementById('progressBar');
        const currentTimeElem = document.getElementById('currentTime');
        const alertMsg = document.getElementById('alertMsg');
        const statusBadge = document.getElementById('statusBadge');
        const audioOutputSelect = document.getElementById('audioOutputSelect');

        const MAX_SECONDS = 5.0;

        async function loadAudioOutputDevices() {{
            if (!('setSinkId' in HTMLAudioElement.prototype)) {{
                audioOutputSelect.innerHTML = '<option value="">기본 브라우저 출력 장치 사용 중</option>';
                audioOutputSelect.disabled = true;
                return;
            }}

            try {{
                await navigator.mediaDevices.getUserMedia({{ audio: true }});
                const devices = await navigator.mediaDevices.enumerateDevices();
                const audioOutputs = devices.filter(device => device.kind === 'audiooutput');

                audioOutputSelect.innerHTML = '';
                if (audioOutputs.length === 0) {{
                    audioOutputSelect.innerHTML = '<option value="">출력 장치를 찾을 수 없습니다</option>';
                    return;
                }}

                audioOutputs.forEach((device, index) => {{
                    const option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = device.label || `출력 장치 ${{index + 1}}`;
                    audioOutputSelect.appendChild(option);
                }});
            }} catch (err) {{
                audioOutputSelect.innerHTML = '<option value="">기본 출력 장치 사용 중</option>';
            }}
        }}

        async function changeAudioOutput() {{
            const deviceId = audioOutputSelect.value;
            if (typeof audio.setSinkId === 'function' && deviceId) {{
                try {{
                    await audio.setSinkId(deviceId);
                    alertMsg.style.color = '#3BCEAC';
                    alertMsg.innerText = '🔊 출력 장치가 변경되었습니다.';
                }} catch (err) {{
                    alertMsg.style.color = '#FF4757';
                    alertMsg.innerText = '⚠️ 출력 장치 변경 실패';
                }}
            }}
        }}

        loadAudioOutputDevices();

        function togglePlay() {{
            if (audio.paused) {{
                if (audio.currentTime >= MAX_SECONDS) {{
                    audio.currentTime = 0;
                }}
                audio.play();
                playBtn.innerHTML = '⏸ 정지';
                alertMsg.innerText = '';
                statusBadge.style.background = 'linear-gradient(135deg, #3BCEAC, #22D3EE)';
                statusBadge.innerText = '🎵 5초 미니 플레이 중...';
            }} else {{
                audio.pause();
                playBtn.innerHTML = '▶ 재생하기';
                statusBadge.style.background = 'linear-gradient(135deg, #FF7597, #FF4B8B)';
                statusBadge.innerText = '⏱️ 일시정지됨';
            }}
        }}

        function resetAudio() {{
            audio.pause();
            audio.currentTime = 0;
            playBtn.innerHTML = '▶ 재생하기';
            progressBar.style.width = '0%';
            currentTimeElem.innerText = '00:00';
            alertMsg.innerText = '';
            statusBadge.style.background = 'linear-gradient(135deg, #FF7597, #FF4B8B)';
            statusBadge.innerText = '⏱️ 최대 5초 감상 가능';
        }}

        audio.addEventListener('timeupdate', () => {{
            const current = audio.currentTime;
            
            if (current >= MAX_SECONDS) {{
                audio.pause();
                audio.currentTime = MAX_SECONDS;
                playBtn.innerHTML = '▶ 재생하기';
                progressBar.style.width = '100%';
                currentTimeElem.innerText = '00:05';
                alertMsg.style.color = '#FF4757';
                alertMsg.innerText = '🔒 5초 미리듣기가 완료되었습니다!';
                statusBadge.style.background = '#A0AEC0';
                statusBadge.innerText = '🔒 5초 제한 완료';
                return;
            }}

            const percentage = (current / MAX_SECONDS) * 100;
            progressBar.style.width = percentage + '%';
            
            const secs = Math.floor(current);
            currentTimeElem.innerText = `00:0${{secs}}`;
        }});

        audio.addEventListener('ended', () => {{
            playBtn.innerHTML = '▶ 재생하기';
        }});
    </script>

    </body>
    </html>
    """
    components.html(player_html, height=290)

# 게임 진행 화면
if not st.session_state.is_finished:
    st.markdown(f"### 🎵 Q{st.session_state.q_idx + 1}. 이 노래의 제목은?")
    
    audio_path = current_q["audio_url"]
    if os.path.exists(audio_path):
        render_5sec_player(audio_path)
    else:
        st.info("💡 MP3 파일이 없어 테스트용 예시 음원으로 재생합니다.")
        render_5sec_player(current_q["fallback_url"])

    st.write("")
    
    user_choice = st.radio(
        "정답을 선택해주세요:", 
        current_q["options"], 
        key=f"q_{st.session_state.q_idx}"
    )

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
        st.write("🥈 훌륭한 실력이에요! 조금만 더 하면 만점!")
    else:
        st.write("👍 수고하셨습니다! 프로미스나인 노래를 더 듣고 재도전해보세요!")

    if st.button("다시 도전하기 🔄"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.is_finished = False
        st.rerun()

st.markdown("""
<div style="margin-top: 40px; text-align: center; color: #718096; font-size: 0.85rem; font-weight: 500;">
    🍀 FLOVER Fan Zone | fromis_9 Music Quiz
</div>
""", unsafe_allow_html=True)
