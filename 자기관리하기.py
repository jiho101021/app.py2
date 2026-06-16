import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 디자인
st.set_page_config(
    page_title="마인드내비 - 일상 & 연애 자기관리",
    page_icon="🌱",
    layout="centered"
)

# 불필요한 테두리 스타일을 제거하고 깔끔하게 다듬은 CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #FFF5F7 0%, #F4F7FF 100%); }
    .main-title { color: #4A4E69; font-size: 2.8rem !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #666; text-align: center; font-size: 1.1rem; margin-bottom: 25px; }
    .content-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(74, 78, 105, 0.15);
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 15px;
        color: #2B2D42;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4A4E69 0%, #9A8C98 100%);
        color: white; border: none; border-radius: 10px; padding: 10px; font-weight: 600; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(74, 78, 105, 0.3); }
    </style>
""", unsafe_allow_html=True)

# 2. Gemini API 초기화
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets에서 'GEMINI_API_KEY'를 설정해주세요.")
    st.stop()

# 3. 헤더
st.markdown("<h1 class='main-title'>🌱 마인드내비 (MindNavi)</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>일상의 무기력함부터 연애의 흔들림까지, 나를 지키는 자기관리</p>", unsafe_allow_html=True)

# --- 🌡️ 실시간 마음 흔들림 온도계 ---
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("#### 🌡️ 지금 나의 멘탈 흔들림 지수")
anxiety_score = st.slider("현재 내 마음의 불안도나 스트레스는 어느 정도인가요?", 0, 100, 30)
if anxiety_score >= 70:
    st.error(f"🚨 **위험 (불안도 {anxiety_score}%)**: 감정 에너지가 과부하된 상태입니다. 즉시 하던 일을 멈추고 심호흡을 하세요.")
elif anxiety_score >= 40:
    st.warning(f"💛 **주의 (불안도 {anxiety_score}%)**: 서운함, 잡념, 혹은 무기력이 시작되고 있네요. 환기가 필요한 시점입니다.")
else:
    st.success(f"💚 **안정 (불안도 {anxiety_score}%)**: 일상과 감정의 밸런스가 아주 좋습니다. 이 상태을 유지해보세요!")
st.markdown("</div>", unsafe_allow_html=True)

# 4. 기능별 대시보드 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["🔥 일상 해결", "💘 연애 해결", "📊 멘탈 성향 테스트", "🤖 AI 상담소"])

# 탭 1: 일상 자기관리 고정 문답
with tab1:
    st.markdown("### 🔍 내 일상을 방해하는 문제점 해결")
    st.caption("가장 공감되는 나만의 일상 문제를 선택해 즉시 솔루션을 확인하세요.")
    
    col1, col2 = st.columns(2)
    daily_problems = {
        "⏰ 스마트폰 중독 / 도파민 중독": "지금 당장 폰을 **'화면이 바닥을 보게'** 물리적으로 먼 곳에 두세요. 그리고 딱 5분만 스쿼트를 하거나 물을 마시고 오세요. 뇌의 회로를 바꾸는 데는 5분의 환기가 필요합니다.",
        "💤 무기력증 / 아무것도 하기 싫음": "큰 일을 하려고 하지 마세요. **'침대 이불 정리하기'**, **'일어나서 기지개 켜기'** 같은 1분짜리 초소형 미션부터 시작하세요. 아주 작은 성취감이 뇌를 깨웁니다.",
        "🤯 할 일이 너무 많아 혼란스러움": "종이와 펜을 꺼내 오늘 해야 할 일을 딱 3 가지만 적으세요. 나머지는 내일로 미룹니다. 지금은 그 중 **가장 하기 싫고 중요한 1가지**에만 25분간 집중하세요.",
        "🥺 타인과의 비교로 인한 우울": "인스타그램이나 SNS 앱을 즉시 종료하세요. 타인의 하이라이트와 나의 비하인드 스토리를 비교하면 불행해집니다. 시선을 내 방, 내 일상으로 돌리세요."
    }
    keys_daily = list(daily_problems.keys())
    with col1:
        if st.button("⏰ 스마트폰 중독"): st.info(daily_problems[keys_daily[0]])
        if st.button("🤯 할 일이 넘쳐남"): st.info(daily_problems[keys_daily[2]])
    with col2:
        if st.button("💤 무기력증 폭발"): st.info(daily_problems[keys_daily[1]])
        if st.button("🥺 비교와 우울감"): st.info(daily_problems[keys_daily[3]])

# 탭 2: 연애 멘탈케어 고정 문답
with tab2:
    st.markdown("### 🚨 내 연애를 흔드는 순간, 행동 지침")
    st.caption("상대방에게 휘둘리지 않고 내 중심을 잡기 위한 멘탈 처방전입니다.")
    
    col3, col4 = st.columns(2)
    love_problems = {
        "📱 연락에 과도하게 집착하게 될 때": "상대방의 답장에 내 행복을 저당 잡히지 마세요. 지금 알림을 무음으로 끄고, 내가 좋아하는 영상을 보거나 밖으로 산책을 나가세요. 내가 바쁠 때 연애 주도권도 따라옵니다.",
        "🤬 서운함이 욱하고 올라올 때": "메모장에 서운한 이유를 감정 빼고 글로 적어보세요. 1시간 뒤에 다시 읽어보면 홧김에 해서 상처 줄 말들을 걸러내고 건강한 대화를 할 수 있습니다.",
        "🎣 어장관리 당하는 것 같을 때": "나를 헷갈리게 하는 사람은 나를 좋아하지 않는 겁니다. 과감하게 한 걸음 물러서서 내 일상에 집중해 보세요. 굳이 애매한 인연에 에너지를 쓸 필요 없습니다.",
        "💔 이별 후 전연인 SNS 염탐할 때": "전연인의 SNS는 내 멘탈을 갉아먹는 독입니다. 지금 즉시 차단하거나 숨김 처리하세요. 과거의 미련을 냉정하게 잘라내야 더 가치 있는 다음 사랑이 찾아옵니다."
    }
    keys_love = list(love_problems.keys())
    with col3:
        if st.button("📱 연락에 자꾸 집착해요"): st.info(love_problems[keys_love[0]])
        if st.button("🎣 어장관리 인가요?"): st.info(love_problems[keys_love[2]])
    with col4:
        if st.button("🤬 사소한 일에 서운해요"): st.info(love_problems[keys_love[1]])
        if st.button("💔 이별 후 미련이 남아요"): st.info(love_problems[keys_love[3]])

# 탭 3: MBTI 스타일 연애 멘탈 유형 테스트 (빈 테두리 완벽 제거 버젼)
with tab3:
    st.markdown("### 📊 내 연애 멘탈 & 자존감 MBTI 테스트")
    st.write("4가지 질문에 솔직하게 답하고 나의 '연애 자기관리 유형'을 확인해보세요!")
    st.write("---")

    # 세션 상태 변수 초기화
    if 'result_type' not in st.session_state:
        st.session_state.result_type = None

    q1 = st.radio(
        "1. 상대방이 주말에 약속이 있어 나를 못 만난다고 할 때 나의 반응은?",
        ["A. '나랑 놀기 싫은가?' 서운해서 하루 종일 신경 쓰인다.", "B. '오히려 좋아!' 밀린 넷플릭스를 보거나 내 취미 생활을 즐긴다."],
        key="test_q1"
    )
    q2 = st.radio(
        "2. 연인 혹은 썸남/썸녀가 카톡을 읽고 3시간 동안 답장이 없을 때 나는?",
        ["A. 핸드폰을 계속 확인하며 카톡방을 들락날락한다.", "B. 바쁜가 보다 생각하고 내 할 일(공부, 업무)에 집중한다."],
        key="test_q2"
    )
    q3 = st.radio(
        "3. 상대방의 사소한 말투나 행동이 평소와 달라 보일 때 나는?",
        ["A. '나한테 질렸나?' 혼자 최악의 시나리오를 쓰며 불안해한다.", "B. 기분 좋은 일이나 다른 일이 있는지 직접 무덤덤하게 물어본다."],
        key="test_q3"
    )
    q4 = st.radio(
        "4. 서운한 점이 생겼을 때 나의 대처 방식은?",
        ["A. 상대가 알아주길 바라며 티만 내거나, 혼자 꾹 참다가 나중에 폭발한다.", "B. 감정이 가라앉은 후 차분하게 내 생각과 마음을 말로 전달한다."],
        key="test_q4"
    )

    if st.button("✨ 내 유형 결과 보기"):
        choices = [q1, q2, q3, q4]
        a_count = sum([1 for c in choices if c.startswith("A")])
        
        # 번잡한 HTML 태그를 모두 없애고 결과의 번호만 세션에 깔끔하게 저장
        st.session_state.result_type = a_count

    # 결과가 있을 때만 Streamlit 내부 기본 제공 컴포넌트로 예쁘게 출력
    if st.session_state.result_type is not None:
        res = st.session_state.result_type
        st.write("---")
        st.markdown("### 🧬 당신의 연애 멘탈 진단 결과")
        
        if res == 4:
            st.error("🚨 **유형: [LOVE-A] 감정 올인형 러버**\n\n상대방이 삶의 중심이 되어 있어 자존감이 쉽게 흔들리는 타입입니다. 상대방의 연락 한 통에 하루의 기분이 결정되곤 해요. \n\n**지금 필요한 자기관리:** 타인에게 집중된 시선을 의도적으로 나 자신에게 돌리는 '중심 잡기' 연습이 시급합니다!")
        elif res == 3 or res == 2:
            st.warning("💛 **유형: [LOVE-S] 눈치 서운형 러버**\n\n독립적으로 행동하고 싶지만 마음 한편으론 끊임없이 불안함과 서운함을 느끼는 타입입니다. 혼자 삭히다가 오해가 깊어질 수 있어요. \n\n**지금 필요한 자기관리:** 서운한 감정이 들 때는 메모장에 생각을 먼저 정리한 뒤, 팩트 기반으로 건강하게 소통하는 연습을 해보세요.")
        elif res == 1:
            st.info("🧱 **유형: [LOVE-I] 철벽 고립형 러버**\n\n상처받기 싫어서 마음을 깊게 주지 않거나, 지나치게 쿨한 척 벽을 치는 타입일 수 있습니다. 자기관리는 잘 되지만 관계의 깊이가 아쉬울 수 있어요. \n\n**지금 필요한 자기관리:** 가끔은 내 약한 모습을 솔직하게 털어놓으며 상대방을 신뢰하는 연습을 해보세요.")
        else:
            st.success("💚 **유형: [LOVE-G] 멘탈 단단형 갓생러**\n\n나 자신을 사랑할 줄 알고 연인과도 건강한 거리를 유지하는 완벽한 밸런스의 소유자입니다! 연애 때문에 일상을 망치지 않는 자존감 끝판왕이시네요. \n\n**지금 필요한 자기관리:** 지금처럼 나만의 루틴을 유지하며 예쁜 사랑을 이어가세요.")

# 탭 4: 예외 상황 맞춤형 AI 코칭 (gemini-2.5-flash-lite)
with tab4:
    st.markdown("### 🤖 무엇이든 물어보는 AI 자기관리 코치")
    st.write("일상의 무기력, 일 관리 슬럼프부터 테스트 결과에 대한 깊은 고민, 아무에게도 말 못 할 미묘한 연애 상황까지 적어주세요.")
    
    user_query = st.text_area("나의 구체적인 상황과 고민", placeholder="예시: 방금 테스트에서 [감정 올인형]이 나왔는데, 연락 집착을 고치고 제 일상 루틴을 되찾을 수 있는 실천 꿀팁을 구체적으로 알려주세요!")
    
    if st.button("AI 맞춤 처방전 받기"):
        if user_query.strip():
            with st.spinner("AI 코치가 당신의 삶의 균형과 자존감을 지켜줄 정답을 분석 중..."):
                try:
                    prompt = (
                        "당신은 일상 자기관리 및 연애 심리 전문가이자, 사용자의 자존감 수호를 최우선으로 여기는 멘토입니다. "
                        "사용자의 고민(일상 슬럼프 또는 연애 고민 등)을 분석하여 다음 원칙에 맞춰 대답하세요. "
                        "1. 따뜻하게 공감할 것. "
                        "2. 일상의 루틴을 회복하고 내면을 단단하게 지킬 수 있는 현실적이고 구체적인 행동 가이드를 2~3가지(번호 매기기)로 제시할 것. "
                        "3. 타인이나 상황에 휘둘리지 말고 자신을 가장 먼저 사랑하라는 메시지로 마무리할 것. 말투는 친근하면서도 뼈가 있는 해요체를 쓰세요."
                    )
                    response = client.models.generate_content(
                        model='gemini-2.5-flash-lite',
                        contents=user_query,
                        config=types.GenerateContentConfig(system_instruction=prompt)
                    )
                    # AI 상담 창도 테두리 제거하고 가독성 좋은 흰색 카드형태로 깔끔히 노출
                    st.markdown(f"<div class='content-card' style='border-left:5px solid #4A4E69; background-color:#FFFDFD;'>{response.text}</div>", unsafe_allow_html=True)
                except APIError as e:
                    st.error(f"Gemini API 오류가 발생했습니다: {e.message}")
                except Exception as e:
                    st.error("오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")
        else:
            st.warning("상담받을 고민 내용을 입력해 주세요.")

# 5. 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>당신의 일상도, 당신의 사랑도 결국 '나 자신'이 바로 서야 행복해집니다. 오늘도 화이팅! 🌿❤️</p>", unsafe_allow_html=True)
