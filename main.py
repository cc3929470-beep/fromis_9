import os
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="fromis_9 5초 음원 퀴즈",
    page_icon="🍀",
    layout="centered"
)

# 프로미스나인 컨셉 Custom CSS
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #E6FAFA 0%, #FFF0F5 50%, #F0F7FF 100%);
    }

    .fromis-header {
        text-align: center;
        padding: 25px 20px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        border: 2px solid #5DE2A4;
        box-shadow: 0 10px 30px rgba(93, 226, 164, 0.2);
        margin-bottom: 25px;
    }

    .fromis-badge {
        display: inline-block;
        background: linear-gradient(90deg, #5DE2A4, #4DA1FF);
        color: white;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 5px 16px;
        border-radius: 20px;
        letter-spacing: 1px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(77, 161, 255, 0.3);
    }

    .fromis-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF6B9D, #4DA1FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 5px 0;
    }

    .fromis-subtitle {
        color: #556B2F;
        font-size: 0.95rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="fromis-header">
    <span class="fromis-badge">🍀 FLOVER MUSIC QUIZ</span>
    <div class="fromis-title">프로미스나인 5초 음원 맞히기</div>
    <div class="fromis-subtitle">음원을 5초간 듣고 어떤 노래인지 맞춰보세요!</div>
</div>
""", unsafe_allow_html=True)

# 백업 샘플 URL이 추가된 퀴즈 데이터
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

# 5초 제한 커스텀 오디오 플레이어 컴포넌트
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
                background: linear-gradient(135deg, #ffffff 0%, #F0FFF8 100%);
                border: 2px solid #5DE2A4;
                border-radius: 20px;
                padding: 18px;
                box-shadow: 0 10px 25px rgba(93, 226, 164, 0.25);
                text-align: center;
                max-width: 480px;
                margin: 0 auto;
            }}
            .timer-badge {{
                display: inline-block;
                background-color: #FF7597;
                color: white;
                font-size: 0.85rem;
                font-weight: 700;
                padding: 4px 12px;
                border-radius: 12px;
                margin-bottom: 12px;
            }}
            .controls {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                margin-bottom: 12px;
            }}
            .btn-play {{
                background: linear-gradient(135deg, #5DE2A4, #3BCEAC);
                border: none;
                color: white;
                font-weight: 700;
                font-size: 0.95rem;
                padding: 10px 24px;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(93, 226, 164, 0.4);
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
                padding: 6px 10px;
                border-radius: 8px;
                border: 1.5px solid #5DE2A4;
                font-size: 0.8rem;
                outline: none;
                background-color: #FFF;
            }}

            .progress-bar-container {{
                width: 100%;
                background-color: #E2F4EC;
                height: 8px;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 8px;
            }}
            .progress-bar {{
                width: 0%;
                height: 100%;
                background: linear-gradient(90deg, #FF7597, #5DE2A4);
                transition: width 0.1s linear;
            }}
            .time-display {{
                font-size: 0.85rem;
                color: #666;
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
            <button class="btn-play" style="background: #A0AEC0;" onclick="resetAudio()">🔄 처음부터</button>
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
                    alertMsg.style.color = '#5DE2A4';
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
                statusBadge.style.backgroundColor = '#5DE2A4';
                statusBadge.innerText = '🎵 5초 미니 플레이 중...';
            }} else {{
                audio.pause();
                playBtn.innerHTML = '▶ 재생하기';
                statusBadge.style.backgroundColor = '#FF7597';
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
            statusBadge.style.backgroundColor = '#FF7597';
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
                statusBadge.style.backgroundColor = '#A0AEC0';
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
    st.subheader(f"문제 {st.session_state.q_idx + 1} / {len(QUIZ_DATA)}")
    
    # MP3 파일 검사 후 파일이 없으면 자동 fallback 처리
    audio_path = current_q["audio_url"]
    if os.path.exists(audio_path):
        render_5sec_player(audio_path)
    else:
        st.info("💡 MP3 파일이 없어 샘플 테스트 음원으로 대체 재생합니다. (assets 폴더에 MP3를 넣으시면 실제 노래가 재생됩니다)")
        render_5sec_player(current_q["fallback_url"])

    # 보기 선택
    user_choice = st.radio(
        "이 노래의 제목은 무엇일까요?", 
        current_q["options"], 
        key=f"q_{st.session_state.q_idx}"
    )

    # 제출 버튼
    if st.button("정답 제출"):
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
        st.write("🥇 만점입니다! 당신은 완벽한 플로버(flover)입니다.")
    elif st.session_state.score >= 50:
        st.write("🥈 훌륭한 실력이에요!")
    else:
        st.write("👍 수고하셨습니다! 다시 한번 도전해보세요.")

    if st.button("다시 하기"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.is_finished = False
        st.rerun()

st.markdown("""
<div style="margin-top: 30px; text-align: center; color: #888; font-size: 0.85rem;">
    🍀 FLOVER Fan Zone | 프로미스나인 5초 음원 퀴즈
</div>
""", unsafe_allow_html=True)
