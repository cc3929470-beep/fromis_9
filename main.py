import os
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="fromis_9 5초 음원 퀴즈", page_icon="🎵")

st.title("🎵 프로미스나인 5초 음원 맞히기")
st.caption("음원을 5초간 듣고 어떤 노래인지 맞춰보세요!")

# 지정해주신 7개 곡 기반 퀴즈 데이터
# 각 항목별 fallback_url은 assets에 파일이 없을 경우 대체 재생될 인터넷 오픈 mp3 링크입니다.
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

# 게임 진행 화면
if not st.session_state.is_finished:
    st.subheader(f"문제 {st.session_state.q_idx + 1} / {len(QUIZ_DATA)}")
    
    # --- 음원 로드 및 예외 처리 구문 ---
    audio_file_path = current_q["audio_url"]
    
    if os.path.exists(audio_file_path):
        # 파일이 로컬/서버 폴더에 존재하는 경우 정상 재생
        st.audio(audio_file_path, start_time=0, end_time=5)
    else:
        # 파일이 없을 경우 에러로 튕기지 않고 경고 노출 후 샘플 음원으로 대체
        st.warning(f"⚠️ '{audio_file_path}' 파일을 찾을 수 없어 테스트용 샘플 음원을 재생합니다. GitHub의 assets 폴더에 MP3 파일을 업로드해주세요.")
        st.audio(current_q["fallback_url"], start_time=0, end_time=5)

    # 보기 선택
    user_choice = st.radio(
        "이 노래의 제목은 무엇일까요?", 
        current_q["options"], 
        key=f"q_{st.session_state.q_idx}"
    )

    # 정답 제출 버튼
    if st.button("정답 제출"):
        if user_choice == current_q["answer"]:
            st.success("정답입니다! 🎉")
            st.session_state.score += 10
        else:
            st.error(f"아쉽네요! 정답은 [{current_q['answer']}] 입니다. 😅")

        # 다음 문제 이동 처리
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
    elif st.session_state.score >= 40:
        st.write("🥈 훌륭한 실력이에요! 조금만 더 연습해보세요.")
    else:
        st.write("👍 수고하셨습니다! 다시 한번 도전해보세요.")

    if st.button("다시 하기"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.is_finished = False
        st.rerun()
