import base64
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="fromis_9 FLOVER 5초 미리듣기",
    page_icon="🍀",
    layout="centered"
)

# 프로미스나인 컨셉 Custom CSS
st.markdown("""
<style>
    @import url('[https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css](https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css)');
    
    * {
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 전체 배경 그라데이션 (상큼한 민트 & 핑크 파스텔) */
    .stApp {
        background: linear-gradient(135deg, #E6FAFA 0%, #FFF0F5 50%, #F0F7FF 100%);
    }

    /* 메인 타이틀 스타일ing */
    .fromis-header {
        text-align: center;
        padding: 25px 20px;
        background: rgba(255, 255, 255, 0.75);
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

    /* 스트림릿 카드 스타일 */
    .css-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(93, 226, 164, 0.3);
        box-shadow: 0 8px 20px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown("""
<div class="fromis-header">
    <span class="fromis-badge">🍀 FLOVER SPECIAL PREVIEW</span>
    <div class="fromis-title">fromis_9 🎵 5초 미리듣기</div>
    <div class="fromis-subtitle">상큼한 프로미스나인 감성의 5초 제한 오디오 플레이어</div>
</div>
""", unsafe_allow_html=True)

# 사이드바 설정
st.sidebar.title("🍀 옵션 선택")

audio_option = st.sidebar.radio(
    "음원 선택 방식",
    ["기본 샘플 음악", "MP3 파일 직접 업로드"]
)

audio_src = ""

if audio_option == "기본 샘플 음악":
    # 샘플 음원 URL
    audio_src = "[https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3](https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3)"
    st.sidebar.info("💡 샘플 음원이 선택되었습니다.")
else:
    uploaded_file = st.sidebar.file_uploader("MP3 음원 파일을 업로드하세요", type=["mp3", "wav", "ogg"])
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        b64_audio = base64.b64encode(audio_bytes).decode()
        audio_src = f"data:audio/mp3;base64,{b64_audio}"
        st.sidebar.success("✅ 파일 업로드 완료!")
    else:
        st.sidebar.warning("음원 파일을 업로드해주세요.")

# 5초 제한 커스텀 HTML/JS 오디오 플레이어 컴포넌트
def render_5sec_player(source):
    player_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('[https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css](https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css)');
            body {{
                font-family: 'Pretendard', sans-serif;
                margin: 0;
                padding: 10px;
                background: transparent;
            }}
            .player-container {{
                background: linear-gradient(135deg, #ffffff 0%, #F0FFF8 100%);
                border: 2px solid #5DE2A4;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 10px 25px rgba(93, 226, 164, 0.25);
                text-align: center;
                max-width: 480px;
                margin: 0 auto;
            }}
            .song-info {{
                font-weight: 700;
                font-size: 1.1rem;
                color: #2E4057;
                margin-bottom: 6px;
            }}
            .timer-badge {{
                display: inline-block;
                background-color: #FF7597;
                color: white;
                font-size: 0.85rem;
                font-weight: 700;
                padding: 4px 12px;
                border-radius: 12px;
                margin-bottom: 15px;
            }}
            .controls {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
                margin-bottom: 15px;
            }}
            .btn-play {{
                background: linear-gradient(135deg, #5DE2A4, #3BCEAC);
                border: none;
                color: white;
                font-weight: 700;
                font-size: 1rem;
                padding: 12px 28px;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(93, 226, 164, 0.4);
                transition: all 0.2s ease;
            }}
            .btn-play:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(93, 226, 164, 0.6);
            }}
            .btn-play:active {{
                transform: translateY(0);
            }}
            .progress-bar-container {{
                width: 100%;
                background-color: #E2F4EC;
                height: 10px;
                border-radius: 5px;
                overflow: hidden;
                margin-bottom: 10px;
            }}
            .progress-bar {{
                width: 0%;
                height: 100%;
                background: linear-gradient(90deg, #FF7597, #5DE2A4);
                transition: width 0.1s linear;
            }}
            .time-display {{
                font-size: 0.9rem;
                color: #666;
                font-weight: 600;
            }}
            .alert-msg {{
                color: #FF4757;
                font-size: 0.82rem;
                font-weight: 700;
                margin-top: 8px;
                height: 18px;
            }}
        </style>
    </head>
    <body>

    <div class="player-container">
        <div class="song-info">🍀 5-SEC LIMITED PREVIEW</div>
        <div class="timer-badge" id="statusBadge">⏱️ 최대 5초 감상 가능</div>
        
        <audio id="myAudio" src="{source}" preload="metadata"></audio>
        
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

        const MAX_SECONDS = 5.0; // 5초 제한

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

        // 재생 시간 실시간 체크 (5초 초과 시 차단)
        audio.addEventListener('timeupdate', () => {{
            const current = audio.currentTime;
            
            if (current >= MAX_SECONDS) {{
                audio.pause();
                audio.currentTime = MAX_SECONDS;
                playBtn.innerHTML = '▶ 재생하기';
                progressBar.style.width = '100%';
                currentTimeElem.innerText = '00:05';
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
    components.html(player_html, height=280)

# 메인 콘텐츠 화면
if audio_src:
    render_5sec_player(audio_src)
else:
    st.warning("👈 사이드바에서 음원을 선택하거나 업로드해 주세요!")

# 하단 커스텀 카드 영역
st.markdown("""
<div style="margin-top: 30px; text-align: center; color: #888; font-size: 0.85rem;">
    🍀 FLOVER Fan Zone | 프로미스나인 스페셜 타이머 플레이어
</div>
""", unsafe_allow_html=True)
