import streamlit as st
import random

st.set_page_config(
    page_title="자기관리 운동 추천 챌린지",
    page_icon="🏆",
    layout="centered"
)

# -------------------
# 운동 데이터
# -------------------

exercise_data = {
    "상": [
        "버피 테스트",
        "HIIT",
        "스프린트",
        "점핑 런지",
        "마운틴 클라이머",
        "배틀 로프",
        "점핑 스쿼트",
        "푸쉬업 챌린지",
        "크로스핏 서킷",
        "인터벌 러닝"
    ],
    "중": [
        "조깅",
        "줄넘기",
        "자전거 타기",
        "계단 오르기",
        "맨몸 스쿼트",
        "빠른 걷기",
        "런지",
        "플랭크",
        "실내 사이클",
        "로잉 머신"
    ],
    "하": [
        "걷기",
        "요가",
        "스트레칭",
        "필라테스",
        "가벼운 산책",
        "명상 걷기",
        "폼롤러 운동",
        "코어 호흡 운동",
        "목·어깨 스트레칭",
        "전신 유연성 운동"
    ]
}

effects = {
    "상": "🔥 고강도 운동으로 체지방 감소 및 체력 향상",
    "중": "💪 균형 잡힌 체력과 근력 향상",
    "하": "🌱 건강 관리와 운동 습관 형성"
}

times = {
    "상": "15~25분",
    "중": "20~40분",
    "하": "20~60분"
}

missions = [
    "물 2L 마시기",
    "30분 일찍 자기",
    "10분 독서하기",
    "야식 먹지 않기",
    "계단 이용하기",
    "하루 5분 명상하기",
    "스마트폰 사용시간 줄이기",
    "비타민 챙겨 먹기",
    "산책 20분 하기",
    "감사일기 작성하기"
]

quotes = [
    "오늘의 작은 실천이 미래의 큰 변화를 만듭니다.",
    "꾸준함은 최고의 재능입니다.",
    "운동은 자신에게 주는 최고의 선물입니다.",
    "포기하지 않는 사람이 결국 성공합니다.",
    "어제보다 조금 더 나아지면 충분합니다."
]

# -------------------
# UI
# -------------------

st.title("🏆 자기관리 운동 추천 챌린지")

st.write("""
운동 강도와 목표를 선택하면
오늘의 운동과 자기관리 미션을 추천합니다.
""")

goal = st.selectbox(
    "🎯 자기관리 목표",
    [
        "체중 감량",
        "근력 향상",
        "체력 향상",
        "건강 관리",
        "스트레스 해소",
        "운동 습관 만들기"
    ]
)

level = st.radio(
    "🔥 운동 강도",
    ["상", "중", "하"],
    horizontal=True
)

# -------------------
# 추천 버튼
# -------------------

if st.button("🚀 운동 추천 받기", use_container_width=True):

    try:
        exercise = random.choice(exercise_data[level])
        mission = random.choice(missions)
        quote = random.choice(quotes)

        # 특별 효과
        st.balloons()
        st.snow()

        st.success("🎉 오늘의 운동 추천이 도착했습니다!")

        st.subheader(f"🏃 추천 운동 : {exercise}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("운동 강도", level)

        with col2:
            st.metric("추천 시간", times[level])

        st.info(effects[level])

        st.divider()

        st.subheader("🎯 오늘의 자기관리 미션")
        st.warning(mission)

        st.divider()

        st.subheader("💬 오늘의 동기부여")
        st.success(quote)

    except Exception as e:
        st.error(f"오류 발생: {e}")

# -------------------
# 랜덤 추천
# -------------------

st.divider()

if st.button("🎲 완전 랜덤 운동 추천", use_container_width=True):

    try:
        all_exercises = []

        for value in exercise_data.values():
            all_exercises.extend(value)

        random_exercise = random.choice(all_exercises)

        st.balloons()

        st.subheader("🎉 랜덤 운동 추천")

        st.success(random_exercise)

    except Exception as e:
        st.error(f"오류 발생: {e}")

# -------------------
# 운동 강도 안내
# -------------------

st.divider()

st.subheader("📊 운동 강도 가이드")

col1, col2, col3 = st.columns(3)

with col1:
    st.error("""
상 (고강도)

• HIIT
• 버피
• 스프린트
• 인터벌 러닝
• 크로스핏
""")

with col2:
    st.warning("""
중 (중강도)

• 조깅
• 줄넘기
• 자전거
• 런지
• 플랭크
""")

with col3:
    st.success("""
하 (저강도)

• 걷기
• 요가
• 스트레칭
• 필라테스
• 명상 걷기
""")

# -------------------
# 푸터
# -------------------

st.divider()

st.caption("🏆 꾸준한 운동과 작은 습관이 최고의 자기관리입니다.")
