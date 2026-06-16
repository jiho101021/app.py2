import streamlit as st
import pandas as pd
import time
from datetime import datetime
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="나만의 시간 관리 뷔페", page_icon="⏳", layout="wide")

# 세션 상태 초기화 (데이터 유지용)
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'time_blocks' not in st.session_state:
    st.session_state.time_blocks = pd.DataFrame(columns=["시간", "할 일"])
if 'comments' not in st.session_state:
    st.session_state.comments = []

def main():
    st.title("⏳ 나만의 시간 관리 뷔페")
    st.markdown("나에게 꼭 맞는 시간 관리 방법을 찾고, 하루를 알차게 채워보세요.")

    # 사이드바 네비게이션
    menu = st.sidebar.radio(
        "시간 관리 방법 선택",
        ["1. 아이젠하워 매트릭스 (우선순위)", "2. 뽀모도로 타이머 (집중)", "3. 타임 블로킹 (일정 관리)", "4. 오늘의 회고 (댓글)", "🤖 AI 시간 관리 코치"]
    )

    # 1. 아이젠하워 매트릭스
    if menu == "1. 아이젠하워 매트릭스 (우선순위)":
        st.header("🎯 아이젠하워 매트릭스")
        st.markdown("할 일의 중요도와 긴급도를 기준으로 우선순위를 정해보세요.")
        
        with st.form("task_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                task_name = st.text_input("할 일 내용")
            with col2:
                importance = st.selectbox("중요도", ["중요함", "중요하지 않음"])
            with col3:
                urgency = st.selectbox("긴급도", ["긴급함", "긴급하지 않음"])
            
            submit = st.form_submit_button("추가하기")
            if submit and task_name:
                st.session_state.tasks.append({"task": task_name, "importance": importance, "urgency": urgency})
                st.success(f"'{task_name}' 추가 완료!")

        st.markdown("---")
        
        # 4분면 화면 구성
        q1_col, q2_col = st.columns(2)
        q3_col, q4_col = st.columns(2)
        
        with q1_col:
            st.subheader("🔥 1사분면: 즉시 실행")
            st.caption("(중요하고 긴급함)")
            for t in st.session_state.tasks:
                if t['importance'] == "중요함" and t['urgency'] == "긴급함":
                    st.info(t['task'])
                    
        with q2_col:
            st.subheader("📅 2사분면: 계획 수립")
            st.caption("(중요하지만 긴급하지 않음 - ★가장 중요)")
            for t in st.session_state.tasks:
                if t['importance'] == "중요함" and t['urgency'] == "긴급하지 않음":
                    st.success(t['task'])

        with q3_col:
            st.subheader("🤝 3사분면: 위임 및 거절")
            st.caption("(중요하지 않지만 긴급함)")
            for t in st.session_state.tasks:
                if t['importance'] == "중요하지 않음" and t['urgency'] == "긴급함":
                    st.warning(t['task'])

        with q4_col:
            st.subheader("🗑️ 4사분면: 제거")
            st.caption("(중요하지도 긴급하지도 않음)")
            for t in st.session_state.tasks:
                if t['importance'] == "중요하지 않음" and t['urgency'] == "긴급하지 않음":
                    st.error(t['task'])

        if st.button("모든 할 일 초기화"):
            st.session_state.tasks = []
            st.rerun()

    # 2. 뽀모도로 타이머
    elif menu == "2. 뽀모도로 타이머 (집중)":
        st.header("🍅 뽀모도로 타이머")
        st.markdown("25분 집중하고 5분 휴식하는 가장 단순하고 확실한 집중법입니다.")
        
        timer_type = st.radio("모드 선택", ["25분 집중 (Pomodoro)", "5분 휴식 (Break)"], horizontal=True)
        minutes = 25 if timer_type == "25분 집중 (Pomodoro)" else 5
        
        if st.button("타이머 시작"):
            timer_placeholder = st.empty()
            total_seconds = minutes * 60
            
            for i in range(total_seconds, -1, -1):
                mins, secs = divmod(i, 60)
                timer_placeholder.metric(label="남은 시간", value=f"{mins:02d}:{secs:02d}")
                time.sleep(1) # 1초 대기
                
            st.balloons()
            st.success("수고하셨습니다! 다음 세션을 준비하세요.")

    # 3. 타임 블로킹
    elif menu == "3. 타임 블로킹 (일정 관리)":
        st.header("🧱 타임 블로킹")
        st.markdown("하루를 덩어리 시간(블록)으로 나누어 계획해보세요.")
        
        with st.form("time_block_form"):
            col1, col2 = st.columns([1, 3])
            with col1:
                time_str = st.text_input("시간 (예: 09:00 - 11:00)")
            with col2:
                activity = st.text_input("계획할 활동")
            
            if st.form_submit_button("블록 추가"):
                if time_str and activity:
                    new_row = pd.DataFrame({"시간": [time_str], "할 일": [activity]})
                    st.session_state.time_blocks = pd.concat([st.session_state.time_blocks, new_row], ignore_index=True)
                    st.success("시간 블록이 추가되었습니다.")
        
        if not st.session_state.time_blocks.empty:
            st.table(st.session_state.time_blocks)
            if st.button("초기화"):
                st.session_state.time_blocks = pd.DataFrame(columns=["시간", "할 일"])
                st.rerun()

    # 4. 오늘의 회고 (댓글)
    elif menu == "4. 오늘의 회고 (댓글)":
        st.header("📝 오늘의 회고 (수업/하루 댓글)")
        st.markdown("오늘 계획한 대로 시간을 잘 썼는지, 어떤 점을 개선하면 좋을지 댓글로 남겨보세요.")
        
        comment_input = st.text_area("오늘의 회고를 남겨주세요.")
        if st.button("댓글 등록"):
            if comment_input:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.comments.append({"시간": current_time, "내용": comment_input})
                st.success("회고가 등록되었습니다.")
                
        st.markdown("### 💬 기록된 회고 목록")
        for idx, c in enumerate(reversed(st.session_state.comments)):
            st.info(f"**{c['시간']}**\n\n{c['내용']}")

    # 5. AI 시간 관리 코치
    elif menu == "🤖 AI 시간 관리 코치":
        st.header("🤖 AI 시간 관리 코치")
        st.markdown("시간 관리에 대한 고민을 적어주시면, AI가 맞춤형 해결책을 제안합니다.")
        
        user_problem = st.text_area("예: '과제가 너무 많은데 자꾸 미루게 돼요. 어떻게 시작해야 할까요?'", height=150)
        
        if st.button("조언 구하기"):
            if not user_problem:
                st.warning("고민을 입력해주세요.")
            else:
                try:
                    # Streamlit Secrets에서 API 키 가져오기
                    api_key = st.secrets["GEMINI_API_KEY"]
                    genai.configure(api_key=api_key)
                    
                    # Gemini 2.5 Flash Lite 모델 설정
                    model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    
                    prompt = f"""
                    당신은 전문적이고 따뜻한 시간 관리 코치입니다.
                    사용자의 다음 고민을 읽고, 아이젠하워 매트릭스, 뽀모도로 기법, 타임 블로킹 등 
                    구체적이고 실천 가능한 시간 관리 기법 하나를 추천하여 짧고 명확하게 조언해주세요.
                    
                    사용자 고민: {user_problem}
                    """
                    
                    with st.spinner("AI가 맞춤형 조언을 생성 중입니다..."):
                        response = model.generate_content(prompt)
                        st.success("코칭 완료!")
                        st.markdown(f"> {response.text}")
                        
                except KeyError:
                    st.error("⚠️ Streamlit Secrets에 `GEMINI_API_KEY`가 설정되지 않았습니다.")
                except Exception as e:
                    st.error(f"⚠️ 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
