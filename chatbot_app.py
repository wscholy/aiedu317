import streamlit as st
from anthropic import Anthropic

# 페이지 설정
st.set_page_config(
    page_title="중3 생물 학습 도우미",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 - API 키 입력 및 정보
with st.sidebar:
    st.title("⚙️ 설정")
    api_key = st.text_input(
        "Claude API 키 입력",
        type="password",
        help="Anthropic에서 발급받은 API 키를 입력하세요"
    )
    
    st.divider()
    st.info(
        "📚 **중3 생물 학습 도우미**\n\n"
        "이 챗봇은 중학교 3학년 생물 교육과정의 내용을 바탕으로 "
        "학생들의 학습을 돕기 위해 설계되었습니다.\n\n"
        "- 세포와 유전\n"
        "- 생식과 발생\n"
        "- 항상성과 신경계\n"
        "- 생태계와 환경"
    )

# 메인 페이지
st.title("🧬 중3 생물 학습 도우미")
st.markdown("궁금한 생물 개념을 물어보세요!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    st.session_state.client = None

if "api_key_provided" not in st.session_state:
    st.session_state.api_key_provided = False

# API 키 검증 및 클라이언트 초기화
if api_key:
    st.session_state.client = Anthropic(api_key=api_key)
    st.session_state.api_key_provided = True
else:
    st.warning("⚠️ API 키를 입력해주세요. (사이드바에서 입력)")
    st.session_state.api_key_provided = False

# 채팅 히스토리 표시
st.subheader("대화 내용")

# 채팅 메시지 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👨‍🎓"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="👨‍🏫"):
            st.markdown(message["content"])

# 사용자 입력
if st.session_state.api_key_provided:
    user_input = st.chat_input(
        "생물에 대해 질문해주세요...",
        key="user_input"
    )
    
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # 사용자 메시지 표시
        with st.chat_message("user", avatar="👨‍🎓"):
            st.markdown(user_input)
        
        # AI 응답 생성
        with st.chat_message("assistant", avatar="👨‍🏫"):
            with st.spinner("생각 중..."):
                try:
                    # 시스템 프롬프트
                    system_prompt = """당신은 중학교 3학년 생물 교사입니다. 다음 역할을 수행하세요:

1. **역할**: 친절하고 이해하기 쉬운 중3 생물 교사
2. **언어**: 항상 한국어로 응답
3. **대상**: 중학교 3학년 학생
4. **교육과정**: 2015 개정 교육과정 중3 생물
5. **톤**: 격려적이고 긍정적인 태도

**주요 학습 영역**:
- 세포의 구조와 기능
- 유전과 진화
- 생식과 발생
- 항상성과 신경계
- 호르몬과 자극 반응
- 생태계와 물질의 순환
- 환경과 생물

**응답 방식**:
1. 학생의 질문을 명확하게 이해
2. 핵심 개념을 먼저 설명
3. 구체적인 예시와 그림 설명으로 이해 향상
4. 어려운 용어는 쉽게 풀어 설명
5. 학생의 흥미를 유지할 수 있는 방식으로 설명
6. 필요시 추가 질문 제시로 깊은 학습 유도"""
                    
                    # Claude API 호출
                    response = st.session_state.client.messages.create(
                        model="claude-3-5-haiku-20241022",
                        max_tokens=1024,
                        system=system_prompt,
                        messages=st.session_state.messages
                    )
                    
                    assistant_message = response.content[0].text
                    
                    # AI 응답 표시
                    st.markdown(assistant_message)
                    
                    # 응답을 메시지 히스토리에 추가
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    
                except Exception as e:
                    st.error(f"❌ 오류 발생: {str(e)}")
                    st.info("API 키를 다시 확인해주세요.")

else:
    st.warning("사이드바에서 API 키를 입력한 후 시작하세요.")

# 하단 정보
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 대화 초기화"):
        st.session_state.messages = []
        st.rerun()

with col2:
    st.caption("Made with Streamlit + Claude API")

with col3:
    st.caption("v1.0")