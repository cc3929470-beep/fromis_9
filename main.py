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
    <div style="color: #4A5568; font-size: 0.95rem; font-weight: 600;">하이라이트 5초를 듣고 어떤 노래인지 맞춰보세요! ✨</div>
</div>
""", unsafe_allow_html=True)

# 곡 데이터 (프로미스나인 공식 유튜브 ID 및 5초 하이라이트 시작 시각)
QUIZ_DATA = [
    {
        "yt_id": "0LiQp7y8Wwc", # Supersonic
        "start_sec": 45,
        "answer": "Supersonic",
        "options": ["Supersonic", "WE GO", "Sky Runner", "Vitamin Me"]
    },
    {
        "yt_id": "HM633a928Bw", # WE GO
        "start_sec": 35,
        "answer": "WE GO",
        "options": ["From", "WE GO", "I Like You Better", "하얀 그리움"]
    },
    {
        "yt_id": "U3cK8eG_V-I", # Sky Runner
        "start_sec": 20,
        "answer": "Sky Runner",
        "options": ["Supersonic", "Sky Runner", "Vitamin Me", "WE GO"]
    },
    {
        "yt_id": "Y8gYm-E6bGA", # Vitamin Me
        "start_sec": 30,
        "answer": "Vitamin Me",
        "options": ["하얀 그리움", "From", "Vitamin Me", "I Like You Better"]
    },
    {
        "yt_id": "bKk2EaT5Vls", # I Like You Better
        "start_sec": 25,
        "answer": "I Like You Better",
        "options": ["I Like You Better", "Supersonic", "WE GO", "Sky Runner"]
    },
    {
        "yt_id": "Y89D9W0p_2A", # 하얀 그리움
        "start_sec": 40,
        "answer": "하얀 그리움",
        "options": ["From", "Vitamin Me", "하얀 그리움", "Sky Runner"]
    },
    {
        "yt_id": "7L9Y8K6zVjA", # From
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
    end_sec = start_sec + 5
    embed_src = f"https://www.youtube.com/embed/{yt_id}?start={start_sec}&end={end_sec}&autoplay=1&enablejsapi=1"
    
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
                
                // 기존 프레임 제거 및 초기화
                box.innerHTML = '';
                if(timer) clearTimeout(timer);

                // 새 문제 음원 iframe 동적 생성 (자동재생 적용)
                var iframe = document.createElement('iframe');
                iframe.setAttribute('src', '{embed_src}');
                iframe.setAttribute('allow', 'autoplay');
                box.appendChild(iframe);

                status.innerText = "🎵 프로미스나인 공식 음원 5초 재생 중...";

                // 정확히 5.5초 후 iframe 제거하여 음악 정지
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
    
    # 문제마다 새로고침 처리
    render_youtube_5sec_player(current_q["yt_id"], current_q["start_sec"], st.session_state.q_idx)

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
