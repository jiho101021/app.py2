import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(
    page_title="StyleMatch AI",
    page_icon="👗",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("👗 StyleMatch AI")
st.markdown("**당신의 외모와 분위기에 딱 맞는 스타일 추천**")
st.caption("Gemini 2.5 Flash Lite • 이미지 업로드 지원")

# API Key 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 **Secrets 설정 오류**: Streamlit Secrets에 `GEMINI_API_KEY`를 추가해주세요.")
    st.info("배포 후 Advanced Settings → Secrets에서 설정하세요.")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"API 키 설정 중 오류 발생: {str(e)}")
    st.stop()

# 모델 초기화
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    system_instruction="""
    너는 10년 이상 경력의 전문 패션 스타일리스트이자 퍼스널 컬러 컨설턴트다.
    사용자의 얼굴형, 체형, 피부톤, 머리색, 분위기, 라이프스타일 등을 종합적으로 분석해서
    실용적이고 구체적인 스타일 추천을 해준다. 한국어로 친근하고 명확하게 답변한다.
    """
)

# 세션 상태
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 사이드바
with st.sidebar:
    st.header("💡 사용 방법")
    st.markdown("""
    1. **사진 업로드** (선택)
    2. 얼굴형, 체형, 피부톤, 머리색, 원하는 무드 등을 입력
    3. AI가 맞춤형 스타일 추천
    """)
    
    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 이미지 업로드
uploaded_file = st.file_uploader("📸 얼굴 사진 업로드 (선택)", type=["jpg", "jpeg", "png"])

# 사용자 입력
if prompt := st.chat_input("외모와 분위기를 자세히 알려주세요..."):
    user_message = prompt
    
    # 이미지 처리
    image_parts = []
    display_image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        image_parts = [image]
        display_image = image
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
        if display_image:
            st.image(display_image, width=300)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # AI 응답
    with st.chat_message("assistant"):
        with st.spinner("분석하고 추천 중입니다..."):
            try:
                if image_parts:
                    response = st.session_state.chat.send_message([prompt] + image_parts)
                else:
                    response = st.session_state.chat.send_message(prompt)
                
                assistant_response = response.text
                st.markdown(assistant_response)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_response
                })
                
            except Exception as e:
                error_msg = f"❌ 오류 발생: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

st.markdown("---")
st.caption("Powered by Gemini 2.5 Flash Lite | Made for Streamlit Community Cloud")
