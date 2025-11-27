import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="2025 생기부 메이트", layout="centered")
st.title("🎁 2025 생기부 메이트")
st.markdown("<p style='color:#888;'>Gift for 2025 1st Grade Teachers</p>", unsafe_allow_html=True)
st.divider()

# --- [중요] API 키 설정 (사용자 입력 없이 서버에서 가져옴) ---
# Streamlit Cloud의 Secrets에서 키를 가져옵니다.
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    # 내 컴퓨터에서 테스트할 때를 위한 예외 처리 (혹은 키 설정을 안 했을 때)
    st.error("API 키가 설정되지 않았습니다. 관리자에게 문의하세요.")
    st.stop()

# 2. 사이드바 (키 입력창 제거됨, 옵션만 남음)
with st.sidebar:
    st.header("옵션 선택")
    st.info("💡 선생님들을 위해 이미 설정이 완료되어 있습니다. 바로 사용하세요!")
    
    options = ["자동(전체)", "학업역량(탐구력)", "인성/공동체(나눔)", "진로적성(전공)", "발전가능성(성장)"]
    selected_mode = st.selectbox("강조할 영역 선택", options)

# 3. 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "선생님, 안녕하세요! 학생의 관찰 내용을 편하게 적어주시면 생기부 문구로 만들어 드립니다."
    })

# 4. 대화 내용 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if prompt := st.chat_input("예: 수학 질문이 많고, 체육대회 때 응원단장을 함."):
    
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # 구글 Gemini 설정
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            system_prompt = f"""
            당신은 고등학교 생활기록부 작성 전문가입니다. 
            사용자가 입력한 학생 정보를 바탕으로 [{selected_mode}] 위주로 
            학교생활기록부 '행동특성 및 종합의견'에 들어갈 문장을 작성하세요.
            문체는 '~함', '~임'으로 끝나는 개조식과 서술형을 적절히 섞어주세요.
            """
            
            response = model.generate_content(
                f"{system_prompt}\n\n[학생 정보]: {prompt}",
                stream=True
            )

            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
