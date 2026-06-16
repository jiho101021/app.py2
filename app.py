import streamlit as st
import google.generativeai as genai
import requests
import json

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="글로벌 축구선수 백과사전 + 하이라이트",
    page_icon="⚽",
    layout="wide"
)

# ==========================================
# 2. API 설정 및 검증
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 GEMINI_API_KEY가 설정되지 않았습니다. Streamlit Secrets 설정을 확인해주세요.")
    st.stop()

# Gemini API 구성
genai.configure(api_key=api_key)

# ==========================================
# 3. 안정성을 위한 보조 함수들 (예외 처리 포함)
# ==========================================
@st.cache_data(show_spinner=False)
def get_wiki_image(wiki_title):
    """위키피디아 영문 페이지 제목을 기반으로 메인 프로필 이미지를 가져옵니다."""
    default_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
    if not wiki_title:
        return default_img
        
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": wiki_title,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 600
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            pages = response.json().get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if "thumbnail" in page_info:
                    return page_info["thumbnail"]["source"]
    except Exception:
        pass
    
    return default_img

@st.cache_data(show_spinner=False)
def check_youtube_video(video_id):
    """유튜브 비디오 ID가 실제로 존재하는지 체크합니다."""
    if not video_id or len(video_id) != 11:
        return False
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except Exception:
        return False

# ==========================================
# 4. 메인 UI 화면 구성
# ==========================================
st.title("⚽ 글로벌 축구선수 종합 리포트 및 하이라이트")
st.markdown("전 세계 어느 축구선수든 이름을 검색하면 **프로필, 스탯, 수상 기록**과 **최고의 순간 동영상**을 바로 확인할 수 있습니다.")
st.divider()

# 검색창 입력
search_query = st.text_input("🔍 축구선수 이름을 입력하세요 (예: 손흥민, 이강인, Lionel Messi)", placeholder="선수 이름 입력 후 Enter")

if search_query:
    with st.spinner(f"'{search_query}' 선수의 데이터를 종합 분석 중입니다..."):
        
        # 엄격한 JSON 스키마 가이드 및 프롬프트
        prompt = f"""
        당신은 전 세계 축구선수 데이터베이스 전문가입니다. '{search_query}'에 대한 정확한 정보를 검색하여 제공된 JSON 형식으로 응답하세요.
        축구선수가 아니거나 정보를 완전히 찾을 수 없다면 {{"error": "not_found"}} 라고만 채워서 반환해야 합니다.
        
        반드시 아래 key 구조를 지켜야 합니다:
        {{
            "error": "선수를 찾았다면 빈문자열 '', 못 찾았다면 'not_found'",
            "name_ko": "선수의 한국어 지정 이름",
            "wiki_en_title": "선수의 정확한 영문 위키피디아 문서 제목 (예: Son Heung-min, Lionel Messi)",
            "nationality": "국적",
            "age": "현재 나이 또는 생년월일",
            "total_goals": "프로 통산 골 수 (예: 200+)",
            "career_clubs": "소속팀 커리어 목록 (콤마로 구분)",
            "summary": "선수 스타일 및 업적 요약 (한국어, 2~3줄)",
            "individual_awards": ["주요 개인 수상 기록 1", "주요 개인 수상 기록 2"],
            "club_awards": ["주요 클럽 우승 기록 1", "주요 클럽 우승 기록 2"],
            "best_moments_youtube_id": "선수의 확실한 하이라이트 유튜브 영상 11자리 ID. 확실하지 않다면 빈 문자열"
        }}
        """
        
        try:
            # response_mime_type을 사용하여 안정적인 JSON 출력 보장
            model = genai.GenerativeModel(
                'gemini-2.5-flash-lite',
                generation_config={"response_mime_type": "application/json"}
            )
            
            response = model.generate_content(prompt)
            player_data = json.loads(response.text)
            
            if not player_data:
                st.error("🤖 AI가 일시적으로 불안정한 데이터를 응답했습니다. 잠시 후 다시 검색해 주세요.")
                
            elif player_data.get("error") == "not_found":
                st.warning("❌ 해당 이름의 축구선수 정보를 찾을 수 없습니다. 이름이나 스펠링을 다시 확인해 주세요.")
                
            else:
                # 1. 위키피디아 이미지 URL 가져오기
                image_url = get_wiki_image(player_data.get("wiki_en_title"))
                
                # 2. 화면 레이아웃 분할
                col1, col2 = st.columns([1, 2.2])
                
                with col1:
                    st.image(image_url, caption=player_data.get("wiki_en_title"), use_container_width=True)
                    
                with col2:
                    st.header(player_data.get("name_ko", search_query))
                    st.markdown(f"**🌐 국적:** {player_data.get('nationality', '정보 없음')}")
                    
                    # 주요 Metric 대시보드
                    sub_col1, sub_col2 = st.columns(2)
                    sub_col1.metric(label="🎂 나이 / 생년월일", value=player_data.get("age", "정보 없음"))
                    sub_col2.metric(label="🥅 통산 골 수", value=player_data.get("total_goals", "정보 없음"))
                    st.divider()

                    # 3. 탭 구성
                    tab1, tab2, tab3 = st.tabs(["📝 선수 요약 및 수상", "🛡️ 클럽 커리어", "📺 최고의 순간 영상"])
                    
                    with tab1:
                        st.subheader("선수 소개")
                        st.write(player_data.get("summary", "소개 정보가 없습니다."))
                        st.divider()
                        
                        ind_awards = player_data.get("individual_awards", [])
                        club_awards = player_data.get("club_awards", [])
                        
                        a_col1, a_col2 = st.columns(2)
                        with a_col1:
                            st.subheader("🏅 개인 수상 기록")
                            if ind_awards and isinstance(ind_awards, list):
                                for award in ind_awards:
                                    st.markdown(f"- {award}")
                            else:
                                st.write("개인 수상 정보가 없습니다.")
                                
                        with a_col2:
                            st.subheader("🏆 클럽 수상 기록")
                            if club_awards and isinstance(club_awards, list):
                                for award in club_awards:
                                    st.markdown(f"- {award}")
                            else:
                                st.write("클럽 수상 정보가 없습니다.")
                            
                    with tab2:
                        st.subheader("⚽ 소속팀 커리어 히스토리")
                        clubs = player_data.get("career_clubs", "정보 없음")
                        st.info(clubs)
                        
                    with tab3:
                        st.subheader("📺 AI가 추천하는 최고의 플레이")
                        video_id = player_data.get("best_moments_youtube_id")
                        
                        search_keyword = player_data.get('wiki_en_title', search_query)
                        search_url = f"https://www.youtube.com/results?search_query={search_keyword}+best+moments+highlights"
                        
                        if video_id and check_youtube_video(video_id):
                            st.video(f"https://www.youtube.com/watch?v={video_id}")
                            st.markdown(f"💡 영상이 안 나오나요? 👉 [**YouTube에서 직접 검색하기**]({search_url})")
                        else:
                            st.warning("⚠️ 특정 동영상을 직접 가져오는 데 실패했습니다. 아래 안전한 유튜브 링크를 통해 하이라이트를 바로 감상해보세요!")
                            st.markdown(f"👉 [**YouTube에서 '{player_data.get('name_ko', search_query)} 하이라이트' 보기**]({search_url})")
                            
        except json.JSONDecodeError:
            st.error("🤖 AI가 JSON 규격을 맞추지 못했습니다. 다시 시도해 주세요.")
        except Exception as e:
            st.error(f"데이터를 처리하는 도중 예상치 못한 오류가 발생했습니다. (오류 내용: {e})")
